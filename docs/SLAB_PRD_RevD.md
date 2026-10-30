# SLAB
## Product Design Brief • Revision D
Portable 6-Channel Production Mixer / USB-C Audio Interface

**Issued:** 18 September 2026
**Owner:** S. DeFibaugh
**Status:** Exterior CAD reference and agentic demonstration brief. Completed rehearsal with findings; NOT a manufacturing release.
**Supersedes:** Rev C for this demonstration brief. Rev C remains an immutable historical record.
**Measured reference:** SLAB_TOP_v13, Autodesk Fusion 2705.1.11, rehearsal of 18 September 2026.

### What changed
Revision D preserves the core Rev C geometry and CMF. It corrects the distinction between requirements and historical results, consolidates DEC-C1–C7, documents provisional artwork and image-validation gaps, and separates product requirements from changing installation instructions. No new electronics, mechanical internals, or tooling approvals are implied.

### How to use this brief
This document states what to build and what evidence is required. The repository skills describe how the agent constructs and verifies it. Read the dimensional skill alongside this brief; report discrepancies rather than silently selecting convenient values. Rev D supersedes stale Rev C status, acceptance and execution statements. Explicit provisional geometry is a reproducible reference, not approval of an open design decision.

The intended workflow is agentic: the agent interprets the brief, plans feature classes, generates Fusion API code, measures results, diagnoses faults and reports findings. Deterministic utilities may install dependencies, measure images and compose a PDF; they must not replace the agent with a hidden full-product build script.

### Document map
1. Product intent and scope
2. Datum, envelope and component structure
3. Housing, panel and controls
4. Markings and provisional artwork
5. Color, material and finish (CMF)
6. Acceptance and deliverables
7. Rehearsal results and limitations
8. Closed decisions and open items
9. Sources, revision control and operational boundary

---PAGE---
## 1. Product intent and scope
SLAB is a portable, battery-powered six-channel production mixer and USB-C audio interface concept, organized around an exposed, tactile control deck. The demonstrator expresses its enclosure, control layout and gray/black/orange visual identity. It does not establish audio performance, electrical design, battery safety, manufacturability or regulatory compliance.

Rev C summarized earlier audio/electronics intentions without sufficient executable specifications. Those intentions remain forward scope; Rev D does not invent missing requirements.

### Included in this demonstration
- Rounded two-part enclosure with feet, panel recess, edge notches and strip cuts.
- Two left-side USB-C aperture representations.
- Plain control panel; twenty small knobs and three large knobs.
- Ten illuminated pads, one toggle representation and one power LED.
- Graduation ticks, pointers, divider rules and lower-deck graphics.
- Custom optical appearances, calibrated renders, line-art views, A3 general arrangement and verification report.

### Explicitly excluded
PCB, battery pack, battery hatch, rear I/O plate and bay, potentiometer shaft holes, bosses/internal ribs, physical lightguides, housing draft and draft analysis, orange panel speckle, and in-panel functional legend text. The cylinder called a power toggle is an exterior placeholder, not a sourced switch mechanism.

### History-based is not parameter-driven
Capture Design History is enabled. The measured reference contains **zero named user parameters**. It demonstrates history-based construction, not named-parameter-driven editing. A future parameterization task must wire dimensions/expressions and verify a change/recompute test; adding unused parameter names does not satisfy it.

### Reference images
The committed hero and plan concepts convey form and color, not dimensional truth. They contain ambiguous controls and stylized lettering and disagree in lighting. Do not trace them into new mechanical requirements. The resolved dimensions and decisions in this brief govern the demonstrator.

### Physical materials
CMF values describe optical appearances only. Physical material assignments and sourcing are unverified. Do not report default-density model mass as product mass, or copy historical ABS/PC/aluminum labels into a release BOM as approved materials.

---PAGE---
## 2. Datum, envelope and component structure
All dimensions are **millimetres** unless explicitly stated. Volumes marked cm³ are verification checksums, not manufacturing tolerances. Fusion API lengths are centimetres; conversion belongs at the API boundary.

