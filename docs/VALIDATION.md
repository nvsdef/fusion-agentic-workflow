# Validation and limitations

## Evidence, not guarantees

A live predecessor rehearsal on Fusion 2705.1.11 produced SLAB_TOP_v13 with 289 bodies, 12 components, zero timeline health issues, ten custom appearances and zero CMF mismatches across 2,214 resolved appearance checks. Measured housing/base/panel volumes were 219.090514 / 209.946958 / 56.970000 cm³. This was agent-generated geometry through MCP, not a prewritten product build.

Hero/plan raytraces, a composed A3 sheet and a native drawing were created. Native creation timed out after 300 seconds; subsequent active-product inspection confirmed Drawing, not the correctness of every native sheet. Colored geometry was saved before the monochrome drawing transition.

### 28 Oct 2026: timed live runs (Claude in Cowork, Fusion 2705.1.11)

Five end-to-end runs on one machine (SLAB_TOP_v4…v8). Details: [docs/runs/2026-10-28.md](runs/2026-10-28.md).

| Run | Profile | Preflight → native drawing open | Build (12 classes) | Native drawing |
|---|---|---|---|---|
| 1 | FULL, as-is | 20:30 | 4:47 | 3:49 (tool, 12+ sheets) |
| 2 | DEMO + fixes | 7:19 | 1:35 | ~2:40 (tool) |
| 3 | DEMO, watched | 7:18 | 1:41 | ~2:50 (tool) |
| 4 | DEMO, API drawing | 5:42 (≈4:40 without two agent errors) | 1:29 | 0:29, but auto-dimension crash |
| 5 | DEMO, API drawing | 4:41 | 0:09 in Fusion | 0:31, but auto-dimension crash |
| Test A | drawing only | — | — | **0:24, auto-dimension off: displayed with parts list** |

Every run passed all 12 class checks, whole-model checks (289 bodies, 12 components, healthy, DEC-C4 0) and the CMF audit (exact tally, 0 mismatches over 2,214 checks). Fusion compute for the full build is about 15 s. In the latest run, about 1:40 of 4:41 was Fusion time; the rest was cloud save latency and agent turns. The human confirmed the native drawing and parts list displayed in Test A. The DEMO plan image is a labelled viewport capture, not a raytrace.

Fixed or learned in these runs, now in the skills: body-first appearance assignment (13× faster per body); timeline health read from the timeline object; per-class `guard()` after a stray GUI click silently deleted a passed class; tested R/I/V outlines (first-pass PASS); the Drawing API instead of the `create_drawing` tool (the tool forces per-component sheets); automatic dimensioning off (it crashed `acadm.crx`, c0000027, behind a modal); the sheet JSON is a template with measured extents and materials TBD.

## Findings carried forward

- **Pad calibration open.** At brightness 1700 / exposure 9.5 with the spec CMF, pads measure G:R 0.663, luminance 179.5, red clipped (spread 4 PASS), identically at preview and q95. Lowering emissive luminance 150 → 25 only reached 0.596 / 166.9, because the albedo saturates red on its own. Needs a spec-owner decision; runs report FAIL and do not tune.
- **composite.py matte leak.** On 28 Oct 2026 the raytraced backdrop was not uniform (levels 172–178), so flood-fill keying leaked: a halo on the hero, and the plan crop shifted off the product. Difference-matte compositing is not yet implemented; the FULL profile must inspect composites and fall back to raw renders.
- **Cloud save latency.** The first `saveAs` took 0.6 s to over 65 s across runs; in the Claude desktop app it can exceed the ~65 s call timeout while succeeding.
- **create_drawing tool.** The pinned add-in hard-codes component sheets (all levels). Use the Drawing API path until the add-in exposes the option.

- First R legend area 39.36 mm² failed; targeted repair gave R40.96, I15.20, V27.30, inside the provisional ±1.5 bands. V/seam intersection remains an artwork decision.
- Original image diagnostic counts the power LED as an eleventh pad. A reviewed run-specific detector identified ten pads but also picked up reflective knob highlights. It is not shipped as a general acceptance validator.
- Plan mean pad luminance 161.1 exceeded the 160.5 limit; not silently accepted.
- Zero named user parameters. History-based features are not demonstrated parameter-driven editing.
- Broad component reset is unsafe for classes sharing the housing. Repair only owned failing features.
- Native drawing API remains experimental. Never use the known-blocking export_drawing_pdf path.
- Missing/blank crop and frame-recrop defects have regression tests in scripts/test_demo_outputs.py.

## Packaging validation

The companion MCP at the commit in mcp.lock.json passed 376 Python tests, lint, MCP stdio schema/ping checks in explicitly mock mode, and isolated Windows installation followed by an unchanged second run. These tests do not exercise Autodesk geometry on a new installation.

The workflow's setup prepares the pinned companion and helper environment. Client registration, skill discovery, and Fusion activation must be verified separately. The source clone includes skills, but native Hermes discovery requires registering external_dirs; direct SKILL.md loading from the workspace is supported.

## Not yet established

- Full clean-machine live build with the packaged companion.
- Repeatability across Fusion releases, machine types, and client versions.
- End-to-end success with any specified 27B model. Parameter count alone is not a compatibility test.
- A comprehensive fail-closed automated geometry/CMF/image validator.
- Native drawing annotation release quality or manufacturing readiness.

Historical renders/ and drawings/ are examples, not new-run proof. Runtime data and personal paths are excluded from this repository. Treat this as an experimental, reviewable workflow release, not a zero-error installation promise.
