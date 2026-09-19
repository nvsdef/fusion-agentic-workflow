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

1. Confirm host-local MCP discovery and active Design with a read-only query.
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
   Set a unique local non-synced run directory under ~/fusion-renders. Record
   spec revision, document ID, outputs and measured results after every class.
   Use dedicated file-edit tools, not inline shell Python writes. In rehearsal,
   an inline write triggered approval then timed out. Never bypass approval;
   wait for user authorization and re-query state before resuming.
5. Run `uv run python scripts/setup/verify_layout.py`. It checks the SPEC, not
   the live model. Observe supplied PDF and both reference images. Rev C skill
   dimensions govern over concept imagery; report discrepancies explicitly.

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
Configure unapplied, assign last. Clear face overrides, audit through bodies
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
Final heights1200/1400, quality95. Two attempts per view maximum; record gaps.

Verify finished state AND actual nonempty valid files. No fabricated progress:
elapsed_seconds may keep increasing after completion. Renders queue; never
submit another job to check an existing job. Keep mutation calls serialized.

## Composite and drawing

Run host utilities with `uv run python`. Compare raw renders before grading.
The existing measure_classes.py is a DIAGNOSTIC, not a fail-closed gate: it can
count power LED as an eleventh pad and highlights as emitters. Confirm exactly
ten square pad regions using projected ROIs or reviewed overlays. Required
G:R0.55±0.03, RGB spread≤7, mean pad luminance144…160.5. Preserve failed checks.
Housing/reference gaps can be reported without an endless exposure loop.

Load fusion-2d-drawings. Announce monochrome line-art explicitly; it does not
change appearances. Save colored model/archive. Capture all four views,
restore prior camera/style in finally. Preserve calibrated frames through PDF
placement. Compose a run-specific sheet JSON from measured geometry, not old
model/date/material claims. Rasterize with PyMuPDF or Poppler and inspect.

Native drawing is experimental and LAST Fusion action. A timeout may succeed;
wait then inspect product state once, never blind-retry. Drawing active proves
creation/activation, not sheet correctness. If it fails, deliver composed PDF
and report the native gap. Do not use export_drawing_pdf.

## Report and end

Write outside Fusion. Include artifact paths and manifest, per-class checks,
actual CMF, render metrics and visual findings, native-drawing status, changes
with reasons, and unresolved decisions. DEC-C3 arithmetic:46−61.18=−15.18 mm
against+2; shortfall17.18, closed nonblocking no-bezel decision.

Keep DEC-C1…C7 closed. Carry TBD-12…19 and omitted internals forward. Zero user
parameters means no demonstrated named-parameter editing. Do not quote default
material mass as product mass. End as complete, complete_with_findings, or
halted with measurements. A failed output must not disappear behind PASS.