| Quantity | Requirement / interpretation |
|---|---|
| Origin | Center of footprint in plan; Z = 0 at ground |
| Axes | +Y away from operator, long axis; +X operator's right; +Z up |
| Housing plan | X 195.0 × Y 340.0; plan corner radius 10.0 |
| Housing top | Z 46.0; this is not the overall control height |
| Split line | Z 23.0 |
| Shell wall | 2.5 on both moldings |
| Base | Z 3.5–23.0; feet Z 0–3.5 |
| Upper | Z 23.0–46.0 |
| Recess | 137 × 213, center (0, +59.5), depth 2.4 |
| Panel | 135 × 211 × 2.0, center (0, +59.5), Z 43.6–45.6 |

**Measured assembly bbox:** X −99.52…+97.52, Y −170.02…+170.02, Z −0.03…61.18; size 197.04 × 340.04 × 61.21. These figures include small API bounding-box padding. Nominal toggle extreme is X −99.5 and pointer top Z 61.15. Do not offset real geometry to manufacture the padding.

### Component structure
| Component identifier | Bodies | Function |
|---|---|---|
| SLAB_Housing_Upper | 1 | Upper shell with cuts |
| SLAB_Housing_Base | 5 | Base shell plus four separate feet |
| SLAB_Panel_Control | 1 | Plain panel |
| SLAB_Knob_Small | 20 | Tapered knobs |
| SLAB_Knob_Large | 3 | Large straight knobs |
| SLAB_Keypad | 10 | Illuminated pads |
| SLAB_Panel_Ticks | 173 | Graduation bars |
| SLAB_Knob_Pointers | 23 | Pointer boxes |
| SLAB_Power_Switch | 2 | Toggle and power LED |
| SLAB_LED_Indicators | 1 | Merged non-emissive divider rules |
| SLAB_Panel_Graphics | 50 | Lower-deck graphics |
| Total | 289 | 12 components INCLUDING the root |

The legacy name SLAB_LED_Indicators is retained as an identifier; it does not imply a modeled lightguide or emissive divider.

---PAGE---
## 3. Housing, panel and controls
### 3.1 Housing and panel
Upper: rounded outline at Z23, height23, hollow inward2.5 with bottom removed. Base: same outline at Z3.5, height19.5, hollow inward2.5 with top removed. The panel is sharp-cornered, without shaft holes. Its recess clearance is1.0 on each side; panel Y range is −46…+165.

| Feature | Geometry and position |
|---|---|
| Recess | 137 × 213 at (0,59.5), Z46 down to43.6 |
| Top-left notch | X width21, Y height14.3, center(−90.2,143.8), depth1.2 |
| Top-right notch | Width21, height9.5, center(91,139.5), depth1.2 |
| Mid-left notch | Width21, height22.9, center(−90.2,40.3), depth1.2 |
| Mid-right notch | Width21, height12.4, center(91,66.5), depth1.2 |
| Six strips | 29 × 1.0 × depth0.5; X±83, Y112.8/57.4/12.6 |
| Four feet | 18 × 18 × 3.5; centers X±77.5, Y±150 |
| USB apertures | Two9.5(Y) ×4.0(Z) through left wall; Y−38/−16, Z center13.5 |

Notches deliberately overhang the X±97.5 outline. Cut their intersection with the shell; do not clamp their rectangles. USB apertures lie entirely in the base band and do not cross Z23.

### 3.2 Knobs
| Feature | Geometry / centers |
|---|---|
| Small knobs | 20; base diameter13.5; height15.5; Z45.6–61.1; 5° narrowing upward; top filletR0.75 |
| Small grid | X−50.4,−16.8,+16.8,+50.4; Y28,58,88,118,148 |
| Large knobs | 3; diameter32; height14; Z45.6–59.6; straight; top filletR1.10 |
| Large centers | X−45,0,+45; Y−23 |

Small nominal unfilleted top diameter is approximately10.79. After filleting, verify circular edges by [Z,radius]: **[45.6,6.75], [60.42,5.454], [61.1,4.707]**. Large: **[45.6,16], [58.5,16], [59.6,14.9]**. Edge radii versus Z discriminate orientation; total volume alone is not an orientation proof.

