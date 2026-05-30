# Master Interior Specification — A to Z

> **Single-source spec for everything you can touch in the house.** Use this as the brief to interior contractors, carpenters, painters, tile vendors, and the lighting team. Every section is keyed to the master palette ([../materials-finishes/master-color-palette.md](../materials-finishes/master-color-palette.md)) so a contractor can buy materials without re-asking for colour codes.
>
> **Style direction (whole house):**
> - **Ground Floor:** Warm Contemporary Indian — calm, premium, practical, not flashy. Teak windows are the anchor.
> - **First Floor:** Warm Modern Luxe (Japandi-with-luxe-accents) — moodier, richer materials. Walnut + travertine + brass.
> - **Common thread:** warm ivory base, no cool whites, no high-gloss surfaces, layered lighting (2700K everywhere except kitchen/bathrooms), one metal vocabulary per zone.

---

## A — Architectural moves (already locked)

| Move | Decision |
|---|---|
| Sunken living floor | 5" drop, 1ft perimeter ledge from all 4 walls (decision-log 2026-04-27) |
| Double-height void | 16'9" × 11' — over the northern half of living area |
| Foyer wall | 9" thick × 6ft wide stone-feature wall on S edge of foyer (East 6 ft of the 9.5 ft S edge; West 3.5 ft is open passage to Living/Pooja). **Stone wraps INTO the cavity reveal for 30 mm depth (revised 2026-05-19)** — see [FOYER_MASTER_ELECTRICIAN_PLAN.md](../electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md) |
| Main door orientation | North-facing (confirmed) |
| GF Common Bathroom door | East wall, left corner (corrected 2026-05-01) |
| GF Common Bathroom ceiling | 8ft RCC slab, no false ceiling |
| False ceiling — GF | Living + Dining + Foyer — confirmed |
| False ceiling — FF | Bedroom 2 only (not Bedroom 1) |
| TV wall | West wall of living, 11'6" usable, anchored under the void |

---

## B — Bathrooms (3 total)

### B.1 GF Common Bathroom — locked
**Theme:** Light Luxury Spa · See [gf-common-bathroom.md](gf-common-bathroom.md) for full detail.

- Tile: warm cream marble-look 600×1200 walls + warm greige 600×600 floor
- Hardware: brushed gold throughout (Jaquar Lighthouse / Kohler Composed series)
- Fixtures: wall-hung WC + concealed cistern · 600mm walnut floating vanity · undermount basin · ceiling rain shower 200mm + handheld
- Glass: clear toughened 10mm fixed panel + 200mm raised threshold
- Lighting: PIR auto-off, 3000K, 4 fittings (mirror + 2 downlights + niche LED)
- Special: south-wall niches (600×200 upper + 400×120 lower) with IP65 LED strip in upper niche · teak fold-down shower bench

### B.2 FF Toilet 1 (Bedroom 1 attached)
**Style:** Same Light Luxury Spa palette as GF for visual consistency.

- Layout: SINK · TOILET · SHOWER (E→W)
- Tile: same as GF bathroom
- Hardware: brushed gold (same series as GF)
- Geyser: 15L, in attic above bathroom — 20A switch outside toilet on bedroom-side wall
- Lighting: PIR inside (10-min timer) · IP65 over shower · IP44 over dry zone · IP44 mirror light
- Niche: 1× single niche on south wall in shower zone, 600×300mm with IP65 LED strip
- Mirror: 600×800 LED backlit, 3000K
- Vanity: 600mm walnut floating cabinet (same finish as GF)

