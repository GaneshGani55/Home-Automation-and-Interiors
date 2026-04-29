# Conduits, Cavities & Lighting — Exact Specifications

> This file is the **field reference** — hand it to your civil contractor and electrician before any chasing or cavity cutting starts. Every dimension is in **mm** (with inches in brackets). Heights are measured from **finished floor level (FFL)**.
>
> Cross-reference: [floor-plans-decoded.md](../floor-plans/floor-plans-decoded.md) for room dimensions · [db-layout.md](db-layout.md) for circuit IDs.

---

## PART 1 — FOYER SCREEN CAVITY (Most Critical — Do First)

### Monitor: Samsung LS22F350 (21.5" IPS)
Panel dimensions (without stand):
- Width: **491mm (19.3")**
- Height: **291mm (11.5")**
- Depth at thinnest (panel edge): **49mm (1.9")**
- VESA hole pattern: **75mm × 75mm**

### Cavity to Cut in Wall

```
        ← 540mm (21.3") →
        ┌─────────────────┐  ─
        │                 │  │
        │   STONE WALL    │  │ 340mm
        │   CAVITY        │  │ (13.4")
        │                 │  │
        └─────────────────┘  ─
             ↑
         depth: 100mm (4")
```

| Dimension | Value | Why |
|---|---|---|
| Cavity width | **540mm (21.3")** | Panel 491mm + 25mm clearance each side |
| Cavity height | **340mm (13.4")** | Panel 291mm + 25mm clearance top and bottom |
| Cavity depth | **100mm (4")** | Panel 49mm + 51mm behind for HDMI/power cables |
| Bottom of cavity from FFL | **1280mm (50.4")** | Screen centre at 1450mm — comfortable eye level |
| Centre of cavity from FFL | **1450mm (57.1")** | Ergonomic eye-level for standing adult |
| Top of cavity from FFL | **1620mm (63.8")** | |
| Horizontal position | **Centred** on the 6ft (1828mm) wall | Left edge at 644mm from left wall, right edge at 1184mm from right wall |

### Inside the Cavity

```
  [Back wall of cavity]
  ┌─────────────────────┐
  │  ●       ●          │  ← 2× VESA screws (75×75mm pattern)
  │     VESA PLATE      │
  │  ●       ●          │
  │                     │
  │  [O]  [O]           │  ← 2× conduit entries bottom-left corner
  │   C1   C2           │     C1 = 25mm power, C2 = 25mm Cat6
  └─────────────────────┘
```

- **VESA plate:** slim flush-mount VESA 75 bracket (10–15mm proud of back wall)
- **Paint inside cavity:** matte black — hides depth shadow around screen edges
- **Conduit entries:** both conduits enter from **bottom-left corner** of the cavity back wall, coming from the staircase niche direction (routing along W wall behind plaster)
- **Stone cladding:** runs right to the cavity edge. No stone inside the cavity.

### Cable Routing Inside Cavity
| Cable | From | To | Length needed |
|---|---|---|---|
| Monitor power cable | 6A socket (inside cavity, right wall) | Monitor power port | ~400mm |
| RPi USB-C power | USB-C charger (share socket) | RPi Zero 2W | ~200mm |
| Mini-HDMI → HDMI | RPi HDMI port | Monitor HDMI input | ~300mm |
| Cat6 patch cable | Keystone inside cavity | RPi USB-OTG Ethernet adapter | ~200mm |

**Socket position:** 1× double 5A socket flush-mounted on the **right inner wall** of the cavity at 1300mm from FFL (just below monitor bottom). Hidden behind monitor face when screen is installed.

---

## PART 2 — ALL CONDUIT RUNS (Floor by Floor)

### Conduit Key
| Label | Size | Colour (if using colour-coded) | Contents |
|---|---|---|---|
| P-25 | 25mm PVC | Red | Power — lighting circuits |
| P-25H | 25mm PVC | Blue | Power — heavy (sockets, ACs, geysers) |
| LV-25 | 25mm PVC | Grey | Low voltage — Cat6 |
| LV-16 | 16mm PVC | Grey | Low voltage — speaker / small LV |

### Rule: Conduit Heights in Walls
| Conduit type | Chase height (from FFL) | Rationale |
|---|---|---|
| Ceiling conduits (horizontal runs) | 150mm below slab soffit | In false ceiling zone or just below slab |
| Switch board feeds (vertical) | Continuous from DB upward in wall | Behind plaster |
| Socket feeds (horizontal) | **300mm from FFL** | Standard socket height = 300mm, conduit runs at same level |
| Switch board conduit (horizontal) | **1200mm from FFL** | Standard switch height = 1200mm |
| AC conduit (vertical, high) | **1800–1900mm from FFL** | AC socket sits at this height |
| Geyser conduit | **1800mm from FFL** | Geyser switch outside bathroom at 1200mm; outlet behind geyser at 1800mm |

---

### GF Conduit Runs — Detail

#### DB to Foyer Ceiling (Circuit B1 — Foyer Lights)
| Item | Value |
|---|---|
| Conduit size | 25mm |
| Route | DB (W wall, 1500mm) → up W wall → across foyer false ceiling → to 2× spotlight ceiling boxes |
| Spotlight box 1 position | 300mm from W wall, 609mm from N edge of foyer |
| Spotlight box 2 position | 300mm from W wall, 1218mm from N edge of foyer (or 609mm from S edge) |
| Depth at ceiling | Flush ceiling box (B-type, 60mm depth) |
| Switch drop | From ceiling conduit → down W wall to switch board at 1200mm |

#### DB to Foyer Screen (Circuits B2 — Screen + Speaker)
| Item | Value |
|---|---|
| Conduit 1 (power) | 25mm · DB → up W wall → across to cavity → enter cavity from bottom-left |
| Conduit 2 (data/LV) | 25mm · Staircase niche → horizontal wall chase → cavity bottom-left corner |
| Conduit 3 (speaker) | 16mm · Staircase niche → ceiling → ceiling rose above foyer centre |
| Cavity entry height | 1250mm from FFL (enters at cavity bottom edge) |

#### DB to Foyer False Ceiling Cove (Circuit B10)
| Item | Value |
|---|---|
| Conduit size | 16mm |
| Route | From B1 ceiling conduit → branch to LED driver box in false ceiling |
| LED driver box position | Above false ceiling, accessible via inspection hatch |
| Cove position | Perimeter of false ceiling (all 4 sides of foyer) |

#### DB to Living Area Ceiling (Circuits B3, B4)
| Item | Value |
|---|---|
| Conduit size | 25mm |
| Route | DB → up W wall → across GF ceiling (under false ceiling layer) |
| B3 (main lights) | 4× ceiling boxes distributed in living zone (away from void) |
| B4 (cove) | 16mm branch to cove LED driver in false ceiling perimeter |
| Chandelier prep (void) | Separate 25mm conduit from DB → vertical up W wall → across FF slab to void centre; terminate in a ceiling rose box at FF beam level |

#### DB to Living Area Sockets (Circuit B5)
| Item | Value |
|---|---|
| Conduit size | 25mm |
| Route | DB → horizontal at 300mm from FFL in W wall → TV wall on W side |
| TV wall cluster | 3 boxes: 16A socket + double 5A + Cat6 keystone plate; all at 300mm FFL |
| General sockets | DB → skirting-level run → socket boxes at 300mm FFL around perimeter |

#### DB to Kitchen (Circuits A3–A8)
| Item | Value |
|---|---|
| A3 (lights) | 25mm · DB → ceiling → kitchen ceiling box (centred) + junction to utility light |
| A4 (counter sockets) | 25mm · DB → horizontal at 1100mm FFL behind counter wall → 4× socket boxes |
| A5 (chimney) | 25mm · DB → up wall → chimney socket at 1900mm FFL above hob |
| A6 (hob) | 25mm · DB → floor-level run under floor screed → emerge at hob position 150mm FFL |
| A7 (washing machine) | 25mm · DB → utility, socket at 300mm FFL |
| A8 (fridge) | 25mm · DB → fridge niche socket at 300mm FFL |

#### DB to Master Bedroom (Circuits C1, C2, E3)
| Item | Value |
|---|---|
| C1 (lights) | 25mm · DB → W wall → ceiling → bedroom ceiling box (centred) + bedside light boxes |
| C2 (sockets) | 25mm · DB → horizontal chase at 600mm FFL along S wall → bedside socket boxes |
| E3 (AC) | 25mm · DB → vertical up W wall → AC socket at 1850mm FFL on S or W wall |

#### DB to GF Bathroom (Circuits A1, A2)
| Item | Value |
|---|---|
| A1 (lights) | 25mm · DB → bathroom ceiling via wall chase |
| PIR switch | Outside bathroom door, W side, at 1200mm FFL |
| Geyser switch | Just below PIR outside door, at 1050mm FFL (lower than PIR for visual separation) |
| A2 (geyser) | 25mm · DB → through bathroom wall → geyser box at 1850mm FFL |

#### Staircase Niche Conduit Hub (E7, E8 + all LV)
| Item | Value |
|---|---|
| UPS socket | 20A socket at 300mm FFL, back wall of niche |
| Server sockets | 2× double 5A at 400mm FFL, back wall |
| Cat6 patch panel | Wall plate at 700mm FFL, side wall of niche |
| Speaker terminals | Strip at 700mm FFL, side wall (same level as Cat6) |
| Niche light | Ceiling/top of niche — pull from staircase circuit |

---

### FF Conduit Runs (DB to First Floor)

#### Vertical Rise — GF to FF
All FF circuits must climb from GF DB to FF level. The cleanest route is **inside the staircase wall** (the 9" W wall of the staircase).

```
DB (GF, 1500mm)
   │
   ├─ Vertical rise inside staircase W wall ─────────────► FF slab level
   │   ├── Bundle 1 (25mm): D1+D2 (BR2 lights + sockets)
   │   ├── Bundle 2 (25mm): D5+D6 (BR1 lights + sockets) — wait, BR1 is east side
   │   │                    Actually: D5 = BR2, D1 = BR1
   │   ├── Bundle 3 (25mm): D3+D4 (T1 geyser+lights), D7+D8 (T2 geyser+lights)
   │   ├── Bundle 4 (25mm): D9 + D10 (FF corridor + balconies)
   │   ├── Bundle 5 (25mm): E4 (BR1 AC), E5 (BR2 AC)
   │   └── LV Bundle (25mm): Cat6 × 2 (BR1 study, BR2 study)
```

**Rule:** Never put more than 3 circuit wires in one 25mm conduit. Each bundle above = one conduit.

#### FF Bedroom 2 (West — false ceiling confirmed)
| Circuit | Route from staircase wall | Socket/light position |
|---|---|---|
| D5 — BR2 lights | Vertical → across FF ceiling → ceiling box centred | Ceiling, room centre |
| D11 — BR2 cove | Branch to cove LED driver in false ceiling | Perimeter of false ceiling |
| D6 — BR2 sockets | Vertical → horizontal at 600mm FFL | Bedside boxes L+R; study box |
| E5 — BR2 AC | Vertical → horizontal at 1850mm → AC socket S or E wall | 1850mm FFL |
| BR2 geyser switch | On outside face of toilet door, right side, 1200mm FFL | |
| D8 — T2 geyser | Vertical → through FF slab/wall → geyser box 1850mm FFL in toilet | |

#### FF Bedroom 1 (East side — no false ceiling)
| Circuit | Route | Position |
|---|---|---|
| D1 — BR1 lights | Vertical → across FF ceiling → ceiling box centred | Ceiling centre |
| D2 — BR1 sockets | Vertical → horizontal at 600mm FFL | Bedside L+R; study |
| E4 — BR1 AC | Vertical → 1850mm FFL | AC socket |
| D3+D4 — T1 lights+geyser | As above pattern | |

---

## PART 3 — LIGHTING EXACT POSITIONS

> All positions given as (distance from Wall-A × distance from Wall-B) measured from **inside face of finished wall**. Ceiling heights: GF = 11ft (3353mm), FF = 10ft (3048mm). False ceiling drops to: Living/Dining/Foyer ~9ft (2743mm) · Bedrooms ~9ft (2743mm).

---

### Foyer (6ft × ~4ft9" space, false ceiling @ 9ft)

| Fitting | Type | Distance from W wall | Distance from N/S | Height (FFL) | Angle | Circuit |
|---|---|---|---|---|---|---|
| Spotlight L | Recessed GU10, 7W, 2700K | **300mm** from W wall | **609mm** from N wall | False ceiling (2743mm) | 30° toward W wall | B1 |
| Spotlight R | Recessed GU10, 7W, 2700K | **300mm** from W wall | **1218mm** from N wall | False ceiling (2743mm) | 30° toward W wall | B1 |
| Cove LED strip | 24V warm white, 9.6W/m | Perimeter of false ceiling cove | — | Inside cove reveal | — | B10 |
| Shelf LED strip | 24V warm white, 6W/m | Under walnut shelf | Full 1828mm width | 900mm (shelf soffit) | Downward | B1 |
| Screen halo LED | 24V warm amber, 4.8W/m | Inside screen cavity reveal | Around perimeter | Cavity edge | Outward | B2 |

**Spotlight aiming note:** Mount the GU10 fittings with **adjustable gimbal ring** so the beam can be angled 30° toward the stone wall after installation. Standard fixed downlights will not achieve the stone-grazing effect.

---

### Living Area (16'11" × ~16'11", false ceiling @ 9ft)

Living area has two zones: **solid slab zone** (left/west) and **double-height void zone** (right/east).

| Fitting | Type | From W wall | From N wall | Height | Notes |
|---|---|---|---|---|---|
| Main light 1 | Recessed COB, 12W, 2700K | 1200mm | 900mm | False ceiling (2743mm) | In solid zone |
| Main light 2 | Recessed COB, 12W, 2700K | 1200mm | 2700mm | False ceiling (2743mm) | In solid zone |
| Main light 3 | Recessed COB, 12W, 2700K | 2400mm | 900mm | False ceiling (2743mm) | Near void edge |
| Main light 4 | Recessed COB, 12W, 2700K | 2400mm | 2700mm | False ceiling (2743mm) | Near void edge |
| Chandelier | Pendant, drop to ~2400mm | Centred over void | Centred over void | Drop from FF beam | ⚠️ Confirm void size & beam position |
| TV wall wash | 2× recessed GU10 | 300mm from W wall | 900mm + 2700mm | False ceiling | Angled toward TV wall |
| Cove LED | 24V warm white | Perimeter cove | — | Inside cove | Full perimeter |

---

### Dining Area (false ceiling @ 9ft)

| Fitting | Type | Position | Height | Notes |
|---|---|---|---|---|
| Pendant | 1× decorative pendant, warm 2700K | Centred over dining table position | Drop to 2100mm from FFL | Table centre — confirm table size first |
| Downlight 1 | Recessed COB, 9W | 800mm from N wall, 600mm from E wall | False ceiling | Supplement pendant |
| Downlight 2 | Recessed COB, 9W | 800mm from N wall, 600mm from W wall | False ceiling | |
| Cove LED | 24V warm | Perimeter cove | Inside cove | |

---

### Kitchen (~10ft deep, no false ceiling)

| Fitting | Type | Position | Height | Notes |
|---|---|---|---|---|
| Main ceiling light | LED panel 24W, 4000K (cool white) | Ceiling centre (5ft × kitchen width centre) | 3353mm (GF ceiling) | Cool/neutral white for task area |
| Under-cabinet LED | 24V warm white strip, 9.6W/m | Underside of wall cabinets | Cabinet soffit (~1700mm) | Full length of counter |
| Hob area downlight | Recessed 9W (optional) | Directly above hob, 400mm from N wall | Ceiling | Only if chimney has no built-in light |

---

### Master Bedroom (11ft ceiling, no false ceiling)

| Fitting | Type | From door wall | From window wall | Height | Notes |
|---|---|---|---|---|---|
| Main ceiling light | Recessed COB 12W, 2700K | Centred in room | Centred in room | 3353mm | |
| Bedside light L | Recessed adjustable GU10, 5W | 600mm from L side of bed headboard | 400mm from headboard wall | 3353mm, angled down | Aimed at pillow zone |
| Bedside light R | Recessed adjustable GU10, 5W | 600mm from R side of bed headboard | 400mm from headboard wall | 3353mm, angled down | Aimed at pillow zone |
| Wardrobe strip | 24V LED strip | Inside wardrobe (N wall + W wall) | — | Wardrobe top rail | Door-activated sensor |

**Bed position assumption:** headboard against N wall (below wardrobes). Confirm with furniture layout before fixing ceiling box positions.

---

### GF Common Bathroom (9ft × 4ft6", ceiling ~3353mm)

| Fitting | Type | Position | Height | Notes |
|---|---|---|---|---|
| Ceiling light | IP44 recessed LED 9W, 4000K | Centred ceiling | 3353mm | |
| Mirror/vanity light | IP44 LED bar 12W, 4000K | 150mm above mirror top, centred over sink | ~1900mm | |
| Exhaust fan | 4" IP44 | Above shower area, corner | ~2400mm | Not centred — near shower to capture steam |

---

### Bedroom 2 — FF (West, false ceiling @ 9ft, 10ft overall ceiling)

| Fitting | Type | Position | Height | Notes |
|---|---|---|---|---|
| Main ceiling light | Recessed COB 12W, 2700K | Centred in room | False ceiling (2743mm) | |
| Bedside light L | Recessed adjustable GU10 5W | 600mm from L bed edge | False ceiling, angled | |
| Bedside light R | Recessed adjustable GU10 5W | 600mm from R bed edge | False ceiling, angled | |
| Study spotlight | Recessed GU10 7W, 3000K | 400mm from study-table wall, above table | False ceiling | Position after study table location is fixed |
| Cove LED | 24V warm white | Perimeter of false ceiling | Inside cove | Full perimeter |
| Wardrobe strip | 24V LED | Inside W-wall wardrobe (3ft deep) | Top rail | |

---

### Bedroom 1 — FF (East, no false ceiling, 10ft ceiling)

| Fitting | Type | Position | Height | Notes |
|---|---|---|---|---|
| Main ceiling light | Recessed COB 12W, 2700K | Centred | 3048mm | |
| Bedside light L | Recessed adjustable GU10 5W | 600mm from L bed edge | 3048mm | |
| Bedside light R | Recessed adjustable GU10 5W | 600mm from R bed edge | 3048mm | |
| Study spotlight | Recessed GU10 7W, 3000K | Above study area | 3048mm | |
| Wardrobe strip | 24V LED | Inside wardrobe | Top rail | |

---

### Toilets (Bedroom 1 + Bedroom 2, 8ft × 5ft each)

| Fitting | Type | Position | Height | Notes |
|---|---|---|---|---|
| Main ceiling light | IP44 LED 9W, 4000K | Centred ceiling | 3048mm | |
| Mirror/vanity light | IP44 LED bar 12W | 150mm above mirror, centred sink | ~1900mm | |
| Exhaust fan | 4" IP44 | Shower zone corner | ~2200mm | |

---

### Staircase

| Fitting | Type | Position | Height | Notes |
|---|---|---|---|---|
| Step lights | LED step nosing, 3W each | Each step riser, left side | Step level | 12–15 steps in GF flight; 8–10 in FF flight |
| Wall light (mid-flight) | Recessed wall light, 5W | Mid-flight W wall | ~1500mm (mid wall) | Backup general light |
| Top landing light | Recessed 9W | FF landing ceiling | 3048mm | On same 2-way switch |

---

## PART 4 — SWITCH BOARD EXACT POSITIONS

| Location | Height (centre of plate) | Horizontal offset from nearest corner |
|---|---|---|
| All indoor switch boards | **1200mm from FFL** | Min 150mm from any corner or door frame |
| Geyser switches (all) | **1050mm from FFL** | Directly below PIR switch or alongside |
| PIR bathroom switches | **1200mm from FFL** | Outside bathroom door, handle side |
| Foyer DB panel | Bottom edge at **1500mm from FFL** | Behind door swing — min 100mm from door frame |
| Outdoor / balcony switches | **1200mm from FFL** | Inside of door before going out |
| AC socket | **1850mm from FFL** | On wall closest to outdoor unit (check AC manual) |
| Kitchen socket (counter) | **1100mm from FFL** | Above counter level |
| Socket (standard) | **300mm from FFL** | Min 150mm from corners |
| Bedside socket | **600mm from FFL** | Within 300mm of bedside table position |

---

## PART 5 — CAVITY FINISH CHECKLIST (for mason / civil team)

Before plastering, verify each cavity is:

- [ ] Screen cavity: 540W × 340H × 100D mm, bottom at 1280mm FFL, centred on foyer wall
- [ ] 2× 25mm conduit stubs visible inside cavity bottom-left corner (power + data)
- [ ] Inside cavity painted **matte black** before stone cladding is done
- [ ] VESA backing board (12mm ply, 600×400mm) fixed to cavity back wall, centred, with rawl plugs for VESA bracket
- [ ] DB recess: 400W × 600H × 100D mm at 1500mm FFL, W wall foyer, behind door swing
- [ ] All conduit entry/exit points in walls are sleeved and labelled before plastering
- [ ] Staircase niche: shelving or back panel fixed, all conduit stubs labelled