### 3.3 Pads and power controls
Pads: ten18.6-square bodies, plan cornerR3, Z44.2–46.6. They stand0.6 above the housing top; no pad recess is included. Centers: bottom(−88,−56),(−44,−56),(0,−56),(44,−56),(88,−56); left(−88,76),(−88,−4); right(88,93),(88,40),(88,−4). Edge inset0.200 is intentional.

Toggle: diameter11 at(−94,+130), Z44.2–59.0; nominal bbox[−99.5,124.5,44.2,−88.5,135.5,59]. Power LED: diameter5.2 at(91,139.5), Z46.0–46.6.

---PAGE---
## 4. Markings and provisional artwork
### 4.1 Graduation ticks and pointers
Graduation bars are width0.8 and height0.45 from Z45.6. Angles span−125°…+125° around +Y. A radial convention is u=(−sin a,cos a); the symmetric pattern does not depend on traversal direction.

| Ring | Bars per knob | Radial range | Total |
|---|---|---|---|
| Small | 7, step250/6° | 8.75–11.25 | 140 |
| Large | 11, step25° | 18.0–21.5 | 33 |

All173 ticks are black. Pointers are1.1(X) ×5.6(Y) ×0.92(Z), oriented +Y. Small: centers at knob center+(0,3.1), Z60.23–61.15. Large: X−45/0/+45, Y−15.65, Z58.73–59.65. Tops are0.05 proud of host top planes; they must not be coplanar.

### 4.2 Section dividers
Orange, non-emissive, height0.5 from Z45.6. One horizontal132×0.9 atY+4; two vertical0.9×47 atX±22.5 fromY+4 down to−43, centerY−19.5. Rules connect into one body; nominal bbox[−66,−43,45.6,66,4.45,46.1].

### 4.3 Lower-deck graphics
All graphics are raised0.15 from Z46.0, outside the control panel.

| Subclass | Bodies | Definition / signature |
|---|---|---|
| Table | 1 | Three193×1.5 rules atY−67.1/−93.6/−116.2; divider1×49.1 centered(−23.8,−91.65); seam1×113 centered(68.5,−103.5). Top area1023±10 mm². |
| Grids | 2 | X−8.3…5.2 and16.8…30.3, Y−141…−127.6; four horizontal and four vertical bars, width0.8, outer edges inset to outline. Area75.84 mm² each. |
| Scale | 30 | X−56.6…−14.1, spacing42.5/29; baselineY−146.7, extends+Y; width0.6, length3.6 every fifth, otherwise2.4. |
| R/I/V | 3 | Lower-deck glyphs, height9.5, nominal stroke1.6. Targets R42.1/I15.2/V27.9 mm², tolerance±1.5. Provisional construction. |
| Waveform | 14 | Width0.8; X34…62, spacing28/13; centeredY−134.3; heights stay in lower-deck band. Provisional. |

Grid horizontal centers runY−140.6…−128.0, step4.2. Vertical centers runx0+0.4…x0+13.1, evenly spaced. Orthogonal bar intersections enclose unwanted cells; reject those cells, not real bars. Do not apply the same minimum-bbox filter to diagonal glyph strokes.

**Open visual issue:** the provisional V intersects the specified seam atX68.5. Correct body count and glyph area do not resolve this. Preserve the finding for ID; do not silently move the seam or glyph and claim conformance. Appendix A records the tested provisional artwork without closing TBD-17/18/19.

---PAGE---
## 5. Color, material and finish
These are **appearance settings**, not approved physical materials. Use the exact identifiers. Configure appearances before assignment; audit effective body/face values, not merely the document's name list. Set both albedo properties to the RGB values below.

