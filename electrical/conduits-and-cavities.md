# Conduits, Cavities & Lighting — Exact Specifications

> This file is the **field reference** — hand it to your civil contractor and electrician before any chasing or cavity cutting starts. Every dimension is in **mm** (with inches in brackets). Heights are measured from **finished floor level (FFL)**.
>
> Cross-reference: [floor-plans-decoded.md](../floor-plans/floor-plans-decoded.md) for room dimensions · [db-layout.md](db-layout.md) for circuit IDs.

---

## PART 0 — ELECTRICIAN ONE-PAGE CHEAT SHEET

> **Read this first. If you only read one section of this document, read this.** Everything below is detail and exception cases.

### 0.1 The Five Rules That Apply Everywhere

| # | Rule | Why |
|---|---|---|
| 1 | **Every switch board gets a NEUTRAL wire** — no exceptions | Smart relay modules (Sonoff/Aqara) need neutral. Without it the smart switch goes dead. |
| 2 | **All switch boxes are 65mm deep minimum** (Indian standard is 50mm — too shallow) | Sonoff/Aqara relay module sits behind the switch plate. 50mm is too tight; 65mm gives wire-bending room. |
| 3 | **All switch boards at 1200mm FFL** (centre of plate); geyser switches 1050mm; sockets 300mm; bedside 600mm; counter sockets 1100mm; AC 1850mm | Standard Indian heights — used everywhere in this house. |
| 4 | **Earth wire (green/yellow) reaches every switch, socket, AND every metal fitting** | Life safety. Test continuity before plastering. |
| 5 | **No power and low-voltage cables in the same conduit, ever** | Cat6 picks up interference from 230V. Always separate conduits. |

### 0.2 Conduit Colour Code (Use Coloured PVC Where Possible)

| Conduit colour | Size | Carries | Found at |
|---|---|---|---|
| 🔴 **RED** | 25mm PVC | Lighting circuit power (1.5mm² wire) | Ceiling runs to lights, switch board feeds |
| 🔵 **BLUE** | 25mm PVC | Heavy-load power (sockets, AC, geyser, hob — 2.5mm² and 4mm²) | Wall chases at 300mm and 1850mm |
| ⚫ **GREY** | 25mm PVC | Cat6 / network / camera data — LV-25 | Staircase niche to all data points |
| ⚫ **GREY** | 16mm PVC | Speaker / sensor / 2-core LV — LV-16 | Doorbell, niche LED drivers, contact sensors |

> **If colour-coded conduit is not available locally**, label conduit ends with paint marker or insulation tape **before** plastering covers them. The colour code stays on paper. **DO NOT** rely on memory.

### 0.3 Wire Colour Code (Indian Standard — Mandatory)

| Wire colour | Function |
|---|---|
| 🔴 RED | LIVE (Phase) — 230V hot |
| ⚫ BLACK | NEUTRAL — return |
| 🟡 GREEN/YELLOW | EARTH — green-with-yellow stripe |
| 🟦 BLUE | LIVE (switch leg / "loop wire") — between switch and load |

> Rule: a **black** wire with current is always a NEUTRAL. A **blue** wire is a switched-live leg. Never confuse them.

### 0.4 Switch Box Cavity Depth — THIS IS NEW (Sonoff Compatibility)

```
            STANDARD SWITCH BOX               SONOFF-READY SWITCH BOX
            (DO NOT USE)                      (USE THIS EVERYWHERE)
            ┌──────────────┐                  ┌────────────────┐
            │              │                  │                │
            │   50mm deep  │                  │   65mm deep    │
            │              │                  │                │
            │   ✗ too      │                  │   ✓ Sonoff R2  │
            │   shallow    │                  │     fits + wire│
            │   for relay  │                  │     bending    │
            └──────────────┘                  │     headroom   │
                                              └────────────────┘
```

