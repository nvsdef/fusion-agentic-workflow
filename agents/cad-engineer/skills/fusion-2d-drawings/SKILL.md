---
name: "fusion-2d-drawings"
description: "How to get 2D output from Fusion 360 - capture orthographic line-art views, compose a dimensioned A3 sheet with a parts list, then create the native drawing document LAST. Covers the create_drawing call that works and how to tell its timeout from a modal hang. Use whenever a drawing, GA sheet, BOM or dimensioned 2D output is requested. Supersedes fusion-product-design's fusion-2d-drawings."
---

# 2D drawings and line-art views from Fusion 360

**Precedence.** Supersedes `fusion-product-design:fusion-2d-drawings`, whose
Part 1 records two failure modes that are now stale. Verified on Fusion build
2705.1.11 (`a40f190f24413dd1bb4f1434f056c1379a3b5224`), 11 September 2026.

---

## The order

```
0  save to cloud (at the START of the run)
1  capture orthographic line-art views          <- reversible
2  compose the dimensioned A3 sheet             <- outside Fusion
3  create the native drawing document           <- LAST Fusion action
```

**Announce the monochrome transition before capture and before opening Drawing.**
The 18 September 2026 rehearsal prompted the operator to ask why the whole model
was white. Explain that line-art/drawing display intentionally omits appearances;
it is not a CMF reassignment. Preserve and restore the prior camera/visual style
in `finally`, save the colored model/archive before Drawing, and deliver the
colored hero/plan alongside the sheet. Do not claim a white Drawing viewport
means body materials changed. On this rehearsal, native drawing creation timed
out at 300 seconds but a later document-type query confirmed Drawing active;
that confirms creation/activation, not every native sheet's correctness.

**Step 3 is a one-way door.** Once a Drawing document is active: `execute_code`
and `get_design_type` no longer run, and no MCP call can activate a different
document — only a human clicking the Design tab can return the session to the
model. So every measurement, render, export and view capture happens first.
State this in the final report when you open it - as a note, not a question.

Doing steps 1–2 before step 3 also means the composed sheet exists regardless of
what the native branch does.

**Never call `export_drawing_pdf`**, on either branch. It opens a modal dialog
and hangs the entire MCP server; `ping` stops answering and Fusion has to be
recovered by hand. There is no version of this workflow where it is the right
call.

---

## 0 · Save to the cloud first

The native branch needs a `DataFile`, and an unsaved document has none.
Discovering that at drawing time costs the drawing. Save at the **start** of the
run — it also names the root component, which takes the filename and cannot be
renamed through the API.

```python
hub  = app.data.activeHub              # activeProject raises on a fresh document
prjs = hub.dataProjects
proj = next((prjs.item(i) for i in range(prjs.count)
             if prjs.item(i).name == 'Default Project'), prjs.item(0))
app.activeDocument.saveAs('MY_MODEL', proj.rootFolder, 'description', 'rev')
```

Confirm `app.activeDocument.dataFile is not None` before step 3.

---

## 1 · Capture the line-art views with explicit cameras

Capture them yourself rather than with `export_view_sheet`, which fits each view
into its own square frame and clips a long flat product — measured crop aspects
5–6 % wrong on `front` and `right` while `top` was fine, which silently corrupts
every dimension placed on the sheet.

Hide the origin, sketch and construction folders on the root **and** every
component, then capture four views at **one shared `viewExtents`**, so px/mm is
identical everywhere and a single calibration serves the whole sheet:

```python
import os
root = design.rootComponent
vp = app.activeViewport
OUT = os.path.expanduser('~/fusion-renders')
os.makedirs(OUT, exist_ok=True)
for c in [root] + [o.component for o in root.occurrences]:
    c.isOriginFolderLightBulbOn = False
    c.isSketchFolderLightBulbOn = False
    c.isConstructionFolderLightBulbOn = False

vp.visualStyle = adsk.core.VisualStyles.WireframeWithVisibleEdgesOnlyVisualStyle
TGT  = (0.0, 0.0, 3.06)          # cm; the elevations centre on this Z
DIRS = {'top':  ((0,0,1),(0,1,0)), 'front': ((0,-1,0),(0,0,1)),
        'right':((1,0,0),(0,0,1)), 'iso':  ((0.7071,-0.5657,0.75),(0,0,1))}
for name, (d, up) in DIRS.items():
    n = math.sqrt(sum(c*c for c in d)); d = tuple(c/n for c in d)
    cam = vp.camera
    cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType
    cam.isSmoothTransition = False
    cam.target = adsk.core.Point3D.create(*TGT)
    cam.eye = adsk.core.Point3D.create(*[TGT[i] + d[i]*200 for i in range(3)])
    cam.upVector = adsk.core.Vector3D.create(*up)
    cam.isFitView = False
    vp.camera = cam; adsk.doEvents()
    c2 = vp.camera; c2.viewExtents = 38.0; c2.isFitView = False   # push, re-read, set, push
    vp.camera = c2; adsk.doEvents()
    # Capture each view inside this loop; OUT was initialized above.
    path = os.path.join(OUT, 'ln_%s.png' % name)
    ok = vp.saveAsImageFile(path, 2200, 2200)
    assert ok and os.path.getsize(path) > 0, 'capture failed: ' + path

vp.visualStyle = adsk.core.VisualStyles.ShadedVisualStyle       # ALWAYS restore
```

