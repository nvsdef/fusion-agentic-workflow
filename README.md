# Fusion Agentic Workflow

**An agentic workflow for Autodesk Fusion:** give the agent a product brief and concept images; it plans, writes CAD operations, measures the model, diagnoses failures, applies appearances, renders, and produces a drawing/report through a live MCP connection.

There is **no prewritten end-to-end SLAB build script**. Skills teach the method; the agent generates and verifies each feature class. Small Python utilities handle installation, image analysis, and PDF composition, not engineering decisions.

## Status

Windows/local-desktop **experimental release candidate**. A predecessor completed the SLAB rehearsal on Fusion 2705.1.11 with 289 bodies and 12 components. See [validation and limitations](docs/VALIDATION.md). Clean-machine live rehearsal of the packaged MCP remains required before calling this production-ready.

## Quick start (Windows PowerShell)

Install/sign into **Autodesk Fusion**, install [Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/installation), and have Git plus [uv](https://docs.astral.sh/uv/getting-started/installation/) available. Then:

```powershell
git clone https://github.com/nvsdef/fusion-agentic-workflow.git
cd fusion-agentic-workflow
.\setup.ps1
```

The installer downloads a **pinned companion MCP**, installs locked helper dependencies, generates client configuration, and prepares project skills. It does not overwrite your global identity, credentials, or approval settings. Close Fusion before adding/updating its add-in. Existing different add-ins require explicit replacement with backup.

Follow [SETUP.md](SETUP.md) for the one-time Fusion activation and client registration. These consent/login steps cannot honestly be advertised as zero-click. Once ready, open an empty **Design** document and ask the agent:

> Read `agents/cad-engineer/skills/slab-run/SKILL.md`. Build SLAB from `docs/SLAB_PRD_RevC.pdf` and the two concept images in `examples/01_slab_mixer/reference/`. Continue through verification, CMF, calibrated hero/plan renders, A3 sheet, experimental native drawing last, and report. Generate the geometry yourself through MCP. Record failures instead of declaring unverified stages passed.

Full prompt: [examples/01_slab_mixer/prompt.md](examples/01_slab_mixer/prompt.md).

## Architecture

```text
Agent on this desktop
  ├─ skills: plan / generate code / inspect / repair / report
  ├─ local utilities: measure pixels / compose PDF / installation tests
  └─ MCP stdio client → companion server → 127.0.0.1:9876
                                          → Fusion add-in / GUI main thread
```

One agent owns all dependent CAD stages. No sandbox deployment or hidden subagent handoff. The [companion MCP](https://github.com/nvsdef/fusion360-mcp) contains transport/API tooling, not product geometry.

## Repository map

| Path | Purpose |
|---|---|
| `AGENTS.md`, `agents/cad-engineer/SOUL.md` | Project-local agent behavior |
| `agents/cad-engineer/skills/` | Six stage skills; `slab-run` is the entry point |
| `plugins/fusion-mcp/skills/` | Transport/install troubleshooting skill |
| `setup.ps1`, `setup.sh`, `scripts/setup/` | Host-local installer and diagnostics |
| `mcp.lock.json` | Companion repository and immutable commit |
| `pyproject.toml`, `uv.lock` | Locked host helper environment |
| `scripts/` | Measurement/composition utilities and tests, no product builder |
| `docs/` | PRD, decisions, validation, release checklist |
| `examples/01_slab_mixer/` | Prompt, acceptance reference, committed concept images |
| `renders/`, `drawings/` | Historical example outputs, not fresh-run proof |
| `.local/`, `BUILD_STATE.json` | Ignored machine/run state; never commit |

## What SLAB demonstrates

- 195 × 340 × 46 mm exterior housing; 20 small knobs, 3 large knobs, 10 illuminated pads.
- Twelve feature classes, 289 bodies, 12 components including root.
- History-based geometry with numeric units/volume/bounding-box checks.
- Ten custom appearances; actual raytraced renders, not generated concept images.
- Raster line-art A3 sheet separate from the experimental native Fusion drawing.

**It does not demonstrate a production-ready mixer or named-parameter-driven editing.** PCB, battery/hatch, rear I/O plate/bay, shaft holes, internal ribs, lightguides, draft analysis, orange speckle and in-panel legend text remain out of scope. Artwork is provisional. See [decisions](docs/SLAB_DECISIONS.md).

## Development and sharing

```powershell
uv sync --frozen
uv run python -m unittest discover -s tests -v
uv run python scripts/test_demo_outputs.py
uv run python scripts/setup/verify_layout.py
uv run python scripts/setup/doctor.py
```

`doctor.py` checks host files/dependencies; `--live` additionally queries the live add-in. Neither claims that a full product was built. Follow [CONTRIBUTING.md](CONTRIBUTING.md) and [release checklist](docs/RELEASE_CHECKLIST.md). Do not commit credentials, machine paths, cloud IDs, run checkpoints, or raw output files.

License: Apache-2.0 for this workflow repository; companion MCP retains MIT upstream attribution. Not affiliated with or endorsed by Autodesk, NVIDIA, or Nous Research. Read [SECURITY.md](SECURITY.md).
