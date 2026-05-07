# Interior Design

Style direction, mood, palette, and room-by-room interior decisions. Image renders generated via the **`/banana`** skill.

## ★ Start here

- **[master-interior-spec.md](master-interior-spec.md)** — A-to-Z whole-house interior brief. Use this as the contractor brief for everything (paint, tile, wood, hardware, lighting, sanitaryware, furniture).
- **[../materials-finishes/master-color-palette.md](../materials-finishes/master-color-palette.md)** — colour palette (hex codes + Asian Paints SKUs) for every zone.

## Per-room files (existing)
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
- **Master-bedroom wardrobes** run 12'0" + 12'3" (L-shape on N + W walls).
- **Cut-out edge on FF** has a beam — visible on the FF Living ceiling/floor edge.

## Open questions
- Overall style direction not yet chosen — pick before generating room renders.
- Budget tier (premium / mid / value) for finishes — drives material spec.
- Climate constraints (Bangalore? Chennai? Hyderabad?) — affects flooring, AC, materials.
