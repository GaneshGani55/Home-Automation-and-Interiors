# Interior Design

Style direction, mood, palette, and room-by-room interior decisions. Image renders generated via the **`/banana`** skill.

## ★ Start here

- **[master-interior-spec.md](master-interior-spec.md)** — A-to-Z whole-house interior brief. Use this as the contractor brief for everything (paint, tile, wood, hardware, lighting, sanitaryware, furniture).
- **[../materials-finishes/master-color-palette.md](../materials-finishes/master-color-palette.md)** — colour palette (hex codes + Asian Paints SKUs) for every zone.

## Per-room files (existing)
- **[staircase-feature-wall.md](staircase-feature-wall.md)** — GF stair feature wall "Ivory Comb" (PROPOSED 2026-10-11): grooved ivory plaster, walnut-lined Waveshare niche, 3 foot lamps, 3 Avia accents on the terrace-flight soffit core cuts, landing spot; from a 3-concept / 3-judge pass; renders `generated-images/staircase-ivory-comb-*.png`.
- **★ [lighting-and-false-ceiling-design.md](lighting-and-false-ceiling-design.md)** — whole-house lighting + false-ceiling design from the TISVA catalogue (PROPOSED 2026-09-29; § 10 photometric check of the living room 2026-10-02, its two changes accepted): plain-language primer, room-by-room fixtures with order codes, gang map, buy list. Interactive map: [lighting-plan/lighting-plan.html](lighting-plan/lighting-plan.html) (edit `lighting-plan/lighting-data.js` → `python3 lighting-plan/build.py`).
- [living-area.md](living-area.md) — full design proposal, layout, palette, lighting
- [gf-common-bathroom.md](gf-common-bathroom.md) — locked light luxury spa direction
- (more rooms to be added as decisions land)

## Image generation workflow
1. Use the `/banana` skill for every render (text-to-image, edits, variations).
2. Save outputs to [generated-images/](generated-images/).
3. Filename pattern: `<room>-<style/mood>-v<N>.png` — e.g. `living-warm-minimal-v1.png`, `master-bed-japandi-v3.png`.
4. When a render is accepted as a direction, link it from the relevant room markdown and add a one-liner to [../decisions/decision-log.md](../decisions/decision-log.md).

## Constraints to keep in every prompt
- **Double-height void** above Living Area — the Living Area's ceiling is the FF slab cut-out, so any living-room render must show the double-height feature.
- **TV wall** on the W side of Living Area, usable TV-unit length about 11'6".
- **Living north wall** is 16'11" with a centred teak window composition.
- **Pooja room** is 5'×5' — designs must respect that footprint.
- **Master-bedroom wardrobes** run 10'3" on S wall + ~3' tail on W wall.
- **Cut-out edge on FF** has a beam — visible on the FF Living ceiling/floor edge.

## Open questions
- Overall style direction not yet chosen — pick before generating room renders.
- Budget tier (premium / mid / value) for finishes — drives material spec.
- Climate constraints (Bangalore? Chennai? Hyderabad?) — affects flooring, AC, materials.
- Lighting design (2026-09-29) proposes extra false ceilings — MBR perimeter band, Bed 1 band, FF living/corridor, FF toilets, and a lid over the void — plus 3000K instead of 2700K house-wide. Accept/reject → decision-log.
- **Decor research (2026-10-03):** [decor-research/02-decor-report.md](decor-research/02-decor-report.md) (report with product photos) · browsable page https://claude.ai/artifact/GqqLMK2FGnYLPpcU1DHpM6 · audit + design DNA in [01-…](decor-research/01-house-audit-and-design-dna.md) · 280 raw finds in `decor-research/raw/` · rebuild with `python3 decor-research/build_report.py`. Nothing bought yet; proposals only.
- **Wall colour is NOT decided** (the Warm Ivory `#F2EBDD` in the palette was a proposal). A floor-matched recommendation is part of the decor research.
- **Feature-wall materials (travertine / greige stone) still being decided**; Ganesh is considering replacing the foyer welcome **monitor** with a **framed photo/artwork**. If the monitor is dropped: revisit the foyer cavity, Pi, halo LED and the conduit map (`CLAUDE.md` rule).
- **Room naming:** Ganesh's own room = WEST balcony bedroom; EAST bedroom = guest room (his late brother's memory); GF master = parents. Repo labels "Bedroom 1/2" are the reverse of his usage — prefer compass + use in new docs.
