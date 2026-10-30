"""Fusion API vocabulary for the agentic SLAB workflow. Runs INSIDE Fusion.

Load once per Fusion session with a single ``execute_code`` call
(REPO = absolute path of this repository, the folder containing AGENTS.md):

    import builtins, types
    m = types.ModuleType('slabu')
    exec(open(REPO + r'\\scripts\\fusion\\slab_helpers.py', encoding='utf-8').read(), m.__dict__)
    builtins.SU = m
    SU.status()

Every later call starts with ``S = SU``. ``builtins`` survives between
``execute_code`` calls; local names do not. Re-load after a Fusion restart.

This module contains NO product geometry. Every SLAB sketch, dimension and
extrude is composed by the agent from the slab-product-spec skill, one feature
class per call. What lives here is the API plumbing that local models kept
getting wrong (ObjectCollection vs list, cm vs mm, saveAs arguments, appearance
property paths, camera push/read-back, drawing preferences). All of it was
verified live on Fusion 2705.1.11 on 28 Oct 2026.

Units: arguments named *_mm are millimetres; *_cm are centimetres (the API's
native unit). Returned measurements are mm unless the key says otherwise.
"""
import json
import math
import os
import time

import adsk.core
import adsk.fusion

V = adsk.core.ValueInput.createByReal
P3 = adsk.core.Point3D.create


def MM(v):
    """Millimetres -> centimetres (the Fusion API unit)."""
    return v / 10.0


def app():
    return adsk.core.Application.get()


def des():
    """Active Design, resolved on every use (never cached). None if a Drawing is active."""
    return adsk.fusion.Design.cast(app().activeProduct)


def stamp():
    return time.strftime('%H:%M:%S')


# ---------------------------------------------------------------- state / guard

EXPECT = {}   # component name -> body count, recorded after each PASS


def check_empty_design():
    """Read-only. Returns the state; raises if this is not a fresh empty Design."""
    a, d = app(), des()
    if d is None:
        raise RuntimeError('Active product is not a Design (Drawing tab?). Ask the user to select the Design tab.')
    root = d.rootComponent
    state = {'doc': a.activeDocument.name, 'saved': a.activeDocument.dataFile is not None,
             'product': a.activeProduct.productType, 'edit': d.activeEditObject.objectType,
             'occ': root.occurrences.count, 'bodies': root.bRepBodies.count, 'timeline': d.timeline.count}
    ok = (state['edit'] == 'adsk::fusion::Component' and state['occ'] == 0
          and state['bodies'] == 0 and state['timeline'] == 0)
    if not ok:
        raise RuntimeError('Not an empty Design; do not clear it, ask the user: %r' % state)
    return state


def guard():
    """First line of every class call: no GUI edit open, earlier passed classes intact."""
    d = des()
    if d is None:
        raise RuntimeError('No active Design')
    if d.activeEditObject.objectType != 'adsk::fusion::Component':
        raise RuntimeError('A GUI edit (sketch?) is open: %s. Stop and ask the user.' % d.activeEditObject.objectType)
    have = {o.component.name: o.component.bRepBodies.count for o in d.rootComponent.occurrences}
    lost = {k: (v, have.get(k)) for k, v in EXPECT.items() if have.get(k) != v}
    if lost:
        raise RuntimeError('Previously passed classes changed (expected, now): %r' % lost)


def passed(component_name, body_count):
    """Record a class that measured PASS so guard() protects it."""
    EXPECT[component_name] = body_count
    return dict(EXPECT)


def health():
    """Timeline items whose healthState is not 0 (read from the timeline object)."""
    tl = des().timeline
    return [(i, tl.item(i).name) for i in range(tl.count) if int(tl.item(i).healthState) != 0]


def status():
    """Read-only one-call summary for preflight and for resuming in a new conversation."""
    a, d = app(), des()
    out = {'t': stamp(), 'doc': a.activeDocument.name if a.activeDocument else None,
           'product': a.activeProduct.productType if a.activeProduct else None,
           'saved': bool(a.activeDocument and a.activeDocument.dataFile)}
    if d is None:
        return out
    root = d.rootComponent
    per = {o.component.name: o.component.bRepBodies.count for o in root.occurrences}
    aps = d.appearances
    names = [aps.item(i).name for i in range(aps.count)]
    out.update(edit=d.activeEditObject.objectType, components=len(per) + 1,
               bodies=sum(per.values()) + root.bRepBodies.count, per_component=per,
               health=health(), timeline=d.timeline.count,
               slab_appearances=sorted(n for n in names if n.startswith('SLAB_')),
               duplicate_appearances=sorted({n for n in names if names.count(n) > 1}),
               expect=dict(EXPECT))
    return out


