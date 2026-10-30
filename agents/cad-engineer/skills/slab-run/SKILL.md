---
name: slab-run
description: "Use when building SLAB end to end in live Fusion."
---

# SLAB: agent-owned end-to-end procedure

Generate CAD code yourself through MCP. This is not playback of a build script.
`slab-product-spec` owns dimensions and CMF; this file owns order. Installation
is in repository SETUP.md. Read project AGENTS.md and SOUL.md. Utility scripts
handle pixels/PDFs, never product modeling decisions.

## Preflight and state

1. Load `fusion-mcp-driving` section 0 BEFORE the first identity query. Use
   `app.activeDocument.name` and `app.activeDocument.dataFile`, never
   `design.name`, `design.dataFile` or speculative Product accessors.
   Confirm host-local MCP discovery and active Design with that read-only query.
   `ping` only proves transport. A Drawing/No active design error means select
   the Design tab; do not blindly create a new document or retry writes.
2. Read BUILD_STATE.json if present. Compare document/cloud ID and completed
   classes with live state. A mismatch is not permission to clear geometry.
   Fresh runs require an empty Design (root bodies AND occurrences inspected).
3. Resolve a cloud project before deriving a unique `SLAB_TOP_vN` name. Use an
   explicitly requested destination; otherwise prefer Default Project when
   available. Do not overwrite an unrelated model. Save before features,
   verify DataFile present, and record stable cloud ID after synchronization.
4. Initialize ignored BUILD_STATE.json from examples/BUILD_STATE.template.json.
   Set a unique local non-synced run directory under ~/fusion-renders (in Cowork,
   use the session outputs folder instead: the Linux sandbox that runs the host
   utilities cannot see the Windows home directory, and `start_render` needs a
   Windows path both sides can read). Record
   spec revision, document ID, outputs and measured results after every class.
   Use dedicated file-edit tools, not inline shell Python writes. In rehearsal,
   an inline write triggered approval then timed out. Never bypass approval;
   wait for user authorization and re-query state before resuming.
5. Run `uv run python scripts/setup/verify_layout.py`. It checks the SPEC, not
   the live model. Observe supplied PDF and both reference images. Rev C skill
   dimensions govern over concept imagery; report discrepancies explicitly.

### Preflight code (verified 28 Oct 2026; paste, do not reinvent)

Order: Step 1 query, then Step 3 save (it picks the name and run folder), then
register the SU helpers **in a separate call**, then write BUILD_STATE.json with
the values Step 3 returned. Do not choose the document name or run folder
yourself before Step 3: `SLAB_TOP_v1…vN` may already exist in the cloud. Use
`~/fusion-renders/<name>`, not a Temp folder.

`execute_code` takes exactly one argument, `code`. There is no `timeout`,
`wait` or `async` parameter; extra arguments are rejected before reaching
Fusion. The request timeout is a client setting (Hermes:
`mcp_servers.fusion360.timeout`, 360 recommended), not something a call can pass.

Step 1, read-only (`execute_code`). Expect `DesignProductType`, an edit object of
`adsk::fusion::Component`, and 0 occurrences, bodies and timeline items for a fresh run:

```python
root = design.rootComponent
{'doc': app.activeDocument.name, 'saved': app.activeDocument.isSaved,
 'product': app.activeProduct.productType, 'edit': design.activeEditObject.objectType,
 'occ': root.occurrences.count, 'bodies': root.bRepBodies.count, 'timeline': design.timeline.count}
```

Step 3, cloud save plus run folder (`execute_code`, one call). Use `app.data.activeHub`:
`app.data.activeProject` raises on an unsaved document, and `saveAs` needs a
**DataFolder** (`proj.rootFolder`), not a name or path:

```python
import os
prjs = app.data.activeHub.dataProjects
proj = next((prjs.item(i) for i in range(prjs.count) if prjs.item(i).name == 'Default Project'), prjs.item(0))
names = [proj.rootFolder.dataFiles.item(i).name for i in range(proj.rootFolder.dataFiles.count)]
n = 1
while 'SLAB_TOP_v%d' % n in names: n += 1
name = 'SLAB_TOP_v%d' % n
run_dir = os.path.join(os.path.expanduser('~'), 'fusion-renders', name)
for d in ('renders', 'views', 'tools'): os.makedirs(os.path.join(run_dir, d), exist_ok=True)
ok = app.activeDocument.saveAs(name, proj.rootFolder, 'SLAB - portable 6-channel production mixer', 'RevC')
{'saved': ok, 'doc': app.activeDocument.name, 'root': design.rootComponent.name,
 'data_file_id': app.activeDocument.dataFile.id if app.activeDocument.dataFile else None, 'run_dir': run_dir}
```

The save takes 1–70 s. If the call times out, run the step 1 query again (the
name will be `SLAB_TOP_vN` if it landed); never call `saveAs` twice.

