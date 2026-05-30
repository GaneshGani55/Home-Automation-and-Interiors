# Conduits, Cavities & Lighting — Exact Specifications

> ⚠️ **FOYER section updates 2026-05-22:** the foyer welcome system has been revised — see [FOYER_MASTER_ELECTRICIAN_PLAN.md § revision summary at top](FOYER_MASTER_ELECTRICIAN_PLAN.md) for the authoritative v1.1 changes. Key foyer changes since this file was last fully edited: (1) cavity speaker → ceiling speaker (speaker pocket dropped, conduit #4 now carries 2-core speaker wire); (2) cavity socket → 8M box with Cat6 keystone (was 2-module); (3) Foyer Switch Panel → 18M vertical (was 6-gang); (4) smart-switch boxes → 50mm + 2 modules where feasible (foyer panel exception: 65mm + 2M-per-Sonoff per § 8.5); (5) doorbell → Hikvision DS-KV6113-WPE1(C) (was Reolink); (6) CAM-1 confirmed provision-only. **If anything below contradicts the master plan v1.1, the master plan wins.**
>
> This file is the **field reference** — hand it to your civil contractor and electrician before any chasing or cavity cutting starts. Every dimension is in **mm** (with inches in brackets). Heights are measured from **finished floor level (FFL)**.
>
> Cross-reference: [floor-plans-decoded.md](../floor-plans/floor-plans-decoded.md) for room dimensions · [db-layout.md](db-layout.md) for circuit IDs · [FOYER_MASTER_ELECTRICIAN_PLAN.md](FOYER_MASTER_ELECTRICIAN_PLAN.md) for foyer authoritative spec.

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

| Switch type | Box depth | Box sizing rule | Where used |
|---|---|---|---|
| **Smart switch + Sonoff ZBMINI R2 (hidden)** | **65mm** GI MS | **+2M per hidden Sonoff** — see § 0.4b below | Living, Bedrooms, Foyer, Dining, Pooja, FF Living, Balconies, Staircase |
| **Dumb switch (no relay)** | 50mm GI MS | Standard 75 × 75 × 50 | Kitchen, Utility, Store room |
| **PIR switch** | 50mm GI MS | Standard | Outside all 3 bathrooms |
| **Geyser switch (20A DP)** | 50mm GI MS | 1-module | Outside each bathroom, 1050mm FFL |
| **Sockets (5A / 16A)** | 50mm GI MS | Standard 2-module / 3-module | All sockets |
| **AC socket (20A)** | 50mm GI MS | Standard 3-module | 1850mm FFL |

> **Sonoff ZBMINI R2 dimensions:** 39.5 × 39.5 × 18.4 mm. Sits behind the rocker inside the box. **65 mm depth = module + neutral block + bent earth wire + switch terminals all fit comfortably.**

### 0.4b — Plate-size sizing rule for hidden-Sonoff boards (+2M per Sonoff)

> **This is the most important sizing rule on the project.** Apply at every smart-switch board.

Six Sonoffs + 6 sets of wires + a neutral bus + earth bonding = a lot of stuff inside one back box. Cramming them into a tight modular plate (where gang count = module count) causes:
- Wire-bend radius violations (insulation cuts on sharp bends)
- Plate can't sit flush (modules bulge against the back of the rocker)
- Neutral bus has no room → looping with twisted joints (unsafe)
- Electrician swears at you, blames "the smart stuff", takes 3× longer

**Rule:** `Plate size (modules) = (number of smart gangs) + (number of hidden Sonoffs × 2M slack)`. Round up to the nearest standard Schneider Unica plate (3M / 4M / 6M / 8M / 12M / 18M).

| Smart gangs | Recommended plate | Approx GI MS box (all 65 mm deep) | Notes |
|---|---|---|---|
| 1 | **3M** | 86 × 86 × 65 mm | 1 rocker + 2M slack |
| 2 | **6M** | 130 × 130 × 65 mm | 2 rockers + 4M slack |
| 3 | **8M** | 175 × 130 × 65 mm OR 225 × 86 × 65 mm | 3 rockers + 5M slack |
| 4 | **12M** | 225 × 130 × 65 mm | 4 rockers + 8M slack |
| 5 | **12M** | 225 × 130 × 65 mm | 5 rockers + 7M slack (tight; go 18M if box fits) |
| **6 (foyer)** | **18M** | **290 × 130 × 65 mm OR 225 × 195 × 65 mm (vertical)** | 6 rockers + 12M slack — **already cut at foyer** |

**For dumb switches**, the +2M rule does NOT apply — gang count = module count (e.g. 4-gang kitchen = 4M plate, 50 mm box).

### 0.4c — Smart-switch hardware: ALL Sonoff ZBMINI R2 hidden behind Schneider Unica plates

After comparing Sonoff vs Aqara H1 vs Schneider Wiser (decided 2026-05-23):

- **All smart gangs use Sonoff ZBMINI R2 (Zigbee)** hidden behind a Schneider Unica modular plate. Z2M pairing post-move-in.
- **Aqara H1 dropped from spec.** Requires non-Indian-modular 86×86 square cavity (vendor lock-in if Aqara dies). Latency / HA-down behaviour identical to Sonoff, so no functional benefit.
- **Schneider Wiser dropped from spec.** Cloud-dependent for many automations; weak HA integration; 5–10× cost; no gain over Sonoff for an HA-driven house.

> **Future Aqara upgrade**: if you ever want a glass-touch plate in 1–2 specific spots (e.g. master-bedroom bedside), cut a fresh 86 × 86 × 50 mm square cavity at that location — this is a post-move-in change. Don't prepare for it pre-plaster.

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

> ⚠️ **AUTHORITATIVE SOURCE: [FOYER_MASTER_ELECTRICIAN_PLAN.md](FOYER_MASTER_ELECTRICIAN_PLAN.md)** (and its PDF at `pdfs/FOYER_ELECTRICIAN_MASTER_PLAN.pdf`).
> This section is a summary — the master plan has full step-by-step procedures, vector diagrams, BOM, sign-off checklists. If anything in this section conflicts with the master plan, the **master plan wins**.

### Monitor: Samsung LS22F320GAWXXL (21.5" IPS, Essential S3) — REVISED 2026-05-26
Panel dimensions (without stand):
- Width: **489.9 mm (19.3")**
- Height: **291.9 mm (11.5")**
- Depth at thinnest (panel edge): **36.2 mm (1.4")** ← thinner than prior F350 (49 mm)
- Weight: **1.6 kg** (without stand)
- VESA hole pattern: **100 mm × 100 mm** ← changed from 75×75 on prior F350
- Refresh: 120 Hz · Dual HDMI · No built-in speakers · 3-yr Samsung India warranty

> The original locked spec named the LS22F350 and claimed "IPS"; Samsung's own datasheet says LS22F350 is **TN**, not IPS. The LS22F320GAW is the modern IPS replacement at lower price, lighter weight, thinner depth, more cavity clearance. See [decisions/decision-log.md](../decisions/decision-log.md) 2026-05-26.

### Cavity to Cut in Wall (REVISED 2026-05-19)

```
   Raw masonry cut (BEFORE stone reveal slips applied):
        ← 580mm (22-3/4") →
        ┌─────────────────┐  ─
        │                 │  │
        │   STONE WALL    │  │ 380mm
        │   CAVITY        │  │ (14-7/8")
        │                 │  │
        └─────────────────┘  ─
             ↑
         depth: 100mm (4")

   Inner usable opening AFTER stone reveal slips (20mm thick on
   all 4 inner walls, front 30mm of depth only):
                    540mm (21-1/4") wide × 340mm (13-1/2") tall
   (this matches monitor 491×291 + 25mm clearance — same as original design)
```

| Dimension | Value (raw cut) | Value (after stone reveal) | Why |
|---|---|---|---|
| Cavity width | **580mm (22-3/4")** raw cut | 540mm (21-1/4") inner usable | Stone slips 20mm thick on each side at front 30mm of depth |
| Cavity height | **380mm (14-7/8")** raw cut | 340mm (13-1/2") inner usable | Same — stone slips on top + bottom inner walls front 30mm |
| Cavity depth | **100mm (4")** | unchanged | Leaves 128mm (5") of solid masonry behind for structural safety |
| Stone reveal depth (front portion clad in stone) | — | **30mm (1-1/4")** | Stone wraps from wall face INTO cavity reveal — creates premium framed-picture effect; halo LED hides behind stone lip |
| Bottom of cavity from FFL | **1280mm (50-1/2")** | unchanged | Screen centre at 1450mm — comfortable eye level |
| Centre of cavity from FFL | **1450mm (57-1/8")** | unchanged | Ergonomic eye-level for standing adult |
| Top of cavity from FFL | **1620mm (63-7/8")** | unchanged | |
| Horizontal position | **Centred on the 6ft (1828mm) feature wall portion of S edge** (the East 6ft of the 9.5ft S edge; the West 3.5ft is open passage to Living/Pooja) | unchanged | Electrician must measure actual wall width on-site and centre on the real measurement |

### Sub-pockets cut INTO the cavity walls

Two small additional pockets are cut beyond the main cavity:

| # | Pocket | Wall | Dimensions | Depth INTO masonry | Position |
|---|---|---|---|---|---|
| 1 | **Socket pocket** | Cavity back wall (NOT right inner wall as previously logged) | 3" × 3" (75 × 75 mm) | 2-1/2" (65 mm) | Centred horizontally; centre at 53" (1346 mm) FFL — below monitor centre, fully hidden behind monitor body |
| 2 | **Speaker pocket** | Cavity back wall | 3" diameter (75 mm) circular | 1" (25 mm) | Centred horizontally; centre at 57-1/8" (1450 mm) FFL — recesses the Visaton FR 8 driver magnet |

Wall capacity check: 9" wall = 228 mm. Main cavity uses 100 mm; deepest sub-pocket (socket) uses an additional 65 mm → total depth used 165 mm; remaining solid masonry behind = 63 mm (2-1/2"). Safe.

### Stone cladding wrap into cavity (REVISED 2026-05-19)

Stone slips (20 mm thick) are applied to **all 4 inner walls** of the cavity (top, bottom, left, right) — but only for the **FRONT 30 mm of depth**. Beyond 30 mm depth into the cavity, inner walls are matte black (painter's domain). Back wall is matte black across full surface (no stone).

Visual effect: the wall's stone face continues seamlessly INTO the cavity for the first 30 mm, framing the recessed monitor like a stone picture frame.

### Inside the Cavity (REVISED — socket on BACK wall, not right inner wall)

```
  [Cavity back wall, viewed from foyer side, looking INTO cavity]
  ◄───────── 580mm raw cut (540mm inner after stone slips) ─────────►
  ┌──────────────────────────────────────────────────────────────────┐
  │              ● Halo conduit (top-centre, 16mm grey)              │
  │                                                                    │
  │                                                                    │
  │                        ╔═══════════════╗                          │
  │                        ║   VESA mount   ║  ← 75×75mm pattern,     │
  │                        ║   on back wall ║     centre at 1450mm FFL │
  │                        ╚═══════════════╝                          │
  │                                                                    │
  │                       ⊙ SPEAKER POCKET  ← 3" dia × 1" deep         │
  │                         centre 1450mm FFL                          │
  │                                                                    │
  │                       ┌──────────┐                                │
  │                       │  SOCKET  │  ← 3"×3"×2.5" pocket,           │
  │                       │  POCKET  │     centre at 53" (1346mm) FFL  │
  │                       └──────────┘                                │
  │                                                                    │
  │  ● Power (25mm RED              ● Data (25mm GREY                  │
  │    from DB-East)                  from niche via floor)            │
  │    bottom-LEFT                    bottom-RIGHT                     │
  └──────────────────────────────────────────────────────────────────┘
```

- **VESA mount:** slim **VESA 100** bracket (Speedio Universal Fixed or equivalent, 15 mm standoff, 15 kg capacity), direct rawl plugs into masonry back wall (no plywood backing needed unless carpenter prefers) — bracket centre at 1450 mm FFL, horizontally centred on back wall. _REVISED 2026-05-26 from VESA 75 to match new LS22F320GAW monitor SKU._
- **Paint inside cavity:** matte black on back wall + deeper 70mm of inner walls (NOT the front 30mm where stone goes)
- **Conduit entries — REVISED (DB moved East 2026-05-17):**
  - Bottom-LEFT corner of back wall = **POWER** (25mm RED, from DB on East wall)
  - Bottom-RIGHT corner of back wall = **DATA** (25mm GREY, Cat6 from staircase niche via FLOOR route)
  - Top-CENTRE of back wall = **HALO 24V** (16mm GREY, from halo driver above false ceiling)
  - PLUS the new 4th conduit: from TOP wall going UP into false ceiling (16mm GREY, **pull string only**, provision for future ceiling speaker)
- **Stone cladding:** WRAPS into front 30mm of inner walls (all 4 sides). Does NOT enter the back wall or the deeper 70mm of inner walls.

### Cable Routing Inside Cavity (REVISED — RPi PoE-powered)

| Cable | From | To | Length needed |
|---|---|---|---|
| Monitor power cable | 5A socket A (inside cavity, BACK wall) | Monitor power port | ~500mm |
| RPi power | **PoE splitter** (powered from Cat6 PoE) | RPi Zero 2W USB-C input | ~200mm |
| Mini-HDMI → HDMI | RPi HDMI port | Monitor HDMI input | ~300mm |
| Cat6 patch | PoE splitter RJ45 out | USB OTG Ethernet adapter on RPi | ~200mm |
| 3.5mm audio | USB sound card on RPi | PAM8403 amp input | ~300mm |
| Speaker wire (2-core) | PAM8403 amp output | Visaton FR 8 speaker terminals | ~300mm |
| CSI ribbon | RPi CSI port | Pi Camera Module 3 on top bezel of monitor | ~250mm (comes with camera) |

**Socket panel position — REVISED:** 2-module modular plate (2× 5A sockets: "Monitor" + "Spare") on the **cavity BACK wall**, centre at 53" (1346mm) FFL. NOT on right inner wall as previously logged. Sonoff Mini R2 sits inside the socket back box and switches only the Monitor socket; Spare socket is always-live. Monitor power cord runs invisibly in the rear gap behind monitor.

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

#### DB position — REVISED 2026-05-17

DB has moved from **West wall** to **East wall** of the foyer (behind door swing). All conduits originating from DB now start on the East wall side. The starter cupboard for water automation (P1 + P2 starters + Sonoff DUALR3) co-locates with DB on East wall. Final DB + cupboard layout (side-by-side vs stacked vertically) is chosen on-site by electrician + carpenter based on 549mm clearance south of door swing arc — see [FOYER_MASTER_ELECTRICIAN_PLAN.md § 6](FOYER_MASTER_ELECTRICIAN_PLAN.md).

#### Conduits originating FROM the DB (only 2 to feed the foyer)

| # | Conduit ID | Size | Route | Wires inside |
|---|---|---|---|---|
| 1 | **C-DB-Foyer-Switch** | 25mm RED | DB (E wall) → up E wall → false ceiling → across to N wall → drops to Foyer Switch Panel at 1200mm FFL | 1.5sqmm L + N + E (feed for all foyer + porch lighting via 6-gang switch panel) |
| 2 | **C-DB-Cavity-Power** | 25mm RED | DB (E wall) → horizontal in E wall at ~1300mm → SE corner → horizontal in S wall (behind stone) → cavity bottom-LEFT corner of back wall | 2.5sqmm L + N + E (direct 230V for cavity sockets; switched by Sonoff inside socket box, not at wall switch) |

#### Foyer Switch Panel (Circuit B-Foyer-Lights) — N wall

| Item | Value |
|---|---|
| Wall | **N wall, 1'6" (457mm) section** between corner window (W) and main door (E) — NOT West wall (foyer has no W wall) |
| Centre height | **1200mm (47-1/4") FFL** |
| Back box | **6-gang GI MS, 335 × 75 × 65mm** (default; electrician may upgrade to 7- or 8-gang if it fits cleanly) |
| Gang 1 | Foyer ceiling GU10 spotlights (no driver needed; GU10 runs on 230V mains direct) |
| Gang 2 | Cove LED 2700K + cavity Halo LED 2200K (linked via Sonoff) |
| Gang 3 | Walnut shelf under-LED (24V via shelf driver) |
| Gang 4 | Foyer spare (capped) |
| Gang 5 | **Porch ceiling light** (NEW) |
| Gang 6 | **Porch wall light** (future provision, capped) |
| Sonoff | Sonoff ZBMINI L2 hidden behind plate; remote control via HA |

#### Conduits FROM Switch Panel to loads (branches from B-Foyer-Lights)

| Conduit | Size | Route | Carries |
|---|---|---|---|
| C-SW-Spots | 25mm RED | Up N wall → false ceiling → 2× spotlight boxes | Switched Live from Gang 1 + N + E |
| C-SW-Cove-Halo | 25mm RED | Up N wall → false ceiling → cove driver + halo driver | Switched Live from Gang 2 + N + E |
| C-SW-Shelf | 16mm RED | Down N wall → floor route → up S wall to shelf area | Switched Live from Gang 3 + N + E |
| C-SW-Spare-4 | 16mm RED | Up N wall → false ceiling (capped) | Pull string only |
| C-SW-Porch-Ceiling | 16mm RED | Up N wall → through N wall → outside porch ceiling | Switched Live from Gang 5 + N + E |
| C-SW-Porch-Wall | 16mm RED | Up N wall → through N wall → outside near door (capped) | Pull string only (future) |

Spotlight box positions: 300mm from W wall area, 609mm from N edge (#1) + 1218mm from N edge (#2). Ceiling box B-type, 60mm depth.

#### Foyer Screen (Circuit B-Foyer-Cavity) — 4 conduits at the cavity

| # | Conduit | Size | Colour | Entry/exit point | From / To |
|---|---|---|---|---|---|
| 1 | POWER | 25mm | RED | Bottom-LEFT corner of cavity back wall (1.5" up + 2" in from edges) | From DB on E wall (C-DB-Cavity-Power) |
| 2 | DATA | 25mm | GREY | Bottom-RIGHT corner of cavity back wall (1.5" up + 2" in) | From staircase niche **via FLOOR route** under floor screed (C-Niche-Cavity-Data, ~12m) |
| 3 | HALO 24V | 16mm | GREY | Top-CENTRE of cavity back wall (3/4" down from top inner edge) | From halo driver above false ceiling |
| 4 | Ceiling speaker (PROVISION) | 16mm | GREY | TOP inner wall, exits UP into false ceiling | Pull string only — future ceiling speaker if music playback desired |

#### Staircase Niche to Entrance — REVISED (Hikvision doorbell replaces CAM-1 install)

| Item | Value |
|---|---|
| Primary face capture (REVISED) | **Hikvision DS-KV6113-WPE1(C) Video Doorbell PoE** mounted on OUTSIDE face of N wall 1'6" section, 1450mm FFL. Doubles as doorbell + face detection. Conduit: **C-Niche-Doorbell** 25mm GREY, **floor route preferred** (single chase shared with cavity Cat6 + CAM-1 spare). Cable: 1× outdoor LSZH UV Cat6 (PoE). Back box: 3"×3"×2-1/2" GI MS modular recessed flush on outside, smaller than the doorbell bracket so it stays hidden behind the doorbell after install. |
| CAM-1 dedicated face camera (PROVISION ONLY) | **DROPPED from base install** — conduit + capped IP67 back box provisioned on porch W wall at 1650mm FFL for future Hikvision install. Pull string only, no cable. Conduit: **C-Niche-CAM1** 25mm GREY via floor route. |
| Porch overview camera CAM-2 (PROVISION ONLY) | Conduit + capped IP67 back box at porch soffit NE corner ~2700mm FFL. Pull string only. Conduit: **C-Niche-CAM2** 25mm GREY via false ceiling route (only viable path — soffit can't be reached via floor). |
| Video doorbell/intercom | **Merged with the Hikvision doorbell above** — the Hikvision DS-KV6113-WPE1(C) is the doorbell + camera + intercom (built-in mic + speaker for 2-way audio). No separate doorbell wiring. Chime is via the Hik-Connect app push, HA playing a tone on any networked speaker, or a paired Hikvision DS-KH-series indoor station (separate purchase); unlike the Reolink it had before, there is no cheap plug-in wireless chime accessory. |
| Door contact sensor | Future provision (no current conduit; the Hikvision doorbell handles "someone at door" detection). |
| Screen-bezel camera (CAM-0) | **Raspberry Pi Camera Module 3** mounted on top-centre of monitor bezel; CSI ribbon to RPi (no conduit needed — entirely inside cavity). Used as secondary close-range face check at the welcome screen. |
| Waveshare staircase panel (Screen 1, LOCKED 2026-05-25 v2.0; cavity dims corrected 2026-05-29 v3.1) | Conduit **C-Niche-Waveshare** 25mm GREY, ~2m, from niche short vertical run to staircase South wall at 1500mm FFL. **Terminates at a custom 280 × 195 × 80 mm masonry cavity** (NOT a standard modular back box — earlier v2.0 spec called for a 75×75mm box which was wrong; corrected v3.1). Cavity vertically aligned above existing 2M staircase light-switch box (~200 mm clear gap). 9" wall = 150 mm structural margin behind cavity. **Conduit carries:** (a) 1× slim HDMI 2.0 cable (3m, from Beelink HDMI 2 → screen) + (b) 1× USB-A to micro-USB cable (3m, touch + 5V power from Beelink USB-A) + (c) existing Cat6 (kept as SPARE for future Pi migration option). Architecture: Beelink-direct (no Pi at panel). Screen: Waveshare 10.1" HDMI LCD (B) with case, 1280×800 (locked v3.1). See [WAVESHARE_INDOOR_PANEL.md](WAVESHARE_INDOOR_PANEL.md). |
| Waveshare dining panel (Screen 2, PROVISION 2026-05-25 v3.0) | **NEW** conduit **C-Niche-Dining** 25mm GREY, **~12m / 35-40 ft** (per electrician walk-through), from niche → vertical up niche wall → long horizontal east through GF slab ceiling chase across kitchen/dining → drop down into dining hall E wall (**near breakfast counter / kitchen-dining partition**) → terminate at back box. Cable: **1× indoor Cat6** + 1× pull-string. Back box: 3"×3"×2½" GI MS modular, **height + exact position defer to interior designer** (screen will mount on plywood under cantilever kitchen shelves). Architecture (refined 2026-05-25): **Pi-at-screen, wired** — matching foyer welcome system pattern. Pi (Zero 2W or 4) behind the screen gets PoE power + Ethernet data over the single Cat6, renders HA dashboard locally, drives Waveshare via short HDMI cable. |
| Dining hall ceiling speaker (PROVISION 2026-05-29, refined to foyer-pattern Option B same day) | **NEW** conduit **C-Niche-DiningSpeaker** **25mm GREY PVC (LV-25, data conduit family)**, ~10m, from staircase niche → up niche wall → horizontal east across GF slab ceiling chase → terminate at a capped ceiling junction box centered above the future dining table position. Cable: **1× indoor Cat6** (PoE-capable, can power a future Pi at the ceiling) + 1× pull-string. **Mono architecture, foyer-pattern** (Pi + PAM8403 amp + 3" flush-mount commercial ceiling speaker — same as the current foyer audio chain locked 2026-05-22 when cavity speaker was dropped in favour of ceiling speaker — ~₹4-6K future spend, vs ~₹22K premium WiiM/Polk path I'd originally specced). Exact ceiling position defer to interior designer. **At install time, choose:** (a) shared dining-screen Pi drives BOTH screen + speaker (Cat6 in this conduit stays as spare; audio runs through false ceiling void from screen Pi to ceiling speaker, ~2-3m) — saves ~₹2K vs dedicated Pi; OR (b) dedicated Pi Zero 2W at ceiling powered by PoE on this conduit's Cat6 — independent of screen Pi, cleaner failure isolation. |

> **Face recognition rule (UPDATED 2026-05-20):** primary face detection is now via the **Hikvision doorbell** (at the door, face level). This is a "reactive welcome" (screen lights up at door) instead of "anticipatory welcome" (screen lights up at approach). The CAM-1 conduit + back box remain provisioned on porch W wall for a future face camera if recognition reliability becomes a concern.

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
| C1 (lights) | 25mm · DB → W wall → ceiling → bedroom ceiling box (centred) + E-wall bedside light boxes + wardrobe-strip driver |
| C2 (sockets) | 25mm · DB → horizontal chase at 600mm FFL to E-wall bedside socket boxes + W/N utility sockets |
| E3 (AC) | 25mm · DB → vertical / ceiling route → AC socket at 1850mm FFL on N wall above door/nook |

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

> **Why this is needed:** A single GF router (in staircase niche) cannot give reliable 5GHz / Wi-Fi 6 coverage to the FF bedrooms — the FF slab + walls attenuate the signal too much. Plan a **second access point on FF**, wired-backhauled via Cat6 from the staircase niche. **Updated 2026-05-29:** A THIRD AP is also added on the **GF false ceiling** (above dining/living junction) because the niche router alone has limited coverage in the dining area — the staircase wall + intermediate walls attenuate enough to make it worth a dedicated ceiling AP. NEW conduit `R-GF-1` covers this (see below).

#### Run R-GF-1: Staircase Niche → GF False Ceiling (NEW GF Ceiling AP — LOCKED 2026-05-29)

| Property | Value |
|---|---|
| Route | Staircase niche → vertical up niche wall → at GF slab level branch east → across GF false ceiling void → terminate at junction box centered in the false ceiling above the open dining/living junction zone |
| Conduit | 25mm GREY PVC (LV-25, data conduit family) |
| Length | ~6-8m (verify on-site) |
| Cables | 1× indoor Cat6 + 1× pull-string for future spare |
| Termination | Capped ceiling junction box flush with false ceiling at central GF dining/living position |
| Power | PoE only — no separate socket needed (AP draws ~12W via PoE on Cat6 from niche TL-SG1210P) |
| AP model | "Ubiquiti UniFi U6-Lite or equivalent" (homeowner placeholder lock 2026-05-29; alternatives: TP-Link EAP670, Aruba Instant On AP22) |
| Purpose | Primary GF Wi-Fi 6 coverage for dining, living, foyer, MBed |

#### Run R-FF-1: Staircase Niche → FF Living **CEILING** (Primary FF AP — UPDATED 2026-05-29)

> **Updated 2026-05-29 v2:** AP termination moved from **wall plate at 2400mm FFL** → **ceiling junction box in FF false ceiling, central position** (over the FF Living open area between BR1/BR2 doors). Same conduit + same 2× Cat6 + pull-string — the cable just continues UP from the originally-planned wall position into the false ceiling void instead of terminating at a wall plate. Drop the 5A power socket beside (was specced at 2400mm) — no longer needed because ceiling APs are PoE-only. AP model: "Ubiquiti UniFi U6-Lite or equivalent" (homeowner placeholder lock 2026-05-29).

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

| Fitting | Type | Position | Height | Notes |
|---|---|---|---|---|
| Main ceiling light | Recessed COB 12W, 2700K | Centred in room, checked against final bed/wardrobe marking | 3353mm | No false ceiling. |
| Bedside light N side | Wall sconce or recessed adjustable GU10, 5W | E wall, north side of headboard | 1400mm for wall sconce, 3353mm for ceiling spot | Aim at pillow zone after bed centreline is marked. |
| Bedside light S side | Wall sconce or recessed adjustable GU10, 5W | E wall, south side of headboard | 1400mm for wall sconce, 3353mm for ceiling spot | Keep clear of S-wall wardrobe path. |
| Wardrobe strip | 24V LED strip | Inside S-wall wardrobe + W-wall tail | Wardrobe top rail | Door-activated sensor. |

**Bed position assumption:** headboard against E wall, queen 75" x 60". Confirm the 3ft door swing before fixing light and socket boxes.

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

---

## Conduit-map review notes (2026-05-30)

Captured while building the interactive conduit map (`conduit-map/`). Flag for review; fold into the sections above when confirmed.

- **CAM-2 overview camera MOVED.** Dropped the porch-ceiling NE-corner position (and its false-ceiling stub). The same overview camera now mounts in the **MIDDLE of the Living Hall NORTH (entrance-facing) wall**, watching the porch + main approach. **Conduit route is the technician's choice on site** (pull from the niche, or tap the nearest data run) — not pre-specced.
- **CAM-4 (E-wall exterior, kitchen/utility) DROPPED** as redundant — remove its LV-25 stub from the camera list.
- **Foyer ceiling speaker is now FIXED (not a future provision).** It sits in the **middle of the foyer ceiling, between the two GU10 spotlights**, fed by a 2-core speaker wire from the PAM8403 amp inside the screen cavity (up through the cavity TOP conduit into the false ceiling).