| Appearance | RGB albedo | Roughness / f0 | Assigned bodies |
|---|---|---|---|
| SLAB_Gray_Flat | 196,196,196 | 0.50 / 0.040 | 1 upper |
| SLAB_Black_Semi | 48,48,50 | 0.38 / 0.055 | 5 base/feet |
| SLAB_Panel_Dark | 78,78,82 | 0.60 / 0.042 | 1 panel |
| SLAB_Knob_Black | 42,42,44 | 0.30 / 0.058 | 196 |
| SLAB_Knob_Orange | 252,108,64 | 0.34 / 0.050 | 4 |
| SLAB_LED_Emissive | 255,122,48 | 0.26 / 0.050 | 11 |
| SLAB_Print_Ink | 58,58,62 | 0.70 / 0.035 | 50 graphics |
| SLAB_Pointer_White | 212,212,212 | 0.50 / 0.045 | 20 |
| SLAB_Toggle_Gray | 200,200,200 | 0.35 / 0.050 | 1 |
| SLAB_Tick_Print | 92,46,22 | 0.62 / 0.040 | 0, defined only |

Knob_Black serves20 small knobs,173 ticks and3 large pointers. Knob_Orange serves3 large knobs and1 divider body. LED_Emissive serves10 pads and1 power LED. Pointer_White serves20 small pointers. Exactly289 bodies are assigned among nine used custom appearances; ten custom appearances are defined. A retained library source may make the total document appearance count11; name/property/assignment audits are more meaningful than that incidental total.

Emissive settings: opaque_emission=True; opaque_luminance=150.0; modifierRGB(255,140,70). Other appearances are non-emissive. Prism property identifiers and library-source selection belong in the maintained CMF skill.

### CMF acceptance
- Both albedos equal the table RGB values; roughness and f0 match within the configured numerical audit tolerance.
- Every component/body uses the specified optical role; using a valid but wrong SLAB appearance fails.
- No unresolved duplicate names or conflicting face overrides.
- Eleven emissive bodies, assigned to pads/power LED only.
- Viewport and raytraced outputs preserve the intended gray/black/orange identity.

The ten-pad illumination check must exclude the power LED. Reflections on orange knobs are not additional emitters. A monochrome line-art or Drawing viewport intentionally omits appearance presentation; it is not a CMF reassignment. Save the colored model before opening the drawing.

---PAGE---
## 6. Acceptance and deliverables
### 6.1 Geometry checks
Use closed-form checks with explicit units. Rounded reference volumes are accepted within0.001 cm³ unless a more specific band is given; this is a computational check, not a production tolerance. Check placement independently. Report failures and preserve evidence rather than changing the expected values.

| Check | Required value |
|---|---|
| Upper rounded solid before shell | 1522.926 cm³ |
| Upper after shell | 219.091 cm³ |
| Upper after recess | 149.056 cm³; recess removal70.0344 cm³ |
| Four notches | removal1241.0–1241.4 mm³ |
| Six strips | removal87.0 mm³ |
| Base after shell, before ports/feet | 209.947 cm³ |
| Two USB cuts | removal190.0 mm³ |
| Each foot | 1.134 cm³ |
| Panel | 56.970 cm³ |
| Assembly | 289 bodies,12 components including root; healthy timeline |

Small/large knob radii and positions, all control counts, graphic connectivity and areas must also pass. Body and face counts alone are not sufficient. CAD API bbox padding is not a geometric tolerance.

### 6.2 Layout checks
| Check | Reference / condition |
|---|---|
| Minimum knob-to-knob plan gap | 13.000 mm; requirement≥4.0 |
| Knob-to-pad plan clearance | 7.700 mm; no overlap |
| Panel inside recess | 1.000 mm all four sides |
| Edge-pad housing inset | 0.200 mm; intentional |
| Pad-to-panel gap | 0.700 mm; positive |
| Indicator burial / boss-aperture | NOT IMPLEMENTED; no passing claim |

Evaluate knobs at their widest sections. The shipped layout arithmetic script checks specified coordinates, not the live model. Re-measure live geometry after changes. Add visual inspection for interactions not captured by these checks, especially artwork/seam conflicts.

### 6.3 Required output set
Cloud-saved Design, per-class verification record, CMF audit, top viewport inspection, hero and plan raytraces, composited images, four orthographic/isometric line-art captures, dimensioned A3 PDF, native model archive, experimental native drawing attempt, and final report/manifest. Distinguish the composed raster-view PDF from an associative native drawing. Neither replaces the other silently.

A3 landscape at1:2.5: three dimensioned orthographic views, isometric, parts list totaling289 bodies, notes and current model/revision/date. Detailed view and scale acceptance continues below.

