# Agentic CAD workflow

Load `agents/cad-engineer/SOUL.md`, then the `slab-run` skill for SLAB work. If skill discovery is unavailable, read the corresponding SKILL.md directly. Product dimensions live in `slab-product-spec`; method/order in `slab-run`. README/SETUP own installation; historical PDFs and example outputs are evidence, not executable instructions.

One agent owns the dependent CAD sequence. Generate geometry through live MCP; do not substitute a product build script, mock response, concept image, or old output for an actual run. Small deterministic utilities for installation, measurement, and sheet composition are appropriate.

## Invariants

- Fusion is a GUI on this desktop. Serialize API calls. `adsk` only exists inside Fusion.
- Use the discovered MCP names, normally server `fusion360`. `execute_code` takes Python source with app/ui/design/component/adsk/math prebound; API lengths are cm, spec lengths mm.
- Reconcile active document with checkpoint before mutations. Never rebuild merely because root bodies=0: inspect occurrences too. Save an empty Design to an approved cloud project before features. Never overwrite an unrelated Design.
- Name sketches, features, bodies. One feature class per build call. Prove geometry with volume, location, radii and health; body count alone cannot establish correctness.
- On timeout, do not replay mutations. Wait, query state, preserve evidence, repair only owned failing features. Never reset all of a component shared by multiple classes.
- Configure appearances before assignment; read back effective body/face properties. Never silently alter tolerances or product dimensions to force PASS.
- Announce stages and visible workspace/style transitions. Print measured stage/class results immediately, with PASS/FAIL/OPEN as warranted.
- Renders: use `view='current', fit=False`, read back camera/exposure, verify files. Elapsed age is not completed render duration.
- Explain monochrome line-art/Drawings before switching. Restore prior display/camera in finally. Save colored model/archive before native Drawing. Native drawing is experimental and last; a created document is not proof its sheets are correct.
- Native drawing: use the Drawing API through `execute_code` (fusion-2d-drawings §3a): main assembly only, iso + parts list sheet and orthogonal sheet, automatic dimensioning off. Create and open in two separate calls (`S.native_drawing`, then `S.open_native_drawing`): opening in the same call crashed Fusion's drawing engine (`acadm.crx`, c0000027) behind a modal the agent cannot see. Always ask the user to confirm the drawing displayed.
- The person at the desk must not click, type, Esc or Ctrl+Z in Fusion during a run. A stray GUI sketch silently deleted a passed class once. Start every class call with `S.guard()` from `scripts/fusion/slab_helpers.py` (slab-product-spec §1). Treat a deltas body count that disagrees with your running total as a stop signal.
- Never batch a render or drawing call behind a call that can refuse: a failed call does not stop the next one in the batch.
- Use the helpers in `scripts/fusion/slab_helpers.py` for all API plumbing (save, appearances, cameras, captures, drawing). Never write your own version of a helper. **Two failures on the same step: stop and report the exact error text to the user.** Do not loop on variations, and never ping or retry during a client cooldown; that is what trips it again.
- Never call `export_drawing_pdf` or write `backgroundEnvironment` in this pipeline. Do not force direct modeling mode or create a new document through a known-unreliable API path.
- Approval denial/timeout is a stop condition. Do not bypass it. Use dedicated file-edit tools for checkpoints rather than inline shell writes. No global approval-policy changes.

## Files and scope

Run outputs go in a unique local, non-synced directory, e.g. `~/fusion-renders/<run-id>/` (in Cowork, the session outputs folder, which both Fusion and the sandbox can see). Initialize ignored `BUILD_STATE.json` from `examples/BUILD_STATE.template.json`; record cloud ID, spec revision, completed classes, findings, artifact paths. Never ship a completed checkpoint as the template.

No PCB/battery/hatch/rear-I/O/shaft holes/lightguides/ribs/draft work unless explicitly scoped. Do not invent TBD values. A parametric design type is not proof of named-parameter-driven geometry.

Before code changes read relevant files, add regression tests, and run them. Do not commit or push unless authorized. Preserve user assets and existing MCP/client configuration. Use `setup.ps1 -SkipAddin` or isolated targets to test installation without touching live Fusion.