# ---------------------------------------------------------------- save

def save_new(prefix, project='Default Project', description='', tag='',
             run_root=None):
    """Cloud-save the active unsaved Design as the next free <prefix>_vN and create the run folder.

    Takes 1-70 s. If the MCP call times out, call status() and check the doc
    name before doing anything else. Never call this twice for one run.
    """
    a = app()
    if a.activeDocument.dataFile is not None:
        name = a.activeDocument.name
    else:
        prjs = a.data.activeHub.dataProjects   # app.data.activeProject raises on unsaved docs
        proj = next((prjs.item(i) for i in range(prjs.count) if prjs.item(i).name == project), prjs.item(0))
        folder = proj.rootFolder                # saveAs needs a DataFolder, not a name/path
        names = {folder.dataFiles.item(i).name for i in range(folder.dataFiles.count)}
        n = 1
        while '%s_v%d' % (prefix, n) in names:
            n += 1
        name = '%s_v%d' % (prefix, n)
        if not a.activeDocument.saveAs(name, folder, description, tag):
            raise RuntimeError('saveAs returned False')
    run_dir = os.path.join(run_root or os.path.join(os.path.expanduser('~'), 'fusion-renders'), name)
    for sub in ('renders', 'views', 'tools'):
        os.makedirs(os.path.join(run_dir, sub), exist_ok=True)
    df = a.activeDocument.dataFile
    return {'doc': a.activeDocument.name, 'root': des().rootComponent.name,
            'data_file_id': df.id if df else None, 'run_dir': run_dir, 't': stamp()}


def save(label=''):
    """Plain save of an already cloud-saved document (about 1 s)."""
    return app().activeDocument.save(label)


# ---------------------------------------------------------------- sketch / feature vocabulary

def comp(name):
    """Get-or-make a component by exact name (never forks a duplicate)."""
    root = des().rootComponent
    for o in root.occurrences:
        if o.component.name == name:
            return o.component
    o = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    o.component.name = name
    return o.component


def plane(c, z_mm):
    """Construction plane at absolute Z (mm), offset from the component XY plane."""
    pi = c.constructionPlanes.createInput()
    pi.setByOffset(c.xYConstructionPlane, V(MM(z_mm)))
    return c.constructionPlanes.add(pi)


def sketch(c, z_mm, name, deferred=False):
    """New named sketch on plane(c, z_mm). deferred=True sets sk.isComputeDeferred
    (a Sketch PROPERTY); call done(sk) after adding curves."""
    sk = c.sketches.add(plane(c, z_mm))
    sk.name = name
    if deferred:
        sk.isComputeDeferred = True
    return sk


def done(sk):
    """End deferred compute; returns the profile count."""
    sk.isComputeDeferred = False
    return sk.profiles.count


def coll(items):
    """Python list -> ObjectCollection (the API rejects plain lists)."""
    if isinstance(items, adsk.core.ObjectCollection):
        return items
    oc = adsk.core.ObjectCollection.create()
    for x in items:
        oc.add(x)
    return oc


def allprof(sk):
    return coll(list(sk.profiles))