| Switch type | Box depth | Box size (mm) | Where used |
|---|---|---|---|
| **Smart switch + Sonoff relay (hidden)** | **65mm** GI MS | 75 × 75 × 65 (1-gang) · 130 × 75 × 65 (2-gang) · 175 × 75 × 65 (3-gang) · 230 × 75 × 65 (4-gang) | Living, Bedrooms, Foyer, Dining, Pooja, FF Living, Balconies, Staircase |
| **Dumb switch (no relay)** | 50mm GI MS | Standard 75 × 75 × 50 | Kitchen, Utility, Store room |
| **PIR switch** | 50mm GI MS | Standard | Outside all 3 bathrooms |
| **Geyser switch (20A DP)** | 50mm GI MS | 1-module | Outside each bathroom, 1050mm FFL |
| **Sockets (5A / 16A)** | 50mm GI MS | Standard 2-module / 3-module | All sockets |
| **AC socket (20A)** | 50mm GI MS | Standard 3-module | 1850mm FFL |

> **Sonoff/Aqara module dimensions (for reference):**
> - Sonoff ZBMINI R2 (Zigbee): 39.5 × 39.5 × 18.4 mm
> - Sonoff MINIR4 (Wi-Fi backup option): 39.5 × 39.5 × 20 mm
> - Aqara Relay T1 (no neutral): 42 × 42 × 22 mm
> - Module sits in the back of the box; switch plate seals the front. **65mm depth = module + neutral block + bent earth wire + switch terminals all fit comfortably.**

### 0.5 Universal Switch-Board Wiring Diagram (apply at every smart switch)

```
                        BOX (75 × 75 × 65 mm GI)
                       ┌──────────────────────┐
   FROM CEILING ───────│  L  N  E             │  ← 3 wires arrive (Live, Neutral, Earth)
   (light wire down)   │   ↓                  │
                       │  ┌──────────────┐    │
                       │  │  SONOFF R2   │    │  ← Sonoff sits at the back, wired to:
                       │  │  Zigbee Relay│    │     L IN  : Live from ceiling
                       │  │              │    │     N IN  : Neutral from ceiling
                       │  └──┬──────┬────┘    │     L OUT : to physical switch terminal
                       │     │      │         │     S1/S2 : physical switch (push-button or rocker)
                       │  ┌──┴──┐   │         │
                       │  │SWITCH│  │         │
                       │  │ rocker│ │         │
                       │  └──────┘  │         │
                       │           ─┴─        │
                       │           LOAD →     │  ← Wire returns to ceiling light
                       └──────────────────────┘
                              ↓
                        FRONT PLATE
                        (modular cover)
```

> **For the electrician:** at every smart-switch location, leave a **300mm tail** of L/N/E wires inside the box. The Sonoff module is inserted later by the homeowner — you do not need to install it. Just pull the wires, label them, and cap them.

### 0.6 What goes where — quick lookup

| Need | Conduit | Wire | Box Depth | MCB |
|---|---|---|---|---|
| Smart light point | 25mm RED | 1.5mm² 3-core | 65mm | 6A |
| Smart switch (with Sonoff) | 25mm RED | 1.5mm² + neutral | **65mm** | 6A |
| Dumb light point | 25mm RED | 1.5mm² 3-core | 50mm | 6A |
| 5A socket | 25mm BLUE | 2.5mm² 3-core | 50mm | 16A |
| 16A socket | 25mm BLUE | 2.5mm² 3-core | 50mm | 16A |
| AC point (20A) | 25mm BLUE | 4mm² 3-core | 50mm | 20A RCBO |
| Geyser (20A) | 25mm BLUE | 2.5mm² 3-core | 50mm | 20A RCBO |
| Hob 25A | 25mm BLUE | 4mm² 3-core | direct hardwire | 25A |
| Cat6 / network | 25mm GREY | Cat6 UTP | 50mm wall plate box | — |
| Camera (PoE) | 25mm GREY | Cat6 UTP | weatherproof IP67 | — |
| Speaker / doorbell LV | 16mm GREY | 2-core 0.75mm² | 50mm | — |
| LED strip 24V DC | 16mm GREY | 2-core 0.75mm² | driver-side only | — |
| Water automation — sensor (PoE) | 20mm GREY | Cat6 outdoor LSZH | JB 200×200×100 IP65 | — |
| Water automation — float (220V) | 16mm GREY | 2-core 1.5mm² double-insulated | DB cupboard terminal block | series with motor coil |
| Motor power (P1 / P2 to outside) | 25mm BLUE | 4mm²/2.5mm² armoured/PVC | DB cupboard | 16A Type C |

