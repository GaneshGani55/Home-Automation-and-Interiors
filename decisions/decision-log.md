# Decision Log

Append-only chronological record of locked-in decisions. One line per decision. **What was chosen** and **why** — keep it short; details go in the relevant subfolder doc.

Format:
```
- YYYY-MM-DD · <area> · <decision> · <one-line reason> · <link to detail doc>
```

Areas: `floor-plan` · `electrical` · `furniture` · `automation` · `interior` · `materials` · `vendor` · `budget` · `timeline`

---

## 2026

- 2026-04-27 · floor-plan · Handwritten plans (GF + FF) declared the canonical reference; AutoCAD screenshots demoted to "reference only" · they reflect the latest design intent · [../floor-plans/floor-plans-decoded.md](../floor-plans/floor-plans-decoded.md)
- 2026-04-27 · tooling · `/banana` skill is the only image-gen tool for interior renders; outputs go to `interior-design/generated-images/` · single tool keeps style consistent and traceable · [../interior-design/generated-images/README.md](../interior-design/generated-images/README.md)
- 2026-04-27 · floor-plan · Building is confirmed **North-facing** (main entrance on N) · confirmed by user
- 2026-04-27 · floor-plan · GF ceiling height **11ft**, FF ceiling height **10ft** · confirmed by user
- 2026-04-27 · floor-plan · Wall thicknesses: structural/external = **9"**, partitions = **4"** (staircase landing, utility–store, bathroom–room) · confirmed by user
- 2026-04-27 · floor-plan · Hand-wash alcove on GF — **keep** · confirmed by user
- 2026-04-27 · floor-plan · FF Balcony (W side, top) projection = **3ft from last column** (expansion under consideration) · confirmed by user
- 2026-04-27 · floor-plan · Common Bathroom (GF) door opens from **West** · confirmed by user
- 2026-04-27 · floor-plan · Foyer wall: **9" thick, 6ft wide** — first thing visible on entry from main door · confirmed by user
- 2026-04-27 · floor-plan · Kitchen target depth **~10ft** out of the 19'6" kitchen+dining zone; exact split with dining TBD
- 2026-04-27 · interior · Foyer feature wall direction **accepted**: full rustic ledgestone cladding (tobacco brown / sandstone beige / charcoal), 22" Samsung monitor recessed flush at 4.5ft centre-height with amber halo LED, dark walnut floating shelf at 3ft, 2× ceiling grazing spotlights · render saved: `interior-design/generated-images/foyer-wall-rustic-stone-v1.png`
- 2026-04-27 · electrical · DB location confirmed: **West wall, foyer, behind door swing** · compact position, short conduit run to staircase niche
- 2026-04-27 · electrical · Smart switches: **Living, Bedrooms, Foyer, Dining, Staircase, Balconies** · Dumb switches: Kitchen · PIR auto-off switches: all 3 Bathrooms
- 2026-04-27 · electrical · AC points in **all rooms** confirmed (install units later): Living, Dining, MBR, BR1, BR2, FF Living = 6 dedicated RCBO circuits
- 2026-04-27 · electrical · False ceiling confirmed for: **Living (GF), Dining (GF), Foyer (GF), Bedroom 2 (FF West — first room after staircase)** · adds cove circuits B4, B9, B10, + new circuit for BR2 cove
- 2026-04-27 · electrical · Geyser size: **15L** for all 3 bathrooms
- 2026-04-27 · electrical · DB upgraded to **48-way** — 42 confirmed circuits + 6 spare
- 2026-04-28 · furniture · Living area long sofa: **pull 5in off the N wall** (pull-forward, not low-back) · standard-height back 32–34in; sunken floor (-5") already reduces sill conflict to ~3", pull-forward clears it and keeps curtain clean behind · [../interior-design/living-area.md](../interior-design/living-area.md)
- 2026-04-27 · floor-plan · Living correction: TV wall is **W wall** with **11'6"** TV-unit length; living **N wall is 16'11"** with centred teak window composition; living floor planned as **5" sunken** inside 1ft wall offset · corrected by user after render review · [../floor-plans/floor-plans-decoded.md](../floor-plans/floor-plans-decoded.md)

<!-- Add new decisions above this line, newest first within each year. -->