Step 4: copy `examples/BUILD_STATE.template.json` **unchanged in shape** to
`<run_dir>/BUILD_STATE.json` and fill `status: "running"`, `document`,
`data_file_id`, `run_dir`. Keep the template's keys; do not invent new ones.
After each class, append to `completed_classes` and set `bodies`.

**If the same call fails twice, stop and re-read this skill rather than trying
variations.** Hermes blocks a tool after about 5 identical failures
(`repeated_exact_failure_block`). It reports this as a cooldown; it is a
harness guardrail, not a Fusion or MCP fault. Waiting does not fix the
cause: correct the call from this skill or fusion-mcp-driving §0 first, then
follow the cooldown protocol there (wait the full interval, one ping, one
corrected read-only query).

## Stages

| Stage | Work | Evidence |
|---|---|---|
| 1 | Save cloud Design | document name, DataFile ID |
| 2 | Inspect current model | fresh/resume/verify decision, live counts |
| 3 | Twelve feature classes | per-class measurements and health |
| 4 | CMF | both albedos, roughness/f0/emission, effective assignment tally |
| 5 | Viewport/layout | orthographic capture and measured clearances |
| 6 | Render workspace/exposure | visible switch, property readback, probe pixels |
| 7 | Hero and plan raytraces | camera readback, job IDs, actual image files |
| 8 | Composite/compare | raw versus composite metrics, pad identity |
| 9 | Line views, A3 PDF, native drawing LAST | crop, raster check, drawing status |
| 10 | Report | changes, arithmetic, failures/open decisions, artifact manifest |

Announce each stage and immediately print `STAGE n · measured values · PASS`,
FAIL, OPEN or NOT IMPLEMENTED as appropriate. Print every class's count,
volume and bbox/radii before proceeding. Maintain the task checklist. A later
summary does not substitute for live progress; the rehearsal missed this rule.

Batching: several one-class calls per turn is fine (run 4 built 12 classes in
1:29). But a call that fails does not stop the next call in the batch, so never
batch `start_render` or `create_drawing` behind a call that can refuse. Create
the run folders in the save step, not in a later guarded call. The first cloud
`saveAs` has taken 54 s to over 65 s: if it times out, query document name and
dataFile before doing anything else, and never replay it.

Clock-stamp every Fusion call: return `time.strftime('%H:%M:%S')` at the start
and end of each `execute_code` result, so per-stage wall time is measured, not
reconstructed.

## Run profiles

Pick one at the start and say which. Geometry, CMF, layout, line views, sheet and
report are identical in both. Only stages 7–9 differ.

| | FULL (deliverable) | DEMO (fast, live audience) |
|---|---|---|
| Exposure probe | 256 px q25 | **skip: the preview hero is the exposure check** |
| Hero | raytrace 1200 px q95 (~70 s) | **raytrace 900 px q50 (17 s measured), labelled "preview render"** |
| Plan | raytrace 1400 px q95, aspect pinned portrait | **viewport capture of the calibrated plan camera, taken in the Design workspace (the Render workspace adds a large ground shadow), labelled "viewport capture, not a raytrace"** |
| Composite | difference-matte composite | **none: deliver the raw render** |
| Pad metrics | projected-ROI, both views | projected-ROI on the hero preview, reported as indicative |
| Native drawing | 2 sheets: iso + parts list, orthogonal views; auto-dimension OFF (~24 s) | same |

Never present a viewport capture or an earlier run's image as a raytrace from
this run. The DEMO profile is fast because it renders less, not because it
pretends.

Baseline (28 Oct 2026, FULL profile, Claude in Cowork): build 6 min, CMF and
layout 2 min, render stage 7.5 min, 2D 1 min, native drawing 3.8 min. Total
20.5 min. Fusion compute for all 289 bodies was ~15 s; agent turns dominate.
Run 2 (same day, DEMO profile, fixes applied, no GUI interaction): 7 min 19 s
preflight to confirmed drawing. Build 1:35, CMF + check + save 0:29, hero
preview 17 s, all view captures 6 s, drawing ~1:05 + one check. The preview's
pad and housing metrics matched the q95 hero to 0.1 levels. The first cloud
`saveAs` took 54 s (0.6 s in run 1), so save early. Tool calls batched together
still run in sequence; the drawing wait can only be hidden by an async MCP call.

## Build and repair

Load fusion-scratch-build and slab-product-spec before stage 3. One feature
class per call; name all features/sketches/bodies. The twelve classes are:
upper shell; upper cuts; base/feet/ports; panel; small knobs; large knobs;
pads; ticks; pointers; toggle/LED; dividers; graphics.

