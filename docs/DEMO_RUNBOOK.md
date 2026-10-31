# SLAB demo runbook

One page for repeating the live DEMO run. Setup details: SETUP.md. Method: the
`slab-run` skill. Evidence and known gaps: docs/VALIDATION.md.

## Before the demo (once per machine, then 2 minutes per session)

1. Update the clone the agent reads: `git pull` in the repository folder that
   Hermes' `skills.external_dirs` (or your Claude workspace) points at.
   Check with `hermes config get skills.external_dirs --json`.
2. Fusion running, the **Fusion360MCP** add-in running, signed in.
3. Hermes: `mcp_servers.fusion360.timeout` 360 (300 also works).
4. Close old conversations; start a **new** agent conversation (it reloads the skills).
5. In Fusion, click the Design tab and open a **new, empty, unsaved Design**.
   Optional: save that empty Design yourself first; it removes the ~1 minute
   cloud save from the run.
6. Keep the Fusion window a normal width (an ultra-wide window makes the hero
   render ~3:1 and slower). **Do not click in Fusion until the agent says done.**

## Prompt

> Build SLAB — a portable 6-channel production mixer and USB-C audio interface — in Fusion 360 using the slab-run skill's DEMO profile; a new unsaved Design is open. Take it all the way: geometry built live and verified class by class, materials, a preview render, a dimensioned A3 general arrangement sheet, and a native Fusion drawing with parts list.

## What should happen (measured 28–30 Oct 2026)

| Step | Fusion time | You see |
|---|---|---|
| Load helpers, cloud save | ~1 min (save) | file becomes `SLAB_TOP_vN` |
| 12 feature classes | ~15 s | the model appears class by class |
| Materials (CMF) | ~10 s | colours appear; the agent reports an exact tally |
| Render workspace + hero preview | ~25 s | Render tab, raytrace progress |
| Plan capture + line views | ~5 s | brief monochrome flash |
| A3 sheet (host) | ~3 s | nothing in Fusion |
| Native drawing: create, then open in a separate call | ~20 s + up to ~1 min | Drawing tab with iso + parts list, then orthogonal sheet |

With Claude the whole run is about 5 minutes. A local model takes longer
(writing code between steps), mostly outside Fusion.

## If something goes wrong

- **The agent reports a "cooldown" or the same error twice.** It should stop by
  itself. Paste the first failing call's error text to whoever maintains the
  skills; don't let it loop.
- **A save or the drawing open "times out".** Normal; the agent checks
  `SU.status()` instead of repeating. Don't re-prompt it to retry.
- **An `acadm.crx … c0000027` popup.** The drawing was opened in the same call
  that created it. Click OK and report it; the skills say to create and open in
  separate calls.
- **The CMF assertion fails.** Report it; the agent must not call CMF passed.
- **The pads report FAIL (G:R 0.663 / lum 179.5).** Known open calibration item,
  identical on every run. Not a regression.

## After the run

The model stays in the cloud as `SLAB_TOP_vN`; click the Design tab to return
to it from the Drawing. Outputs are in `~/fusion-renders/SLAB_TOP_vN/`
(hero preview, plan capture, line views, A3 PDF, drawing log).
