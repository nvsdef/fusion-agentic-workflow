# Contributing

This is a single-agent, skill-led workflow. Product modeling decisions belong in skills/specs; infrastructure and deterministic postprocessing belong in utilities. Do not add a hidden end-to-end product builder.

## Checks

```
uv sync --frozen
uv run python -m unittest discover -s tests -v
uv run python scripts/test_demo_outputs.py
uv run python scripts/setup/verify_layout.py
```

Test setup with an isolated cache/add-in target, not a running user's Fusion installation. Add regression tests before behavior changes. Record actual results and distinguish mocked, host-only and live Fusion tests. Preserve named decisions; do not loosen tolerances just to pass.

Edit the canonical skills under agents/cad-engineer/skills and plugins/fusion-mcp/skills. No shared-skill fan-out or subagent synchronizer exists. Keep the entry point concise and stage details progressively loaded. Use clear construction steps, inputs, expected evidence, bounded repair and output contracts.

MCP changes belong in https://github.com/nvsdef/fusion360-mcp. Update mcp.lock.json only after testing its immutable commit. Do not overwrite global client identity, credentials or approvals. Exclude machine paths, caches, checkpoint/run outputs and secrets from commits. Review docs/RELEASE_CHECKLIST.md before publishing.
