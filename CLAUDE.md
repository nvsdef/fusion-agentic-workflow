# Claude entry point

Read `AGENTS.md` (project rules), then `agents/cad-engineer/SOUL.md`. For any
SLAB build, render, drawing or report, load `agents/cad-engineer/skills/slab-run/SKILL.md`
first; it names the other stage skills to load and when.

Use the skill files in this repository, not any older installed copies with the
same names (`slab-run`, `slab-product-spec`, `fusion-*`) or the legacy
`fusion-product-design` plugin. If both are visible, say which copy you loaded.

Run profile: unless the user asks for deliverable-quality renders, use the DEMO
profile in slab-run (one preview raytrace, labelled plan viewport capture,
two-sheet native drawing with parts list, auto-dimension off). Geometry is always
generated live, one feature class per `execute_code` call. Never run a
prewritten product build script.

Client setup for Claude (MCP registration, ~65 s call timeout, sandbox
utilities): SETUP.md, "Claude desktop app (Cowork) or Claude Code".