### 0.7 Water Automation — see dedicated schedule

> **Water automation conduits are listed separately in [water-automation-conduits.md](water-automation-conduits.md).** That doc has the full 7-conduit schedule (sensors to terrace Sintex and outside sump, motor power, float failsafes), JB specs, DB cupboard requirements, and electrician acceptance checklist. Both starters (P1 borewell, P2 booster) live INSIDE the home in a lockable cupboard adjacent to the DB — no outdoor starter enclosures.

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
| P-25 | 25mm PVC | 🔴 Red | Power — lighting circuits (1.5mm²) |
| P-25H | 25mm PVC | 🔵 Blue | Power — heavy (sockets, ACs, geysers — 2.5mm² / 4mm²) |
| LV-25 | 25mm PVC | ⚫ Grey | Low voltage — Cat6 / network / camera data |
| LV-16 | 16mm PVC | ⚫ Grey | Low voltage — speaker, sensor, doorbell, contact, LED 24V DC |
| LV-25-AP | 25mm PVC | ⚫ Grey | **NEW** — Cat6 to Wi-Fi access points (router runs to FF + GF AP positions) |

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

#### Staircase Niche to Entrance Face Detection / Doorbell (Low Voltage)
| Item | Value |
|---|---|
| Primary face-capture camera | LV-25 · staircase/server niche → outside main-door latch-side wall/jamb; pull 1× Cat6 + draw wire |
| Primary camera termination | Weatherproof 4×4" back box at **1600–1700mm FFL**, 150–250mm from latch-side door frame, protected under porch/eave |
| Primary camera aim | Aim at a capture line **1000–1800mm outside the threshold**; keep vertical tilt within ~15–20° and horizontal angle within ~30° |
| Porch overview camera | LV-25 · staircase/server niche → porch ceiling/soffit corner; pull 1× Cat6 + draw wire |
| Porch overview termination | Weatherproof camera box at **2400–2700mm FFL**; wide 2.8mm lens is OK here because this camera is for context, not face ID |
| Video doorbell/intercom | LV-16 · staircase/server niche/low-voltage PSU → latch-side doorbell box; pull 1× Cat6 + 2-core bell/12V cable |
| Doorbell termination | Modular/doorbell box at **1400–1450mm FFL**, 150–200mm from latch-side frame |
| Door contact sensor | LV-16 · staircase/server niche → top of main-door frame; pull 2-core sensor cable |
| Screen-bezel camera (CAM-0) | LV-16 sleeve · screen cavity back wall → top-centre of screen bezel; **Raspberry Pi Camera Module 3 via CSI ribbon cable** — no PoE, powered by RPi Zero 2W; streams RTSP over existing Cat6 in cavity |
| Screen camera height | **1600–1650mm FFL** lens height, facing into foyer; secondary face verification when person stands at welcome screen |

> **Face recognition rule:** do not rely on the high porch CCTV camera for identity. It will see the top of heads. The face-recognition camera must be close to face level and view people front-on as they approach or pause at the door.

#### Additional CCTV Camera Conduit Stubs (CAM-3, CAM-4, CAM-5)

> These three stubs must be chased and terminated **before plastering closes the walls**. All run LV-25 (25mm PVC grey), pull 1× Cat6 + draw wire each. All terminate in a weatherproof IP67 outdoor camera back-box.

**CAM-3 — FF Front Balcony Bird's-Eye**
| Item | Value |
|---|---|
| Camera type | Hikvision ColorVu 4MP, 2.8mm, IP67, PoE |
| Purpose | Elevated overview of compound, gate, driveway, full N-side approach |
| Mount position | NW corner of front balcony (11'9" × 7') soffit/underside or parapet inner face |
| Mount height | ~200–300mm below balcony soffit (approx 5500mm from ground) |
| Conduit route | Staircase niche (GF) → vertical up staircase W wall (join existing FF conduit bundle) → at FF slab level branch horizontally along FF corridor ceiling (N direction) → into front balcony ceiling/soffit → terminate at NW corner weatherproof back-box |
| Conduit size | 25mm LV-PVC |
| Termination | Weatherproof back-box IP67, 4×4", fixed to balcony soffit or parapet inner face at NW corner |

