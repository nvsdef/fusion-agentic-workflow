# SLAB Rev C decisions

Dimensional authority: agents/cad-engineer/skills/slab-product-spec/SKILL.md.
Procedure: slab-run. PDF is the historical human record. Earlier versions of this register incorrectly reused DEC-C4/C5 for tick/pointer colors; the identifiers below match Rev C.

| ID | Closed CAD decision |
|---|---|
| DEC-C1 | Long axis Y340 mm, X195 mm, +Y away from operator, Z0 ground. |
| DEC-C2 | Twenty small knobs in a 4×5 matrix, plus three large knobs. |
| DEC-C3 | No bezel. Enclosure top46 minus tallest61.18 = -15.18 versus required+2; shortfall17.18 mm. Transport cover, not raised rim. Nonblocking for CAD; PM/ID tooling signature outstanding. |
| DEC-C4 | No connector aperture crosses Z23 parting line. Rear I/O belongs on a separate plate/bay; not modeled. Two USB-C cuts wholly in base. |
| DEC-C5 | Toggle Y+130 mm, X-94 mm. |
| DEC-C6 | Ten pads are emissive buttons; same appearance also on power LED. |
| DEC-C7 | Divider verticals run downward Y+4 to-43. |

All173 ticks are black. Twenty small pointers white, three large pointers black. These are CMF specifications, not alternative DEC-C4/C5 definitions.

## Open

| ID | Owner / item |
|---|---|
| TBD-12 | PM/ID: pre-tooling signature on cover/no-bezel decision. |
| TBD-13 | ME: rear I/O plate and bay, not built. |
| TBD-14 | CAD: zero named user parameters; parameter-edit demonstration not implemented. |
| TBD-15 | ME: panel shaft-hole diameters unstated; no holes modeled. |
| TBD-16 | CAD: boss positions predate axis correction; bosses/check not implemented. |
| TBD-17 | ID: fourteen-bar waveform definition provisional. |
| TBD-18 | ID: R/I/V construction provisional; area alone does not catch seam intersection. |
| TBD-19 | ID: scale anchored by baseline Y-146.7; approve interpretation. |

Not modeled: PCB, battery/hatch, lightguides, ribs, draft/analysis, orange speckle, in-panel legend text. Appearance is not a physical material assignment. Default-density mass is not product mass.
