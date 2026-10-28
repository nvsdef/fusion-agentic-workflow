# Fusion MCP tool reference

Use the client-discovered names, normally under server fusion360. The pinned companion provides all eight recommended tools. Project setup generates connection configuration; SETUP.md describes consent-aware registration and filtering.

| Tool | Use / verification |
|---|---|
| ping | Transport only, not main-thread readiness. |
| get_design_type | Confirm active Design. On Drawing/No active design, select Design before mutations. |
| execute_code | Python source in Fusion; app/ui/design/component/adsk/math prebound. Return measured data. API lengths cm. No host import of adsk. |
| render_view | Fast viewport inspection, not a raytrace. Top view for layout. |
| start_render | Raytrace; absolute filename, current view, fit=False. Verify camera/exposure first; retain job ID. |
| get_render_status | Poll; verify finished state and actual valid PNG. Elapsed may be submission age, not render duration. |
| set_scene_environment | Thin scene wrapper; inspect unsupported fields and read back applied settings. |
| create_drawing | **Fallback only.** It forces a sheet per component (12+ sheets, minutes, timeouts). Default is the Drawing API through execute_code (fusion-2d-drawings §3a): 2 sheets, parts list, auto-dimension OFF, ~24 s. Cloud save first, LAST Fusion action, never blind-retry. Active Drawing is not sheet signoff; ask the user to confirm it displayed. |

No automatic retry of uncertain mutations. Save before changes, query state after timeouts. Do not call export_drawing_pdf or assign backgroundEnvironment in this pipeline. Preserve calibrated camera and display state; announce monochrome drawing transitions.

Host utilities: composite.py (postprocessing; its colour key leaks when the backdrop is not uniform, so inspect every output), measure_classes.py (diagnostic only), pad_roi.py (ten-pad acceptance metrics at projected ROIs), make_views.py (calibrated line crops), make_drawing.py plus a run-specific copy of the slab_sheet.json template (composed PDF; refuses unfilled `<RUN DATE>`/`<DOCUMENT NAME>`). Run with uv run python, or python3 in the Cowork sandbox. They do not build SLAB. PyMuPDF provides a Python rasterization option when Poppler is absent.