`viewExtents` assigned to a camera you have not yet pushed is ignored — push the
camera, re-read `vp.camera`, set `viewExtents` on *that*, push again.

Then crop and calibrate:

**`vp.saveAsImageFile` is synchronous and returns a bool.** There is no job to
poll — but it can silently write nothing. After each capture, check the file
exists with non-zero bytes before moving on:

```python
ok = vp.saveAsImageFile(path, 2200, 2200)
assert ok and os.path.getsize(path) > 0, 'capture failed: ' + path
```

Write the views to a **local, non-synced** directory. A cloud-synced folder
slows every write and drops build artefacts into the repo.

```bash
python scripts/make_views.py --dir ./views --target-z 30.6 \
    --bbox=-99.52,97.52,-170.02,170.02,-0.03,61.18
```

Both of the composed-sheet scripts need a **terminal and Python with PIL, numpy
and reportlab**, plus `pdftoppm` for the raster check. If the harness has no
terminal, the sheet cannot be composed — say so and deliver the line-art views,
rather than substituting a shaded render and calling it a drawing.

Note the `=` — the value starts with a minus sign.

It prints a crop-aspect error per view. **Expect ≤ 0.11 %**; measured on a clean
run: top 0.04 %, front 0.07 %, right 0.11 %. Anything over 1 % means the capture
was clipped or the crop is wrong — re-capture and re-crop, **at most twice**.
If it is still over 1 % on the third measurement, place no dimensions: deliver
the views unannotated and record the crop error as an open item.

Two things the script handles, and why they need handling:

- **The plate is lighter than the ink on a dark Fusion theme**, so ink is
  `plate_lum − lum`, and `plate_lum` must be the **modal** luminance of the
  frame. A corner pixel can land on a grid line, which inverts the mask and
  returns the whole frame as ink.
- **The world-origin marker overhangs the model.** It projects ~21 px below the
  model in both elevations and adds ~3.8 mm of apparent Z to an ink-bbox crop —
  about 6 % aspect error. Turning off the origin folders does not remove it. The
  script rejects blue-tinted pixels (`b − r >= 30`) and crops the elevations
  **analytically** from the known camera rather than from ink bounds,
  calibrating px/mm on the **top** view where the marker sits inside the
  silhouette.

### A shaded render from above is not a drawing view

Orthographic line art has visible edges only, no materials, no shading. Shaded
perspective renders handed over as a "general arrangement sheet" have been
rejected, correctly. Also: **always judge layout on an orthographic top view** —
perspective foreshortens repeated radial features into what looks like scatter.

---

## 2 · Compose the dimensioned sheet

```bash
python scripts/make_drawing.py scripts/slab_sheet.json -o MODEL_GA.pdf --views-dir ./views
```

`slab_sheet.json` ships raster-checked and collision-free: A3 landscape at
1:2.5, three dimensioned orthographic views, an isometric with balloons, a
12-row parts list totalling 289 bodies, notes, title block. **Edit its content,
not its layout** — update the date, the revision and any note whose figure has
changed. Rebuilding the layout is where collisions come from.

**Dimension from measured geometry, never from the parameter table.** A model can
carry 50 well-formed named parameters of which `Overall_Depth` reads 150 against
a measured 195; a sheet built from that table is confidently, silently wrong. On
a model with zero named parameters there is nothing to dimension from at all.

Use the **full** bounding box including controls standing proud, not the
enclosure:

```python
EXT = {"top": (197.040, 340.040), "front": (197.040, 61.210), "right": (340.040, 61.210)}
```

Scale placement requires preserving the calibrated image frame all the way into
the PDF. Never re-crop orthographic line images to their ink bounds: the live
rehearsal regression test changed a 100x200 frame to 80x160, causing a 1.25x
scale error when stretched to the original physical extents. `make_drawing.py`
now preserves the frame and rejects blank input; `make_views.py` rejects blank
and out-of-bounds crops. Run `scripts/test_demo_outputs.py` before release.

Two rendering details that matter: **force the plate to pure white before
masking** (reportlab's `mask` takes RGB ranges, so anything short of pure white
leaves a grey rectangle behind every view — whiten above luminance 205, then
mask `[252,255]×3`), and **A3 at 1:2.5 fits a 340 mm part** with room for
dimensions, a parts list and notes; 1:2 collides with the border.

