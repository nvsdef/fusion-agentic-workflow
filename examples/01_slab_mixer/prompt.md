# SLAB agent prompt

Read `agents/cad-engineer/skills/slab-run/SKILL.md` first. Use the repository copies of the skills, not older installed copies with the same names. Generate and verify CAD through the connected Fusion MCP yourself; do not execute a prebuilt product builder. The person at the desk will not touch Fusion during the run.

## DEMO profile (default for live demos, ~4.5–5 min measured)

Build SLAB, a portable 6-channel production mixer / USB-C audio interface, from the slab-product-spec skill:

1. Preflight on an empty Design; register the spec §1/§1b helpers once; save to the cloud and create the run folder. If the save times out, query the document; do not retry.
2. Build the twelve feature classes live, one class per `execute_code` call, each starting with `guard()` and printing its measured checks.
3. Whole-model check, then configure ten appearances before assignment (body first, then faces), audit CMF, save.
4. Measured layout check; announce the Render workspace; set exposure and the hero camera.
5. One preview raytrace of the hero (900 px, q50), labelled as a preview. Measure pads with projected ROIs and report once.
6. Plan as a viewport capture from the Design workspace, labelled as not a raytrace. Announce monochrome line art; capture four views; compose and raster-check the A3 sheet from the template.
7. Last Fusion action: the two-sheet native drawing (iso + parts list, orthogonal views, auto-dimension off) through the Drawing API. Ask me to confirm it displayed.
8. Report per-stage PASS/FAIL/OPEN with clock times and an artifact manifest.

## FULL profile (deliverable renders)

Same as DEMO, except: a 256 px exposure probe; hero 1200 px q95 and plan 1400 px q95 raytraces (plan aspect pinned portrait); composites only after inspecting the matte (fall back to the raw render if it leaks); two finals per view maximum.

## Both profiles

Print measured PASS/FAIL/OPEN after every class/stage. Continue healthy work without unnecessary checkpoints requiring a reply; stop for real safety/approval/environment blocks or exhausted repair budget. Do not invent TBD values, tune CMF to pass a render check, or claim omitted internals or parameter-driven editing. Preserve unrelated documents and settings.
