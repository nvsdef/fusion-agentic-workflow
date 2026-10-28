# Release checklist

## Repository release

- [ ] README/SETUP links resolve and match actual installer behavior.
- [ ] mcp.lock.json points to a published immutable companion commit.
- [ ] uv sync --frozen succeeds from a clean clone.
- [ ] python -m unittest discover -s tests -v and scripts/test_demo_outputs.py pass.
- [ ] scripts/setup/verify_layout.py passes (spec arithmetic only).
- [ ] PowerShell setup tested in isolated cache/add-in target, then rerun idempotently.
- [ ] No user paths, credentials, cloud IDs, completed checkpoints or generated caches staged.
- [ ] Skills explain construction/verification/repair, not a hidden product build script.
- [ ] All known gaps are visible in VALIDATION.md.

## Demo readiness (separate from source publication)

- [ ] Real target client discovers correct skills and eight required tools.
- [ ] Live add-in and read-only main-thread probe work on intended machine.
- [ ] Fresh cloud Design, unique run folder, before-build save verified.
- [ ] Full cold build with per-class evidence; CMF and layout audited.
- [ ] Render files and pad identities verified; open gaps reported.
- [ ] Line-art frames preserved; PDF raster checked; native drawing inspected.
- [ ] Native drawing displayed on screen with parts list (human-confirmed; no acadm.crx dialog). Auto-dimension off.
- [ ] Only the repository copies of the skills are active (no legacy plugin or older uploaded skills with the same names).
- [ ] Nobody touched the Fusion GUI during the timed run; per-class guard never fired.
- [ ] Interrupted resume and second-document rehearsal show no duplication.
- [ ] Record model/provider/context limits and human interventions.
- [ ] Test a named 27B model before making a 27B compatibility claim.

Publish experimental source with unresolved live-validation items clearly labeled. Never convert an unchecked item into a success statement.