def extrude(c, profs, h_mm, taper_deg=0.0, cut=False, name=None):
    """Extrude profiles (list, collection or a sketch) by h_mm; negative = opposite direction.

    Returns the ExtrudeFeature. Its bodies are feature.bodies (a collection),
    not the return value itself.
    """
    if isinstance(profs, adsk.fusion.Sketch):
        profs = allprof(profs)
    profs = coll(profs) if not isinstance(profs, adsk.fusion.Profile) else profs
    op = (adsk.fusion.FeatureOperations.CutFeatureOperation if cut
          else adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ei = c.features.extrudeFeatures.createInput(profs, op)
    dist = adsk.fusion.DistanceExtentDefinition.create(V(MM(abs(h_mm))))
    dr = (adsk.fusion.ExtentDirections.NegativeExtentDirection if h_mm < 0
          else adsk.fusion.ExtentDirections.PositiveExtentDirection)
    if taper_deg:
        ei.setOneSideExtent(dist, dr, V(math.radians(taper_deg)))
    else:
        ei.setOneSideExtent(dist, dr)
    f = c.features.extrudeFeatures.add(ei)
    if name:
        f.name = name
    return f


def fillet_edges(c, edges, r_mm, name=None):
    fi = c.features.filletFeatures.createInput()
    fi.isRollingBallCorner = True
    fi.addConstantRadiusEdgeSet(coll(edges), V(MM(r_mm)), True)
    f = c.features.filletFeatures.add(fi)
    if name:
        f.name = name
    return f


def vertical_edges(b):
    ed = adsk.core.ObjectCollection.create()
    for e in b.edges:
        g = e.geometry
        if g.objectType == adsk.core.Line3D.classType():
            d = g.startPoint.vectorTo(g.endPoint)
            if abs(d.x) < 1e-6 and abs(d.y) < 1e-6:
                ed.add(e)
    return ed


def circles_above(c, z_mm, tol=0.001):
    ed = adsk.core.ObjectCollection.create()
    for b in c.bRepBodies:
        for e in b.edges:
            g = e.geometry
            if g.objectType == adsk.core.Circle3D.classType() and g.center.z > MM(z_mm) - tol:
                ed.add(e)
    return ed


def face_at_z(b, z_mm):
    fs = adsk.core.ObjectCollection.create()
    for f in b.faces:
        g = f.geometry
        if (g.objectType == adsk.core.Plane.classType() and abs(g.normal.z) > 0.99
                and abs(g.origin.z - MM(z_mm)) < 1e-4):
            fs.add(f)
    return fs


def shell(c, faces, wall_mm, name=None):
    si = c.features.shellFeatures.createInput(coll(faces), False)
    si.insideThickness = V(MM(wall_mm))
    f = c.features.shellFeatures.add(si)
    if name:
        f.name = name
    return f


def rect(sk, cx, cy, w, h):
    """Centre + size in mm (the raw API's second point is an absolute corner)."""
    sk.sketchCurves.sketchLines.addCenterPointRectangle(
        P3(MM(cx), MM(cy), 0), P3(MM(cx + w / 2.0), MM(cy + h / 2.0), 0))


def circle(sk, cx, cy, d):
    """Centre + DIAMETER in mm."""
    sk.sketchCurves.sketchCircles.addByCenterRadius(P3(MM(cx), MM(cy), 0), MM(d / 2.0))


def poly(sk, pts_mm):
    """Closed polyline through (x, y) mm points with shared endpoints (always one loop)."""
    L = sk.sketchCurves.sketchLines
    P = [P3(MM(x), MM(y), 0) for x, y in pts_mm]
    first = L.addByTwoPoints(P[0], P[1])
    prev = first
    for i in range(1, len(P) - 1):
        prev = L.addByTwoPoints(prev.endSketchPoint, P[i + 1])
    L.addByTwoPoints(prev.endSketchPoint, first.startSketchPoint)


def bar(sk, cx, cy, angle_deg, r0, r1, w):
    """Radial bar (mm). Angle measured from +Y, positive toward +X; radius r0 -> r1; width w."""
    a = math.radians(angle_deg)
    rd = (-math.sin(a), math.cos(a))
    tn = (math.cos(a), math.sin(a))
    poly(sk, [(cx + rd[0] * r + tn[0] * s * w / 2.0, cy + rd[1] * r + tn[1] * s * w / 2.0)
              for r, s in ((r0, -1), (r1, -1), (r1, 1), (r0, 1))])


def profile_extent(p):
    bb = p.boundingBox
    return [round(bb.minPoint.x * 10, 2), round(bb.minPoint.y * 10, 2),
            round(bb.maxPoint.x * 10, 2), round(bb.maxPoint.y * 10, 2)]


def reset_component(c):
    """Delete a component's own features/bodies/sketches/planes so a class can be rebuilt cleanly."""
    for group in (list(reversed(list(c.features))), list(c.bRepBodies), list(c.sketches), list(c.constructionPlanes)):
        for x in group:
            try:
                x.deleteMe()
            except Exception:
                pass
    return c.bRepBodies.count


# ---------------------------------------------------------------- measurement

def bbox(b):
    x = b.boundingBox
    return [round(v * 10, 3) for v in (x.minPoint.x, x.minPoint.y, x.minPoint.z,
                                       x.maxPoint.x, x.maxPoint.y, x.maxPoint.z)]


def cbbox(c):
    bb = [bbox(b) for b in c.bRepBodies]
    return [min(v[i] for v in bb) for i in range(3)] + [max(v[i] for v in bb) for i in range(3, 6)]


def radii(b):
    return sorted([[round(e.geometry.center.z * 10, 2), round(e.geometry.radius * 10, 3)]
                   for e in b.edges if e.geometry.objectType == 'adsk::core::Circle3D'])


def top_area(b):
    """Largest horizontal planar face area, mm^2."""
    return round(max([f.area * 100 for f in b.faces
                      if f.geometry.surfaceType == 0 and abs(f.geometry.normal.z) > 0.99] + [0]), 2)


def vol_cm3(b):
    return round(b.volume, 3)


# ---------------------------------------------------------------- appearances (CMF)

def _library_source(name='Plastic - Glossy (Black)'):
    lib = app().materialLibraries.itemByName('Fusion Appearance Library')
    return lib.appearances.itemByName(name)


def find_appearance(name):
    """Resolve a design appearance by iterating (itemByName returns the first duplicate)."""
    aps = des().appearances
    hits = [aps.item(i) for i in range(aps.count) if aps.item(i).name == name]
    if len(hits) != 1:
        raise RuntimeError('%s resolved to %d appearances' % (name, len(hits)))
    return hits[0]


def make_appearance(name, rgb, roughness, f0, luminance=None, luminance_rgb=None):
    """Create ONE appearance from the library source and set it while unapplied.

    Raises if the name already exists (a second run would make duplicates).
    luminance (+ luminance_rgb) turns on emission.
    """
    aps = des().appearances
    if any(aps.item(i).name == name for i in range(aps.count)):
        raise RuntimeError('%s already exists; do not create duplicates' % name)
    ap = aps.addByCopy(_library_source(), name)
    P = ap.appearanceProperties
    col = adsk.core.Color.create(rgb[0], rgb[1], rgb[2], 255)
    P.itemById('surface_albedo').value = col     # the renderer reads this one
    P.itemById('opaque_albedo').value = col
    P.itemById('surface_roughness').value = roughness
    P.itemById('opaque_f0').value = f0
    if luminance is not None:
        P.itemById('opaque_emission').value = True
        P.itemById('opaque_luminance').value = float(luminance)
        lr = luminance_rgb or rgb
        P.itemById('opaque_luminance_modifier').value = adsk.core.Color.create(lr[0], lr[1], lr[2], 255)
    return ap


def assign(body, ap):
    """Body FIRST, then only faces that still differ (face-first writes every face, ~13x slower)."""
    body.appearance = ap
    n = 0
    for f in body.faces:
        if f.appearance is not None and f.appearance.name != ap.name:
            f.appearance = ap
            n += 1
    return n


def assign_component(component_name, appearance_name):
    """Assign one appearance to every body of a component. Returns the body count."""
    ap = find_appearance(appearance_name)
    c = comp_existing(component_name)
    for b in c.bRepBodies:
        assign(b, ap)
    return c.bRepBodies.count


def comp_existing(name):
    for o in des().rootComponent.occurrences:
        if o.component.name == name:
            return o.component
    raise RuntimeError('No component named %s' % name)


def appearance_tally():
    """Body count per effective body appearance, plus stray face overrides."""
    tally, overrides = {}, 0
    for o in des().rootComponent.occurrences:
        for b in o.component.bRepBodies:
            n = b.appearance.name if b.appearance else None
            tally[n] = tally.get(n, 0) + 1
            overrides += sum(1 for f in b.faces if f.appearance and f.appearance.name != n)
    return {'tally': tally, 'total': sum(tally.values()), 'face_overrides': overrides}


# ---------------------------------------------------------------- render

def render_setup(brightness, camera_exposure):
    """Activate the Render workspace visibly, write and read back exposure.

    Values come from the render skill (brightness is lux, cameraExposure is
    inverse: lower is brighter)."""
    a = app()
    a.userInterface.workspaces.itemById('FusionRenderEnvironment').activate()
    adsk.doEvents()
    ss = des().renderManager.sceneSettings
    ss.brightness = float(brightness)
    ss.cameraExposure = float(camera_exposure)
    return {'workspace': a.userInterface.activeWorkspace.id, 'brightness': ss.brightness,
            'cameraExposure': ss.cameraExposure}


def design_workspace():
    a = app()
    a.userInterface.workspaces.itemById('FusionSolidEnvironment').activate()
    adsk.doEvents()
    return a.userInterface.activeWorkspace.id


def perspective_camera(az_deg, el_deg, fov_deg, dist_cm, target_cm=(0.0, 0.0, 0.0)):
    """Perspective camera that HOLDS its distance (Fusion rescales eye to keep viewExtents)."""
    vp = app().activeViewport
    az, el = math.radians(az_deg), math.radians(el_deg)
    u = (math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el))

    def place(d, ve=None):
        cam = vp.camera
        cam.cameraType = adsk.core.CameraTypes.PerspectiveCameraType
        cam.isSmoothTransition = False
        cam.target = adsk.core.Point3D.create(*target_cm)
        cam.eye = adsk.core.Point3D.create(*[target_cm[i] + d * u[i] for i in range(3)])
        cam.upVector = adsk.core.Vector3D.create(0, 0, 1)
        cam.perspectiveAngle = math.radians(fov_deg)
        cam.isFitView = False
        if ve is not None:
            cam.viewExtents = ve
        vp.camera = cam
        adsk.doEvents()
        c = vp.camera
        return c.eye.distanceTo(c.target), c.viewExtents

    dist, ve = place(dist_cm)
    hist = [round(dist, 2)]
    for _ in range(4):
        if abs(dist - dist_cm) <= 0.05:
            break
        ve = ve * (dist_cm / dist) ** 2
        dist, ve = place(dist_cm, ve)
        hist.append(round(dist, 2))
    return {'distance_history_cm': hist, 'viewport': [vp.width, vp.height]}