Target 289 bodies in 12 components. Check every specified volume, position,
radius, graphics area and timeline health. Whole-model bbox is approximately
[-99.52,-170.02,-0.03,97.52,170.02,61.18] mm including API padding. Do not
adjust actual geometry to reproduce instrumentation padding.

On failure, record measured/expected and the specific cause. Query first after
an uncertain transport outcome. Repair only the failed class's owned features,
in reverse dependency order. Upper shell and upper cuts share a component:
never reset the whole component for a cut failure. Maximum two targeted repair
attempts after the initial attempt, then halt modeling and write the report.
A provisional glyph-area miss may be carried OPEN after that budget, but not a
body-count or structural failure; never call a miss PASS. Keep TBD-17/18 open.

A warm model may skip construction only after ALL geometry checks are actually
performed, not merely a total body count. Unknown appearance names, missing
properties, swapped class assignments or absent emissions fail CMF. No bundled
gate script is claimed to be a comprehensive validator: derive and execute the
required checks from the spec and preserve the results.

## Finish

Load the spec CMF table. Create ten exact SLAB appearance names from the library
source exposing the seven required properties; check source before copying.
Configure unapplied, assign last, all 289 in one call: set the body appearance
FIRST, then fix only faces that still differ (spec §5 step 4; face-first is
~13x slower and is what used to hit the request timeout). Audit through bodies
and faces. Expected tally: Gray_Flat1, Black_Semi5, Panel_Dark1, Knob_Black196,
Knob_Orange4, LED_Emissive11, Pointer_White20, Toggle_Gray1, Print_Ink50;
Tick_Print is unused. All names have SLAB_ prefix. Total289.

Judge layout on top orthographic view. Measure widest knob gap13.000 mm,
knob/pad7.700, recess margins1.000, pad inset0.200, pad/panel0.700. Checks for
indicator-under-knob and boss-to-aperture are not implemented. Graphics area
alone cannot see glyph/seam intersections; inspect them and report, not hide.

## Render

Load fusion-photoreal-render. Activate Render visibly before camera setup.
Write brightness1700 and cameraExposure9.5 as initial calibration values,
read back; low-resolution test housing band177…185. These values are a tested
starting point, not universal exposure truth. Explicit `view='current',
fit=False`; otherwise the wrapper can reset framing. Hero152cm target distance,
303deg azimuth,46deg elevation,14deg FOV; plan +Z/up+Y orthographic fit×1.10.
Final heights1200/1400, quality95 (FULL profile; DEMO is in the profile table).
Two attempts per view maximum; record gaps.

FULL plan: pin `sceneSettings.aspectRatio` to a portrait value before the plan
render. The viewport is landscape and the composite crops to 0.656, so an
unpinned 2242x1400 plan discards ~60% of its pixels (117 s measured).

Verify finished state AND actual nonempty valid files. No fabricated progress:
elapsed_seconds may keep increasing after completion. Renders queue; never
submit another job to check an existing job. Keep mutation calls serialized.
While a raytrace runs, Fusion's main thread is busy: `execute_code`,
`render_view` and `get_design_type` block until it finishes. Poll only with
`get_render_status`, and spend the wait on host-side work (composite the
previous view, BUILD_STATE, report draft).

**Pad check is an open calibration item, not a tuning loop.** On 28 Oct 2026 the
spec CMF at brightness 1700 rendered pad red clipped at 255: G:R 0.66, luminance
~179, against 0.55±0.03 and ≤160.5. Lowering emissive luminance from 150 to 25
only reached 0.596 / 166.9, because the albedo saturates red on its own. Measure
once, report FAIL with numbers, and do not edit CMF to chase it.

## Composite and drawing

Run host utilities with `uv run python`. Compare raw renders before grading.
The existing measure_classes.py is a DIAGNOSTIC, not a fail-closed gate: it can
count power LED as an eleventh pad and highlights as emitters. Confirm exactly
ten square pad regions using projected ROIs: after the render finishes, project
each pad's top-centre with `app.activeViewport.modelToViewSpace`, write
`{"vp":[w,h],"pads":[[x,y],...]}` to JSON, and run
`scripts/pad_roi.py <render.png> <rois.json>` (it scales by image height over
viewport height). Colour thresholds also catch the orange knobs. Required
G:R0.55±0.03, RGB spread≤7, mean pad luminance144…160.5. Preserve failed checks.
Housing/reference gaps can be reported without an endless exposure loop.

composite.py keys by flood-fill within ±6 of the modal backdrop. On 28 Oct 2026
the backdrop was not uniform (border std 1.66, levels 172–178), so the matte
leaked: a halo on the hero, and the plan crop shifted off the product. Raising
the tolerance did not fix it. Until a difference matte (empty-plate render at
identical settings) is implemented, inspect every composite and fall back to the
raw render if the matte leaks.

