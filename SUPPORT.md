# Support

Run `uv run python scripts/setup/doctor.py`; add `--live` only with Fusion open and a Design active. A mock protocol test is not live readiness.

- Connection refused: open Fusion and enable its add-in.
- Ping succeeds but API query fails: close modal dialogs; wait for outstanding work; check active Design.
- Drawing active: select Design tab before modeling.
- Different installed add-in: preserve it; close Fusion and use explicit replacement with backup.
- Timeout: work may have succeeded. Never replay mutations; query state after waiting.
- Missing helper packages: `uv sync --frozen`, then use `uv run python`.
- Skills absent: verify external_dirs or read SKILL.md directly through project AGENTS.md.

Do not force-kill Fusion or erase checkpoints as a routine fix. Save before long operations. Include Fusion/client versions, exact call, measured outcome, logs with secrets removed, and repository/MCP revisions in GitHub issues.
