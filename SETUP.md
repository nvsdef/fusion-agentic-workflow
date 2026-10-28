# Installation (Windows, host-local)

## Prerequisites

Install Autodesk Fusion, sign in, and verify it opens normally. Install a local agent client (Hermes recommended), Git and uv. Setup does not install/licence Fusion or retrieve model-provider credentials. Use a model capable of sustained tool use; provide vision or arrange human image review.

Sources: [Fusion](https://www.autodesk.com/products/fusion-360/overview), [Git](https://git-scm.com/download/win), [uv](https://docs.astral.sh/uv/getting-started/installation/), [Hermes](https://hermes-agent.nousresearch.com/docs/getting-started/installation).

## Prepare automatically

Open PowerShell in the clone and run `./setup.ps1`. If PowerShell blocks scripts, inspect the files and follow your organization's policy; do not disable machine-wide policy. Git Bash users can use `bash setup.sh` with Python bootstrap flags.

Options:
- `-SkipAddin`: prepare dependencies/MCP/config only; does not touch Fusion installation.
- `-AddinTarget <folder>`: isolated installer test; not a live installation.
- `-ReplaceAddin`: explicitly replace a different add-in, retaining a sibling backup. Close Fusion first.
- `-CacheDir <folder>`: override local cache location.

Setup installs the locked project environment and downloads the exact companion commit in mcp.lock.json. Existing edited caches fail rather than being overwritten. Configuration is written only into ignored `.local/`. No credentials/global settings are read or rewritten. Do not move the clone/cache after client registration without reconfiguring paths.

## One-time Fusion step

Open Fusion > Utilities > Scripts and Add-Ins > Add-Ins > Fusion360MCP > Run. Enable Run on Startup and **close the dialog**. Open an empty Design tab. A Drawing tab is not an empty Design. Reinstalling files does not reload a running add-in; restart it only after saving work.

## Connect the agent

Use Hermes's MCP setup UI/consent flow to add a local stdio server named `fusion360`. Copy command, args and env from `.local/mcp-client.json`. Other MCP clients can import its mcpServers entry. Never choose mock mode for a demo.

CLI alternative (substitute the generated interpreter path):

```text
hermes mcp add fusion360 --command <absolute-python-path> --args -m fusion360_mcp --mode socket
```

Discovery/client consent may be interactive. Do not register a second server over an existing unrelated `fusion360` configuration without reviewing it.

For Hermes, use supported config commands (not manual YAML edits) to set:

```text
hermes config set mcp_servers.fusion360.timeout 360
hermes config set mcp_servers.fusion360.supports_parallel_tool_calls false
hermes config set mcp_servers.fusion360.tools.include '["ping","get_design_type","execute_code","render_view","start_render","get_render_status","set_scene_environment","create_drawing"]'
```

Use `hermes config get <key> --json` to verify each. Current client defaults vary by release. The companion uses 300-second add-in and 330-second socket timeouts; the client must wait longer. Do not turn off approvals globally.

### Claude desktop app (Cowork) or Claude Code

This is the client the 28 Oct 2026 timed runs used (docs/runs/2026-10-28.md).

1. **Register the MCP server.** In the Claude desktop app, open Settings > Developer > Edit Config and add the `fusion360` entry from `.local/mcp-client.json` under `mcpServers`, keeping any existing servers. Restart the app and confirm the `fusion360` tools are listed. For Claude Code: `claude mcp add fusion360 -- <absolute-python-path> -m fusion360_mcp --mode socket`, plus the env vars from the same file.
2. **Open the clone as the workspace folder.** `CLAUDE.md` points the agent at `AGENTS.md`, `SOUL.md` and the six stage skills, which are read directly from `agents/cad-engineer/skills/`. No skill upload is needed.
3. **Don't run a second, older copy of these skills.** If this machine has the legacy `fusion-product-design` plugin, or older uploaded skills named `slab-run`, `slab-product-spec` or `fusion-*`, disable or remove them, or ask the agent explicitly to use the repo copies. Conflicting copies cost time and give contradictory instructions (for example, native drawing first versus last).
4. **The call timeout is about 65 s and cannot be raised from the client.** The skills handle this. The first cloud `saveAs` and a raytrace can exceed it while still succeeding. The agent then queries document state instead of retrying.
5. **Host utilities run in the Cowork Linux sandbox** with `python3`, not `uv run`. They need Pillow, numpy and reportlab, plus `pdftoppm` (poppler-utils). If one is missing: `pip install --break-system-packages pillow numpy reportlab`. Run outputs go to the session outputs folder, because the sandbox cannot see `~/fusion-renders` on Windows.
6. **Pre-approve** the fusion360 tools and shell for the session where your client allows it, so an approval prompt cannot stall an unattended run.

## Skills and identity

Open this clone as the client workspace. AGENTS.md tells the agent where the six skills and local identity live. The agent can read their SKILL.md files directly; **no global SOUL.md replacement is needed**.

For native Hermes skill discovery, add these absolute directories to your existing `skills.external_dirs` using the supported config CLI, preserving other entries:
- `<clone>/agents/cad-engineer/skills`
- `<clone>/plugins/fusion-mcp/skills`

Start a fresh conversation and ask it to load `slab-run`; verify the loaded path belongs to this clone. Do not remove unrelated installed skills. Ask the agent to diagnose any name collision explicitly. Official details: https://hermes-agent.nousresearch.com/docs/guides/work-with-skills

## Verify before building

```powershell
uv run python scripts/setup/doctor.py
uv run python scripts/setup/doctor.py --live
uv run python scripts/setup/verify_layout.py
```

Then ask the agent to report its discovered tools, active Design, cloud-save readiness and output folder before the first feature. Paste the example prompt. Cloud save is a real external write and may require approval.

## Updating and rollback

Update this repository, review mcp.lock.json and run setup again. Same source/content returns unchanged. Different add-in content requires -ReplaceAddin; backup stays beside the add-in directory. To roll back, close Fusion, retain the current folder as another backup, and restore the desired backup under the exact name Fusion360MCP. Never edit/restart a live add-in mid-campaign.

## Validation boundary

Automated setup and tests do not eliminate Autodesk version/account/network differences. The bundled workflow is experimental; native drawing API is preview functionality. A full clean-machine live rehearsal remains a release gate. See docs/VALIDATION.md and SECURITY.md.