**CAM-4 — East-Side Exterior (Kitchen / Utility Zone)**
| Item | Value |
|---|---|
| Camera type | Hikvision ColorVu 4MP, 2.8mm, IP67, PoE |
| Purpose | Covers E-side approach, kitchen windows, utility back area; critical if utility has external door |
| Mount position | E-wall exterior, at kitchen–utility junction (N corner of E wall) |
| Mount height | 2400–2600mm FFL |
| Conduit route | Staircase niche (GF) → horizontal ceiling-level run east (above kitchen/dining ceiling, 150mm below GF slab soffit) → exit through E wall at kitchen–utility zone → terminate at weatherproof back-box |
| Conduit size | 25mm LV-PVC |
| Termination | Weatherproof back-box IP67, E-wall exterior at NE kitchen–utility corner |
| ⚠️ Confirm | Does utility room have an external door to outside? If yes, this camera is mandatory; if E-side is fully enclosed compound, it becomes optional perimeter cover |

**CAM-5 — Terrace Staircase Exit**
| Item | Value |
|---|---|
| Camera type | Hikvision ColorVu 4MP, 2.8mm, IP67, PoE |
| Purpose | Monitors terrace access (prevents unauthorized entry); elevated neighbourhood overview |
| Mount position | Parapet wall beside FF→terrace staircase opening, facing the terrace |
| Mount height | ~2500mm from terrace floor level |
| Conduit route | Staircase niche (GF) → vertical up staircase W wall (with existing FF bundle) → continue up FF staircase wall to terrace level → exit near terrace door/opening → terminate at parapet wall back-box |
| Conduit size | 25mm LV-PVC (UV-resistant at terrace level — fully exposed) |
| Termination | Weatherproof back-box IP67, fully exposed to rain and UV; use UV-rated conduit for the last 500mm above roof line |

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

### 🆕 FF ROUTER / WI-FI ACCESS POINT — NEW CONDUIT RUNS

> **Why this is needed:** A single GF router (in staircase niche) cannot give reliable 5GHz / Wi-Fi 6 coverage to the FF bedrooms — the FF slab + walls attenuate the signal too much. Plan a **second access point on FF**, wired-backhauled via Cat6 from the staircase niche. This is best done with conduit *now*, before plastering closes the walls.

#### Run R-FF-1: Staircase Niche → FF Living Wall (Primary FF Router/AP)

| Item | Value |
|---|---|
| Conduit size | **25mm LV-25 (grey)** |
| Pull cables | **2× Cat6 UTP** (1 for router uplink to GF switch, 1 spare for future AP daisy-chain) + draw wire |
| Route | Staircase niche (GF) → vertical up the staircase W wall (join the existing FF conduit bundle) → at FF slab level **branch east** along the FF Living ceiling/wall → terminate on **FF Living wall, central position** between Bedroom 1 and Bedroom 2 doors |
| Termination | Modular wall plate box, 50mm depth — Cat6 keystone (×2) + 5A power socket beside it on a separate 16mm conduit (lighting circuit D9 feed) |
| Termination height | **2400mm FFL** (high mount — best for AP signal coverage; clear of furniture) |
| Power for AP | 5A socket on D9 circuit, located **300mm to the side of** the Cat6 plate, **same height (2400mm)** so PoE injector or AP power adapter sits clean. PoE-capable APs (Ubiquiti UniFi U6-Lite, TP-Link EAP610) need only Cat6 — no socket required. |
| Mount surface | Wall (NOT ceiling) — central FF Living wall, on the partition between BR1 and BR2 doors. Equidistant from both bedrooms gives the most balanced 5GHz coverage. |

#### Run R-FF-2: Staircase Niche → FF Bedroom 2 Wall (Secondary AP / Wired Drop)