def ortho_camera(direction, up, target_cm, view_extents_cm=None, fit_margin=None):
    """Orthographic camera. Either a fixed viewExtents, or fit then scale by fit_margin."""
    vp = app().activeViewport
    n = math.sqrt(sum(q * q for q in direction))
    d = [q / n for q in direction]
    cam = vp.camera
    cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType
    cam.isSmoothTransition = False
    cam.target = adsk.core.Point3D.create(*target_cm)
    cam.eye = adsk.core.Point3D.create(*[target_cm[i] + d[i] * 200 for i in range(3)])
    cam.upVector = adsk.core.Vector3D.create(*up)
    cam.isFitView = fit_margin is not None
    vp.camera = cam
    adsk.doEvents()
    if fit_margin is not None:
        vp.fit()
        adsk.doEvents()
    c = vp.camera
    c.isFitView = False
    c.viewExtents = view_extents_cm if view_extents_cm is not None else c.viewExtents * fit_margin
    vp.camera = c
    adsk.doEvents()
    return round(vp.camera.viewExtents, 3)


def project_tops(component_name, out_json=None):
    """Viewport pixel position of each body's top-centre (for pad ROIs). Writes {'vp','pads'} JSON."""
    vp = app().activeViewport
    pts = []
    for b in comp_existing(component_name).bRepBodies:
        bb = b.boundingBox
        v = vp.modelToViewSpace(adsk.core.Point3D.create((bb.minPoint.x + bb.maxPoint.x) / 2,
                                                         (bb.minPoint.y + bb.maxPoint.y) / 2, bb.maxPoint.z))
        pts.append([round(v.x, 1), round(v.y, 1)])
    data = {'vp': [vp.width, vp.height], 'pads': pts}
    if out_json:
        with open(out_json, 'w') as fh:
            json.dump(data, fh)
    return data