---PAGE---
## 6.4 Render acceptance
Drawing acceptance: preserve analytical crop frames through PDF placement. Reject blank/out-of-bounds views, inspect clipping and rasterize the sheet. Crop-aspect target≤0.11% is necessary but not sufficient; verify linework and scale. Native drawing activation does not certify sheet content.
| Item | Requirement / reference |
|---|---|
| Hero camera | Perspective; azimuth303°, elevation46°, FOV14°; distance152 cm from target(0,0,26 mm); up+Z |
| Plan camera | Orthographic, eye+Z, up+Y; fit then frame expansion1.10 |
| Final raw images | Hero height1200 px; plan height1400 px; quality95 reference setting |
| Framing | Whole product visible; verify actual pixel dimensions and camera |
| Post aspect | Hero1.328; plan0.656; preserve all product geometry |
| Initial exposure probe | Brightness1700, cameraExposure9.5; housing luminance177–185 on low-resolution test |
| Pad count | Exactly10 identified square pads, excluding power LED/highlights |
| Pad G:R | Mean0.55±0.03 |
| Pad luminance | Mean144.0–160.5 in the defined raw-image sampling method |
| Pad uniformity | Across-pad mean RGB channel spread≤7 levels |

Exposure values are a measured starting point for the reference document, not universal physical settings. Use calibrated cameras and explicit current-view/no-refit behavior regardless of tool defaults. API commands and timeout values belong in SETUP and skills, not in permanent dimensional requirements.

The pad luminance lower bound144.0 follows the current workflow's rounded envelope and includes the concept-plan value144.8; it replaces the inconsistent144.9 wording in Rev C. It does not excuse an upper-bound failure. Glyph acceptance consistently uses±1.5 mm² rather than Rev C's alternate±2 statement.

Record whether metrics use raw renders or composites, the masks/ROIs, exclusions, resolution and aggregation method. Threshold-selected bright cores and whole-pad samples are not interchangeable. Preserve overlays so pad identity can be reviewed. Current scripts are diagnostics, not a complete fail-closed image validator.

Reference class means reported historically: housing174.9(hero)/179.5(plan); dark43.4/27.8; pad luminance159.0/144.8. These are historical samples, not independently re-certified pixel masks. Report housing/dark gaps without endlessly tuning exposure to one image at the expense of another. Do not treat a reference band as a reason to change product albedo silently.

### 6.5 Stage disposition
Use PASS, FAIL, OPEN or NOT IMPLEMENTED with measured evidence. A completed demonstration may contain documented findings; it is not an unconditional release. Structural/count/checksum failures require bounded targeted repair or halt. A provisional artwork miss must remain explicitly open, never relabeled PASS. A failed native drawing attempt does not erase the delivered model/renders/composed sheet, but must be reported.

---PAGE---
## 7. Latest rehearsal results
**Observed on18 September2026; these are results, not new requirements.** The run used the existing local MCP extension. Packaging tests for the newer companion are separate from live CAD validation.

| Stage | Observed result |
|---|---|
| Geometry | 289 bodies,12 components,zero timeline health issues |
| Upper/base/panel | 219.090514 /209.946958 /56.970000 cm³ at their specified checkpoints |
| Cut checks | Recess70.0344 cm³; notches1241.352 mm³; strips87 mm³; ports190 mm³ |
| Layout | Knob gap13.000; knob-pad7.700; pad inset0.200 mm |
| CMF | Ten custom appearances;289 assigned bodies;2214 resolved appearance checks;zero mismatches |
| Artwork | Initial R39.36 failed; targeted repairR40.96/I15.20/V27.30 passed provisional area bands |
| Other graphics | Table1023.1 mm²; two grids75.84 mm² each;50 graphic bodies |
| Exposure | Brightness1700,exposure9.5; probe housing182.3 inside177–185 |
| Raw renders | Hero2993×1200; plan3492×1400; verified nonempty PNGs |
| Composites | Hero1593×1200; plan918×1400; whole product visible |
| Composed sheet | A3,12 parts rows,11 dimensions; four nonempty views; reported crop errors0.04/0.07/0.11% |
| Native drawing | Request timed out after300s; later query confirmed Drawing active; native contents not fully audited |

