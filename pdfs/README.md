# PDF Deliverables

Two ready-to-share PDFs generated from the project markdown.

| PDF | What it is | Hand to | Pages |
|---|---|---|---|
| [ELECTRICIAN_REFERENCE.pdf](ELECTRICIAN_REFERENCE.pdf) | Drilling, cavity depths, switch boxes (65 mm Sonoff-ready), conduit colour code, FF router runs, full pre-plaster checklist | Electrician + mason | 12 |
| [INTERIOR_SUGGESTIONS.pdf](INTERIOR_SUGGESTIONS.pdf) | Whole-house A-to-Z brief: palette (with hex swatches), tiles, wood, hardware, lighting, furniture, sanitaryware, vendor cheat sheet | Interior contractor + carpenter + painter | 24 |
| [WATER_AUTOMATION.pdf](WATER_AUTOMATION.pdf) | Water level automation: 7-conduit pre-plaster schedule, system overview diagram, JB specs, DB cupboard layout, starter control circuit (how Sonoff taps Magnum Pradhaan), PoE power chain, BOM, sequencing, electrician sign-off | Electrician + plumber + owner | 11 |
| `WATER_AUTOMATION_VISUAL.pdf` | ⚠️ **SUPERSEDED 2026-05-29** by v2. Kept as historical reference; the hero shot was too zoomed-out to be useful. | — (historical) | 4 |
| **[WATER_AUTOMATION_VISUAL_v2.pdf](WATER_AUTOMATION_VISUAL_v2.pdf)** ★ NEW 2026-05-29 | Annotated visual handoff: 5 close-up AI-rendered images each with precise Python-overlaid callout labels. Sintex riser modification, Sintex JB on parapet, sump cross-section, sump JB on porch wall, JB internals. Each page shows ONE thing with labelled features. | Electrician + owner (future-self reference) | 6 |
| **[WATER_AUTOMATION_SCHEMATIC.pdf](WATER_AUTOMATION_SCHEMATIC.pdf)** ★ NEW 2026-05-29 | Pure-Python technical schematics (no AI). 4 clean wiring diagrams: system block diagram (control plane + power plane), top-down floor plan with all 7 conduits colour-coded, starter wiring (Magnum Pradhaan + Sonoff parallel tap), float failsafe topology. | Electrician (primary, for wiring) + owner | 5 |

## Regenerating the PDFs

If you change any of the source markdown (electrical or interior-design files), re-run:

```bash
cd .claude/worktrees/happy-heisenberg-e58746/pdfs
pip3 install --user fpdf2     # one-time
python3 build_electrician_pdf.py
python3 build_interior_pdf.py
python3 build_water_automation_pdf.py
python3 build_water_automation_visual_pdf.py    # (SUPERSEDED) original visual handoff
python3 build_water_automation_visual_v2_pdf.py # 6-page annotated visual handoff (current)
python3 build_water_automation_schematic_pdf.py # 5-page pure-Python technical schematics
```

The Python scripts (`build_*.py`) are the source of truth for PDF formatting — edit them if you want to add sections, change layout, or update content.

## Source markdown files

| PDF | Pulls content from |
|---|---|
| Electrician | `electrical/conduits-and-cavities.md` (PART 0 cheat sheet), `electrical/ground-floor-electrical.md`, `electrical/first-floor-electrical.md`, `electrical/db-layout.md`, `electrical/materials-checklist.md` |
| Interior | `interior-design/master-interior-spec.md`, `materials-finishes/master-color-palette.md`, `interior-design/living-area.md`, `interior-design/gf-common-bathroom.md`, `materials-finishes/wall-finishes.md`, `materials-finishes/flooring.md` |
| Water Automation | `electrical/water-automation-conduits.md` (7-conduit schedule, JB specs, DB cupboard, BOM), `decisions/decision-log.md` (2026-05-13 entries) |
