# Fusion MCP integration

The maintained companion is https://github.com/nvsdef/fusion360-mcp. The sole source pin is ../../mcp.lock.json. Root setup.ps1/setup.sh prepares its checkout and dependencies; no separate legacy host install scripts are required.

The client launches the companion over stdio; it connects to Fusion's loopback add-in. See root SETUP.md for activation, consent-aware registration and readiness checks. host/fusion_mcp.py is a diagnostic socket probe, not a server or installer. Native rendering/drawing extensions are in the companion, not upstream Faust's public main alone.