### Findings not closed by completion
- Plan pad mean luminance161.1 exceeded160.5 under the run-specific bright-region sampling method. Hero mean160.48; G:R0.5601(hero)/0.5619(plan). Report this gap; the method itself needs a general projected-ROI replacement.
- Ten pads were visually identified, but the original diagnostic counted the power LED as an eleventh pad. The run-specific plan detector also caught three knob highlights among small regions. No universal detector acceptance is claimed.
- V intersects the vertical seam. Correct area/count does not establish artwork layout approval.
- Drawing callout balloons3/5/6 initially covered the silhouette; the composed sheet was adjusted and rechecked. That does not certify native-sheet annotations.
- Some required per-class progress lines were not printed immediately despite saved measurements. This procedural presentation gap remains recorded.

### Readiness limits
The published companion passed automated protocol/unit/installer checks, but a full fresh-machine live rehearsal of the exact packaged combination remains outstanding. No specific27B-model success or general model-size compatibility has been demonstrated. No production, tooling, regulatory, audio or physical-material signoff is implied.

---PAGE---
## 8. Closed decisions and open items
### 8.1 Closed for CAD demonstration
| ID | Decision |
|---|---|
| DEC-C1 | Y340 long axis, X195 short axis, +Y away from operator. |
| DEC-C2 | Twenty small pots in4×5 grid governs; do not revert to16. |
| DEC-C3 | No bezel; transport cover addresses protection. PM/ID pre-tooling signature still open. |
| DEC-C4 | No connector aperture crossesZ23; rear I/O in separate unmodeled plate/bay. |
| DEC-C5 | Power toggleY+130.0. |
| DEC-C6 | Ten pads are lit buttons;11 bodies including power LED use emissive appearance. |
| DEC-C7 | Vertical dividers run downwardY+4 to−43. |

The historical decision-register reuse of DEC-C4/C5 for tick/pointer color is corrected. Tick and pointer colors are CMF specifications, not alternate definitions of those IDs.

### 8.2 Governing constraint arithmetic
Using the measured bounding-box convention:46.000−61.180=−15.180 mm against required≥+2.000 mm; shortfall17.180 mm. DEC-C3 makes this nonblocking for the exposed-deck CAD demonstrator. Do not add an18 mm bezel to make a check pass. This calculation is not transport-cover design validation.

### 8.3 Open ownership
| ID | Owner | Item / disposition |
|---|---|---|
| TBD-12 | PM / ID | Cover/no-bezel signature before tooling. |
| TBD-13 | ME | Rear I/O plate and recessed bay; not modeled. |
| TBD-14 | CAD | Named parameters and verified parametric edit behavior; absent. |
| TBD-15 | ME | Shaft diameter/source selection; no panel holes. |
| TBD-16 | CAD | Boss layout after axis correction; no bosses or clearance check. |
| TBD-17 | ID | Approve or replace14-bar waveform interpretation. |
| TBD-18 | ID | Approve R/I/V construction and resolve V/seam relationship. |
| TBD-19 | ID | Approve scale baseline anchoring atY−146.7. |

Additional validation work: stable pad ROIs/masks and sampling protocol; exact packaged MCP clean-machine live test; native-sheet content inspection; named smaller-model evaluation. These are verification tasks, not silent changes to product geometry or tolerances.

---PAGE---
## Appendix A. Reproducible provisional artwork
This appendix records the latest tested interpretation only. It is not a claim that the concept artwork uniquely determines these coordinates. All points are millimetres in the XY plane, with closed straight-line outlines extruded fromZ46.0 to46.15.

### R
Origin(−69.5,−146.7). Local outer polygon, in order:
(0,0);(1.6,0);(1.6,4);(3,4);(5.4,0);(7,0);(4.6,4);(6.5,4);(6.5,9.5);(0,9.5);close.

Subtract the interior rectangular counter centered at local(3.25,6.75), size3.3×2.3. Preserve the outer profile and reject the counter; do not reject the diagonal leg by a minimum-bbox-width filter. Measured plan area40.96 mm², one body. This repaired an initial39.36 mm² version by widening the bowl while keeping its orthogonal wall widths.