def viewport_capture(path, width, height):
    """Shaded viewport image (NOT a raytrace). Returns bytes written."""
    ok = app().activeViewport.saveAsImageFile(path, width, height)
    if not ok or not os.path.exists(path) or os.path.getsize(path) == 0:
        raise RuntimeError('capture failed: ' + path)
    return os.path.getsize(path)


def capture_line_views(out_dir, target_cm, view_extents_cm, size=2200, views=None):
    """Monochrome line-art views at one shared viewExtents; restores style, folders and camera."""
    a, d = app(), des()
    vp = a.activeViewport
    root = d.rootComponent
    comps = [root] + [o.component for o in root.occurrences]
    prev = [(x.isOriginFolderLightBulbOn, x.isSketchFolderLightBulbOn, x.isConstructionFolderLightBulbOn)
            for x in comps]
    prev_cam = vp.camera
    views = views or {'top': ((0, 0, 1), (0, 1, 0)), 'front': ((0, -1, 0), (0, 0, 1)),
                      'right': ((1, 0, 0), (0, 0, 1)), 'iso': ((0.7071, -0.5657, 0.75), (0, 0, 1))}
    out = {}
    try:
        for x in comps:
            x.isOriginFolderLightBulbOn = False
            x.isSketchFolderLightBulbOn = False
            x.isConstructionFolderLightBulbOn = False
        vp.visualStyle = adsk.core.VisualStyles.WireframeWithVisibleEdgesOnlyVisualStyle
        for name, (direction, up) in views.items():
            ortho_camera(direction, up, target_cm, view_extents_cm=view_extents_cm)
            p = os.path.join(out_dir, 'ln_%s.png' % name)
            out[name] = viewport_capture(p, size, size)
    finally:
        vp.visualStyle = adsk.core.VisualStyles.ShadedVisualStyle
        for x, (o1, o2, o3) in zip(comps, prev):
            x.isOriginFolderLightBulbOn = o1
            x.isSketchFolderLightBulbOn = o2
            x.isConstructionFolderLightBulbOn = o3
        vp.camera = prev_cam
        adsk.doEvents()
    return out