**Rasterise and look at the whole page**: `pdftoppm -jpeg -r 115`. Layout
collisions are invisible in the PDF object model and obvious in the raster.
Budget one fix round and check the whole page, not just the region you changed.

---

## 3 · The native drawing document

### 3a · Default: Drawing API through `execute_code` (tested 28 Oct 2026)

**Call `S.native_drawing(run_dir + r'\drawing_log.json')`, then
`S.open_native_drawing()` in the next call**, from `scripts/fusion/slab_helpers.py`. It is this exact code. The block below
documents the settings; do not retype it.

Two sheets in the Drawing workspace: an isometric view with the **parts list**,
and the orthogonal views. Main assembly only. Measured on SLAB: `createDrawing`
19 s, open 5 s, no timeouts. Save the coloured model first; this is the last
Fusion action. Write the log before opening, because the MCP response can be
lost once the Drawing becomes active.

```python
import time, json, adsk.drawing as D
LOG = r'<run folder>\drawing_log.json'
r = {'t0': time.strftime('%H:%M:%S')}; w = lambda: json.dump(r, open(LOG, 'w'), indent=1)
mgr = D.DrawingManager.get()
di = mgr.createDrawingInput(app.activeDocument.dataFile, D.DrawingCreationModes.AutomaticDrawingCreationMode)
di.baseDocumentType = D.BaseDocumentTypes.FromScratchBaseDocumentType
di.standard = D.DrawingStandardTypes.ISODrawingStandardType
di.units = D.DrawingUnitTypes.MillimeterDrawingUnitType
di.sheetSize = D.SheetSizes.A3ISOSheetSize
di.orientationType = D.SheetOrientationTypes.LandscapeSheetOrientationType
di.sheetCreationType = D.SheetCreationTypes.FirstLevelOnlySheetCreationType
g = di.automationPreferences.globalPreferences
g.isMainAssemblySheetGenerated = True
g.isComponentSheetGenerated = False          # the add-in tool forces True -> 12+ sheets, minutes
g.isSubAssemblySheetGenerated = False
g.isAnimationSheetGenerated = False
g.isFlatPatternSheetGenerated = False
g.isFoldedModelSheetGenerated = False
g.isDetectAndOmitFasteners = True
g.isAutoDimensionEnabled = False             # keep off; dimensions live on the A3 sheet
m = di.automationPreferences.mainAssemblyPreferences
m.isoViewSheetPreferences.isSheetCreated = True
m.isoViewSheetPreferences.isPartsListIncluded = True
m.orthogonalViewSheetPreferences.isSheetCreated = True
m.orthogonalViewSheetPreferences.isPartsListIncluded = False
m.autoDimensionPreferences.isAutoDimensionEnabled = False
v = m.drawingViewPreferences
v.style = D.DrawingViewStyleTypes.VisibleEdgesDrawingViewStyleType
v.tangentEdgesType = D.TangentEdgeDisplayTypes.OffTangentEdgeDisplayType
w(); df = mgr.createDrawing(di); r['t_created'] = time.strftime('%H:%M:%S'); w()
app.documents.open(df); r['t_opened'] = time.strftime('%H:%M:%S'); w()
r
```

Do not read `app.activeProduct.productType` straight after opening: it raises
`InternalValidationError : adapter`. The API exposes the sheets but not their
views or parts lists, so file creation proves nothing about display. **Ask the
user to confirm the drawing and parts list are on screen.**

**Create and open in two separate calls.** Opening the drawing in the same
`execute_code` call that created it raised `Exception in acadm.crx ARX Command —
Unhandled Exception c0000027` on the first drawing after a fresh build 4 times
out of 4 (SLAB_TOP v7, v8, v12, v13; auto-dimension on or off, with or without a
3-minute wait). The file was created, but it never displayed. Creating it in one
call and opening it in the next displayed it with the parts list and no popup
(v14, 30 Oct 2026). The likely reason is that Fusion is still generating views
after `createDrawing` returns. Earlier notes blaming auto-dimension or upload
timing were disproved.

```python
# call 1
SU.native_drawing(run_dir + r'\drawing_log.json')     # creates, does not open
# call 2 (separate execute_code call)
SU.open_native_drawing()                                # LAST Fusion action
```

The open can take over a minute and may exceed the client's request timeout
while succeeding. Never call it twice; after a timeout, ask the user what is on
screen. Then ask the user to confirm the drawing and parts list displayed.

Auto-dimension stays off: dimensions live on the composed A3 sheet, measured
from geometry (§2), and enabling it was never shown to be safe.

### 3b · Fallback: the `create_drawing` MCP tool

```
create_drawing(sheet_size='A3ISO', standard='ISO', units='mm',
               center_marks=False, open_drawing=True)
```

