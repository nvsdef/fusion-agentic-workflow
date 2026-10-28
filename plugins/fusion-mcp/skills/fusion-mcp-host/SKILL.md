---
name: fusion-mcp-host
description: "Use when diagnosing the local Fusion MCP connection."
---

# Fusion MCP host connection

One host-local agent/client launches the companion over stdio. The server dials
127.0.0.1:9876; the add-in marshals API calls onto Fusion's main thread. No
sandbox agent or retired fusion-mcp-core skill is required.

## Install and discover

Read repository SETUP.md. setup.ps1/setup.sh prepares the immutable companion
commit in mcp.lock.json, locked dependencies and local config. Close Fusion
before add-in installation; existing different files require explicit replacement
with backup. Register through the client's supported consent UI/CLI. Skills
can be read directly from the workspace or registered as external directories.
Do not overwrite global identity, credentials or approval policy.

## Readiness

1. Verify client tool discovery and source revision.
2. `ping` tests transport only. A read-only scene/Design query tests main-thread
   responsiveness. A modal may block API calls while ping still succeeds.
3. Confirm Design active; Drawing/no-active-design is not an empty model.
4. Confirm cloud-save access and writable unique local output directory.

Socket refusal means no listener; API timeout may be a modal or ongoing work.
Wait and inspect rather than repeatedly sending mutations. Use root doctor.py
--live (under scripts/setup) for a real stdio plus scene probe. Mock smoke tests
are explicitly not CAD evidence.

## Timeouts and recovery

The pinned companion uses add-in300s, socket330s; client360s recommended.
The Claude desktop app (Cowork) times out at about 65 s and cannot be
raised. The first cloud saveAs (54–70 s measured) and raytraces can exceed it
while succeeding. These are request budgets, not render-job duration. A timeout
does not cancel queued work. Never replay a mutation after an uncertain send.
Wait, query live state, audit names/counts/health and checkpoint identity, then
repair only owned failing features. Save at the start and after CMF; later
saves took about 1 s. No universal source-line/profile cap is established: 173
tick profiles succeeded in one feature-class call.

## Rendering/drawing

Use start_render then get_render_status, not a blocking sleep inside Fusion.
Jobs queue and die with Fusion. Verify finished state plus actual valid file;
elapsed may continue growing after completion and is not proof of progress.
Avoid include_image on status; inspect the returned local image file.

Native drawing: prefer the Drawing API through execute_code (fusion-2d-drawings
§3a). The create_drawing tool forces per-component sheets and holds the main
thread for minutes. Keep auto-dimension off: on SLAB it crashed acadm.crx behind a
modal that ping cannot see. It is preview API and LAST Fusion action. Drawing activation is not sheet
signoff. Follow fusion-2d-drawings. Never use export_drawing_pdf, and do not
replace or restart the live add-in during a campaign.

## Security

Arbitrary Python executes as the logged-in user. Loopback is not authentication;
other local processes may access the socket. Never expose/tunnel the port.
Approval denial or timeout requires explicit user authorization before resuming;
do not change tools to bypass it. Keep transport tests, mock tests and live CAD
results distinctly labeled.