| Item | Value |
|---|---|
| Conduit size | **25mm LV-25 (grey)** |
| Pull cables | **1× Cat6 UTP** + draw wire |
| Route | Staircase niche (GF) → vertical → at FF slab level branch west → into BR2 wall → terminate on N wall of BR2, near the wardrobe end |
| Termination | Cat6 keystone wall plate, 700mm FFL (study desk height) |
| Purpose | Wired internet drop for BR2 study desk, AND a fallback AP mount point if the central FF Living AP underperforms in BR2 corner |

#### Run R-FF-3: Staircase Niche → FF Bedroom 1 Wall (Mirror of R-FF-2)

| Item | Value |
|---|---|
| Conduit size | **25mm LV-25 (grey)** |
| Pull cables | **1× Cat6 UTP** + draw wire |
| Route | Staircase niche (GF) → vertical → at FF slab level branch east → into BR1 wall → terminate on study wall |
| Termination | Cat6 keystone wall plate, 700mm FFL |
| Purpose | Wired internet drop for BR1 study desk |

#### Run R-FF-4 (optional): FF Living AP → Front Balcony / W Balcony Outdoor AP

| Item | Value |
|---|---|
| Conduit size | 16mm LV-16 (grey) |
| Pull cables | 1× Cat6 UTP outdoor-rated (UV jacket) |
| Route | FF Living AP wall plate → through partition wall → onto front balcony soffit |
| Termination | Outdoor IP67 keystone box at balcony soffit corner |
| Purpose | **Future option:** outdoor mesh AP for terrace/balcony Wi-Fi if needed. Pull draw wire only now; install AP later. |

#### FF Router/AP Mount Box Detail

```
     FF LIVING WALL — central position between BR1 and BR2 doors
     (on the partition wall, equidistant from both bedrooms)

           ←──── 300mm ────→
        ┌─────────────┐  ┌─────────────┐
        │  Cat6 ×2    │  │   5A power  │  ← ROUTER/AP MOUNT ZONE
        │  keystone   │  │   socket    │      (height: 2400mm FFL)
        │  wall plate │  │             │
        │  (50mm box) │  │  (50mm box) │
        └─────────────┘  └─────────────┘
              ↑                  ↑
         LV-25 grey          16mm conduit
         from staircase      from D9 lighting/socket
         niche               circuit

        ROUTER/AP itself sits ON the wall here, wall-mounted,
        plugged into both Cat6 keystones (or Cat6 + PoE injector).
```

