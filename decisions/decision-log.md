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
- 2026-04-27 · floor-plan · Common Bathroom (GF) door opens from **West** · ~~confirmed by user~~ **SUPERSEDED — see 2026-05-01 correction**
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

- 2026-04-30 · interior · ~~GF Common Bathroom: dark charcoal theme, matte black hardware, false ceiling, 9ft drop~~ **SUPERSEDED — layout errors and theme rejected — see 2026-05-01 corrections**

- 2026-05-01 · floor-plan · **CORRECTION** — GF Common Bathroom door is on the **East wall**, left corner, 2.5ft wide, swings inward-left (not West as previously logged) · corrected by user
- 2026-05-01 · floor-plan · GF Common Bathroom ceiling: **8ft effective height** — attic sits directly above the lintel; standard GF 11ft does NOT apply here · confirmed by user
- 2026-05-01 · interior · GF Common Bathroom: **no false ceiling** — attic constraint makes it impossible · confirmed by user
- 2026-05-01 · floor-plan · GF Common Bathroom fixture sequence on **North wall** (E→W): Vanity → Commode → Glass partition → Shower · West wall: 3ft × 4ft frosted window · confirmed by user
- 2026-05-01 · interior · GF Common Bathroom direction **accepted**: light luxury spa — off-white/cream 600×1200mm porcelain tiles, walnut floating vanity, brushed gold hardware, 3000K lighting, clear glass partition, west window natural light · render saved: `interior-design/generated-images/gf-common-bathroom-light-luxury-v3.png` (SE corner, correct sequence) · [../interior-design/gf-common-bathroom.md](../interior-design/gf-common-bathroom.md)
- 2026-05-01 · interior · GF Bathroom south wall (shower zone): two stacked recessed niches (600×200mm upper + 400×120mm lower), IP65 warm LED strip inside upper niche, fold-down teak shower seat at 450mm height · [../interior-design/gf-common-bathroom.md](../interior-design/gf-common-bathroom.md)
- 2026-05-01 · automation · GF Bathroom lighting: PIR timer switch (Legrand/Schneider, 10-min delay) controls all lights; exhaust fan on separate manual switch; all lights recessed into RCC slab via attic access · [../automation-iot/gf-bathroom-lighting-automation.md](../automation-iot/gf-bathroom-lighting-automation.md)
- 2026-05-01 · budget · GF Bathroom budget target: **₹85,000–95,000** all-in (tiles ₹18–27K, sanitaryware ₹16–22K, fittings ₹12–19K, labour ₹26–37K) · [../materials-finishes/gf-bathroom-budget.md](../materials-finishes/gf-bathroom-budget.md)

- 2026-05-01 · electrical · GF Bathroom full electrical layout completed: 2 circuits (A1 6A RCBO lighting, A2 16A RCBO geyser), 4 light points (L1 mirror IP44 + L2 dry-zone downlight IP44 + L3 shower downlight IP65 + L4 niche LED IP65), IP65 exhaust fan ceiling-mount at x=8ft, 4-module switch board on east wall (PIR + exhaust switch + 16A geyser switch), geyser 15L in attic, all conduit runs via attic above lintel · [../electrical/gf-bathroom-electrical.md](../electrical/gf-bathroom-electrical.md)

- 2026-05-01 · floor-plan · **CORRECTION** — FF Toilet 2 (Bedroom 2 attached) fixture sequence is **SINK · TOILET · SHOWER** (W→E, entering from west) — not SHOWER·TOILET·SINK as previously decoded · corrected by user from floor plan reading
- 2026-05-01 · interior · FF Bedroom 2 (west, personal master): style direction locked as **Warm Modern Luxe** (Japandi bones with dark-luxe accents, warm/tactile/dimmable/matte, Indian residential context) · approved by user after seeing renders
- 2026-05-01 · interior · FF Bedroom 2 north wall (work zone) **LOCKED**: Italian travertine honed vein-cut stone cladding 9ft floor-to-ceiling, two floating 5ft walnut shelves with under-shelf 2700K LED strips, 2×3ft frameless glass writing board (standoff hardware, right of desk left of door), 4ft height-adjustable walnut-top desk, monitor on articulating arm, Macbook, Aeron chair, brass desk lamp · render approved (~90% perfect by user): `interior-design/generated-images/ff-bedroom2-northwall-warm-modern-luxe-v2.png` (2K, 16:9, gemini-3.1-flash-image-preview)

- 2026-05-02 · automation · Face detection system architecture locked: CAM-1 (outside, face-level) → Frigate NVR on Beelink EQ12 (OpenVINO) → CompreFace face match → Home Assistant → RPi Zero 2W → Samsung welcome screen display · [../electrical/conduits-and-cavities.md](../electrical/conduits-and-cavities.md)
- 2026-05-02 · automation · Primary face-capture camera (CAM-1): **Hikvision DS-2CD2143G2-LU (ColorVu 4MP, 4mm, IP67, PoE)** — ColorVu chosen over AcuSense because Frigate bypasses on-camera AI; ColorVu gives full-colour night vision critical for face recognition; buy from I Secure India, Chitradurga · [../electrical/materials-checklist.md](../electrical/materials-checklist.md)
- 2026-05-02 · automation · Porch overview camera (CAM-2): **Hikvision DS-2CD2347G2-LU (ColorVu 4MP, 2.8mm, IP67, PoE)** — wide 2.8mm for full porch/approach context; same brand as CAM-1 for consistent NVR management
- 2026-05-02 · automation · 6-camera plan confirmed: CAM-0 (screen-bezel CSI→RPi), CAM-1 (face-capture, main door), CAM-2 (porch overview), CAM-3 (FF front balcony bird's eye), CAM-4 (E-wall exterior, kitchen/utility side), CAM-5 (terrace staircase exit) · [../electrical/conduits-and-cavities.md](../electrical/conduits-and-cavities.md)
- 2026-05-02 · automation · Screen-bezel camera (CAM-0): **Raspberry Pi Camera Module (CSI ribbon cable)** — connects to RPi Zero 2W CSI port (not USB); streams RTSP over existing Cat6; no PoE needed; USB OTG port stays free for Ethernet adapter
- 2026-05-02 · electrical · PoE switch upgraded: **TP-Link TL-SG1210P (8× PoE, 10-port)** replaces TL-SG1008P (4× PoE) — 5 outdoor PoE cameras require more than 4 PoE ports · [../electrical/materials-checklist.md](../electrical/materials-checklist.md)
- 2026-05-02 · automation · 3 new camera conduit stubs to chase before plastering: CAM-3 (FF front balcony NW soffit), CAM-4 (E-wall exterior 2400–2600mm FFL), CAM-5 (terrace staircase exit parapet) — all LV-25, 1× Cat6 + draw wire · [../electrical/conduits-and-cavities.md](../electrical/conduits-and-cavities.md)

<!-- Add new decisions above this line, newest first within each year. -->
