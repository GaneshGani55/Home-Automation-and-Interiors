# Lighting plan — interactive ceiling map

Tap-to-detail reflected ceiling plans (GF + FF) with every TISVA product code, position read-out (mm from finished walls), switch gang, false-ceiling schedule and buy list. Phone-first, works offline.

| File | What |
|---|---|
| `lighting-data.js` | **Single source of truth** — rooms, false-ceiling polygons, every fixture/strip/driver with code + MRP. Edit this. |
| `lighting-plan.src.html` | Page template (loads `lighting-data.js`). |
| `build.py` | Inlines the data into `lighting-plan.html` and prints the BOM as Markdown (`python3 build.py`). |
| `lighting-plan.html` | **Generated** single file — share by WhatsApp/AirDrop; open in any browser. Do not hand-edit. |

Published copy: https://claude.ai/artifact/E8pURfRVXApDEXaeP6uM3E (republish after every `build.py` by passing that URL).

Stair wall (3 soffit accents F80–F82, 3 foot lamps): [../staircase-feature-wall.md](../staircase-feature-wall.md). Design narrative + primer: [../lighting-and-false-ceiling-design.md](../lighting-and-false-ceiling-design.md). Coordinates: feet, x from the EAST wall (→ west), y from the SOUTH wall (→ north); drawn like the handwritten sheets (top = south).

## Photometric check (`photometric/`)

| File | What |
|---|---|
| `photometric/photometric_living.py` | Lux model of the double-height living room: reads fixture positions from `lighting-data.js`, point-source + line-source photometry (TISVA Axios documented lumens/optics; Rega Plus + strips estimated, shapes fitted to TISVA's published Orrin data), room-cavity bounce, 4 scenes, sensitivity cases. `python3 photometric/photometric_living.py` |
| `photometric/tables.md`, `results.json` | Generated tables (key points, grid stats, sensitivity, beam footprints, inverse-square, fixture→surface) and raw numbers |
| `photometric/living-lux-heatmap-*.png`, `living-section.svg` | Generated figures (FULL, EVENING, FULL-with-recommended-tweaks heatmaps; N–S section with heights) |

Write-up with provenance of every number: [`../lighting-and-false-ceiling-design.md` § 10](../lighting-and-false-ceiling-design.md). To re-verify with real TISVA data later, edit `P` / `SHAPES` at the top of the script and re-run.