> **Cable count update — staircase niche to FF:** Previous bundle was 5 conduits + 1 LV. With these new runs the niche-to-FF total is now: 5× P-25/P-25H + **3× LV-25 (grey, dedicated to network/router) + 1× LV-16** (existing CAM-3, CAM-5 reuse the original LV-25). Add a **dedicated chase channel ~150mm wide** in the staircase wall to keep these bundles tidy.

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
| Primary face-capture camera | **1600–1700mm from FFL** | Outside main door, latch-side jamb/wall; face-level, front-on view |
| Video doorbell | **1400–1450mm from FFL** | Latch side of main door, 150–200mm from frame |
| Porch overview camera | **2400–2700mm from FFL** | Porch ceiling/soffit corner; context/security only, not face ID |
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
- [ ] LV-16 sleeve from screen cavity to top-centre screen camera point at 1600–1650mm FFL
- [ ] Inside cavity painted **matte black** before stone cladding is done
- [ ] VESA backing board (12mm ply, 600×400mm) fixed to cavity back wall, centred, with rawl plugs for VESA bracket
- [ ] DB recess: 400W × 600H × 100D mm at 1500mm FFL, W wall foyer, behind door swing
- [ ] **CAM-1** LV-25 stub: primary face-capture camera outside main door, latch-side, **1600–1700mm FFL** — Cat6 + draw wire, weatherproof 4×4" back-box
- [ ] **CAM-2** LV-25 stub: porch overview camera, porch ceiling/soffit corner, **2400–2700mm FFL** — Cat6 + draw wire, weatherproof back-box
- [ ] **CAM-3** LV-25 stub: FF front balcony NW corner soffit — route up staircase wall → FF corridor ceiling → balcony soffit — Cat6 + draw wire, IP67 back-box
- [ ] **CAM-4** LV-25 stub: E-wall exterior at kitchen–utility junction, **2400–2600mm FFL** — horizontal run through GF ceiling — Cat6 + draw wire, IP67 back-box
- [ ] **CAM-5** LV-25 stub: terrace level near staircase exit parapet, **~2500mm from terrace floor** — extend staircase vertical run to terrace — Cat6 + draw wire, IP67 UV-rated back-box
- [ ] LV-16 stub to doorbell/intercom point at 1400–1450mm FFL
- [ ] LV-16 stub to concealed main-door contact sensor at top of frame
- [ ] All conduit entry/exit points in walls are sleeved and labelled before plastering
- [ ] Staircase niche: shelving or back panel fixed, all conduit stubs labelled
- [ ] **🆕 R-FF-1** LV-25 stub: FF Living central wall (between BR1/BR2 doors) at **2400mm FFL** — pull 2× Cat6 + draw wire; 50mm wall plate box; 5A power socket 300mm beside on D9
- [ ] **🆕 R-FF-2** LV-25 stub: FF BR2 study wall, **700mm FFL** — pull 1× Cat6 + draw wire; 50mm wall plate box
- [ ] **🆕 R-FF-3** LV-25 stub: FF BR1 study wall, **700mm FFL** — pull 1× Cat6 + draw wire; 50mm wall plate box
- [ ] **🆕 R-FF-4** LV-16 stub (optional): FF Front Balcony soffit — pull 1× Cat6 outdoor + draw wire only; cap until needed
- [ ] **🆕 SONOFF-READY SWITCH BOXES** — every smart-switch location uses **65mm-deep GI MS box** (NOT 50mm). Verify before plastering: Foyer SB, Living SB×2, Dining SB, MBR SB, FF Living SB, BR1 SB, BR2 SB, Pooja SB, Staircase SB×2, Front balcony SB, W balcony SB, Foyer 2-way SB
- [ ] **🆕 NEUTRAL WIRE** present at every smart-switch box (visual inspection — black wire visible in tail bundle)
- [ ] **🆕 EARTH WIRE** present at every switch + socket box (green/yellow visible in tail bundle)
- [ ] **🆕 LABEL EVERY CABLE TAIL** with masking tape + permanent marker before plastering — circuit ID (e.g. "B1", "D9", "R-FF-1 Cat6")

### Water automation conduits (see [water-automation-conduits.md](water-automation-conduits.md) for full spec)

- [ ] **C-Sintex-1** — 20mm grey from server niche to Sintex JB on terrace SW parapet (~42 ft); through staircase shaft + embedded under terrace screed before tiling
- [ ] **C-Sintex-2** — 16mm parallel to C-Sintex-1, ≥50mm separation, terminating at DB cupboard for Sintex float (~45 ft)
- [ ] **C-Sump-1** — 20mm grey from server niche to Sump JB on east external wall above manhole (~25 ft); sleeved through east wall, slope outward
- [ ] **C-Sump-2** — 16mm parallel to C-Sump-1, ≥50mm separation, terminating at DB cupboard for sump float (~25 ft)
- [ ] **C-DB-Backup** — 20mm empty with pull string only, server niche to DB cupboard (~12 ft); both ends capped and labelled "WATER AUTOMATION — FUTURE Cat6"
- [ ] **C-Motor-P1** — 25mm blue from DB cupboard to borewell head outside; **confirm existing run can be repurposed**
- [ ] **C-Motor-P2** — 25mm blue from DB cupboard to P2 cage on east outside wall (~5 ft)
- [ ] **DB cupboard** built (lockable, ventilated, ≥600×400×250mm internal) adjacent to existing DB; houses both Magnum Pradhaan starters + Sonoff DUALR3 + float terminal blocks
- [ ] Pull string in EVERY water-automation conduit
- [ ] Both ends of each conduit labelled with conduit ID (C-Sintex-1, etc.) using paint marker on permanent tag