### I
One rectangle centered at(61.0,−141.95), size1.6×9.5; area15.20 mm². Its left edge isX60.2, matching the stated IV anchor.

### V
Origin(64.0,−146.7). Local polygon:
(0,9.5);(1.6,9.5);(3.4,2.5);(5.2,9.5);(6.8,9.5);(4.2,0);(2.6,0);close.

Measured area27.30 mm², one connected body. The nominal1.6 stroke convention is an approximation for diagonal outlines, not a certified constant-normal-width typeface. This version crosses the separate seam centeredX68.5. Do not present it as final ID artwork.

### Waveform
Fourteen bars, each width0.8; centersX=34+i×28/13 for i=0…13; each centeredY−134.3. Heights, left to right:
3.0,5.0,8.0,11.0,13.2,9.0,5.0,3.0,6.0,10.0,12.0,8.0,5.0,2.4.

Total volume0.012072 cm³ at0.15 thickness. Heights are the recorded rehearsal interpretation; TBD-17 remains open.

### Status of these data
These coordinates remove needless reconstruction ambiguity for a reproducibility test while preserving the approval boundary. If the agent chooses another interpretation, record it, prove its count/area/location, and keep unresolved ID decisions open. Do not edit the housing or other passing geometry merely to hide an artwork conflict.

---PAGE---
## 9. Sources, revision control and operational boundary
### Maintained sources
- Workflow: https://github.com/nvsdef/fusion-agentic-workflow
- Companion MCP: https://github.com/nvsdef/fusion360-mcp
- Workflow instructions: AGENTS.md and agents/cad-engineer/skills/slab-run/SKILL.md.
- Dimensional/API reference: agents/cad-engineer/skills/slab-product-spec/SKILL.md.
- Installation and registration: SETUP.md; immutable companion revision in mcp.lock.json.
- Known validation limits: docs/VALIDATION.md; release checklist in docs/RELEASE_CHECKLIST.md.
- This document's editable source: docs/SLAB_PRD_RevD.md. PDF generated by scripts/build_prd_pdf.py.

### Operating assumptions
Fusion is a licensed interactive GUI on the same desktop as the MCP client. The agent works in a unique saved Design and a unique local output folder. Setup prepares dependencies; Autodesk login, add-in activation and client consent may remain human steps. A successful mock/protocol test is not a live CAD test. Skill discovery must be verified in a fresh session.

A mutation timeout means its outcome is uncertain, not that it was canceled. Re-query before repair; never blind-retry. Repair only the failed class's owned features; housing shell and cuts share a component. Approval denial or timeout is a genuine stop condition, not permission to use another tool to bypass it.

Current-view rendering must preserve the calibrated camera. Capture/restore display and camera around monochrome line-art extraction; announce the transition before it happens. Native drawing automation is preview functionality and the last Fusion step. Preserve colored artifacts beforehand. These are operational requirements; exact API spellings, tool defaults and release-specific timeout settings stay in maintained skills/setup.

### Change register: C to D
| Topic | Rev D disposition |
|---|---|
| Core geometry / CMF | Preserved, with nominal versus padded bbox distinguished. |
| Status language | Exterior demonstrator completed with findings, not full release. |
| Decision identifiers | DEC-C1–C7 consistent; no alternateC4/C5 definitions. |
| Artwork | Reproducible provisional appendix; seam conflict retained. |
| Glyph tolerance | Consolidated to±1.5 mm²; does not certify layout. |
| Pad luminance | Consolidated144.0–160.5 mean; method must be recorded; latest plan miss retained. |
| Drawing acceptance | Nonempty/correctly scaled views and actual sheet inspection; creation alone insufficient. |
| Execution appendix | Replaced with maintained source links and high-level safety boundary. |
| Model readiness | No named-parameter, physical-material, clean-machine or27B compatibility claim. |

Rev D is a documentation reconciliation, not a new product or tooling approval. Rev C remains available for audit. Future decisions must update source and generated PDF together with a dated change record.