Load fusion-2d-drawings. Announce monochrome line-art explicitly; it does not
change appearances. Save colored model/archive. Capture all four views,
restore prior camera/style in finally. Preserve calibrated frames through PDF
placement. Compose a run-specific sheet JSON from measured geometry, not old
model/date/material claims. Rasterize with PyMuPDF or Poppler and inspect.

**Not by default: the composed sheet as a picture in the Design.** The drawing and
parts list belong in the Drawing workspace (native drawing below). Only if a
viewer explicitly asks to see the composed PDF inside Fusion: rasterize the
PDF at 150 dpi (`pdftoppm -png -r 150 -singlefile`) and insert it as a canvas
on the root XY plane: `root.canvases.createInput(png, root.xYConstructionPlane)`,
then `canvas.transform` = Matrix2D with cells (0,0)=42.0, (1,1)=29.7 (true A3 in
cm) and translation (0,2)=14.0, (1,2)=-14.85, which puts it beside the model at
X +140…+560 mm. Name it as an image ("GA_Sheet_A3 (composed sheet image)"),
frame a top orthographic view on both, and save. A canvas is not a body or a
component, so the 289/12 checks stand. Its timeline entry reports healthState 4
with no message; exclude canvases from the health check. Measured: 2 s.

Native drawing is experimental and LAST Fusion action. A timeout may succeed;
wait then inspect product state once, never blind-retry. Drawing active proves
creation/activation, not sheet correctness. If it fails, deliver composed PDF
and report the native gap. Do not use export_drawing_pdf.

**Create the native drawing through the Drawing API in `execute_code`, main
assembly only, two sheets.** Exact code: fusion-2d-drawings §3a. Do not use the `create_drawing` MCP tool: the
pinned add-in hard-codes `isComponentSheetGenerated = True` with
`AllLevelsSheetCreationType`, so Fusion also builds one sheet per component
(11 more sheets of views). That is what held the main thread for ~2.5–3.8 min
and pushed every call past Cowork's ~65 s MCP timeout. Turning off
iso/parts list/dimensions (tried in runs 2 and 3) removed the sheet the user
wants and saved nothing. Settings (`import adsk.drawing as D`):

- `createDrawingInput(doc.dataFile, AutomaticDrawingCreationMode)`;
  FromScratch base, ISO, mm, `A3ISOSheetSize`, landscape,
  `sheetCreationType = FirstLevelOnlySheetCreationType`
- global: main-assembly sheet ON; component, sub-assembly, animation,
  flat-pattern and folded-model sheets OFF; **auto-dimension OFF**
  (`globalPreferences.isAutoDimensionEnabled` and
  `mainAssemblyPreferences.autoDimensionPreferences.isAutoDimensionEnabled`)
- main assembly: iso sheet ON with `isPartsListIncluded = True`; orthogonal
  sheet ON, no parts list; view style visible edges, tangent edges off
- `mgr.createDrawing(di)` then `app.documents.open(df)`

**Never enable automatic dimensioning on SLAB.** On 28 Oct 2026, runs 4 and 5
(parts list ON + auto-dimension ON) raised `Exception in acadm.crx ARX Command —
Unhandled Exception c0000027` in Fusion's drawing engine. The drawing file was
still created in the cloud with 2 sheets, so an API readback reported success,
but the drawing never displayed. With auto-dimension OFF and everything else
the same, in the same Fusion session, it created in 19 s, opened in 5 s, and
showed the parts list. Dimensions live on the composed A3 PDF (measured
values). The crash dialog is modal and invisible to the agent: after opening,
**ask the user to confirm the drawing displayed**, and never claim a native
drawing from file creation alone.

Measured 28 Oct 2026 (SLAB_TOP_v8, auto-dimension off): `createDrawing` 19 s,
open 5 s. **24 s total, no timeouts, no crash.** The API sets sheets, not individual views: the
orthogonal sheet comes as one set. Write a JSON timing log *before* opening:
reading `app.activeProduct.productType` on the just-opened Drawing raises
`InternalValidationError : adapter`, and the MCP response is lost.
The fix belongs in the add-in too: expose `component_sheets` and
`sheet_creation` arguments on `create_drawing` (default off / first level).

## Report and end

Write outside Fusion. Include artifact paths and manifest, per-class checks,
actual CMF, render metrics and visual findings, native-drawing status, changes
with reasons, and unresolved decisions. DEC-C3 arithmetic, from the measured
tallest feature: 46.000−61.150=−15.150 mm against +2; shortfall 17.150 (the
historical −15.18 / 17.18 used the API-padded 61.18). Closed, nonblocking
no-bezel decision.

Keep DEC-C1…C7 closed. Carry TBD-12…19 and omitted internals forward. Zero user
parameters means no demonstrated named-parameter editing. Do not quote default
material mass as product mass. End as complete, complete_with_findings, or
halted with measurements. A failed output must not disappear behind PASS.