# ---------------------------------------------------------------- native drawing

def native_drawing(log_path, parts_list=True, orthogonal=True, iso=True, open_drawing=True):
    """Two-sheet native drawing via the Drawing API. LAST Fusion action.

    Main assembly only, first level, NO component sheets, auto-dimension OFF.
    The FIRST drawing after a fresh build has crashed Fusion's drawing engine
    (acadm.crx c0000027 popup, file still created); after the user clicks OK
    and returns to the Design tab, calling this again has displayed it. See
    fusion-2d-drawings §3a for the retry procedure. Writes timings to log_path
    before opening, because the MCP response can be lost once the Drawing is
    active. Afterwards the agent cannot see the drawing: ask the user to
    confirm it displayed with the parts list.
    """
    import adsk.drawing as D
    a = app()
    r = {'t0': stamp()}

    def w():
        with open(log_path, 'w') as fh:
            json.dump(r, fh, indent=1)

    if a.activeDocument.dataFile is None:
        raise RuntimeError('Document is not cloud-saved; save_new() first')
    mgr = D.DrawingManager.get()
    di = mgr.createDrawingInput(a.activeDocument.dataFile, D.DrawingCreationModes.AutomaticDrawingCreationMode)
    di.baseDocumentType = D.BaseDocumentTypes.FromScratchBaseDocumentType
    di.standard = D.DrawingStandardTypes.ISODrawingStandardType
    di.units = D.DrawingUnitTypes.MillimeterDrawingUnitType
    di.sheetSize = D.SheetSizes.A3ISOSheetSize
    di.orientationType = D.SheetOrientationTypes.LandscapeSheetOrientationType
    di.sheetCreationType = D.SheetCreationTypes.FirstLevelOnlySheetCreationType
    g = di.automationPreferences.globalPreferences
    g.isMainAssemblySheetGenerated = True
    g.isComponentSheetGenerated = False
    g.isSubAssemblySheetGenerated = False
    g.isAnimationSheetGenerated = False
    g.isFlatPatternSheetGenerated = False
    g.isFoldedModelSheetGenerated = False
    g.isDetectAndOmitFasteners = True
    g.isAutoDimensionEnabled = False
    m = di.automationPreferences.mainAssemblyPreferences
    m.isoViewSheetPreferences.isSheetCreated = bool(iso)
    m.isoViewSheetPreferences.isPartsListIncluded = bool(parts_list)
    m.orthogonalViewSheetPreferences.isSheetCreated = bool(orthogonal)
    m.orthogonalViewSheetPreferences.isPartsListIncluded = False
    m.autoDimensionPreferences.isAutoDimensionEnabled = False
    vw = m.drawingViewPreferences
    vw.style = D.DrawingViewStyleTypes.VisibleEdgesDrawingViewStyleType
    vw.tangentEdgesType = D.TangentEdgeDisplayTypes.OffTangentEdgeDisplayType
    w()
    df = mgr.createDrawing(di)
    r['t_created'] = stamp()
    r['drawing'] = df.name if df else None
    w()
    if open_drawing:
        a.documents.open(df)
        r['t_opened'] = stamp()
    else:
        r['opened'] = False   # user opens it from the Data Panel
    w()
    return r
