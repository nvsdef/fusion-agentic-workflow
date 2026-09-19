# Validation and limitations

## Evidence, not guarantees

A live predecessor rehearsal on Fusion 2705.1.11 produced SLAB_TOP_v13 with 289 bodies, 12 components, zero timeline health issues, ten custom appearances and zero CMF mismatches across 2,214 resolved appearance checks. Measured housing/base/panel volumes were 219.090514 / 209.946958 / 56.970000 cm³. This was agent-generated geometry through MCP, not a prewritten product build.

Hero/plan raytraces, a composed A3 sheet and a native drawing were created. Native creation timed out after 300 seconds; subsequent active-product inspection confirmed Drawing, not the correctness of every native sheet. Colored geometry was saved before the monochrome drawing transition.

## Findings carried forward

- First R legend area 39.36 mm² failed; targeted repair gave R40.96, I15.20, V27.30, inside the provisional ±1.5 bands. V/seam intersection remains an artwork decision.
- Original image diagnostic counts the power LED as an eleventh pad. A reviewed run-specific detector identified ten pads but also picked up reflective knob highlights. It is not shipped as a general acceptance validator.
- Plan mean pad luminance 161.1 exceeded the 160.5 limit; not silently accepted.
- Zero named user parameters. History-based features are not demonstrated parameter-driven editing.
- Broad component reset is unsafe for classes sharing the housing. Repair only owned failing features.
- Native drawing API remains experimental. Never use the known-blocking export_drawing_pdf path.
- Missing/blank crop and frame-recrop defects have regression tests in scripts/test_demo_outputs.py.

## Packaging validation

The companion MCP at the commit in mcp.lock.json passed 376 Python tests, lint, MCP stdio schema/ping checks in explicitly mock mode, and isolated Windows installation followed by an unchanged second run. These tests do not exercise Autodesk geometry on a new installation.

The workflow's setup prepares the pinned companion and helper environment. Client registration, skill discovery, and Fusion activation must be verified separately. The source clone includes skills, but native Hermes discovery requires registering external_dirs; direct SKILL.md loading from the workspace is supported.

## Not yet established

- Full clean-machine live build with the packaged companion.
- Repeatability across Fusion releases, machine types, and client versions.
- End-to-end success with any specified 27B model. Parameter count alone is not a compatibility test.
- A comprehensive fail-closed automated geometry/CMF/image validator.
- Native drawing annotation release quality or manufacturing readiness.

Historical renders/ and drawings/ are examples, not new-run proof. Runtime data and personal paths are excluded from this repository. Treat this as an experimental, reviewable workflow release, not a zero-error installation promise.
