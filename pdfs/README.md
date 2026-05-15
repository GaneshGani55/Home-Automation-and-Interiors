# PDF Deliverables

Two ready-to-share PDFs generated from the project markdown.

| PDF | What it is | Hand to | Pages |
|---|---|---|---|
| [ELECTRICIAN_REFERENCE.pdf](ELECTRICIAN_REFERENCE.pdf) | Drilling, cavity depths, switch boxes (65 mm Sonoff-ready), conduit colour code, FF router runs, full pre-plaster checklist | Electrician + mason | 12 |
| [INTERIOR_SUGGESTIONS.pdf](INTERIOR_SUGGESTIONS.pdf) | Whole-house A-to-Z brief: palette (with hex swatches), tiles, wood, hardware, lighting, furniture, sanitaryware, vendor cheat sheet | Interior contractor + carpenter + painter | 24 |
| [WATER_AUTOMATION.pdf](WATER_AUTOMATION.pdf) | Water level automation: 7-conduit pre-plaster schedule, system overview diagram, JB specs, DB cupboard layout, starter control circuit (how Sonoff taps Magnum Pradhaan), PoE power chain, BOM, sequencing, electrician sign-off | Electrician + plumber + owner | 11 |

## Regenerating the PDFs

If you change any of the source markdown (electrical or interior-design files), re-run:

```bash
cd .claude/worktrees/happy-heisenberg-e58746/pdfs
pip3 install --user fpdf2     # one-time
python3 build_electrician_pdf.py
python3 build_interior_pdf.py
python3 build_water_automation_pdf.py
```

The Python scripts (`build_*.py`) are the source of truth for PDF formatting — edit them if you want to add sections, change layout, or update content.

## Source markdown files

| PDF | Pulls content from |
|---|---|
| Electrician | `electrical/conduits-and-cavities.md` (PART 0 cheat sheet), `electrical/ground-floor-electrical.md`, `electrical/first-floor-electrical.md`, `electrical/db-layout.md`, `electrical/materials-checklist.md` |
| Interior | `interior-design/master-interior-spec.md`, `materials-finishes/master-color-palette.md`, `interior-design/living-area.md`, `interior-design/gf-common-bathroom.md`, `materials-finishes/wall-finishes.md`, `materials-finishes/flooring.md` |
| Water Automation | `electrical/water-automation-conduits.md` (7-conduit schedule, JB specs, DB cupboard, BOM), `decisions/decision-log.md` (2026-05-13 entries) |