### B.3 FF Toilet 2 (Bedroom 2 attached)
**Style:** Same as B.2 — but **shift accents to walnut** (matches BR2's Warm Modern Luxe direction).

- Layout: SINK · TOILET · SHOWER (W→E)
- Tile: same warm cream walls + warm greige floor
- Vanity: 750mm wider walnut floating cabinet (matches BR2 wardrobe finish)
- Hardware: brushed gold
- Geyser: 15L in attic · 20A switch outside on bedroom-side wall
- Special: tower-storage column to right of vanity (4ft tall, walnut, recessed niches)

---

## C — Ceilings & Cove Lighting

### C.1 False ceiling specification (where applied)

| Zone | Drop from slab | Type | Cove? | Finish |
|---|---|---|---|---|
| Foyer | Slab 11ft → false ceiling 9ft (drop 2ft) | Gypsum board with POP cornice | Perimeter cove (LED strip 2700K) | Soft snow `#F8F4EC` matte emulsion |
| Living | Slab 11ft → false ceiling 9ft (drop 2ft) — only south of void edge | Gypsum board, perimeter cove | Yes — perimeter cove | Same |
| Dining | Slab 11ft → false ceiling 9ft (drop 2ft) | Gypsum board | Yes — perimeter cove | Same |
| Bedroom 2 (FF) | Slab 10ft → false ceiling 9ft (drop 1ft) | Gypsum board | Yes — perimeter cove with smart dimmer (D11 circuit) | Same |
| All bathrooms | None — RCC slab exposed | — | — | Bathroom paint (washable matte) |
| Bedroom 1 (FF) | None | — | — | Direct slab paint, soft snow |
| Master Bedroom (GF) | None — keep 11ft height | — | — | Direct slab paint |
| Kitchen | None — keep 11ft height | — | — | Direct slab paint |

### C.2 Cove specification

- Cove pocket: 100mm wide × 75mm deep, gypsum returns to slab
- LED inside cove: 24V warm white 2700K, CRI≥90, 9.6W/m
- Driver: Meanwell 24V 60W per zone, hidden in inspection-hatch zone
- Switching: smart dimmer (Sonoff/Aqara) — separate scene control
- Beam edge (FF cut-out): 2-shade-warmer paint to define void edge

---

## D — Doors & Windows

| Item | Spec |
|---|---|
| Main door | Solid teak, frame stained to match windows; smart Godrej video-lock + smart-lock combo (decision-log) |
| Internal doors (bedrooms, bathrooms, pooja, utility) | Flush teak veneer doors, 32mm thick, 7ft tall · matt PU finish |
| Door hardware | Brushed gold lever handles (consistent with bathroom hardware) |
| Door stops | Floor-mounted brushed gold |
| All windows | Existing teak windows retained — natural polished finish, no paint |
| Window mesh | Honeycomb fly-mesh, retractable type, on all bedroom + kitchen windows |
| Window grills | Mild steel, matte black powder coat, simple vertical-bar pattern (no decorative scrolls) — only where security needs require |
| Curtain tracks | Ceiling-recessed double aluminium track (sheer + drape) — see [living-area.md § Curtains](living-area.md#curtains) |
| Curtain operation | Living north window: motorized (height-driven decision); all other rooms: manual |

---

## E — Electrical & Smart Home (cross-reference)

See:
- **★ [../electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md](../electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md) ★** — authoritative foyer welcome system plan (18 sections; PDF version at `pdfs/FOYER_ELECTRICIAN_MASTER_PLAN.pdf`)
- [../electrical/conduits-and-cavities.md](../electrical/conduits-and-cavities.md) — cavity depths, switch box specs (65mm GI MS); foyer Part 1 is a summary, master plan above has full detail
- [../electrical/db-layout.md](../electrical/db-layout.md) — circuits + DB (DB on East wall of foyer per 2026-05-17 correction)
- [../electrical/materials-checklist.md](../electrical/materials-checklist.md) — buy list (revised 2026-05-22 with foyer-scope items)

**Switch plate finish (whole house):** Schneider Unica **champagne** OR Legrand Mylinec **bronze** — pick one and stick. **Foyer Switch Panel is 6-gang (default; possibly 7- or 8-gang if box fits)** on N wall 1'6" section between corner window and main door.

**Foyer welcome system summary** (full detail in foyer master plan):
- Hikvision DS-KV6113-WPE1(C) Video Doorbell PoE on N wall outside (face detection + bell + 2-way audio)
- Samsung 21.5" monitor recessed in S feature wall cavity (centre 1450 mm FFL)
- Stone slips wrap 30 mm INTO cavity reveal (all 4 inner walls); back wall + deeper portion matte black
- Halo LED 24V 2200K behind stone reveal lip — glows around monitor edges
- Cavity speaker (Visaton FR 8) hidden behind monitor — voice from screen
- RPi Zero 2W powered via PoE (no extra 230V wires for the RPi)
- 2 MCBs: B-Foyer-Lights + B-Foyer-Cavity (30mA RCBO)
- Waveshare touchscreen indoor unit provisioned on staircase S wall (design deferred)

---

## F — Furniture (per room)

### F.1 Living Area
See [living-area.md](living-area.md) for full detail.

| Item | Size | Material |
|---|---|---|
| L-sofa long side (N wall) | 10–11ft × 36–38" deep, pulled 5in off N wall | Oatmeal `#D4C4B0` performance fabric |
| L-sofa return (E side) | 6–7ft × 36–38" deep | Same fabric |
| Lounge chairs ×2 (S side) | 28–32" wide each | Teak/cane frame OR upholstered |
| Coffee table | 48×28" rectangle OR 42" round | Travertine top `#D6C5A8` |
| Rug | 10×13ft | Low-pile wool, oatmeal/grey blend |
| Side tables ×2 | 18–22" diam | One stone, one walnut |
| Floor lamp | 5–6ft tall | Brass shade `#B08D57` |
| Console (S ledge, optional) | 4–5ft × 14" deep | Walnut |

### F.2 Dining Area

| Item | Size | Material |
|---|---|---|
| Dining table | 6-seater 6×3ft (or 8-seater 7×3.5ft) | Walnut top, brass-clad legs |
| Dining chairs | 6 chairs | Walnut frame, oatmeal upholstered seat |
| Sideboard / buffet | 5–6ft × 18" deep | Walnut + brushed brass handles |

### F.3 Master Bedroom (GF) — layout locked 2026-05-10

**Room:** ~12' × 12'3" usable · 11ft ceiling, no false ceiling, direct slab paint · SE quadrant of house · door from central passage.

**Wall-by-wall:**

| Wall | Length | Contents (ordered) |
|---|---|---|
| **S wall** (exterior) | 12'3" | SE corner: 2'×5' teak window · then 10'3" L-wardrobe S-run with sliding doors |
| **E wall** (exterior, **solid — no windows**) | ~12' | Bed wall — Queen 75×60", head-to-east, centered with slight N bias · 2× wall sconces flanking headboard · 2× walnut bedside tables |
| **W wall** (interior, shared w/ Common Bath + Staircase) | ~12' | SW corner: ~3' wardrobe tail (continuation of L) · then ~4' sleek dressing/powder unit · then NW corner: 3.5'×5' teak window |
| **N wall** (interior, opens to passage) | 12'3" | NW corner: closed sewing-machine cabinet (machine tucks away, fold-out work surface, walnut + cream finish to match wardrobe) · middle ~6': reading nook · NE corner: 3ft door swinging inward to E (left as you enter) · AC unit high above door/nook |

**Reading nook (N wall middle):**
- Cane-back walnut armchair, low-slung
- Brass arc floor lamp angled over chair
- Small round walnut side table, 12" dia, marble top
- Framed pichwai or madhubani panel above (~30×40", walnut frame)

**Furniture spec:**

| Item | Size | Material / finish |
|---|---|---|
| Bed | Queen 75×60" with upholstered headboard | Walnut frame, cream linen headboard |
| Bedside tables ×2 | 22×16" | Walnut |
| L-wardrobe (S 10'3" + W ~3' tail) | Floor-to-ceiling, **sliding doors** (space-tight) | Walnut + matte cream shutter mix, brass slim handles |
| Dressing/powder unit (W wall) | ~4ft wide × 16–18" deep, sleek/minimal | Walnut, framed mirror, brass pulls |
| Reading nook chair | Single armchair | Cane-back + walnut frame |
| Side table (nook) | 12" diameter | Walnut + marble top |
| Floor lamp (nook) | Arc | Brushed brass |
| Sewing cabinet (NW) | ~3ft wide × 18" deep × ceiling height | Walnut + cream — closed when not in use |

**Style/mood:** TBD — choosing between Warm Heritage Calm / Modern Indian Luxe / Japandi-Indian Hybrid (renders pending).

**AC point:** high on N wall above door/nook (provisioned).

### F.4 FF Bedroom 1

| Item | Size | Material |
|---|---|---|
| Bed | Queen 75×60" | Walnut, low-profile headboard |
| Bedside tables ×2 | 18" diam round | Walnut |
| Wardrobe | 8ft run | Walnut + matte cream |
| Study desk | 4×2ft | Walnut top, slim metal legs |
| Study chair | Mid-back ergonomic | Black mesh |
| Window seat (S wall, if retained) | 5ft × 18" deep | Cream upholstered cushion top + storage below |

### F.5 FF Bedroom 2 (Warm Modern Luxe — work zone locked)

| Item | Size | Material |
|---|---|---|
| Bed | Queen 75×60" | Walnut, cream linen upholstered headboard |
| Bedside tables ×2 | 18×16" | Walnut |
| Wardrobe (W wall, 3ft deep) | 8ft run | Walnut |
| Study desk (N wall — LOCKED) | 4ft height-adjustable | Walnut top, charcoal metal frame |
| Study chair | Aeron (already chosen) | Black |
| Floating shelves (N wall) | 2× 5ft shelves | Walnut with under-shelf 2700K LED |
| Glass writing board | 2×3ft frameless | Brass standoff hardware |

### F.6 Kitchen

| Item | Spec |
|---|---|
| Layout | L-shape, top-left corner (per AutoCAD) |
| Lower cabinets | 18mm BWP marine ply, charcoal grey matte PU laminate `#3F3A35` |
| Upper cabinets | Same carcass, warm cream matte laminate `#E8DCC8` |
| Counter top | Quartz cream `#E0D4C0` (Stone Studio "Crema Vienna" or equivalent) |
| Backsplash | Warm cream subway 100×300mm matte ceramic |
| Sink | Stainless steel undermount double-bowl 32×18" |
| Hob | 4-burner glass top OR induction (decision pending) |
| Chimney | Auto-clean, 90cm, brushed black |
| Handles | Brushed brass D-pulls (Hettich / Hafele) |
| Bar stools | 2 bar stools at island/peninsula end | Teak frame, cream cushion |

### F.7 Pooja

| Item | Spec |
|---|---|
| Pooja unit | Burnished teak, traditional carved panels, floor-to-ceiling |
| Idol niche | Backlit with warm amber LED behind brass-leaf laminate |
| Idol shelf | Brass-clad, 24in wide |
| Floor cushions | 2× kneeling cushions, cream linen with kantha embroidery accent |

---

## G — Glazing & Glass

| Item | Spec |
|---|---|
| Windows (existing teak frames) | Double-glazed where possible OR good single 6mm clear toughened — already in place; do NOT replace |
| Bathroom shower partitions | 10mm clear toughened, frameless, brushed-gold pivot/handle (or fixed panel + kerb) |
| BR2 writing board | 8mm frosted toughened, brass standoffs |
| Foyer screen | 21.5" Samsung LS22F350 recessed in S feature wall cavity. **Full design in [electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md](../electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md)** (the authoritative source for the welcome system — face detection via Hikvision doorbell, halo LED, ceiling speaker, etc.) |

---

## H — Hardware standards

| Category | Brand | Finish |
|---|---|---|
| Cabinet handles (visible) | Hettich / Hafele | Brushed brass `#B08D57` |
| Cabinet hinges | Hettich / Hafele soft-close | Standard nickel |
| Drawer channels | Hettich / Hafele Quadro | Soft-close |
| Wardrobe internal | Hettich / Ebco | Standard |
| Door locks | Godrej Locks (matches main video lock series) | Brushed gold finish |
| Door handles (lever) | Yale / Dorset | Brushed gold |
| Curtain finials | Custom or off-the-shelf | Antique brass |

> Rule: never use chrome anywhere. Pick brushed gold/champagne brass for ALL visible hardware. Inside cabinets where hardware is hidden, plain nickel is fine.

---

## I — Iron & metal work

| Item | Finish |
|---|---|
| Sunken-floor step edge L-profile | Matte black aluminium 25×25mm OR brass inlay 6mm |
| Staircase railing (existing) | Retain — matte black powder coat if rusty |
| Bathroom robe hooks | Brushed gold |
| Towel bars | Brushed gold |
| Outdoor balcony railings | Matte black powder coat MS |
| Window grills (where added) | Matte black powder coat, simple vertical bars |

---

## J — Joinery (built-ins)

All built-ins use the same construction recipe to ensure life and consistency:

| Element | Standard |
|---|---|
| Carcass (wardrobes, kitchen, vanities, TV unit) | **18mm BWP/BWR marine ply** — never MDF, never particle board |
| Shutters | Laminate on 18mm ply, matte/suede/anti-fingerprint finish |
| Edge banding | 2mm ABS, matched to laminate |
| Handles | Brushed brass D-pulls, 96mm centre OR push-to-open for high-end zones |
| Drawer slides | Soft-close, full extension (Hettich Quadro or Hafele Salice) |
| Hinges | Soft-close clip-on (Hettich) |
| Backing | 6mm BWP plywood, dust-sealed inside cabinets |
| Adjustable shelves | 18mm BWP, edge-banded |
| Wardrobe internal lighting | 24V LED strip on door-actuated reed switch |

---

## K — Kitchen specification

(Already covered in F.6.) Additional spec:

| Item | Spec |
|---|---|
| Tall pantry | 30in wide × ceiling height, walnut shutters |
| Microwave + OTG niche | 2 niches at counter level |
| Refrigerator niche | 30in wide (per AutoCAD) — measure your fridge first |
| RO water purifier | Below counter, near sink |
| Cutlery drawer | Hettich organiser inserts |
| Drying rack | Built into cabinet above sink |
| Plumbing rough-in | Hot + cold water at sink, wash basin, RO |
| Gas point | DG cylinder line OR PNG (whichever applies) |

---

## L — Lighting Design (whole house — layered)

Each room has 4 layers. Mix appropriately.

| Layer | Purpose | Example fittings |
|---|---|---|
| **Ambient** | General room illumination | Recessed COB downlights, ceiling LED panels |
| **Task** | Reading, cooking, mirror, study | Mirror lights, under-cabinet LEDs, study spots |
| **Accent** | Texture / feature highlight | TV wall washers, stone-grazing spots, niche LEDs |
| **Decorative** | Visual focal point | Chandelier, pendants, floor lamps, table lamps |

**Per-room spec:** see [../electrical/conduits-and-cavities.md § PART 3](../electrical/conduits-and-cavities.md#part-3--lighting-exact-positions) for exact fixture positions and circuits.

**Best lighting selections by room:**

| Room | Best ambient | Best task | Best accent | Best decorative |
|---|---|---|---|---|
| Foyer | 2× recessed GU10 7W gimbal (stone-grazing) | — | Cove + screen halo | Walnut shelf with LED below |
| Living | 4× recessed COB 12W 2700K | — | TV wall wash 2× GU10 + cove | **Vertical cluster pendant in void** (24–36" diam, antique brass/champagne — over coffee-table area) |
| Dining | 2× recessed COB 9W + cove | — | Cove perimeter | **1× decorative pendant over dining table** (drop to 2100mm FFL, warm 2700K) |
| Kitchen | 24W LED panel 4000K (cool/neutral) | Under-cabinet 24V warm strip | — | — |
| MBR | Recessed COB 12W centre | Wardrobe LED + bedside reading | Headboard wall wash (optional) | Bedside table lamps with brass shade |
| Pooja | Soft warm 12W LED panel | — | Niche backlight 2200K | — |
| Stairs | Wall recessed + step nosings | — | Step lights | — |
| BR1 | Recessed COB 12W centre | Study spot 7W 3000K + wardrobe LED | Headboard accent (optional) | Bedside lamp |
| BR2 | Recessed COB 12W + cove | Study desk pendant + walnut-shelf strips + Aeron-area task light | Travertine wall-grazer on N wall | **Brass desk lamp + bedside walnut lamp** |
| Toilets (FF) | IP44 recessed 9W 3000K | Mirror LED bar 12W | Niche LED (where present) | — |
| GF Bath | (locked — see B.1) | — | — | — |
| Front Balcony | 1× IP65 LED 9W 3000K | — | — | — |
| W Balcony | 1× IP65 LED 7W | — | — | — |

---

## M — Material palette (cross-reference)

See [../materials-finishes/master-color-palette.md](../materials-finishes/master-color-palette.md) for hex codes + Asian Paints SKUs.

---

## N — Network & Wi-Fi (interior touch points)

This is where electrical meets interior aesthetics. Hide cables; show only what should be seen.

| Item | Visible? | Where |
|---|---|---|
| Main router | Hidden | Inside staircase niche on shelf |
| FF Wi-Fi access point | Visible (small white/black puck) | FF Living central wall, 2400mm FFL — keep clean |
| Cat6 wall plates (BR1 + BR2 study) | Visible | At study desk — match modular plate finish to switch plates |
| Cat6 wall plate (TV wall) | Hidden | Behind TV unit |
| 12-port patch panel | Hidden | Inside staircase niche, 700mm height |

---

## O — Outdoors (balconies, façade)

| Item | Spec |
|---|---|
| Front balcony floor | Wood-look porcelain 200×1200mm, R11 anti-slip, IPE finish `#6E5234` |
| W balcony floor | Same |
| Balcony parapet | Concrete (already in place); paint inside face warm taupe `#A8967E`, outside face matching house exterior |
| Balcony railings (where retained) | Matte black powder coat MS |
| Outdoor planters | Terracotta `#9C5A3C` + matte black `#1F1B16` mix; 4 large + 6 small |
| Outdoor furniture (front balcony) | 2× metal/cane chairs + small round side table; cream cushions |
| Outdoor lighting | IP65 wall lights 3000K + step lights as detailed in electrical |

---

## P — Paint (whole house)

Colour codes in [master-color-palette.md](../materials-finishes/master-color-palette.md). Application:

| Surface | Product | Coats |
|---|---|---|
| Interior walls (premium) | Asian Paints **Royale Aspira** matte | 1 primer + 2 finish |
| Interior walls (standard zones) | Asian Paints **Royale Luxury** matte | 1 primer + 2 finish |
| Ceilings | Asian Paints **Premium Emulsion** flat | 1 primer + 2 finish |
| Trim / doors | PU matte (factory-finished doors) OR Asian Paints Trucare PU on site | Factory pref |
| Bathroom walls (above tile) | Asian Paints **Royale Bathroom & Kitchen** | 1 primer + 2 finish |
| Exterior | Asian Paints **Apex Ultima** | 1 primer + 2 finish |

> Always do a 2×2ft sample on actual wall before signing off.

---

## Q — Quartz / Stone surfaces

| Surface | Stone | Reason |
|---|---|---|
| Kitchen counter | Quartz `#E0D4C0` "Crema Vienna" type | Stain-proof, non-porous, no sealing |
| Living TV feature wall | Microcement `#B8A88F` OR travertine slab | Tactile, premium, no joints visible |
| BR2 N wall (locked) | Italian travertine, vein-cut, honed `#D6C5A8` | Already locked decision |
| Foyer feature wall | Rustic ledgestone (tobacco brown / sandstone beige / charcoal) | Already locked decision |
| Bathroom counters (vanity tops) | Marble-look porcelain slab OR small-format quartz | Easier to maintain than natural stone |

---

## R — Rugs & soft furnishing

| Room | Item | Size | Material |
|---|---|---|---|
| Living | Floor rug | 10×13ft | Low-pile wool, oatmeal/grey weave |
| Dining | Optional rug | 6×9ft | Flat-weave |
| MBR | Bedside runners | 2×6ft each side | Wool dhurrie |
| BR1 | Floor rug | 5×8ft | Wool |
| BR2 | Floor rug | 6×9ft | Wool, charcoal/cream |
| Foyer | Optional runner | 2×4ft | Cotton dhurrie OR none |

---

## S — Sanitaryware brand recommendations

| Item | Budget pick | Mid pick | Premium pick |
|---|---|---|---|
| WC + cistern | Parryware / Hindware | Jaquar Continental | Kohler / TOTO |
| Basin | Parryware | Jaquar | Kohler |
| Faucets / mixers | Jaquar Continental | Kohler Composed / Jaquar Lighthouse | Grohe Essence (brushed gold) |
| Shower head | Local | Jaquar | Hansgrohe |
| Concealed cistern | Geberit Sigma | Geberit Sigma | Geberit |
| Geyser | Bajaj 15L | Racold Eterno 15L | AO Smith 15L |
| Mirror | Local LED 600×800 | Branded LED frameless | Custom |

> One brand for all hardware in a bathroom = clean look. **Recommended:** Jaquar Lighthouse OR Kohler Composed (brushed gold) for all 3 bathrooms. Single SKU reduces your purchase friction and ensures shade match.

---

## T — Tiles

| Zone | Tile | Size | Brand pick |
|---|---|---|---|
| Living + Dining + Foyer | Warm ivory-greige marble-look matte porcelain | 1200×1200 | Kajaria Eternity / Somany Slimtec |
| Master Bedroom | Same as living | 1200×1200 | Same |
| Pooja | Same as living | 1200×1200 | Same |
| Kitchen floor | Warm greige R10 anti-slip porcelain | 600×600 | Kajaria/Somany |
| Utility / Store room | Warm greige R10 | 600×600 | Local OK |
| Kitchen backsplash | Warm cream subway matte ceramic | 100×300 | Local OK |
| All bathroom walls | Warm cream marble-look matte porcelain | 600×1200 | Kajaria Eternity / RAK Infinite |
| All bathroom floors | Warm greige R10 anti-slip | 600×600 | Same |
| Front balcony | Wood-look porcelain IPE finish R11 | 200×1200 | Kajaria Vintage Wood / Somany Wood |
| W balcony | Same | Same | Same |
| Bedroom 1 + Bedroom 2 (FF) | Same as living (1200×1200 ivory-greige) | 1200×1200 | Same |

> **Rule:** the same living tile runs through foyer + living + dining + master bedroom + pooja for visual continuity. Bedrooms upstairs use the same tile too — saves stocking different sizes and gives whole-house visual flow.

---

## U — Utility & service (kitchen utility, store, balcony storage)

| Zone | Spec |
|---|---|
| Utility | Washing machine + sink + 1 broom cupboard + ceiling-mount cloth rack |
| Store room | Built-in shelves floor-to-ceiling, BWP ply painted in `#F2EBDD` |
| Balcony storage (front) | Small storage bench with cushion top |
| Pooja storage | Inside the pooja unit cabinets |

---

## V — Visible decor (rules)

- **Less is more.** One large statement piece beats six small clutter items.
- 1 large indoor plant per room minimum (areca palm, fiddle leaf fig, rubber, snake plant, ZZ).
- Art: ONE large piece in the living, ONE in MBR, ONE in dining. No more than 3 framed photos in any single sightline.
- Pillows: max 4 per sofa, mix of plain + texture + 1 accent.
- Books on coffee tables: 3–5 books in a small stack, never sprawling.
- Candles, vases, brass figures: group in odd numbers (1 or 3, never 2).
- Avoid: tassels, fringes, very ornate frames, religious posters in living/foyer (pooja room is the right place).

---

## W — Wardrobes & closets

| Room | Spec |
|---|---|
| MBR | 10'3" (S wall) + ~3' tail (W wall) — see master-color-palette.md for finish |
| BR1 | 8ft N wall (TBD exact) — walnut + cream split shutters |
| BR2 | 8ft along S/W wall, 3ft deep on W wall — walnut shutters with brass D-pulls |
| All wardrobes internal | Hettich Quadro drawers, soft-close hinges, internal LED strip on door-actuated switch |
| Hanging | Stainless steel hanging rod with brass-clad hangers (optional) |
| Sliding vs hinged | Hinged for visibility unless space is tight; sliding for narrow rooms |

---

## X — eXterior finish (for visible-from-inside surfaces)

The exterior of the house is outside the scope of this interior spec, but anything **visible through windows** affects interior mood:

- Compound wall inside face: paint warm taupe `#A8967E` to match interior accent — soft view through windows
- Gate: matte black powder coat
- Outside-window planters: terracotta `#9C5A3C` to soften concrete

---

## Y — Yard / landscaping (for context)

| Zone | Plantings |
|---|---|
| Front porch | 2× large pots with areca palm or bird-of-paradise |
| North entrance approach | Low gravel + 3 large stones + 1 flowering shrub |
| Side balcony view | 2 pots with cascading plants (turtle vine, money plant) |

---

## Z — Z lock / Sign-off checklist (before bulk material order)

- [ ] Master colour palette signed off by user (this file)
- [ ] All paint samples painted on actual walls (2×2ft each) and approved at 3 times of day
- [ ] All tile samples seen on actual floor in actual daylight
- [ ] All wood/laminate samples lined up under 2700K bulb + natural light
- [ ] Stone slab samples (TV wall + BR2 N wall + foyer feature) brought home and reviewed
- [ ] Hardware sample: 1 faucet + 1 cabinet handle compared for shade match
- [ ] Curtain fabric swatches draped in actual window for an evening
- [ ] Modular switch plate sample confirmed against hardware shade
- [ ] Total cost of materials within budget envelope (cross-reference: GF bathroom budget ₹85K, electrical ₹3.7L; whole-house tile + paint + furniture est. ₹15–20L additional — **TBD: get full quotation**)
- [ ] Interior contractor signed off on this brief
- [ ] Carpenter signed off on joinery brief
- [ ] Painter signed off on paint codes

---

## Appendix — Brand cheat sheet (one-shot vendor list)

| Category | Vendor | Phone/branch |
|---|---|---|
| Paint | Asian Paints / Berger / Dulux dealer in Chitradurga | TBD |
| Tile (premium) | Kajaria / Somany / RAK Ceramics — Bangalore showroom for samples | TBD |
| Quartz / stone | Stone Studio / Classic Marbles — Bangalore | TBD |
| Hardware | Hettich / Hafele showroom — Bangalore | TBD |
| Sanitaryware | Jaquar showroom OR local Plumber's Choice — Chitradurga / Bangalore | TBD |
| Modular switches | Schneider / Legrand authorised dealer | TBD |
| Wood/laminate | Greenply / Century / Merino — local distributor | TBD |
| CCTV / cameras | I Secure India, Chitradurga (already confirmed Hikvision dealer) | confirmed |
| Electrical | Schneider Acti9 distributor | TBD |
| Curtains/blinds | Local interior tailor + motor (D'Decor / Marshalls fabric source) | TBD |
| Kitchen hardware | Hettich / Hafele | TBD |
| Furniture (custom) | Local carpenter; high-end pieces from Pepperfry / Wooden Street | TBD |

---

## Appendix — Quantity Take-off (rough)

| Item | Approx qty | Notes |
|---|---|---|
| Tile (1200×1200 living) | 100 sqm | Living + dining + foyer + bedrooms + pooja = ~1100 sqft |
| Tile (600×1200 bathroom wall) | 70 sqm | All 3 bathrooms |
| Tile (600×600 floor) | 30 sqm | Bathrooms + kitchen + utility |
| Tile (200×1200 wood-look) | 25 sqm | Both balconies |
| Paint (premium emulsion) | 200 litres | Whole house interior including primer |
| Paint (exterior) | 50 litres | Exterior face |
| Plywood (BWP 18mm) | 50 sheets (8×4ft) | All built-ins |
| Laminate (matte) | 60 sheets (8×4ft) | All built-ins |
| Curtain fabric (sheer + drape) | 80 metres total | All windows |
| Cove LED strip (24V 2700K) | 30 metres | All cove zones |
| Recessed COB downlights | 35 nos | Whole house |
| GU10 spots | 20 nos | Foyer + bedside + study spots |

> Treat this as a *budgeting* take-off, not a contractor BOQ. Contractor will do exact measurements on site before ordering.