The pinned add-in always generates a sheet per component
(`isComponentSheetGenerated = True`, all levels). On SLAB that is 12+ sheets
and 2.5–4 minutes of main-thread time, and its own flags (auto-dimension, parts
list, iso) don't change that. Use it only if `execute_code` is unavailable.
Expect timeouts, and pass `auto_dimension=False`.

Two arguments are non-negotiable: `sheet_size` needs the full enum stem
**`A3ISO`**, not `A3`, and `center_marks=True` raises `CenterMarkDisplayTypes
not available in this Fusion build`. **A bare `create_drawing()` cannot
succeed.** `open_drawing=True` is what puts the Drawing workspace on screen.

**The call takes longer than the MCP request timeout.** It returns
`Error: Request timed out` and `ping` stops answering for ~45 s. That is also
the signature of a modal hang, so the instinct is to retry — don't.

**How to read it:**

**Do not poll at all here.** Hermes blocks a tool after ~5 identical failures
(`repeated_exact_failure_block`), counting failures rather than attempts, so
probing `ping` while Fusion is busy spends the whole budget in under a minute and
locks you out of the tool you are testing with. **That block is a harness
guardrail, not a Fusion failure - it says nothing about whether the drawing
worked.** Wait once, then check the document type. That is the entire procedure.

**There is no progress signal. Do not invent one.** `create_drawing` reports no
percentage, no elapsed time and no remaining time. A run has been observed
narrating "~25 s remaining", then "~16 s remaining", then "almost clear" - none
of those numbers existed. If you catch yourself producing a countdown, you are
filling an information gap with fiction; say "no signal available" and wait.

**The only fact that settles it is the document type**, so check that rather than
liveness:

- `app.activeProduct` is `adsk::fusion::Drawing`, or `get_design_type` errors with
  `'Drawing' object has no attribute 'designType'` -> **the drawing was created.**
- `app.activeProduct` is still `adsk::fusion::Design` and the workspace is back to
  `FusionSolidEnvironment` -> **the call did not land.** Nothing was created,
  nothing was damaged, and the model is intact. Report it and stop; do not retry
  into the guardrail.

That second case is real: one run polled `ping` five times, hit the block, and
left a healthy 289-body Design document with no drawing.

**The sequence, exactly:**

1. Before calling: confirm `app.activeDocument.dataFile is not None` and the
   document is saved. An unsaved document returns `DESIGN_NOT_SAVED`.
2. Call `create_drawing`. It returns `Error: Request timed out`. **Do nothing.**
3. Wait ~45 s. You have no sleep primitive, so **spend the time on work that
   does not touch Fusion**: draft the stage-10 report, update `BUILD_STATE.json`,
   write the composite summary. Do not poll `ping` - it answers whether or not a
   drawing was made, so it cannot settle the question and it spends guardrail
   budget you may need.
4. Then call `get_design_type` **once**:
   - errors with `'Drawing' object has no attribute 'designType'` -> **created.**
     Only a live Drawing document produces it, because the MCP reads
     `design.designType` and a Drawing product has no such attribute. The MCP can
     no longer operate on the model; the run is over. Say so.
   - returns a design type normally -> **not created.** The model is intact and
     undamaged. Record it as the one open item and finish the run: write the
     report, state that the native drawing did not land on this build, and point
     at the composed A3 sheet as the delivered 2D output.
5. **At most one retry**, and only from step 1. Never a third.

**A failed drawing does not fail the run.** Stage 9 is the last Fusion action and
the only one that is a one-way door; everything of value - model, CMF, renders,
sheet - already exists before it. Deliver those and report the drawing honestly
rather than burning the remaining turns on it.

### History, for the audit trail

| Date | Build | `create_drawing` |
|---|---|---|
| 8 Sep 2026 | `a40f190f…` | `3 : Failed to create drawing document` |
| 9 Sep 2026 | later build | `DESIGN_NOT_SAVED` from a precondition check |
| **11 Sep 2026** | **2705.1.11** | **succeeds**, exceeding the request timeout |

The earlier diagnosis — that this build's `DrawingManager` lacked
`createAutomaticDrawing` and the documented entry point was absent — no longer
describes the behaviour. Re-test each run and report which you get; the version
gap has closed at least once.

---

## What to say when a drawing is requested

**Do not ask which is wanted.** In an autonomous run, produce all three, in the
order below, and label each for what it is:

| Want | How |
|---|---|
| A Fusion-native drawing document | `create_drawing` per §3 — works, and is a one-way door |
| A dimensioned A3 sheet with a parts list, as a PDF | Compose it, §2 |
| Orthographic line-art views of the model | §1, fully scriptable |

Deliver them in that order and never hand over the third while calling it the
first. State in the final report - not as a question - that the session ends in
the Drawing workspace and a human must click the Design tab to reuse the model.
That is a note for the reader, not a blocker: the run is already complete.

