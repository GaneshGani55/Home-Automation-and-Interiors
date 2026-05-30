# FOYER MASTER ELECTRICIAN PLAN

**Version 1.1 — 2026-05-22** (was v1.0 of 2026-05-20)
**Project:** Ganesh Prasad Home, Chitradurga
**Scope:** Foyer welcome system — cavity, switches, cameras, lighting, all conduits, all wiring
**Status:** Pre-plaster preparation document (plaster window opens ~2026-05-23)

---

## ⚠️ REVISION SUMMARY — v1.1 changes (2026-05-22)

If you read v1.0 already, these 6 things changed:

| # | What changed | Why | Where in this doc |
|---|---|---|---|
| 1 | **Cavity speaker → ceiling speaker.** Visaton FR 8 driver, MDF baffle, and the 3" speaker pocket in cavity back wall are all DROPPED. 3" flush ceiling speaker added at foyer false-ceiling centre. PAM8403 amp stays in cavity. Speaker wire runs up Conduit #4 (16mm grey, cavity-top → false ceiling — previously pull-string-only, now carries 2-core speaker wire). | Electrician (nephew) flagged 3" blind pocket is hard to plaster reliably. Also: the new monitor (LS22F320GAW) has no built-in speakers, so external speaker was always required. | § 7 Component 4, § 7.6 (pocket dropped), § 9 (ceiling speaker added) |
| 2 | **Cavity Socket Panel: 2-module → 8-module (8M).** Adds a **Cat6 keystone jack** for the data conduit termination (proper structured cabling). Sonoff stays inside box (clean). Both power and data conduits terminate in this 8M box. Socket pocket grows to ~7"×3"×2" deep. | 8M = 2 sockets (4M) + keystone (2M) + 2M spare; gives the Sonoff relay clean room without needing 65mm depth. | § 7 Component 5, § 7.6 (pocket size), § 14 |
| 3 | **Foyer Switch Panel: 6-gang → 18-module vertical grid.** Pocket already cut on-site, fits vertically on the 1'6" N wall section. Extra modules reserved for porch switches + walnut shelf switch + possible foyer↔living 2-way (living-hall 2-way deferred to electrician). | More headroom, future-proofing. | § 8 |
| 4 | **Smart-switch box approach RELAXED: depth-as-needed + extra modules per Sonoff.** Supersedes the blanket 2026-05-06 "65mm-deep everywhere" mandate. General rule: standard 50mm depth + 2 extra modules per Sonoff where feasible. **Exception (per § 8.5 revision of 2026-05-23): high-density boards like the Foyer Switch Panel (6 Sonoffs in one box) still need 65mm depth + 2M-per-Sonoff slack** — for those, follow Section 8.5's spec. | 65mm depth isn't reliably available in small modular sizes; "+2M per Sonoff" handles wire bending + relay room. For 6-Sonoff density, both 65mm depth AND extra width are needed. | § 8.5 (Foyer Panel), § 14, conduits-and-cavities § 0.4b |
| 5 | **Doorbell: Reolink Video Doorbell PoE → Hikvision DS-KV6113-WPE1(C).** 2MP/1080p IP villa door station, 131° FOV, 120dB WDR, PoE, IP65. Datasheet confirms **continuous RTSP + ONVIF** — works with Frigate 24/7 for the known-face auto-welcome flow (NOT press-only). Use DS-KABV6113-A mount accessory for theft resistance; TAMPER alarm built in. | Same brand as CAM-3/4/5 for unified NVR. Caveat: verify RTSP enabled in device config once in hand. | § 2 hardware chain, § 5 Zone E, § 10 (all subsections), § 15 |
| 6 | **CAM-1: confirmed provision-only.** Conduit + flush-capable IP67 back box + pull string on porch W wall, NO camera installed now. If future install: small flush anti-theft PoE pinhole. | Hikvision doorbell does continuous face detection; CAM-1 would sit ~2-3 ft away (redundant). Conduit/box left ready in case it's needed later. | § 10 |

**Other context to know:** the screen monitor was also swapped (LS22F350 → Samsung LS22F320GAWXXL, VESA 100, IPS, 36.2mm deep, no speakers) on 2026-05-26 — that's already reflected in § 7 Components 1+2. The thinner monitor gives ~64 mm cavity rear gap (up from ~51 mm), which makes the 8M socket box + RPi + amp layout comfortable.

This doc was migrated from the originally-specced Reolink Video Doorbell to the **Hikvision DS-KV6113-WPE1(C)** on 2026-05-22; the body below now names the Hikvision throughout. A few "Reolink" mentions remain only where a passage explains the swap itself (this changelog and the § 10 banner) or flags a Reolink-origin figure still pending Hikvision datasheet confirmation. Section 10 has the authoritative doorbell spec.

---

## TABLE OF CONTENTS

| # | Section | Audience |
|---|---|---|
| 1 | Document purpose + how to use this | Everyone |
| 2 | The big picture — what we're building | Everyone |
| 3 | Plain-English glossary | Everyone (especially homeowner) |
| 4 | Foyer geometry (corrected) | Mason, electrician |
| 5 | The four installation zones (overview) | Everyone |
| 6 | East wall — DB + starter cupboard | Mason, electrician, carpenter |
| 7 | South wall — Screen cavity (detailed) | Mason, electrician, painter, carpenter |
| 8 | North wall — Switch panel + doorbell + window + door | Mason, electrician |
| 9 | Foyer ceiling — Spotlights + cove + halo driver | Electrician, false-ceiling contractor |
| 10 | Porch + niche routes — Doorbell + future cameras + Waveshare stub | Electrician |
| 11 | Complete conduit schedule (every run) | Electrician |
| 12 | Wire schedule (every wire) | Electrician |
| 13 | MCB plan (2 MCBs for foyer) | Electrician |
| 14 | Switch board and socket schedule | Electrician |
| 15 | Bill of materials | Homeowner (purchasing), electrician |
| 16 | Phase-by-phase build order | Project manager, all trades |
| 17 | Pre-plaster sign-off checklist | Homeowner, electrician, mason |
| 18 | Flagged open items (decide later) | Homeowner |

---

## SECTION 1 — Document purpose + how to use this

This document is the **single source of truth** for the foyer welcome system installation. It contains everything needed to:

1. Lay the right conduits in the right places BEFORE plastering
2. Cut the right cavities in the right walls (cavity + DB recess + starter cupboard cutout + socket pocket + speaker pocket)
3. Pull the right wires through the right conduits
4. Install the right switches, sockets, cameras, doorbell, and screens

### Who reads what

| Trade | Sections to read |
|---|---|
| **Electrician** (in this region, also cuts cavity + DB recess + chases using core drill / chisel + wall grinder + lays conduits + pulls wires + installs switches) | 4–14, 16, 17 |
| **Mason** (plastering after conduits in, stone wall building if applicable) | 4, 16, 17 |
| **Painter** (cavity interior matte black, side walls, ceiling) | 7, 9 |
| **Carpenter** (VESA mounting board, cupboard plywood facade, Waveshare frame, walnut shelf) | 6, 7, 8, 10 |
| **Stone cladder** (cladding the S feature wall around the cavity) | 7, 16 |
| **False-ceiling contractor** (gypsum/POP, cove pocket, inspection hatch) | 9 |
| **Smart-home installer** (commissioning, software setup, camera config) | 2, 5–10 |
| **Homeowner** (decisions + sign-off) | All, especially 3, 4, 17, 18 |

**Regional note:** In Chitradurga construction practice, the **electrician** does the cavity cutting, DB recess cutting, switch box cutting, and conduit chasing — using core drills, wall grinders, and chisels. The mason's role is primarily plastering after the electrical work and any stone/brickwork. Trade assignments in this document reflect this practice.

### Critical timing

| Date | Event |
|---|---|
| **2026-05-20** | Document version 1.0 published — design locked |
| **2026-05-21 to 22** | Final on-site walkthrough with mason + electrician; chalk-mark every cavity, conduit chase, switch box, socket box |
| **2026-05-23** | Mason starts cutting cavities + chases; electrician lays conduits behind |
| **~2026-05-30 (1 week)** | Plaster begins — all conduits + back boxes must be in place by this date |

**Once plaster goes on, changes require breaking walls. There is no second chance.**

### How to use this document

1. **Read Section 2 first** to understand what the system does
2. **Skim Section 3 (glossary)** if any term is unfamiliar
3. Each subsequent section is **self-contained** — you can jump to the wall or zone you're working on without reading every prior section
4. **Section 17 is the final pre-plaster checklist** — sign it off before plaster crew arrives

---

## SECTION 2 — The big picture: what we're building

The foyer welcome system is the first thing a visitor experiences when they approach the home. It does three things automatically:

### 1. Sees the visitor

The **Hikvision video doorbell** mounted on the North wall (the 1'6" wall section between the main door and the corner window) captures the visitor's face as they approach the door. A future second camera can be added on the porch's West wall (conduit provisioned for this).

### 2. Recognises the visitor

A small server (**Beelink EQ12**) in the staircase niche runs face-recognition software (Frigate for detection, CompreFace for matching). If the face matches a family member or pre-registered visitor, the system identifies them within ~2 seconds.

### 3. Greets the visitor

A **21.5" Samsung monitor recessed into the South stone feature wall** lights up with a personalised welcome message ("Welcome home, Ganesh"). A warm amber LED glow appears around the monitor edges. A soft chime plays from a hidden speaker inside the cavity. The visitor feels expected.

If the visitor is unknown, the monitor stays in idle mode and the doorbell handles the introduction.

### The same hardware supports a smart-home indoor unit

A **Waveshare touchscreen** is mounted on the staircase South wall (just above the server niche). It displays:
- Water tank level (from the water automation system)
- Visitor video (live, when the doorbell rings)
- Room light controls
- Welcome / home information
- Future: door unlock, dining hall music control, climate, etc.

### Visual map of the welcome system

**Foyer floor plan (N at top, all device positions labelled):**

```
                          N (PORCH outside, gate ~7.5 ft north)
   ┌──────────────────────────────────────────────────────┐
   │                                                       │
   │  [CAM-1 spare conduit]            [Hikvision Doorbell]│
   │   porch W wall, 1650 mm FFL        on N wall 1'6"     │
   │   ── no camera yet ──              section, 1450 mm    │
   │   capped box + pull string         ── DOES face       │
   │   only                             detection ──        │
   │                                                       │
   ├────────┬─────────┬───────────────────────────────────┤
   │ CORNER │  WALL   │             MAIN DOOR              │
   │ WINDOW │ (1'6")  │       (3.2 ft, hinges EAST,        │
   │ 3.5 ft │         │        swings against E wall)      │
   │ + wraps│         │                                    │
   │ N corner         │                                    │
   ├────────┴─────────┴───────────────────────────────────┤
   │                                                        │
   │   [Foyer Switch Panel on N wall, 1'6" section,         │
   │    1200 mm FFL — spots / cove+halo / shelf / spare]    │
   │                                                        │
   │                                                        │
   │  ◄── OPEN to ──►                              ┌──────┐ │
W  │     Living /                                   │ DB + │ │ E
   │     Dining /                                   │ cup- │ │  (EXTERIOR
   │     Staircase                                  │ board│ │   wall, 9")
   │     (no W wall)                                │  on  │ │
   │                                                │  E   │ │
   │                                                │ wall │ │
   │                                                │(beh- │ │
   │                                                │ ind  │ │
   │                                                │ door │ │
   │                                                │swing)│ │
   │                                                └──────┘ │
   │                                                        │
   ├─────────┬──────────────────────────────────────────────┤
   │ OPEN    │       STONE FEATURE WALL (9" thick)          │
   │ PASSAGE │   ┌────────────────────────┐                 │
   │ 3.5 ft  │   │   Welcome screen        │                │
   │ to      │   │   (Samsung 21.5"         │               │
   │ Living/ │   │    in cavity)            │               │
   │ Pooja/  │   │                          │               │
   │ Dining  │   │   + halo LED             │               │
   │         │   │   + hidden speaker       │               │
   │         │   │   + bezel camera CAM-0   │               │
   │         │   └────────────────────────┘                 │
   │         │   + walnut floating shelf below              │
   │         │   ◄────── 6 ft ──────►                       │
   └─────────┴──────────────────────────────────────────────┘
                          S (Living / Pooja side)
```

**Separately, in the staircase area (West side of house, outside foyer):**

```
   ┌───────────────────────────────┐
   │   Waveshare touchscreen        │  ← Indoor control unit
   │   on staircase South wall      │     (Cat6 PoE stub provisioned;
   │   1500 mm FFL                  │      full hardware design
   │                                 │      deferred to other session)
   ├───────────────────────────────┤
   │   SERVER NICHE (below screen)  │  ← Brain of the system
   │   - Beelink EQ12 (Home          │
   │     Assistant + Frigate +       │
   │     CompreFace)                 │
   │   - PoE switch (TP-Link         │
   │     TL-SG1210P)                 │
   │   - TP-Link AX55 router         │
   │   - 12-port Cat6 patch panel    │
   │   - UPS                         │
   └───────────────────────────────┘
```

### Estimated cost (this plan's scope only)

| Category | Estimate |
|---|---|
| Conduits + wires + back boxes | ~₹8,000 |
| MCBs + RCBO (2 breakers for foyer) | ~₹2,500 |
| Switches + sockets (Schneider Unica or equivalent, decide later) | ~₹3,500 |
| Sonoff smart relays (2 inside cavity socket box + 1 inside switch panel) | ~₹1,500 |
| Samsung LS22F320GAWXXL monitor + VESA 100 bracket (REVISED 2026-05-26 — was LS22F350 + VESA 75; new SKU is actually IPS, lighter, thinner, dual HDMI, ₹2,500 cheaper) | ~₹7,000 |
| Raspberry Pi Zero 2W + PoE splitter + USB sound card + Pi Camera 3 | ~₹4,500 |
| Speaker (Visaton FR 8 + PAM8403 amp + MDF baffle) | ~₹2,200 |
| Halo LED strip + driver (24V 2200K, ~2m) | ~₹2,500 |
| Cove LED strip + driver (24V 2700K, ~10m perimeter) | ~₹4,500 |
| 2× GU10 ceiling spotlights + transformers | ~₹2,500 |
| Walnut floating shelf + LED strip | ~₹6,000 |
| Hikvision DS-KV6113-WPE1(C) Video Doorbell PoE | ~₹8,000 ⚠️ (old Reolink price — confirm) |
| Waveshare 10.1" touchscreen + Pi 4 + PoE HAT + mount frame | ~₹24,000 |
| Stone cladding (south feature wall, 6 ft × 11 ft) | ~₹18,000 |
| **Subtotal (excluding labour)** | **~₹96,200** |
| Labour (mason + electrician + painter + carpenter, foyer portion) | ~₹15,000 |
| **Grand total** | **~₹111,200** |

This excludes: smart door lock, dining hall speaker, anything outside the foyer + porch + niche-to-foyer zone.

---

## SECTION 3 — Plain-English glossary

Every technical term used in this document, defined plainly. The electrician will know most of these; the homeowner can use this as a reference.

### Electrical terms

| Term | Plain-English meaning |
|---|---|
| **DB (Distribution Board)** | The panel of breakers in the wall. Every wire in the house starts here. Ours is on the East wall of the foyer. |
| **MCB (Miniature Circuit Breaker)** | A trip switch inside the DB. One per circuit. Trips on overload or short circuit. |
| **RCBO / RCCB** | Like an MCB but also trips on leakage to earth (saves you from electrocution). Mandatory for electronics + wet circuits. |
| **Circuit** | One wire run from a single MCB feeding a group of devices. E.g., "B-Cavity" circuit = all things in the screen cavity. |
| **FFL (Finished Floor Level)** | Top of the installed floor tile (not bare slab). All heights in this document are measured from FFL. |
| **Conduit** | A plastic (PVC) pipe inside the wall. Wires get pulled through it. We use red conduit for 230V power, grey for low voltage. |
| **Chase** | The groove cut into the wall where the conduit sits. The mason cuts chases; the electrician lays conduits in them. |

### Switch / socket terms

| Term | Plain-English meaning |
|---|---|
| **Gang** | One switch position on a plate. A "4-gang plate" has 4 separate switches. |
| **Switch Board (SB) / Switch Panel** | The wall plate + back box that holds the switches for a room. We call the foyer's switch panel the **"Foyer Switch Panel"**. |
| **Modular plate** | The removable face plate that snaps onto a back box. Each "module" slot holds one switch, socket, or other unit. |
| **Back box** | The metal box recessed into the wall behind the plate, holding wiring and any hidden relays. **65 mm deep for smart switches.** |
| **5A socket** | The small 3-pin Indian socket for low-current things (chargers, monitors, TVs, lamps). 230V, up to ~1100W. |
| **16A socket** | The bigger 3-pin socket for heavy appliances (geysers, ACs, microwaves). 230V, up to ~3500W. |
| **Smart switch** | A switch that takes commands over WiFi or Zigbee in addition to manual press. Lets HA turn it on/off. |
| **Sonoff / Aqara** | Two brand names. **Sonoff** = WiFi smart relay, fits behind the plate as a hidden unit. **Aqara H1** = Zigbee, replaces the entire switch face. We use Sonoff hidden + standard rocker face. |

### Light + LED terms

| Term | Plain-English meaning |
|---|---|
| **LED strip** | A thin sticky strip with tiny LED dots along its length. Comes in 24V (most common) or 12V varieties. |
| **Driver (LED driver)** | A small electronic brick that converts 230V AC to the low voltage (24V DC) that LED strips need. Like a phone charger but for LEDs. |
| **Halo LED** | The warm amber LED strip stuck around the inner front edges of the screen cavity. Creates a floating glow around the monitor. |
| **Cove LED** | The 2700K LED strip hidden in a recessed channel ("cove") around the foyer false ceiling perimeter. Provides ambient warm light. |
| **Spotlight** | A focused beam of light. We use GU10 fittings (a standard bulb shape) for the 2 ceiling spots that graze the stone wall. |
| **CCT (Colour Correlated Temperature)** | The "warmth" of light. 2200K = candle-warm amber. 2700K = warm white. 4000K = neutral. 6500K = daylight blue. We use 2200K and 2700K only. |

### Camera / network terms

| Term | Plain-English meaning |
|---|---|
| **PoE (Power over Ethernet)** | Sending power AND data over the same Cat6 cable. Up to ~25W per device. |
| **Cat6** | Category 6 Ethernet cable. Carries gigabit data + PoE power. The standard cable for everything network-related. |
| **LSZH** | Low Smoke Zero Halogen — describes the cable jacket. Doesn't release toxic gas in a fire. Premium standard for indoor cabling. |
| **UV-resistant** | Cable jacket that doesn't crack in sunlight. Required for cables that go outdoors or near windows. |
| **RTSP** | Real-Time Streaming Protocol. The video stream format used by IP cameras. Frigate reads RTSP streams. |
| **NVR (Network Video Recorder)** | The device that records and processes camera streams. Ours = Beelink EQ12 running Frigate. |
| **Frigate** | Free open-source NVR software. Detects "object events" (face, person, car) in camera streams. |
| **CompreFace** | Free open-source face-recognition software. Takes a face image and tells you who it is. |
| **Home Assistant (HA)** | The smart-home brain software. Reads sensors, decides actions, controls devices. Runs on the Beelink EQ12. |
| **MQTT** | A messaging protocol smart devices use to talk to each other. HA uses MQTT internally. |

### Cavity / screen terms

| Term | Plain-English meaning |
|---|---|
| **Cavity** | The rectangular hole cut into the South feature wall to recess the Samsung monitor. Like a built-in medicine cabinet. |
| **VESA bracket** | A small metal plate that screws into the back of the monitor (75×75 mm pattern) and onto the wall. Lets the monitor hang. |
| **Baffle** | A small wooden plate that holds the speaker driver. The driver mounts on the baffle; the baffle attaches to the cavity back wall. |
| **Vascal** | The small wall section to the East of the door, between the door jamb and the East exterior wall corner. (Indian construction term.) |
| **Niche** | The server cupboard built into the staircase wall. Houses Beelink + PoE switch + router + UPS + patch panel. |

### Door + camera terms

| Term | Plain-English meaning |
|---|---|
| **Hinge side** | The side of the door where the hinges are. Our main door's hinges are on the **East** side. |
| **Latch side** | The side of the door where the handle / latch is. Our main door's latch is on the **West** side. |
| **Doorbell (Hikvision DS-KV6113-WPE1(C))** | A combined doorbell + camera + intercom unit. Visitors press the button, it rings inside and shows their face on the Waveshare. |
| **Bird's-eye camera** | A camera mounted high up (e.g., on a balcony soffit) looking down. Captures area context, not faces. |
| **Face-capture camera** | A camera mounted at face height (~1650 mm FFL). Captures faces head-on for recognition. |

---

## SECTION 4 — Foyer geometry (corrected)

This section locks in the exact dimensions of the foyer and what's on each wall.

### Big-picture orientation

The foyer is in the **North-East corner of the ground floor**, opening to the porch via the main door. The main door faces **North**. The L-shaped house extends South and West from the foyer.

### Foyer dimensions

| Dimension | Value (imperial) | Value (metric) | Notes |
|---|---|---|---|
| **N–S depth (door to feature wall)** | 5 ft (60") | 1524 mm | **Fixed** — South feature wall is built |
| **E–W width at S edge (feature wall portion)** | 6 ft (72") | 1828 mm | The stone feature wall portion |
| **E–W width at S edge (opening portion)** | 3.5 ft (42") | 1066 mm | The opening to Living / Pooja area |
| **E–W width at N edge (door wall)** | 9.5 ft (114") | 2895 mm | Total length of N exterior wall |
| **GF ceiling height (slab)** | 11 ft (132") | 3353 mm | Raw slab |
| **Foyer false ceiling height** | 9 ft (108") | 2743 mm | Drop of 2 ft from slab |
| **Exterior wall thickness** | 9" | 228 mm | Brick / block masonry (N exterior, E exterior, W exterior) |
| **South feature wall thickness** | **9"** | **228 mm** | **Structural / load-bearing — same 9" thickness as exterior walls. Not a 4" partition.** This is critical because the cavity is cut into this wall, and we rely on 5" of remaining wall behind the cavity for structural integrity. |
| **Partition wall thickness (general)** | 4" | 102 mm | Used elsewhere in the house for non-load-bearing partitions; NOT applicable to the foyer South feature wall |

**Important geometric quirk:** the foyer is **not a simple rectangle**. The South edge is split between a 6 ft stone feature wall (East portion) and a 3.5 ft open passage (West portion). The West side has no wall at all — it opens directly to Living/Dining/Stairs.

### The four boundaries

```
   [Top-down floor plan of foyer, North at top]

                              N (PORCH outside, gate to north)
   ┌──────────────────────────────────────────────────────────┐
   │  WINDOW        │  WALL  │       DOOR ZONE                │
   │  (corner,      │ (1'6" )│  (3.2 ft door,                 │
   │  3.5 ft +      │        │   hinged on East,              │
   │  wraps NW      │        │   includes vascal              │
   │  corner)       │        │   East-side return)            │
   ├────────────────┴────────┴────────────────────────────────┤
   │                                                            │
   │                                                            │
   │                                                            │
   │                                                            │
   │                                                            │
   │  ◄── OPEN ──►                                              │
   │   (no wall on                                              │ E
W  │    West side; foyer        FOYER                           │  (EXTERIOR
   │    transitions into                                        │   wall —
   │    Living/Dining/                                          │   DB +
   │    Stairs area)            5 ft N-S                        │   starter
   │                                                            │   cupboard
   │                                                            │   live
   │                                                            │   here)
   │                                                            │
   │                                                            │
   ├──────────────────────┬─────────────────────────────────────┤
   │   OPEN PASSAGE       │   STONE FEATURE WALL                │
   │   3.5 ft             │   6 ft (with screen cavity          │
   │   (to Living /       │   centred + halo + shelf below)     │
   │   Pooja / Dining /   │                                     │
   │   Kitchen)           │   ◄── 6 ft ──►                      │
   │                      │                                     │
   └──────────────────────┴─────────────────────────────────────┘
                              S (Living / Pooja side)
```

### What's on each boundary

| Boundary | Length | Surface | What's on it |
|---|---|---|---|
| **North (exterior, faces porch)** | 9.5 ft | 9" masonry, exterior | **Door** (3.2 ft, hinges East), **vascal** (~6", East of door), **wall section** (1.5 ft, between door and window — Foyer Switch Panel + Hikvision doorbell), **corner window** (3.5 ft, wraps NW corner extending North) |
| **East (exterior)** | 5 ft | 9" masonry, exterior | **DB recess** (400×600×100 mm flush) + **Starter cupboard** (600×400×250 mm surface-mounted). Both behind the open door swing. |
| **South (partition + feature wall)** | 9.5 ft total | Mixed | **Stone feature wall** 6 ft (East portion, with screen cavity), **Open passage** 3.5 ft (West portion, no wall) |
| **West** | 5 ft (notional) | OPEN | **No wall** — foyer transitions directly into Living/Dining/Stairs area |

### Key reference points (heights from FFL)

| Reference | Height (imperial) | Height (mm) | Why |
|---|---|---|---|
| Cavity centre (screen eye level) | 57⅛" | 1450 | Comfortable standing eye level |
| Cavity bottom edge | 50½" | 1280 | Ergonomic recess |
| Cavity top edge | 63⅞" | 1620 | Auto-derived from above |
| Walnut shelf top surface | 35⅜" | 900 | Below cavity, holds keys/plants/mail |
| Hikvision doorbell centre | 57" | 1450 | Face level for adult |
| Foyer Switch Panel centre | 47¼" | 1200 | Standard switch height |
| DB bottom edge | 59" | 1500 | Top within reach, MCBs at chest height |
| False ceiling height | 108" | 2743 | 9 ft drop from 11 ft slab |
| Spotlight ceiling box | 108" | 2743 | At false ceiling level |
| Cove pocket inside | ~108" minus 3" | ~2670 | Inside cove pocket above false ceiling rim |

### Orientation convention used throughout this document

When this document says **"left"** or **"right"** for the cavity or any wall, it means:
- **You are standing in the foyer**, looking AT the wall in question
- **Left** = the side on your left hand as you look at the wall
- **Right** = the side on your right hand

For the South feature wall (looking south at the cavity from foyer):
- **Left = East side** (the DB direction)
- **Right = West side** (the staircase niche direction)

For the North wall (looking north at the door from inside foyer):
- **Left = West side** (where the corner window is)
- **Right = East side** (where the door + vascal are)

---

## SECTION 5 — The installation zones (overview)

The foyer welcome system installation happens across **6 zones**: 4 inside the foyer, 1 external (porch), and 1 in the indoor staircase area. This section gives a high-level view of each zone; later sections give the full detail.

### Zone A — East wall (interior face) — Section 6

**What's here:**
- Distribution Board (DB) recess — flush in wall
- Starter cupboard for water automation — surface-mounted
- Both positioned behind the main door's open swing (hidden when door is open)

**Trades:** Electrician (cuts recess + lays conduits), Carpenter (builds plywood cupboard facade with hinged lockable door)

**Key conduits originating here:**
- **2 conduits go OUT of the DB** to feed the foyer: one to the Foyer Switch Panel (for all foyer lights — branches to spots/cove/halo/shelf from the panel), one direct to the Cavity (for the cavity's own circuit, no wall switch)
- **5 conduits come INTO the cupboard** from the water automation system (Sintex float, sump float, motor cables, niche backup)

---

### Zone B — South feature wall (interior face) — Section 7

**What's here:**
- Screen cavity (21¼" × 13½" × 4" deep) cut into the centre of the 6 ft feature wall portion
- Inside cavity: monitor + RPi + Sonoffs + speaker + halo LED + bezel camera
- Walnut floating shelf below cavity at 900 mm FFL

**Trades:** Electrician (cuts cavity + sub-pockets + lays conduits + installs sockets + Sonoffs), Carpenter (walnut shelf + MDF speaker baffle + optional VESA backing), Painter (cavity interior matte black where stone doesn't reach), Stone cladder (full 6 ft × 11 ft wall **PLUS** stone wrapping into the cavity reveal — see refinement note below)

**Stone cladding design refinement (per homeowner direction):** Stone cladding does NOT stop flat at the cavity edge. Instead, stone wraps INTO the cavity reveal (the inner front lip of the cavity) for a partial depth — adds visual richness, lets the halo LED hide behind the stone reveal. **Detail in Section 7.** Affects cavity dimensions slightly (cavity cut ~40 mm wider/taller so the inner usable opening after stone is still 540 × 340 mm for the monitor).

**Key conduits entering here:** 3 — Power (from DB, bottom-left of back wall), Cat6 (from niche via floor, bottom-right of back wall), Halo 24V (from above false ceiling, top-centre of back wall)

---

### Zone C — North wall (interior face) — Section 8

**What's here:**
- Foyer Switch Panel (4-gang at 1200 mm FFL, in the 1'6" wall section between door and window)
- Main door (3.2 ft wide, hinged East)
- Corner window (3.5 ft wide, sill 914 mm FFL, height 1524 mm, wraps NW corner)
- Hikvision DS-KV6113-WPE1(C) Video Doorbell on the OUTSIDE face of the 1'6" section (covered in Zone E)

**Trades:** Electrician (switch box + chases), Carpenter (door + window architrave finishing if applicable)

**Key conduits on/entering this wall:**
- 1 IN from DB (Foyer-Lights feed, via false ceiling) → terminates at Foyer Switch Panel back box
- 4 OUT of Foyer Switch Panel (one per gang's load): to spots, to cove driver, to halo driver, to walnut shelf LED

---

### Zone D — Foyer ceiling (above false ceiling void) — Section 9

**What's here:**
- 2 × GU10 ceiling spotlight boxes (in false ceiling)
- Cove LED strip around perimeter (in cove pocket above false ceiling rim)
- Cove LED driver + Halo LED driver (above false ceiling, beside each other on a small shelf)
- Inspection hatch (300 × 300 mm) for driver access

**Trades:** Electrician (lays ceiling conduits + mounts spots + installs drivers + runs LED strips), False-ceiling contractor (drops ceiling to 9 ft + builds cove pocket + installs hatch)

**Key items above ceiling:** 2 drivers (cove + halo), short conduit branches from the Switch Panel feed to spots / cove driver / halo driver, plus the 24V output runs from the drivers to their respective LED strips

---

### Zone E — Porch (EXTERNAL) — Section 10

**What's here (outside the foyer, under porch overhang):**
- Hikvision DS-KV6113-WPE1(C) Video Doorbell on outside face of 1'6" N wall section, 1450 mm FFL
- CAM-1 spare conduit + capped back box on porch West wall, 1650 mm FFL (no camera yet)
- CAM-2 stub on porch ceiling NE corner (future overview camera, no camera yet)

**Trades:** Electrician only (lays conduits + back boxes + pull strings; installs Hikvision doorbell)

**Key conduits in this zone:**
- 1 Cat6 from staircase niche → Hikvision doorbell (used + cable pulled)
- 1 Cat6 conduit from niche → CAM-1 spare on porch W wall (pull string only, no cable)
- 1 Cat6 conduit from niche → CAM-2 stub on porch ceiling (pull string only, no cable)

---

### Zone F — Staircase indoor area — Section 10 (covered together with Zone E routes)

**What's here (inside the home, on the staircase side):**
- Waveshare touchscreen on staircase South wall, 1500 mm FFL (future indoor control unit, hardware design deferred)
- Server niche directly below — already exists per main electrical plan (Beelink EQ12, PoE switch, router, patch panel, UPS)

**Trades:** Electrician (lays Cat6 stub conduit from niche up to Waveshare position)

**Key conduits in this zone:**
- 1 short Cat6 conduit from niche → Waveshare position on staircase S wall (~1-2 m run, pull string + Cat6 cable pulled)

---

### Quick zone summary table

| Zone | Wall / area | Detail section | Key device(s) | Conduit count |
|---|---|---|---|---|
| A | East wall (interior) | 6 | DB + starter cupboard | 2 out (DB) + 5 in (water auto cupboard) |
| B | South feature wall | 7 | Screen cavity + walnut shelf | 3 entering cavity |
| C | North wall | 8 | Switch panel + door + window | 1 in (DB feed) + 4 out (to loads) |
| D | Foyer ceiling | 9 | Spots + cove + halo drivers + hatch | Branch conduits from switch panel |
| E | Porch (external) | 10 | Hikvision doorbell + CAM-1 spare + CAM-2 stub | 3 long-runs from niche |
| F | Staircase indoor | 10 | Waveshare + server niche | 1 short-run from niche |

---

## SECTION 6 — East wall (Zone A): DB + Starter Cupboard

The East wall is the **power and control hub** of the entire house. Two pieces of equipment live here, side-by-side or stacked vertically (electrician decides on-site):

1. **Distribution Board (DB)** — the panel of MCBs for the whole house
2. **Starter Cupboard** — the lockable enclosure for the water automation system's pump starters + Sonoff

Both are positioned in the area covered by the open main door (when door is swung 90° against East wall), so they're hidden from view during normal use of the foyer.

### 6.1 — DB recess specifications

| Property | Value |
|---|---|
| **DB shell model** | Schneider Acti9 IEF48 (48-way, single-phase) |
| **Recess dimensions (W × H × D)** | 400 × 600 × 100 mm |
| **Recess dimensions (imperial)** | 15¾" × 23⅝" × 4" |
| **Mounting type** | Flush recessed (flush with finished wall plaster) |
| **Bottom edge of recess from FFL** | **1500 mm (59")** — MCBs at chest height, top within reach |
| **Top edge of recess from FFL** | 2100 mm (82¾") |
| **Distance from N corner of E wall (door jamb side)** | Minimum 100 mm offset so the open door clears the DB cover |
| **Wall depth used** | 100 mm of the 228 mm (9") East exterior wall |
| **Wall depth remaining behind DB** | 128 mm (5") solid masonry — safe |

### 6.2 — Starter cupboard specifications

> **Updated 2026-05-29:** Electrician chased the masonry deeper than the original 9" wall thickness allowed, so the starter is now **wall-flushed** (not surface-mounted as originally specced). This is the on-site decision and current state — the docs originally said "can't be fully recessed in 9" wall" but the electrician's nephew found a way. Trade-off: slightly thinner remaining wall behind starter (was 5" with DB, now ~25 mm behind starter — still structurally fine for a non-load-bearing-equipment cavity in an exterior wall, but verified on-site).

| Property | Value |
|---|---|
| **Cupboard outer dimensions (W × H × D)** | 600 × 400 × 250 mm (minimum) |
| **Cupboard outer dimensions (imperial)** | 23⅝" × 15¾" × 9⅞" |
| **Mounting type** | **Wall-flushed (recessed)** — locked 2026-05-29. Electrician chased the 9" East wall deeper than initial spec allowed; cupboard now sits flush with finished wall. (Was originally specced "surface-mounted" because 250 mm depth > 228 mm wall thickness; on-site, the deeper chase made flush mounting possible.) |
| **Door** | Hinged with lock (child / tenant safety) |
| **Ventilation** | Slatted openings top + bottom (~5% of door area) — starters dissipate heat |
| **Material (cupboard body)** | Wood / MDF / plywood with metal hinges |
| **Material (facade — carpenter scope)** | BWP plywood, walnut veneer or PU finish, matching foyer wood palette |
| **Interior contents** | P1 starter (Magnum PSP1H) + P2 starter (Magnum PSP1) + Sonoff DUALR3 + 4-way terminal block + small DIN rail (optional) + earthing busbar |

Detailed interior layout is in [water-automation-conduits.md](water-automation-conduits.md) §4.

### 6.3 — The geometric constraint (door swing vs equipment footprint)

> **LOCKED 2026-05-29 — Stacked vertical arrangement chosen (DB above, Starter below).** Of the two original options (1: side-by-side, 2: stacked), the electrician picked **Option 2 stacked** because (a) DB needs to be at chest-height for usability while Starter doesn't, and (b) the door swing arc covers more of the wall side-by-side than stacked. **DB sits on top, Starter sits directly below it, both flush-mounted, both behind the open door swing.** Original "Arrangement Option 1" (side-by-side) is no longer applicable but documented below for reference.

```
   [Plan view — East wall length = 5 ft (1524 mm)]

   N corner ◄──────────────────────────────────────────► S corner
            ◄──────── 975 mm door swing arc ─────────► ◄─ 549 mm ─►
                     (door panel against wall)             clear
   ┌─────────────────────────────────────────────────────────────┐
   │                                                              │
   │                                                              │
   │  Door panel lies flat against E wall here when open 90°      │
   │                                                              │
   └─────────────────────────────────────────────────────────────┘
```

**The problem:**
- DB needs 400 mm width
- Cupboard needs 600 mm width
- Side-by-side total: 1000 mm
- Available space south of the door swing arc: only 549 mm
- **Side-by-side doesn't fit.**

**The solutions (electrician + carpenter choose ON-SITE):**

#### Arrangement Option 1 — DB recessed behind door swing, Cupboard south of door swing

```
   [East wall, viewed from inside foyer looking East]

   N corner ◄──── 975 mm door swing ────►◄── 549 mm clear ──►
   ┌──────────────────────────────────────────────────────────┐
   │                                                            │
   │   ┌──────────────────┐                                     │
   │   │  DB RECESS       │       ┌──────────────────┐         │
   │   │  flush in wall   │       │  STARTER         │         │
   │   │  400 × 600       │       │  CUPBOARD        │         │
   │   │  bottom edge     │       │  surface-mounted │         │
   │   │  1500 mm FFL     │       │  600 × 400 × 250 │         │
   │   │                  │       │                  │         │
   │   │  hidden by open  │       │  600 mm width    │         │
   │   │  door panel      │       │  > 549 mm clear  │         │
   │   │                  │       │  zone — needs    │         │
   │   │                  │       │  ~50 mm overhang │         │
   │   │                  │       │  into door zone  │         │
   │   └──────────────────┘       └──────────────────┘         │
   │                                                            │
   └──────────────────────────────────────────────────────────┘
```

**Pros:** DB is fully hidden when door is open. Cupboard easy to access.
**Cons:** Cupboard slightly overhangs the door swing zone (~50 mm). Door panel may bump cupboard at full 90° swing — door stopper at 85° solves this.

#### Arrangement Option 2 — Both stacked vertically inside door swing zone

```
   [East wall, viewed from inside foyer looking East]

   N corner ◄────── 975 mm door swing ──────►
   ┌─────────────────────────────────────────┐
   │                                          │
   │   ┌──────────────────────┐               │
   │   │  DB RECESS           │               │
   │   │  flush, 400 × 600    │               │
   │   │  bottom edge 1500    │               │
   │   │  FFL                 │               │
   │   └──────────────────────┘               │
   │                                          │
   │   ┌──────────────────────┐               │
   │   │  STARTER CUPBOARD    │               │
   │   │  surface-mounted     │               │
   │   │  600 × 400 × 250     │               │
   │   │  centered below DB   │               │
   │   │  (cupboard extends   │               │
   │   │  ~100 mm above       │               │
   │   │  cabinet top edge    │               │
   │   │  area)               │               │
   │   └──────────────────────┘               │
   │                                          │
   └─────────────────────────────────────────┘
```

**Pros:** Both fit entirely within door swing zone; door swings flat against wall with no obstruction.
**Cons:** Total vertical height ~1000 mm; cupboard ergonomics slightly worse (need to bend a bit to access starters).

**Decision: Choose on-site after Phase 2 (chasing). Photograph the final layout; get homeowner sign-off.**

### 6.4 — Conduits ORIGINATING from the DB

**Important: only 2 conduits actually start at the DB to feed the foyer.** Within each conduit, multiple wires run together (Live + Neutral + Earth, and any return wires). Loads are then fed downstream from the Foyer Switch Panel — NOT directly from the DB.

| # | Conduit ID | Size | Colour | Goes to | Wires inside | Purpose |
|---|---|---|---|---|---|---|
| 1 | **C-DB-Foyer-Switch** | 25 mm | RED | Up through E wall → false ceiling → across to N wall → drops down to Foyer Switch Panel at 1200 mm FFL | 1× 1.5 sqmm Red (Live) + 1× 1.5 sqmm Black (Neutral) + 1× 1.5 sqmm Green/Yellow (Earth) | Feed for all foyer lighting (Circuit **B-Foyer-Lights**). From here, separate conduits branch out of the Switch Panel to each load (spots, cove, halo, shelf). |
| 2 | **C-DB-Cavity-Power** | 25 mm | RED | Horizontal in E wall at ~1300 mm FFL → SE corner → horizontal in S wall (behind stone) → enters cavity at bottom-LEFT corner of back wall | 1× 2.5 sqmm Red (Live) + 1× 2.5 sqmm Black (Neutral) + 1× 2.5 sqmm Green/Yellow (Earth) | 230V for cavity (Circuit **B-Foyer-Cavity**). No wall switch in this path — cavity sockets are controlled by Sonoff Mini relays INSIDE the cavity socket box. |

**Why only 2:** every foyer load lives on one of these two circuits. The lighting circuit goes through the wall switch panel first; the cavity circuit goes direct because it has electronic control (Sonoff) at the destination.

### 6.4a — Conduits originating from the Foyer Switch Panel (downstream of the DB-feed)

These are NOT DB conduits — they originate at the Switch Panel on the N wall. Listed here for completeness because they're part of the same Circuit B-Foyer-Lights chain. Full detail in Section 8.

| Conduit ID | Size | From → To | Carries (switched lives downstream of each gang) |
|---|---|---|---|
| C-SW-Spots | 25 mm RED | Switch Panel → up N wall → false ceiling → to 2× spot ceiling boxes | Switched Live from Gang 1 + shared N + E |
| C-SW-Cove-Halo | 25 mm RED | Switch Panel → up N wall → false ceiling → splits to cove driver + halo driver | Switched Live from Gang 2 (linked: cove + halo) + shared N + E |
| C-SW-Shelf | 16 mm RED | Switch Panel → down N wall → across to walnut shelf location | Switched Live from Gang 3 + 24V driver primary if shelf driver is in panel area |
| C-SW-Spare | 16 mm RED | Switch Panel → up N wall → false ceiling (terminated capped, pull string only) | Spare — for future load on Gang 4 |

These 4 conduits **leave the Switch Panel** and route to their respective loads. Each carries the switched Live wire (the wire that becomes live ONLY when the gang switch is pressed), plus shared Neutral and Earth.

### 6.4b — Conduits entering the DB (incoming utility / mains)

| Conduit ID | Size | From | Purpose |
|---|---|---|---|
| C-Main-Incomer | 25 mm BLUE (or per local code) | Utility meter outside | Single-phase mains from BESCOM meter |
| C-Earth | 16 mm | House earth pit | Main earth wire to DB earth bus |

### 6.5 — Conduits ENTERING the starter cupboard (water automation system)

Cross-reference: [water-automation-conduits.md](water-automation-conduits.md). Summary only:

| # | Conduit ID | Size | From | Carries |
|---|---|---|---|---|
| 1 | C-Sintex-2 | 16 mm | Sintex tank float (terrace SW corner) | 2-core 1.5 sqmm 220V float wire |
| 2 | C-Sump-2 | 16 mm | Sump JB (east external wall) | 2-core 1.5 sqmm 220V float wire |
| 3 | C-DB-Backup | 20 mm | Staircase server niche | Empty pull string (future Cat6) |
| 4 | C-Motor-P1 | 25 mm | Outside, to borewell head | 3-core 4 sqmm XLPE armoured |
| 5 | C-Motor-P2 | 25 mm | Outside, to P2 pump cage (east wall) | 3-core 2.5 sqmm |

All 5 enter the cupboard through the bottom or back panel. The carpenter cuts cable entry holes in the cupboard during build.

### 6.6 — Carpenter scope for the cupboard facade

| Item | Specification |
|---|---|
| Facade material | BWP plywood, 18 mm |
| Finish | Walnut veneer with polyurethane sealant OR PU paint matching foyer walnut shelf |
| Door | Hinged, full-height, opening direction TBD on-site (likely opens South so it doesn't conflict with main door) |
| Lock | Cam lock or magnetic catch with child-safe latch |
| Ventilation | 5% of door area in slatted openings (top + bottom) |
| Visible footprint | ~620 × 420 mm front face + 260 mm depth (slightly larger than cupboard body for clean trim) |
| Estimated cost | ~₹3,000 (carpentry + materials) |

### 6.7 — Pre-plaster sign-off for Zone A (East wall)

Before plaster goes on the East wall:

- [ ] Final layout (Arrangement Option 1 or 2) selected on-site after Phase 2
- [ ] Homeowner sign-off photographed (with chalk marks of equipment outlines)
- [ ] DB recess cut to 400 × 600 × 100 mm (verify with tape measure + spirit level)
- [ ] Cupboard mounting position marked; ventilation considered
- [ ] All 5 outgoing DB conduits routed and labelled (each conduit end taped with permanent marker showing ID)
- [ ] All 5 incoming water automation conduits terminated at cupboard back panel
- [ ] Draw strings (nylon twine) inserted in every conduit before plaster
- [ ] All conduit ends capped with masking tape (so plaster doesn't enter)
- [ ] Earth wire (separate motor earth pit) routing confirmed
- [ ] Mounting bracket / anchor points for DB shell installed (rawl plugs ready)

---

## SECTION 7 — South wall (Zone B): The Screen Cavity

This is the most complex zone in the foyer. The cavity is a recessed box cut into the 9" thick South feature wall. It houses the welcome screen and all its supporting hardware. Stone cladding wraps from the wall face INTO the front portion of the cavity, creating a premium reveal effect.

### 7.1 — Cavity overview (mental picture)

Imagine a small medicine cabinet built into a wall — that's exactly what the cavity is. A rectangular hole cut into the South feature wall, open on the front (where the monitor hangs), with solid masonry on all other sides (top, bottom, left inner wall, right inner wall, and back wall).

**Which part of the South edge gets the cavity:**

The South edge of the foyer is 9.5 ft long total, split into two parts:
- **6 ft of stone feature wall** — starts at the SE corner of the foyer (where the East exterior wall meets the South edge) and extends WEST for 6 ft. **This is where the cavity is cut.**
- **3.5 ft of open passage** — continues further WEST from where the feature wall ends, all the way to the SW corner. This is the opening to Living/Pooja.

So the cavity sits in the 6 ft stone feature wall section, NOT in the open passage section.

**Within that 6 ft section, the cavity sits centred horizontally** — 24⅝" (~625 mm) from each side edge of the feature wall.

**Vertical position:** the cavity centre is at 1450 mm FFL — comfortable eye level for a standing adult.

### 7.2 — Cavity cut dimensions

| Dimension | Value (imperial) | Value (metric) | Notes |
|---|---|---|---|
| **Cavity cut width (raw masonry cut)** | **22¾"** | **580 mm** | Wider than monitor + final inner opening, to accommodate 20 mm stone slips on each inner side wall |
| **Cavity cut height (raw masonry cut)** | **14⅞"** | **380 mm** | Same reason as width |
| **Cavity depth (into 9" wall)** | **4"** | **100 mm** | Leaves 5" (128 mm) of solid masonry behind the cavity for structural integrity |
| **Inner usable opening AFTER stone slips** | 21¼" × 13½" | 540 × 340 mm | This is what the monitor "sees" — matches monitor size (491 × 291 mm) with 25 mm design margin all around |
| **Stone reveal depth (front portion clad in stone)** | 1¼" | 30 mm | The first 30 mm of cavity depth has stone slips on the inner walls; deeper than 30 mm is matte black |
| **Stone slip thickness on each inner wall** | ¾" | 20 mm | Thin stone slip applied to the masonry inner wall by stone cladder |

### 7.3 — Cavity position on the feature wall

```
   [Front view of S feature wall (6 ft × 11 ft) from foyer side]
   
   ◄──────────── 72" (6 ft) ────────────►
   ┌─────────────────────────────────────┐  ▲
   │                                       │  │
   │                                       │  │
   │   Top of cavity at 63⅞" (1620 mm) FFL │  │
   │              │                        │  │
   │              ▼                        │  │
   │        ┌───────────┐                  │  │
   │        │           │                  │  │
   │        │  RAW CUT  │ ← cavity cut     │  │  ◄── 132" (11 ft)
   │        │ 22¾"× 14⅞"│   in masonry     │  │
   │        │           │                  │  │
   │        │           │                  │  │
   │        └───────────┘                  │  │
   │              ▲                        │  │
   │              │                        │  │
   │   Bottom of cavity at 50½" (1280 mm)  │  │
   │                                       │  │
   │  ◄ 24⅝" ►        ◄ 24⅝" ►            │  │
   │   distance        distance             │  │
   │   from L edge     from R edge          │  │
   │   (cavity centred horizontally —       │  │
   │   ⚠️ MEASURE ACTUAL WALL WIDTH on-site  │  │
   │   first; construction may make the     │  │
   │   feature wall slightly more or less   │  │
   │   than 72". Centre cavity on the       │  │
   │   actual measured width, not the       │  │
   │   nominal 72".)                        │  │
   │                                       │  │
   │   Walnut floating shelf at 35⅜" (900 │  │
   │   mm) FFL — runs the full 72" width   │  │
   │   ═════════════════════════════════   │  │
   └─────────────────────────────────────┘  ▼
                  FFL (floor)
```

### 7.4 — Stone reveal wrap (design refinement)

After the cavity is cut at 580 × 380 × 100 mm (raw cut), the **stone cladder applies stone slips to ALL FOUR inner walls of the cavity** (top inner wall, bottom inner wall, left inner wall, right inner wall) — but only for the FRONT 30 mm of depth from the cavity face.

The back wall of the cavity does NOT get stone slip (the back wall is painted matte black instead).

#### How it looks from the foyer side (looking INTO the cavity)

```
   [Looking AT the cavity from foyer, monitor removed]
   
                 ◄── inner opening 540 mm ──►
              ╔════════════════════════════╗
              ║░░░░░░░░░░░░░░░░░░░░░░░░░░░░║  ◄── top inner wall:
              ║░ stone slip on TOP        ░║      stone slip wraps from
              ║░ inner wall (front 30 mm) ░║      the wall face into the
              ║░░░░░░░░░░░░░░░░░░░░░░░░░░░░║      cavity for 30 mm depth
              ║                             ║
              ║░                          ░║  ◄── left inner wall:
              ║░                          ░║      stone slip on left
              ║░                          ░║      inner wall (front 30 mm)
              ║░    deeper interior is    ░║
              ║░    matte black (no       ░║
              ║░    stone here)           ░║      ⊙ right inner wall:
              ║░                          ░║      stone slip on right
              ║░                          ░║      inner wall (front 30 mm)
              ║░                          ░║
              ║░░░░░░░░░░░░░░░░░░░░░░░░░░░░║  ◄── bottom inner wall:
              ║░ stone slip on BOTTOM     ░║      stone slip on bottom
              ║░ inner wall (front 30 mm) ░║      inner wall (front 30 mm)
              ║░░░░░░░░░░░░░░░░░░░░░░░░░░░░║
              ╚════════════════════════════╝
              ▲                              ▲
              │                              │
              The "frame" you see around the monitor is
              all stone — the wall's stone face continues
              seamlessly INTO the cavity for the first 30 mm
```

#### Plain-English explanation (what stone goes where, exactly)

The cavity is a box with 6 surfaces:
- 1 OPEN front (the foyer-facing opening — no surface here)
- 4 INNER walls (top, bottom, left side, right side — the surfaces that face INTO the cavity volume)
- 1 BACK wall (the deep end of the cavity)

**Stone slips are applied to 4 of these 6 surfaces**:
- ✅ Top inner wall — front portion only (first 30 mm of depth)
- ✅ Bottom inner wall — front portion only (first 30 mm of depth)
- ✅ Left inner wall — front portion only (first 30 mm of depth)
- ✅ Right inner wall — front portion only (first 30 mm of depth)
- ❌ Back wall — NO stone (painted matte black across full surface)
- ❌ Front opening — NO surface (this is the opening where the monitor sits)

**Each inner wall is 100 mm (4 inches) deep** — that's the full depth of the cavity, from the foyer face to the back wall. Of this 100 mm depth on each inner wall:
- **First 30 mm (front portion, closest to foyer):** stone slip glued to the masonry
- **Remaining 70 mm (back portion, closer to the back wall):** raw masonry painted matte black

The stone and matte black are NEXT TO each other along the depth of the inner wall. They do NOT stack on top of each other.

**Tunnel analogy:** imagine you're walking into a short tunnel that's 100 mm long.
- The first 30 mm of the tunnel's walls (closest to the entrance) have stone tiles glued to them.
- The remaining 70 mm of the tunnel's walls (closer to the far end) are painted matte black.
- You don't see stone tiles AND black paint stacked on top of each other on the same patch of wall. You see stone in the front section, black paint in the back section. Different patches of the same wall surface.

**Simple flat representation (one inner wall, shown flat as if rolled out):**

```
         ◄── DEPTH FROM CAVITY FRONT FACE ──►
   
         ◄── 30 mm ──►◄────── 70 mm ──────►
         ┌────────────┬───────────────────┐
   inner │   STONE    │    MATTE BLACK     │
   wall  │   SLIP     │    PAINT           │
   surf. │   (front   │    (back portion   │
         │   portion) │    of the same     │
         │            │    inner wall)     │
         └────────────┴───────────────────┘
         ▲            ▲                   ▲
         │            │                   │
         Front edge   "Step" at 30 mm     Back wall
         of cavity    depth (where halo   meets here
         (foyer face) LED strip sits)
```

**Same pattern applies to all 4 inner walls** (top, bottom, left, right). Each inner wall has its OWN stone section (front 30 mm) and its OWN matte black section (back 70 mm).

**The back wall is different** — it's a SINGLE flat surface at the deep end. The back wall does NOT get stone; it's painted matte black across its entire surface.

#### Where the halo LED strip sits

The strip is mounted on each inner wall at the boundary (the "step") where the stone section ends and the matte black section begins — specifically on the matte-black side of that boundary, very close to the stone edge.

The strip fires FORWARD (toward the foyer). The 20 mm-thick stone slip in front of the strip blocks direct line of sight from the foyer to the strip itself. Viewers see only the warm amber glow spilling forward around the edges of the monitor — the source (the strip) stays hidden behind the stone lip.

### 7.5 — What goes INSIDE the cavity (the 6 main components)

```
   [Front view of cavity with everything in place — monitor removed for clarity]

                    ◄── 21¼" inner opening ──►
                  ╔════════════════════════════╗  ▲
                  ║ ▓▓▓▓▓▓▓▓ HALO ▓▓▓▓▓▓▓▓▓▓▓ ║  │
                  ║ ▓                        ▓ ║  │
                  ║ ▓  ┌──────────────────┐  ▓ ║  │
                  ║ ▓  │   ●  CAM-0 on    │  ▓ ║  │  ◄── CAM-0 at TOP of
                  ║ ▓  │      top bezel   │  ▓ ║  │     monitor bezel,
                  ║ ▓  │                   │  ▓ ║  │     centred horizontally
                  ║ ▓  │    MONITOR        │  ▓ ║  │ 13½"
                  ║ ▓  │    (Samsung       │  ▓ ║  │ inner
                  ║ ▓  │   LS22F320GAW)    │  ▓ ║  │
                  ║ ▓  │                   │  ▓ ║  │
                  ║ ▓  │  hung on VESA     │  ▓ ║  │
                  ║ ▓  │  bracket          │  ▓ ║  │
                  ║ ▓  │                   │  ▓ ║  │
                  ║ ▓  │                   │  ▓ ║  │
                  ║ ▓  └──────────────────┘  ▓ ║  │
                  ║ ▓▓▓▓▓▓▓▓ HALO ▓▓▓▓▓▓▓▓▓▓▓ ║  │
                  ╚════════════════════════════╝  ▼
                  ▲                              ▲
                  │                              │
                  Stone reveal (front 30 mm of cavity)
                  Halo strip is BEHIND this stone lip, glowing out
```

#### Component 1 — The monitor (Samsung LS22F320GAWXXL) — REVISED 2026-05-26

| Property | Value |
|---|---|
| Make / model | **Samsung LS22F320GAWXXL** (21.5" **IPS** FHD 120Hz, Essential S3 line) |
| Dimensions (no stand) | **489.9 × 291.9 × 36.2 mm** (was 491 × 291 × 49 mm on prior LS22F350) |
| Weight (no stand) | **1.6 kg** (was 2.3 kg on prior LS22F350 — 30% lighter, easier on rawl plugs) |
| VESA pattern | **100 × 100 mm** (was 75 × 75 mm — bracket spec changed accordingly) |
| Ports | Dual HDMI 1.4, no VGA, no speakers |
| Power | 230 V, ~25 W, via standard 5A plug |
| Mounting | Hangs from VESA 100 bracket on back wall; front face flush with stone face plane of cavity opening |
| Visible from foyer | Yes — the screen content is what visitors see |
| Cavity-depth clearance | **63.8 mm** free behind monitor (100 mm cavity − 36.2 mm monitor depth) — roomy for VESA bracket + RPi mounting + cable routing |
| **Status** | **ORDERED 2026-05-26** |

> **Why the swap from LS22F350:** The locked spec said "LS22F350 IPS" but Samsung's own datasheet confirms the LS22F350 is **TN panel**, not IPS — the locked doc was wrong. The LS22F320GAW is the modern Essential S3 replacement: genuine IPS, ₹2,500 cheaper (₹6,499 vs ₹9,000), 30% lighter, half the depth, dual HDMI, 120 Hz refresh. Trade-offs: VESA pattern is now 100×100 instead of 75×75 (any modern dual-pattern bracket handles both).

#### Component 2 — VESA bracket + anchor — REVISED 2026-05-26

| Property | Value |
|---|---|
| Bracket type | Slim flat-mount **VESA 100** (low profile, ~15 mm thick) — Speedio Universal Fixed Wall Mount or equivalent |
| Compatibility | Dual-pattern brackets supporting both VESA 75 and 100 work fine |
| Capacity | 15 kg (monitor is only 1.6 kg — 10× safety margin) |
| Anchor to wall | Either: (a) 4 rawl plugs + screws directly into masonry back wall, OR (b) small 8" × 4" × ½" plywood backing screwed to masonry first, then bracket to plywood. Electrician + carpenter choose on-site. |
| Position | Centred horizontally on cavity back wall; VESA centre at 57⅛" (1450 mm) FFL — exactly the monitor centre |
| Holds | The monitor's weight (1.6 kg) plus minor lateral force |
| **Status** | **ORDERED 2026-05-26** |

#### Component 3 — Components mounted to cavity back wall (the "brain")

All these stick to the cavity back wall with 3M VHB tape or zip ties to small anchors:

| Component | Size | Position |
|---|---|---|
| Raspberry Pi Zero 2W | 2½" × 1¼" × ¼" | Beside or below VESA bracket area |
| PoE splitter | 2" × 1½" × ¾" | Near RPi (Cat6 from conduit feeds in here) |
| Sonoff Mini R2 (Monitor socket control) | 1¾" × 1¾" × ⅞" | Inside the socket back box (NOT on the cavity wall — see Component 5 below) |
| USB sound card (for audio) | 1¼" × ½" × ¼" | Plugged into RPi's USB hub |
| PAM8403 amplifier | 1¼" × ¾" × ½" | On cavity back wall, beside speaker baffle |

#### Component 4 — Ceiling speaker (PRIMARY, revised 2026-05-22)

> **Revised 2026-05-22:** the original cavity speaker (Visaton FR 8) has been **DROPPED**. Reason: electrician (homeowner's nephew) flagged that a 3" diameter blind pocket in masonry is hard to plaster cleanly and unreliable. Decision: move the speaker to the ceiling instead. Trade-off accepted: lose the "voice-from-screen" effect; gain plaster reliability + simpler cavity work + the new LS22F320GAW monitor has **no built-in speakers anyway**, so an external speaker was always required. The 16 mm conduit previously provisioned as pull-string-only for a future ceiling speaker (was Component 4b) **is now active** with real speaker wire.

| Property | Value |
|---|---|
| Speaker type | 3" flush-mount ceiling speaker (8-ohm, ~5W), recessed B-type ceiling box. Brand: any decent quality (JBL Control 12C, Polk RC60i, or comparable Indian brand) |
| Position | **Centre of foyer false ceiling** (at ~9 ft FFL), midway between the 2 GU10 spotlights — ceiling rose box B-type, 60mm depth |
| Amp location | **Inside the cavity** with the RPi (PAM8403, stuck to back wall via 3M tape) — unchanged from prior design |
| Audio source | RPi Zero 2W → USB sound card → 3.5 mm cable → PAM8403 amp (inside cavity) |
| Speaker wire route | Amp output → 2-core 1.5 sqmm speaker wire → up through **Conduit #4** (16 mm grey, cavity top wall → false ceiling) → to ceiling speaker terminals |
| Direction speaker fires | DOWN into foyer (standard ceiling install) |
| Best for | Chimes + welcome voice + general audio + ambient music (better acoustics than cavity-bound speaker for fill sound) |
| Cost | ~₹1,800-3,000 (ceiling speaker) + ~₹150 (PAM8403) — amp + RPi unchanged |
| Cavity benefit | No speaker pocket needed in cavity back wall (drops the 3" dia × 1" pocket); more rear-gap space for components |

#### Component 5 — Cavity Socket Panel (on back wall) — REVISED 2026-05-22

> **Revised 2026-05-22:** upgraded from 2-module to **8-module** plate to give the Sonoff relay clean internal room and add a **Cat6 keystone jack** for the data conduit (proper structured-cabling termination). Both the power conduit AND the data conduit now terminate inside this box (data via the keystone). The +2 extra modules approach (electrician's recommendation, supersedes the old 65mm-depth mandate) lets us use a standard **50 mm-deep** box with extra width for the relay + wires instead of chasing hard-to-source 65 mm boxes.

| Property | Value |
|---|---|
| Plate | **8-module modular plate** (Schneider Unica champagne or matching brand), matte black face |
| Modules | 2× 5A sockets ("Monitor Socket A" and "Spare Socket B") + 1× Cat6 keystone jack (RJ45) + 5M blank/spare |
| Position | Cavity back wall, centred horizontally; **centre of plate at 53" (1346 mm) FFL** (low enough that monitor's bottom region covers it, high enough that wires reach the monitor's power port) |
| Back box | **8-module GI MS, ~440 × 75 × 50 mm** (or grid format if dealer offers — confirm exact dimensions). Recessed into cavity back wall by 50 mm. |
| Socket pocket cut in cavity back wall | **~7" × 3" × 2"** (~175 × 75 × 50 mm) — matches 8M box footprint, going further into masonry beyond the cavity back wall. (Wall capacity: 9" wall − 4" cavity − 2" socket pocket = 3" of masonry remaining behind — safe.) |
| Sonoff Mini R2 inside back box | One unit; wires inline between conduit Live and Socket A's Live terminal; switches only Socket A (monitor). Lives inside the box (clean) thanks to extra module width. |
| **Cat6 keystone jack (NEW 2026-05-22)** | RJ45 keystone (Cat6-rated, e.g., AMP/Commscope/D-Link keystone). The in-wall outdoor LSZH UV Cat6 from the niche terminates here (electrician punches it down). Short patch cable from keystone → PoE splitter input → RPi. |
| Socket A use | Powers the Samsung monitor adapter |
| Socket B use | Always-live spare (future use, RPi backup power, installer tools) |
| Why 8M | 2 sockets (2M each = 4M) + 1 keystone (2M) + 2M spare/relay-room = 8M total. Sound math, leaves room for the Sonoff relay + wire bends + future upgrade. |

#### Component 6 — Bezel camera (CAM-0)

| Property | Value |
|---|---|
| Camera | Raspberry Pi Camera Module 3 (~₹2,500) |
| Position | Top edge of the monitor bezel, centred horizontally |
| Mount | 3M VHB adhesive pad OR small 3D-printed bracket clipped to monitor top |
| Connection to RPi | CSI ribbon cable (~250 mm, comes with camera), runs DOWN the back of the monitor into the rear gap, plugs into RPi's CSI port |
| Purpose | Secondary face check at close range when a visitor is standing right at the welcome screen |
| Conduit needed | NONE — ribbon stays entirely inside the cavity |

#### Component 7 — Halo LED strip

**What this actually is (in plain words):**

The "Halo LED" is a flexible LED ribbon — a flat strip about 8-10 mm wide with tiny LED dots every ~15 mm along its length, with a sticky 3M backing on the underside. You buy it in a 5m roll, peel off the protective tape, and stick it to a clean wall surface. It looks like this:

```
   ┌──────────────────────────────────────────────┐
   │ ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  │  ← LED dots
   ├──────────────────────────────────────────────┤
   │   3M sticky backing (peel off, stick to wall)  │
   └──────────────────────────────────────────────┘
```

**Important: this is NOT a halo ring fixture or a halo spotlight.** When searching online, use the term **"24V LED strip 2200K"** or **"LED cove strip warm amber"** — not "halo light" (which finds different products).

| Property | Value |
|---|---|
| Type | Flexible LED strip (sticky-backed ribbon) |
| Voltage | 24V DC |
| Power density | 4.8 W/m |
| Colour temperature | 2200K (warm amber, like candle flame) |
| LED chip type | 5050 SMD or 2835 SMD (either works) |
| IP rating | IP20 (indoor, no waterproofing) |
| Dimmable | Yes (via the driver and/or Home Assistant) |
| Length needed for cavity | ~2 m (covers all 4 inner walls at the "step") |
| Length to buy | A 5m roll (use ~2m, keep ~3m as future accent or replacement) |
| Position in cavity | Stuck onto the inner walls of the wider deeper portion of the cavity, right at the 30 mm depth step. Points FORWARD toward foyer. |
| Hidden by | The stone reveal "lip" (the front 30 mm of stone-clad inner wall) blocks direct line of sight to the strip; only its glow reaches the foyer |
| Power | 24V DC from halo driver above false ceiling, via 16 mm grey conduit entering at the top-centre of cavity back wall |

**Where to buy in India (search terms + brand suggestions):**

| Search / source | Product to look for | Approx price |
|---|---|---|
| Amazon India | "24V LED strip 2200K dimmable 5m" | ~₹600-1500 for 5m roll |
| Mufasa LED (mufasaled.in) | 24V 2200K 4.8W/m IP20 strip | ~₹800-1200 |
| OREVA / similar Indian LED brand | 24V warm amber strip | ~₹600-900 |
| AliExpress (international, slower shipping) | "24V 2200K LED strip 5m" | ~₹400-600 |
| Local lighting store (Chitradurga) | "24V cove LED strip warm amber" — bring this document or a colour swatch | ~₹500-1000 |

**Note on the cove + shelf LEDs (same product family, different colour):**

The cove and shelf LED strips use the same product type but at **2700K** (warm white, not amber). 2700K is far more common locally than 2200K. So when shopping:
- **Halo (cavity):** 2200K — may need to order online (less commonly stocked locally)
- **Cove (false ceiling) + Shelf (under walnut shelf):** 2700K — widely available at local stores

### 7.6 — Sub-pockets cut INTO the cavity walls (REVISED 2026-05-22)

> **Revised 2026-05-22:** speaker pocket DROPPED (cavity speaker moved to ceiling — see Component 4). Socket pocket ENLARGED for the new 8M cavity socket panel. Only ONE sub-pocket now.

The electrician cuts ONE sub-pocket into the cavity back wall (beyond the main cavity cut):

| # | Pocket | Wall | Dimensions | Depth | Position |
|---|---|---|---|---|---|
| 1 | **Socket pocket** (for 8M cavity socket panel) | Cavity back wall | **~7" × 3"** (175 × 75 mm — matches 8M box footprint; confirm exact dims with dealer) | **2"** (50 mm) deep into masonry (50 mm box depth per the new "50mm + 2 extra modules" approach) | Centred horizontally; centre at 53" (1346 mm) FFL |
| ~~2~~ | ~~Speaker pocket~~ | — | — | — | **DROPPED 2026-05-22** — cavity speaker → ceiling speaker; pocket no longer needed |

Wall capacity check (single pocket now):

| Position | Depth used | Remaining masonry behind |
|---|---|---|
| Main cavity area | 4" | 5" |
| Socket pocket area | 4" + 2" = 6" | 3" |

Safe — minimum 3" of solid masonry remains behind the socket pocket.

### 7.7 — The 3 conduits entering the cavity

```
   [Front view of cavity BACK WALL — looking from foyer into the cavity,
    monitor removed, showing where conduits punch through]

                    ◄── 22¾" (raw cut) ──►
                  ┌─────────────────────────┐  ▲
                  │          ●               │  │
                  │       (top-centre)       │  │  ◄── Halo LED conduit
                  │       ⅝" (16 mm) grey    │  │     (from above false
                  │       PVC                │  │      ceiling, drops
                  │                          │  │      down through wall
                  │                          │  │      to here)
                  │       ┌──────┐           │  │
                  │       │ SKT  │           │  │  ◄── Socket pocket
                  │       │  3"×3"│          │  │     (cut INTO back
                  │       └──────┘           │  │      wall, 2½" deep,
                  │       (centred,          │  │      centre at 53" FFL)
                  │        at 53" FFL)       │  │
                  │                          │  │
                  │      ┌──────┐            │  │  ◄── Speaker pocket
                  │      │ SPK  │            │  │     (cut INTO back
                  │      │ ⊙ 3" │            │  │      wall, 1" deep,
                  │      └──────┘            │  │      centre at 57⅛" FFL)
                  │                          │  │
                  │  ●                    ●  │  ▼  ◄── Power (left) and
                  │ 1" (25 mm) RED      1" (25 mm) GREY  Data (right) conduits
                  │ (POWER, from East   (DATA, from West niche  enter at bottom
                  │  DB, bottom-LEFT     via floor, bottom-RIGHT  corners, 1½"
                  │  corner of back     corner of back wall)      up from bottom,
                  │  wall)                                        2" in from each side
                  └─────────────────────────┘
                     ▲                    ▲
                     EAST                 WEST
                     side                 side
```

| # | Conduit | Size | Colour | Entry point on cavity back wall | From |
|---|---|---|---|---|---|
| 1 | **POWER** | 1" (25 mm) | RED | **Bottom-LEFT corner** (East side of cavity) — 1½" up from bottom inner edge, 2" in from left inner edge | DB on East wall (Circuit B-Foyer-Cavity, via wall chase through SE corner) |
| 2 | **DATA** | 1" (25 mm) | GREY | **Bottom-RIGHT corner** (West side of cavity) — 1½" up from bottom inner edge, 2" in from right inner edge | Staircase niche on West (via floor route) |
| 3 | **HALO 24V** | ⅝" (16 mm) | GREY | **Top-CENTRE** of back wall — ¾" down from top inner edge, centred horizontally | Halo LED driver above false ceiling (drops down through wall) |
| 4 | **CEILING SPEAKER (future provision)** | ⅝" (16 mm) | GREY | **Top wall of cavity (the upper INNER wall, not the back wall)** — exits cavity going UP into the S wall toward false ceiling | Goes UP through S wall to false ceiling void (where future ceiling speaker will live). **Pull string only — no cable now.** |

**Conduit #4 detail:** unlike the other 3 conduits which enter the cavity through the BACK wall, conduit #4 exits the cavity through the TOP inner wall, going upward into the S wall toward the false ceiling. This is because it's destined for a future ceiling speaker (above false ceiling), not for a back-wall component. Length ~1.5 m. Cost ~₹100 in conduit + ~₹20 in pull string. If homeowner never adds a ceiling speaker, this conduit just sits unused — no harm.

All 4 conduit stubs protrude **1 to 1½ inches** into the cavity from the wall surface. All capped with masking tape until commissioning.

### 7.8 — Wiring inside the cavity (how everything connects)

**Power chain:**

```
   Conduit #1 (POWER, 25mm RED) enters at bottom-LEFT of back wall
        │
        │ wires inside conduit: 1× 2.5sqmm Red (Live) +
        │                        1× 2.5sqmm Black (Neutral) +
        │                        1× 2.5sqmm Green/Yellow (Earth)
        │
        ▼ wires routed up through cavity along the left inner wall edge
        │
        ▼ enter the Socket back box (in centre of back wall)
        │
   ┌────┴──────────────────────────────────────┐
   │  Inside the Socket back box:               │
   │                                            │
   │  L wire ──► Sonoff Mini R2 ──► Socket A Live (Monitor)    │
   │  L wire ──────────────────────► Socket B Live (Spare, always live) │
   │  N wire ──► Socket A Neutral + Socket B Neutral           │
   │  E wire ──► Socket A Earth + Socket B Earth + cavity      │
   │                                            metal earth bonding │
   └────────────────────────────────────────────┘
        │
        ▼ from Socket A: 230V → Samsung monitor's power adapter (via its plug)
        ▼ from Socket B: 230V always available for spare use
```

**Data + power for RPi chain:**

```
   Conduit #2 (DATA, 25mm GREY) enters at bottom-RIGHT of back wall
        │
        │ Cable inside: 1× outdoor LSZH UV Cat6
        │
        ▼ Cat6 routed up through cavity along the right inner wall edge
        │
        ▼ plugs into PoE splitter (mounted on back wall via 3M tape)
        │
   ┌────┴────────────────────────────────────┐
   │  PoE splitter output:                     │
   │                                           │
   │  RJ45 (data) ──► RPi via USB OTG          │
   │                  Ethernet adapter         │
   │                  (RPi's micro-USB port)   │
   │                                           │
   │  USB-C (5V power) ──► RPi power input     │
   └───────────────────────────────────────────┘
        │
        ▼ RPi powered + connected to network
        │
        ├──► Audio: USB sound card plugged into RPi USB hub
        │           ──► 3.5mm cable to PAM8403 amp
        │           ──► amp output to speaker
        │
        ├──► Video out: HDMI cable from RPi to monitor's HDMI input
        │              (~30 cm cable inside cavity)
        │
        └──► CAM-0: CSI ribbon (~250 mm) plugged into RPi's CSI port,
                     other end at monitor top bezel
```

**Halo LED chain:**

```
   Conduit #3 (HALO 24V, 16mm GREY) enters at top-CENTRE of back wall
        │
        │ Wires inside: 2-core 0.75 sqmm (24V DC + & DC -)
        │
        ▼ wires routed around the upper portion of cavity
        │
        ▼ connected to the halo LED strip's input terminals
        │
   ┌────┴──────────────────────────────────────┐
   │  Halo LED strip runs around all 4         │
   │  inner walls at the "step" (30 mm depth)  │
   │  where stone reveal ends:                  │
   │                                            │
   │  top run → right run → bottom run → left  │
   │  run → back to entry point                 │
   └────────────────────────────────────────────┘
```

### 7.9 — Painter scope inside the cavity

| Surface | Treatment | Order |
|---|---|---|
| Cavity back wall (all of it) | Matte black acrylic emulsion, 2 coats | After plaster, BEFORE stone cladding |
| Cavity inner walls (deeper than 30 mm, behind stone slip area) | Matte black acrylic emulsion, 2 coats | Same time as back wall |
| Cavity inner walls (front 30 mm portion, where stone slips will go) | DO NOT paint — stone goes here | — |
| VESA backing ply (if used) | Matte black, 1 coat | Before installation |
| MDF speaker baffle | Matte black, 1 coat | Before installation |

Critical: paint the cavity interior BEFORE stone cladding starts. Once stone is up, you can't paint cleanly inside.

### 7.10 — Stone cladder scope for Zone B

| Task | Detail |
|---|---|
| Main wall cladding | Apply rustic ledgestone (tobacco brown / sandstone beige / charcoal mix) to the 6 ft × 11 ft face of S feature wall |
| Cavity reveal slips | Apply 20 mm thick stone slips to the FRONT 30 mm of all 4 inner walls of the cavity. Stops cleanly at the 30 mm depth line. |
| Around cavity edge | The stone face of the wall meets the stone slip of the cavity reveal at the cavity front edge — creates a continuous stone "frame" around the monitor |
| What NOT to do | Don't apply stone deeper than 30 mm into the cavity — the rest of the interior is matte black (painter's domain). Don't block the conduit stubs at the back wall corners. Don't cover the socket or speaker pockets. |
| Adhesive | High-bond MS polymer adhesive + mechanical clips for stones over 5 kg |

### 7.11 — Carpenter scope for Zone B

| Item | Detail |
|---|---|
| MDF speaker baffle | 3½" × 3½" × ¼" with 3⅛" circular cutout for Visaton FR 8 driver. Paint matte black. |
| Optional VESA backing ply | If electrician + carpenter decide to use one: 8" × 4" × ½" BWP plywood, painted matte black, screwed to cavity back wall with 4 rawl plugs at corners. VESA bracket then attaches to ply. (Alternative: VESA bracket directly into masonry — no ply.) |
| Walnut floating shelf | Separately, below the cavity — 6 ft long × 10" deep × 1¼" thick, dark walnut finish. Top surface at 35⅜" (900 mm) FFL. Hidden steel brackets into masonry. Detail in Section 8 since this is on the S wall just outside the cavity area. |

### 7.12 — Pre-plaster sign-off for Zone B (Screen Cavity)

Before plaster + stone cladding starts on the S feature wall:

- [ ] Cavity cut to **22¾" × 14⅞" × 4"** (580 × 380 × 100 mm) with chalk-line accuracy
- [ ] Cavity centred on 6 ft feature wall: 24⅝" from each side edge
- [ ] Bottom edge of cavity at 50½" (1280 mm) FFL — verified with tape from FFL chalk line
- [ ] Socket pocket cut: **~7" × 3" × 2"** deep (8M box, revised 2026-05-22), centred horizontally, centre at 53" FFL
- [ ] ~~Speaker pocket~~ **DROPPED 2026-05-22** — cavity speaker moved to ceiling; no speaker pocket needed
- [ ] Conduit #1 (Power) entry hole: 1" diameter, bottom-LEFT corner, 1½" up + 2" in
- [ ] Conduit #2 (Data) entry hole: 1" diameter, bottom-RIGHT corner, 1½" up + 2" in
- [ ] Conduit #3 (Halo) entry hole: ⅝" diameter, top-CENTRE, ¾" down from top
- [ ] All 3 conduit stubs protrude 1-1½" into cavity, capped with masking tape, draw strings inserted, labelled
- [ ] Stone cladder briefed on the 30 mm reveal depth specification — both verbally + with marked tape line inside cavity
- [ ] Painter briefed: do NOT paint the front 30 mm of inner walls (stone goes there); DO paint the rest matte black
- [ ] All cavity dimensions photographed before plaster crew arrives
- [ ] Homeowner sign-off photographed

---

## SECTION 8 — North wall (Zone C): Switch Panel, Door, Window

The North wall is the exterior wall facing the porch. It's **9.5 ft (2895 mm) long**, **9" thick (228 mm)**, and contains the main door, a corner window, the Foyer Switch Panel, and (on its outside face — covered in Section 10) the Hikvision doorbell.

### 8.1 — N wall geometry overview

```
   [Looking at the N wall from inside the foyer (looking NORTH toward porch)]

   ◄────────── N wall total length: 9'6" (2895 mm) ──────────►
   
   W corner ◄────────────────────────────────────────► E corner
   
   ◄── 3'6" ──►◄── 1'6" ──►◄────────── 4'6" ──────────►
     window     wall section    door zone (door + vascal)
              (Foyer Switch
               Panel home)
   
   ┌────────────┬───────────┬───────────────────────────┐
   │            │           │                            │
   │ CORNER     │  WALL     │                            │
   │ WINDOW     │ (Foyer    │   MAIN DOOR                │
   │ 3.5 ft     │  Switch   │  (3.2 ft wide,             │
   │ wide       │  Panel    │   hinged on EAST jamb,     │
   │            │  on inside│   swings against E wall)   │
   │ Sill at    │  face;    │                            │
   │ 3 ft FFL   │ Hikvision │                            │
   │            │  doorbell │   PLUS vascal (~1'4") on   │
   │ Height     │  on       │   East side of door —      │
   │ 5 ft       │  outside  │   the wall return between  │
   │            │  face)    │   door frame and E wall    │
   │ Wraps NW   │           │   corner                   │
   │ corner     │           │                            │
   │ extending  │           │                            │
   │ North      │           │                            │
   └────────────┴───────────┴───────────────────────────┘
```

**Key numbers (from W corner going E):**

| Section | E-W width | Detail |
|---|---|---|
| Corner window | 3'6" (1066 mm) | West side; wraps NW corner extending North |
| Wall section (Foyer Switch Panel home) | 1'6" (457 mm) | Between window and door — where 4-gang switch panel goes (inside) + Hikvision doorbell (outside) |
| Door zone (door + vascal) | 4'6" (1372 mm) | Door 3.2 ft wide + vascal ~1'4" on East side |
| **TOTAL** | **9'6" (2895 mm)** | Matches N wall length |

### 8.2 — Main door specifications

| Property | Value |
|---|---|
| Width | 3'2" (~975 mm) |
| Type | Solid teak (existing per architectural plan) |
| Hinge side | **EAST** (right jamb when viewed from foyer side looking out) |
| Latch side | **WEST** (left jamb when viewed from foyer side looking out) |
| Swing direction | Opens INTO the foyer; door panel swings against the East exterior wall |
| Frame finish | Stained to match windows (per interior design plan) |
| Header / lintel height | 8 ft (2438 mm) FFL — top of door frame |

### 8.3 — Corner window specifications

| Property | Value |
|---|---|
| Width on N wall | 3'6" (1066 mm) — the West-most 3.5 ft of N wall |
| Wraps corner | YES — continues around the NW corner of the foyer, extending North along the Living area's exterior wall |
| Sill height (bottom of window) | 3 ft (914 mm) FFL |
| Top of window | 8 ft (2438 mm) FFL (top of window matches door header) |
| Height of window opening | 5 ft (1524 mm) |
| Frame | TBD by carpenter / homeowner (likely powder-coated aluminium or wooden frame) |

### 8.4 — Vascal (East door return)

| Property | Value |
|---|---|
| Position | Between the East jamb of the main door and the East exterior wall corner |
| Width | ~1'4" (~400 mm) — part of the 4'6" door zone, minus the 3'2" door width |
| Function | Structural wall return; provides space for the door header + visual separation between door and East wall corner |
| Outside face | Plastered + painted to match porch (no fittings) |
| Inside face | Plastered + painted to match foyer (no fittings) |

**Note:** the homeowner mentioned a possible decorative door grill on the East jamb side. If installed, it goes on the OUTSIDE face of the vascal area, not affecting electrical work.

### 8.5 — Foyer Switch Panel position + back box (REVISED 2026-05-23 — 18M cavity as cut on site)

The Foyer Switch Panel is the main lighting control for the foyer. It sits in the 1'6" wall section between the door (East) and the window (West) — the only continuous wall section on the N wall.

> **Revision 2026-05-23**: electrician cut an **18M vertical cavity** on site (longer side oriented top-to-bottom). The original 6-gang horizontal box (335 × 75 × 65) has been superseded by the 18M vertical cavity. This is the **electrician's "+2M-per-Sonoff" rule in action** — 6 hidden Sonoffs need ~12M of slack space inside the box for clean wire-bending and the neutral bus. See [conduits-and-cavities.md § 0.4b](conduits-and-cavities.md#04b--plate-size-sizing-rule-for-hidden-sonoff-boards-2m-per-sonoff).

| Property | Value |
|---|---|
| Wall | N wall, 1'6" section (between door East and window West) |
| Position on the 1'6" section (centred) | Centred horizontally — measure actual wall width on-site and centre accordingly |
| Centre height (FFL) | **1200 mm (47¼")** — standard switch height |
| Back box | **18M vertical GI MS, ~290 × 135 × 65 mm OR 225 × 195 × 65 mm** (as cut on site by electrician) |
| Orientation | **VERTICAL** — longer side runs top-to-bottom; 6 rockers stack as 2 rows × 3 columns or 3 rows × 2 columns |
| Box depth requirement | **65 mm deep — mandatory** (verify with tape; electrician committed to "at least 2 inches" = ~50 mm — must be 65 mm for 6 hidden Sonoffs) |
| Plate brand | **Schneider Unica 18M plate** (matching same brand used house-wide for uniform finish) |
| Wall capacity check | 1'6" = 457 mm wide; vertical 18M is 135 mm wide → **322 mm of horizontal wall spare** (fits with huge margin) |
| Vertical span | 18M vertical plate spans ~295 mm top-to-bottom around the 1200 mm FFL centre → top rocker at ~1350 mm, bottom rocker at ~1050 mm (reachable but tall — guests find by feel) |

**Slack rationale (don't reduce the box):**
- 6 smart gangs × 2M slack each = 12M of slack inside
- 6 hidden Sonoff ZBMINI R2 modules + 6 sets of L/N/S1 wires + earth + neutral bus = needs every bit of that slack
- 12M slack also gives a future-proof buffer: a 7th or 8th smart gang can be added later without re-cutting the cavity

### 8.6 — Gang assignments (6-gang default; 7 & 8 spare if larger box fits)

| Gang | Label | Controls | Circuit |
|---|---|---|---|
| **1 (leftmost — closer to window)** | "Foyer Spots" | 2× GU10 ceiling spotlights | B-Foyer-Lights, branch to spots |
| **2** | "Cove + Halo" | Cove LED 2700K + Cavity Halo LED 2200K — **linked** (one gang switches both) | B-Foyer-Lights, branch to cove driver + halo driver |
| **3** | "Shelf" | Walnut floating shelf under-LED strip | B-Foyer-Lights, branch to shelf LED |
| **4** | "Foyer Spare" | Future foyer addition (capped, wires looped) | B-Foyer-Lights, spare run |
| **5** | "Porch Ceiling" | Porch ceiling light(s) | B-Foyer-Lights, branch to porch ceiling |
| **6 (rightmost in 6-gang setup — closer to door)** | "Porch Wall" | Porch wall light(s) — provisioned for future | B-Foyer-Lights, branch to porch wall area (capped if no fitting now) |
| **7 (IF 7-gang installed)** | "Spare 7" | Future use (capped) | spare |
| **8 (IF 8-gang installed)** | "Spare 8" | Future use (capped) | spare |

### 8.7 — Wires inside the Foyer Switch Panel back box

```
   [Inside the 4-gang back box, layout from above looking down]
   
   ┌─────────────────────────────────────────────────────┐
   │                                                       │
   │  Incoming feed from DB (Conduit C-DB-Foyer-Switch):   │
   │  - Live (red, 1.5 sqmm)                                │
   │  - Neutral (black, 1.5 sqmm)                           │
   │  - Earth (green/yellow, 1.5 sqmm)                      │
   │                                                       │
   │  ┌─────────────────────────────────────────────────┐  │
   │  │ 6× SONOFF ZBMINI R2 (Zigbee) — hidden behind     │  │
   │  │ the Schneider Unica plate, one per smart gang.   │  │
   │  │ Each module sits inline between Live IN and the  │  │
   │  │ gang's Live OUT — allows HA to remotely control  │  │
   │  │ that gang's load via the staircase-niche Zigbee  │  │
   │  │ coordinator (Sonoff Dongle Plus on Beelink HA).  │  │
   │  │                                                   │  │
   │  │ Wiring identical for ALL gangs — detach-mode     │  │
   │  │ (decoupling rocker from relay) is a post-pair    │  │
   │  │ HA setting, not a wiring change.                  │  │
   │  └─────────────────────────────────────────────────┘  │
   │                                                       │
   │  Gang 1: Live in → Sonoff → out to "Spots" conduit    │
   │  Gang 2: Live in → Sonoff → out to "Cove+Halo" conduit│
   │  Gang 3: Live in → Sonoff → out to "Shelf" conduit    │
   │  Gang 4: Live in → Sonoff → out to "Spare" (capped)   │
   │                                                       │
   │  Shared Neutral and Earth go to all 4 outgoing        │
   │  conduits (the Sonoff doesn't switch N or E)          │
   │                                                       │
   │  Each smart-switch gang gets:                          │
   │  - 300 mm tail of L + N + E wires capped inside box   │
   │    (so module can be inserted later by homeowner)     │
   │                                                       │
   └─────────────────────────────────────────────────────┘
```

### 8.8 — Conduits IN and OUT of the Foyer Switch Panel

| Conduit ID | Size | Colour | Direction | Route | Carries |
|---|---|---|---|---|---|
| **C-DB-Foyer-Switch** | 25 mm | RED | INCOMING (from DB) | Up E wall → false ceiling → across to N wall → drops to back box | Feed: L + N + E |
| **C-SW-Spots** | 25 mm | RED | OUTGOING (Gang 1 → spots) | Up N wall → false ceiling → to 2 spotlight boxes | Switched live + shared N + E |
| **C-SW-Cove-Halo** | 25 mm | RED | OUTGOING (Gang 2 → cove driver + halo driver) | Up N wall → false ceiling → splits to cove + halo drivers | Switched live + shared N + E |
| **C-SW-Shelf** | 16 mm | RED | OUTGOING (Gang 3 → shelf LED) | Down N wall → floor route → up S wall → to shelf area | Switched live (230V) + N + E to shelf driver location (Option 1 or 2 — see 8.9) |
| **C-SW-Spare** | 16 mm | RED | OUTGOING (Gang 4 → spare, future) | Up N wall → false ceiling → terminated capped | Spare with pull string |
| **C-SW-Porch-Ceiling** (NEW) | 16 mm | RED | OUTGOING (Gang 5 → porch ceiling light) | Up N wall → through 9" wall → exits outside → up to porch ceiling fitting | Switched live + N + E |
| **C-SW-Porch-Wall** (NEW) | 16 mm | RED | OUTGOING (Gang 6 → porch wall light, future) | Up N wall → through 9" wall → exits outside near door at ~1900-2100 mm FFL | Pull string only (capped) until porch wall light is chosen |
| **C-SW-Spare-7** (IF 7-gang installed) | 16 mm | RED | OUTGOING (Gang 7) | Up N wall → false ceiling → terminated capped | Spare, pull string only |
| **C-SW-Spare-8** (IF 8-gang installed) | 16 mm | RED | OUTGOING (Gang 8) | Up N wall → false ceiling → terminated capped | Spare, pull string only |

### 8.9 — Walnut floating shelf (physically on S wall, electrically wired from Switch Panel Gang 3)

The walnut floating shelf is physically mounted on the S feature wall directly below the cavity. Its under-LED strip is electrically powered by the foyer lighting circuit, controlled by Foyer Switch Panel Gang 3.

| Property | Value |
|---|---|
| Material | Solid walnut (or veneered MDF if budget-constrained) |
| Dimensions | 6 ft wide × 10" deep × 1¼" thick (1828 × 254 × 32 mm) |
| Top surface height (FFL) | **900 mm (35⅜")** |
| Mounting | Hidden steel L-brackets into S wall masonry (4 anchors, ~24" apart) |
| Under-LED strip | 24V, 6 W/m, 2700K, length matches shelf (6 ft / 1.8 m) |
| Estimated cost | Shelf ~₹4,500 (carpentry + walnut) + LED ~₹1,500 + driver ~₹600 |

**LED driver location — TWO OPTIONS (electrician chooses on-site):**

| Option | Driver location | Pros | Cons |
|---|---|---|---|
| **Option 1 (default)** | Above false ceiling, alongside cove + halo drivers (shared inspection hatch) | All 3 LED drivers in one accessible spot; central service location | 24V cable runs from above-ceiling driver DOWN through S wall to under-shelf strip — longer cable, needs a small vertical chase in S wall |
| **Option 2 (alternative)** | Hidden BEHIND or UNDER the walnut shelf itself | Very short 24V cable run from driver to strip (~6" / 150 mm); easier to access if driver fails (just remove shelf bracket cover) | Driver heat dissipation tighter — needs small ventilation gap or perforated shelf-back; 230V wire must reach the shelf area (via C-SW-Shelf conduit which already goes there) |

In **Option 1**, the C-SW-Shelf conduit carries 230V switched live + N + E up to the above-ceiling driver; then the driver's 24V output drops down through a separate small chase or conduit to the under-shelf strip.

In **Option 2**, the C-SW-Shelf conduit carries 230V switched live + N + E directly to the shelf area (via floor route as already specified); the driver lives under the shelf; 24V output goes directly into the strip beside it.

**Carpenter note:** install shelf AFTER stone cladding is complete on the S wall. The shelf brackets penetrate the stone-clad wall — use long anchor bolts that grip the masonry behind the stone. If Option 2 is chosen, leave a small ventilation gap (~10 mm) behind the shelf for driver heat dissipation.

### 8.10 — Pre-plaster sign-off for Zone C (N wall)

- [ ] N wall total length verified (~9'6" / 2895 mm) — measure actual on-site, may vary slightly
- [ ] Door opening cut to 3'2" wide × 7 ft tall (matching existing door)
- [ ] Window opening cut to 3'6" wide × 5 ft tall (with corner wrap)
- [ ] Vascal wall section confirmed (~1'4" on East side of door)
- [ ] 1'6" wall section between door and window confirmed
- [ ] Foyer Switch Panel back box installed: **18M vertical GI MS, ~290 × 135 × 65 mm (or 225 × 195 × 65 mm)**, centred horizontally in 1'6" section, centre at 1200 mm FFL — **confirm 65 mm depth with tape before plaster**
- [ ] 6× Schneider Unica 1-module rocker insert positions reserved in the 18M frame; remaining 12 module slots stay blank (slack for 6× Sonoff ZBMINI R2 + wiring)
- [ ] C-DB-Foyer-Switch conduit terminated at back box (incoming feed)
- [ ] 4 outgoing conduits (Spots, Cove+Halo, Shelf, Spare) routed from back box to their destinations
- [ ] Draw strings in all 5 conduits
- [ ] All conduit ends capped with masking tape
- [ ] Hikvision doorbell back box installed on OUTSIDE face of 1'6" section (see Section 10 for spec)
- [ ] Homeowner sign-off photographed

---

## SECTION 9 — Foyer ceiling (Zone D): Spotlights, Cove, Drivers

The foyer ceiling drops from the raw slab at 11 ft FFL to a false ceiling at 9 ft FFL (2 ft drop). The false ceiling space hides the LED drivers and houses the inspection hatch. Two GU10 spotlights are recessed into the false ceiling, and a cove LED strip runs around the perimeter.

### 9.1 — False ceiling specifications

| Property | Value |
|---|---|
| **Slab height (raw)** | 11 ft (3353 mm) FFL |
| **False ceiling height (finished)** | 9 ft (2743 mm) FFL |
| **Drop from slab** | 2 ft (610 mm) |
| **Material** | 12.5 mm gypsum board on GI grid |
| **Coverage** | Full foyer area (~9.5 ft × 5 ft N-S in the foyer rectangular area; transitions into Living area at the 3.5 ft open passage edge) |
| **Cove pocket** | 100 mm wide × 75 mm deep around full perimeter — built INTO the false ceiling at the rim |

### 9.2 — Inspection hatch

| Property | Value |
|---|---|
| Size | 300 × 300 mm (12" × 12") |
| Position | Above the W edge of the foyer false ceiling (near where the foyer transitions to Living) |
| Why this position | Close to where the LED drivers sit; doesn't disrupt the central foyer ceiling visual |
| Hatch type | Standard plasterboard inspection hatch with magnetic catch + flush trim |
| Cost | ~₹500 |

Above the hatch (in the void) sit:
- Cove LED driver (Meanwell APV-100-24 or equivalent, ~₹1,500)
- Halo LED driver (Meanwell APV-12-24, ~₹600)
- Walnut shelf LED driver (Meanwell APV-12-24, ~₹600)
- Junction boxes for 230V splits + 24V terminations

### 9.3 — GU10 ceiling spotlights

The 2 spotlights "graze" the stone feature wall — they're aimed at an angle to catch the texture of the rustic stone, creating shadows that emphasise the wall's roughness. Critical for the visual effect; they're not general room lighting.

**Important: GU10 LED bulbs do NOT need a separate driver.** Each GU10 bulb has driver electronics built INTO the bulb itself. They run on 230V AC mains directly. So unlike the cove, halo, and shelf LEDs (which need 24V drivers), the GU10 spots wire directly from the Foyer Switch Panel Gang 1 to the GU10 socket in the ceiling. No driver brick needed anywhere.

| Property | Value |
|---|---|
| Fitting type | Recessed GU10 gimbal (adjustable angle), 7W LED bulb, 2700K, CRI 90+ |
| Beam type | 30° narrow flood (adjustable) |
| Position #1 (closer to East side) | 300 mm from W wall area (i.e., 300 mm from the side opposite the cavity), **609 mm from N edge** of foyer |
| Position #2 (closer to West side) | 300 mm from W wall area, **1218 mm from N edge** of foyer (or 609 mm from S edge) |
| Aim | Each spot aimed at a point on the S feature wall at ~1700 mm FFL; centre of beam ~300 mm out from the wall face |
| Ceiling cut-out | Standard GU10 trim cut-out, ~85 mm diameter |
| Ceiling box (above false ceiling) | B-type, 60 mm depth |
| Wire | **Direct 230V from Gang 1** of Foyer Switch Panel (switched live + N + E) — no driver in the path |
| Driver needed? | **NO** — built into the GU10 bulb |

### 9.4 — Cove LED strip

The cove strip runs around the full perimeter of the foyer false ceiling, hidden inside the 100 mm wide × 75 mm deep cove pocket built INTO the rim of the false ceiling. The strip points UPWARD; light bounces off the slab above and creates an indirect warm wash.

| Property | Value |
|---|---|
| Strip | 24V DC, 9.6 W/m, 2700K, CRI 90+, IP20 (indoor) |
| Length | ~10 m (perimeter of foyer false ceiling) |
| Routing inside cove pocket | One continuous run, starts and ends at the driver location |
| Total power | ~96 W — well within the 100W driver capacity |
| Driver | Mean Well APV-100-24 (~₹1,500), above false ceiling |
| Wire from driver to strip | 2-core 1.5 sqmm 24V cable, runs along cove pocket to strip start point |
| Control | Switched by Gang 2 of Foyer Switch Panel (linked with Halo LED) |

### 9.5 — Halo LED driver

| Property | Value |
|---|---|
| Driver | Mean Well APV-12-24 (12W, 24V output, ~₹600) |
| Position | Above false ceiling, beside the cove driver, on a small shelf or zip-tied to slab anchor |
| Primary side (230V incoming) | From the same source as cove driver (Gang 2 of switch panel) — they share the switched live |
| Secondary side (24V outgoing) | 2-core 0.75 sqmm cable, routes through 16 mm grey conduit down to top-centre of cavity back wall (Conduit #3 — see Section 7) |

### 9.6 — Walnut shelf LED driver (Option 1 above-ceiling location)

| Property | Value |
|---|---|
| Driver | Mean Well APV-12-24 (12W, 24V output, ~₹600) |
| Position (Option 1 — default) | Above false ceiling, beside the cove + halo drivers (all 3 drivers in same area for easy access via inspection hatch) |
| Position (Option 2 — alternative) | Hidden behind or under the walnut shelf itself (shorter 24V run; needs small ventilation gap; see Section 8.9 for trade-off detail) |
| Primary side (230V incoming) | From Gang 3 of Foyer Switch Panel via C-SW-Shelf conduit |
| Secondary side (24V outgoing) | 2-core 0.75 sqmm cable to the shelf strip — route depends on which option is chosen |

**Choose Option 1 OR Option 2 on-site based on what's easier to install. Either works; pros/cons documented in Section 8.9.**

### 9.7 — Above-ceiling layout (the "driver shelf")

```
   [Top-down view of false ceiling void above the inspection hatch]
   
   ┌─────────────────────────────────────────┐
   │                                          │
   │   ◄── 600 mm wide shelf ──►              │
   │   ┌─────────────────────────┐            │
   │   │  ┌────┐ ┌────┐ ┌────┐  │            │
   │   │  │COVE│ │HALO│ │SHELF│ │            │
   │   │  │drv │ │drv │ │drv  │ │            │
   │   │  │100W│ │12W │ │12W  │ │            │
   │   │  └────┘ └────┘ └────┘ │            │
   │   │                         │            │
   │   │  Plus: junction boxes   │            │
   │   │  for 230V split, 24V    │            │
   │   │  terminations           │            │
   │   └─────────────────────────┘            │
   │              │                            │
   │              ▼ Below = inspection hatch    │
   │              (300 × 300 mm)               │
   │                                          │
   └─────────────────────────────────────────┘
```

### 9.8 — Pre-plaster sign-off for Zone D (Foyer ceiling)

- [ ] False ceiling drop confirmed at 2 ft (from 11 ft slab to 9 ft FFL)
- [ ] Cove pocket dimensions confirmed: 100 mm wide × 75 mm deep, around full perimeter
- [ ] Inspection hatch position marked (300 × 300 mm, W edge of foyer ceiling)
- [ ] 2× GU10 ceiling box positions marked (with chalk, on raw slab)
- [ ] All conduits arriving at false ceiling area terminated and labelled (incoming from switch panel: C-SW-Spots, C-SW-Cove-Halo; outgoing to cavity: C-Halo-24V down to cavity top-centre)
- [ ] Driver shelf location marked (above inspection hatch)
- [ ] Cove strip routing path inside cove pocket confirmed (continuous, ~10m loop)
- [ ] Homeowner sign-off photographed

---

## SECTION 10 — Porch (Zone E) + Staircase indoor area (Zone F): External conduits and routes

> ⚠️ **DOORBELL BRAND CHANGED 2026-05-22:** the doorbell is the **Hikvision DS-KV6113-WPE1(C)** (it replaced the originally-specced Reolink Video Doorbell PoE — same install spot, same Cat6 PoE wiring, same mounting position; different brand + model). The body below now names the Hikvision throughout; a few "Reolink" mentions remain only where the physical install detail still needs re-verification against the Hikvision datasheet. The Hikvision is 2MP/1080p, 131° FOV, 120dB WDR, PoE, IP65, supports continuous RTSP + ONVIF for Frigate. Use accessory **DS-KABV6113-A** for theft-resistant mount; built-in TAMPER alarm. Same dealer (I Secure India, Chitradurga). The DS-KAW50-1 / DS-KABV6113-RS / DS-KAW50-1N are other compatible accessories (rain shield / surface back box / power supply — see datasheet).
>
> **Why the swap:** datasheet-confirmed RTSP/ONVIF for Frigate 24/7 (the original Reolink concern about press-only streaming is moot — the Hikvision streams continuously); same brand as CAM-3/4/5 for unified NVR ecosystem. See decision log 2026-05-22 entry.
>
> Detailed back-box dimensions in the install procedure below (3" × 3" × 2½" GI MS modular, recessed flush) — those dimensions still apply; only the doorbell unit + bracket brand changed.

This section covers everything outside the foyer plus the Waveshare indoor unit conduit. All conduits in this zone originate at the **staircase niche** (the server cupboard on the West side of the house) and route to various endpoints.

### 10.1 — Porch geometry recap

| Property | Value |
|---|---|
| **E-W length** | 13 ft (3962 mm) |
| **N-S depth (out from house)** | 7.3 ft (2225 mm) |
| **Roof** | Yes — underside of FF balcony slab forms the porch ceiling |
| **Lintel height (door header)** | 8 ft (2438 mm) FFL |
| **Porch ceiling height (under FF slab)** | ~10 ft (3000 mm) approx — confirm on-site |
| **Boundaries** | E: neighbour's exterior wall; W: ~4'9" of Living Area exterior wall, then open passage to compound; N: open to compound (gate ~7.5 ft north) |

### 10.2 — Staircase niche (origin point for all external conduits)

The niche is the existing server cupboard on the West side of the house, in the staircase area. It already houses:
- Beelink EQ12 (Home Assistant + Frigate + CompreFace)
- TP-Link TL-SG1210P PoE switch (8 PoE ports)
- TP-Link AX55 Wi-Fi router
- 12-port Cat6 keystone patch panel
- UPS

All conduits in this zone start at this niche and route OUT to various external endpoints.

### 10.3 — The 5 conduits from the niche (overview)

**3 conduits go via floor route, 1 via ceiling route, 1 is a short vertical run on the niche wall.**

```
   [Map of conduits originating at the staircase niche, going to their endpoints]

   Staircase niche (West side, ~700 mm FFL)
        │
        ├──► 1. C-Niche-Cavity-Data — to FOYER CAVITY (data + PoE for RPi)
        │       PRIMARY: floor route — down to floor → under floor East → up S wall →
        │                                cavity bottom-right
        │       Length ~10 m
        │
        ├──► 2. C-Niche-Doorbell — to HIKVISION DOORBELL on N wall 1'6" section (outside face)
        │       PRIMARY: floor route — down to floor → under floor East-then-N → up N wall →
        │                                exits through N wall to outside face at 1450 mm FFL
        │       Length ~7 m
        │
        ├──► 3. C-Niche-CAM1 — to CAM-1 SPARE on porch W wall (capped, future)
        │       PRIMARY: floor route — down to floor → under floor East across Living area →
        │                                up Living's E wall to 1650 mm FFL → exits to porch W
        │       Length ~7 m (pull string only)
        │
        ├──► 4. C-Niche-CAM2 — to CAM-2 STUB on porch soffit NE corner (capped, future)
        │       PRIMARY: ceiling route — up niche wall → above false ceiling → North →
        │                                  through N exterior wall → into porch soffit area →
        │                                  terminates at NE corner of soffit ~2700 mm FFL
        │       (Floor route NOT viable — destination is at ceiling level)
        │       Length ~7 m (pull string only)
        │
        └──► 5. C-Niche-Waveshare — to WAVESHARE STUB on staircase S wall (indoor, ~1500 mm FFL)
                Short vertical run — up the niche wall to 1500 mm FFL on same wall
                Length ~1-2 m
```

**Floor-route advantage:** since 3 of 5 conduits go via floor (Cavity, Doorbell, CAM-1), they can share the same floor chase from the staircase niche going East. The electrician digs ONE channel in the floor screed and lays 3 conduits side-by-side in it. More efficient than 3 separate routes.

**⚠️ Critical timing:** all 3 floor-route conduits MUST be laid in the floor screed BEFORE the tile contractor arrives. Once tiles go down, no more floor conduits can be added.

### 10.4 — Conduit details

#### Conduit C-Niche-Cavity-Data (foyer cavity Cat6, via floor)

| Property | Value |
|---|---|
| ID | C-Niche-Cavity-Data |
| Size | 25 mm (1") |
| Colour | GREY (LV-25) |
| From | Staircase niche, ~700 mm FFL on the niche back wall (next to patch panel) |
| Route | Down from niche to floor level → horizontal under-floor (in floor screed, ~25 ft East) → reaches S wall under floor → vertical climb up S wall (~50½" up) → enters cavity bottom-right corner of back wall |
| To | Cavity bottom-RIGHT corner of back wall (West side of cavity) |
| Cable inside | 1× outdoor LSZH UV-resistant Cat6 |
| Length | ~10 m |
| Critical timing | **Floor segment MUST be laid before tiles** — coordinate with tile contractor |

#### Conduit C-Niche-Doorbell (Hikvision doorbell Cat6)

| Property | Value |
|---|---|
| ID | C-Niche-Doorbell |
| Size | 25 mm (1") |
| Colour | GREY (LV-25) |
| From | Staircase niche |
| **PRIMARY route (default — via floor)** | Down from niche to floor level → under floor East-then-N (shares floor chase with C-Niche-Cavity-Data and C-Niche-CAM1) → up the N wall to 1450 mm FFL → exits through N wall to OUTSIDE face at the doorbell mount position |
| Secondary route (alternative — via false ceiling) | Up niche wall to false ceiling level → across foyer false ceiling area toward N wall → drops down INSIDE N wall (1'6" section between door and window) → exits through N wall to the OUTSIDE face |
| Route choice | **Use floor route as primary**, since it shares chase with the other 2 floor-route conduits (Cavity Cat6 and CAM-1 spare). Falls back to ceiling route only if floor is not viable on-site. |
| To | Outside face of 1'6" N wall section, **1450 mm (57") FFL** — back box per Section 10.5 spec (electrician's discretion on exact box brand/size) |
| Cable inside | 1× outdoor LSZH UV-resistant Cat6 (cable PULLED — Hikvision doorbell installed) |
| Length | ~7 m (floor route) or ~5 m (ceiling route, if used) |

#### Conduit C-Niche-CAM1 (CAM-1 spare conduit, no camera now)

| Property | Value |
|---|---|
| ID | C-Niche-CAM1 |
| Size | 25 mm (1") |
| Colour | GREY (LV-25) |
| From | Staircase niche |
| **PRIMARY route (default — via floor)** | Down from niche to floor → under floor East across Living area (shares floor chase with C-Niche-Cavity-Data and C-Niche-Doorbell) → up the Living E exterior wall (= porch W wall) to 1650 mm FFL → exits through wall to outside (porch West side) at face level |
| Secondary route (alternative — via false ceiling) | Up niche wall to false ceiling → across Living false ceiling area going N → reaches Living E exterior wall → drops down inside this wall → exits through wall to outside (porch West side) at face level |
| Route choice | **Use floor route as primary**, since it shares chase with the other 2 floor-route conduits. Falls back to ceiling route only if floor is not viable on-site. |
| To | **Porch West wall**, 1650 mm (65") FFL — weatherproof back box, capped, no camera |
| Cable inside | NONE NOW — pull string only |
| Length | ~7 m (floor route) |
| Purpose | Future upgrade: if face recognition via doorbell becomes inadequate, pull Cat6 through this conduit and install Hikvision DS-2CD2143G2-LU (or equivalent PoE camera) on porch W wall |

#### Conduit C-Niche-CAM2 (CAM-2 stub, no camera now)

| Property | Value |
|---|---|
| ID | C-Niche-CAM2 |
| Size | 25 mm (1") |
| Colour | GREY (LV-25) |
| From | Staircase niche |
| Route | Up niche wall → above false ceiling → North → through N exterior wall → into porch soffit area (the underside of the FF balcony slab) → terminates at the NE corner of the porch soffit |
| To | Porch soffit NE corner, ~2700 mm (~8'10") FFL — weatherproof IP67 back box, capped, no camera |
| Cable inside | NONE NOW — pull string only |
| Length | ~7 m |
| Purpose | Future upgrade: porch overview camera (wide 2.8 mm lens, for context/security, not face ID). Pull Cat6 through conduit when ready. |

#### Conduit C-Niche-Waveshare (indoor unit, Zone F)

| Property | Value |
|---|---|
| ID | C-Niche-Waveshare |
| Size | 25 mm (1") |
| Colour | GREY (LV-25) |
| From | Staircase niche (top of niche, ~1200 mm FFL) |
| Route | Short vertical run up the staircase S wall (the same wall as the niche), to the Waveshare position above |
| To | **Staircase S wall, ~1500 mm (59") FFL** — back box for Waveshare touchscreen mount (carpenter builds the exact mount frame later) |
| Cable inside | 1× outdoor LSZH UV-resistant Cat6 (cable PULLED, ready for future Waveshare install) |
| Length | ~1-2 m |
| Note | Waveshare hardware design (touchscreen + Pi 4 + PoE HAT + mount frame) deferred to a separate session. Conduit + Cat6 ready when homeowner is ready. |

### 10.5 — Hikvision doorbell installation procedure (step-by-step)

The Hikvision DS-KV6113-WPE1(C) Video Doorbell PoE mounts on the OUTSIDE face of the 1'6" N wall section. This is the most precise install in the foyer plan. Follow these steps exactly.

> ⚠️ **The physical dimensions, bracket and app steps in this § 10.5 were written for the original Reolink unit.** The back-box position (1450 mm FFL, centred in the 1'6" section) and the Cat6 PoE wiring are unchanged, but the unit's exact size + the DS-KABV6113-A flush mount must be confirmed from the Hikvision DS-KV6113-WPE1(C) datasheet before cutting the back box.

#### Doorbell physical dimensions (⚠️ Reolink figures — re-verify for Hikvision)

| Dimension | Value | Notes |
|---|---|---|
| Width | 2" (~50 mm) | Tall, narrow form factor |
| Height | 5⅛" (~130 mm) | |
| Depth (proud of wall after surface mount) | 1" (~26 mm) | Unit sits this far OUT from finished wall |
| Cat6 cable entry | Centre-back of the unit, near the bottom | Goes through the bracket |

#### Back box specifications

The original Reolink doorbell was **2" wide × 5⅛" tall (50 × 130 mm)** — a tall, narrow unit. ⚠️ The Hikvision DS-KV6113-WPE1(C) has different dimensions and uses the DS-KABV6113-A flush mount — confirm its footprint from the datasheet before cutting the back box. The mounting bracket footprint roughly matches the unit.

**The back box must be smaller than the doorbell's mounting bracket so the bracket fully COVERS the box opening when installed.** Otherwise you'd see the back box rim around the doorbell — looks like a frame. We want only the doorbell itself visible.

| Dimension | Value | Why |
|---|---|---|
| Back box (W × H × D) | **3" × 3" × 2½" (75 × 75 × 65 mm)** — standard 1-module Indian GI MS modular back box | Smaller than the doorbell's bracket → fully hidden behind the bracket → clean look. Adequate room for Cat6 + RJ45 + 300 mm service loop curled inside. |
| Position centre (FFL) | **1450 mm (57⅛")** | Face level for adult visitors — critical for face detection |
| Distance from East door jamb | 9" (228 mm) | Centred in the 1'6" wall section |
| Distance from West window frame | 9" (228 mm) | Centred — equal margins both sides |
| Mounting | Flush-recessed into masonry from the OUTSIDE face; rim flush with finished plaster surface | So the doorbell's bracket sits flat against the wall |
| Conduit entry | 25 mm conduit enters from the BOTTOM or SIDE of the back box | Cable exits inside the box for RJ45 termination |
| Weather protection | Standard Indian modular GI MS boxes are NOT IP-rated, but the porch is roofed — no direct rain. **Apply silicone sealant around the conduit entry point** to keep humidity / driven rain out. |  |
| Brand availability | Anchor, Legrand, Schneider, Indo Asian — all stock this. Local electrical supply stores in Chitradurga always have it. | ~₹100 |
| Visible from outside? | NO — fully hidden behind the doorbell's bracket when installed | |

**📝 Note on back box choice — electrician's discretion:**

The 75 × 75 × 65 mm modular GI MS box is the homeowner's recommendation based on doorbell-size matching. However, the on-site electrician has experience with various doorbell installs and may prefer a different approach (e.g., a dedicated outdoor doorbell back box, a smaller cable-exit hole with surface-mount only, or a different IP-rated box). **The electrician has final discretion** based on their experience with this brand of doorbell.

Key constraints regardless of which box is used:
- Must be smaller than (or equal to) the doorbell's mounting bracket footprint, so the box stays hidden behind the bracket after install
- Must provide a sealed cable termination point (with silicone or rubber gasket against the conduit entry)
- Must allow Cat6 + RJ45 + 300 mm service loop to be coiled inside
- Must be installed BEFORE plaster, recessed flush with finished wall surface

**Visual layering (front to back):**

```
   You see (from outside) :
   ┌───────────────────────────────────────────────────┐
   │                                                    │
   │       ┌─────────────┐                              │
   │       │             │                              │
   │       │  HIKVISION   │  ← Only this is visible      │
   │       │   DOORBELL   │     (5⅛" tall × 2" wide,    │
   │       │   UNIT       │      mounted on its bracket) │
   │       │             │                              │
   │       └─────────────┘                              │
   │                                                    │
   │       PORCH WALL                                   │
   └───────────────────────────────────────────────────┘
   
   Inside the wall (hidden):
   
        ┌─────────────┐
        │  HIKVISION   │  ← Mounting bracket
        │   BRACKET    │     (smaller than the back box opening)
        │   ~50×130    │
        └─────────────┘
        
           ┌──────┐
           │      │
           │ BACK │       ← 75 × 75 × 65 mm GI MS box
           │ BOX  │          fully hidden behind the bracket
           │      │
           └──────┘
           ▲
           │
           Cat6 conduit enters at bottom/side
```

#### Phase 1 — BEFORE plaster (electrician pre-plaster work)

| Step | Task | Tools | Time |
|---|---|---|---|
| 1 | On the OUTSIDE face of the 1'6" wall section, chalk-mark the centre of the doorbell (1450 mm FFL, 9" from each side edge) | Tape measure, chalk, spirit level | 5 min |
| 2 | Chalk-mark a **3" × 3" square** around the centre point — this is the back box outline (vertical orientation matches the doorbell shape) | Chalk, builder's square | 3 min |
| 3 | Cut the cavity recess: **3" × 3" × 2½" deep (75 × 75 × 65 mm)**, into the masonry from the OUTSIDE face | Wall chaser, chisel & hammer, OR core drill | 20 min |
| 4 | Cut a conduit chase from the back box cavity → through the 9" wall thickness → to the conduit entry point on the INSIDE face | Wall chaser or grinder + chisel | 20 min |
| 5 | Lay the 25 mm grey conduit (C-Niche-Doorbell) through this chase, with one end protruding ~1" INTO the back box cavity, the other end going to the staircase niche route (ceiling or floor — see 10.4) | Conduit + conduit bends | 30 min |
| 6 | Install the **3" × 3" × 2½" GI MS modular back box**, flush with finished wall surface (NOT plaster surface — box rim should be SLIGHTLY recessed so plaster can be applied around the rim cleanly) | Back box, screws, rawl plugs | 10 min |
| 7 | **Apply silicone sealant around the conduit entry point** where it meets the back box (since this is a standard modular box, not natively IP-rated) | Silicone tube + sealant gun | 5 min |
| 8 | Pull outdoor LSZH UV-resistant Cat6 through the conduit; leave **~300 mm tail inside the back box** for later RJ45 termination | Cat6 cable, fish tape | 20 min |
| 9 | Cap the Cat6 tail with masking tape; close back box with a temporary blanking plate (so plaster doesn't enter) | Masking tape, blanking plate | 5 min |
| 10 | Photograph the installed back box with measurements; get homeowner sign-off | Camera | 5 min |
| **Total Phase 1** | | | **~2 hours** |

#### Phase 2 — AFTER plaster + porch finishing (electrician + smart-home installer)

| Step | Task | Tools | Time |
|---|---|---|---|
| 1 | Remove the temporary blanking plate from the back box | Screwdriver | 1 min |
| 2 | Pull out the 300 mm Cat6 tail | (none) | 1 min |
| 3 | Strip Cat6 jacket back ~25 mm; arrange the 4 twisted pairs per T568B colour code | Crimping tool, RJ45 connector | 10 min |
| 4 | Crimp an RJ45 connector onto the Cat6 end | Crimping tool | 5 min |
| 5 | **TEST the cable with a Cat6 tester** — verify all 8 pins are correctly wired | Cat6 tester (~₹500) | 5 min |
| 6 | Plug the RJ45 into the Hikvision doorbell's network port (on the back of the unit) | (none) | 1 min |
| 7 | Mount the doorbell's surface bracket over the back box, using the screws provided in the doorbell kit | Screwdriver | 5 min |
| 8 | Clip the doorbell unit onto its bracket | (none) | 2 min |
| 9 | At the staircase niche end: terminate the OTHER end of the Cat6 with an RJ45 and plug into a PoE port on the TP-Link TL-SG1210P switch | Crimper + RJ45 + Cat6 tester | 15 min |
| 10 | Verify the doorbell powers ON (PoE provides power immediately; you'll see a small LED on the unit) | Visual check | 1 min |
| 11 | In the Hik-Connect app, add the doorbell to your account; verify live video feed | Phone with Hik-Connect app | 5 min |
| 12 | In Home Assistant, add the Hikvision (ONVIF) integration; verify motion detection + face capture work | HA dashboard | 10 min |
| 13 | Press the bell button — verify chime triggers + visitor video shows on Waveshare (if installed) + welcome screen logic fires (if face is recognised) | Test by ringing bell + walking past camera | 10 min |
| **Total Phase 2** | | | **~1 hour 10 min** |

#### What you need to BUY for this install (and when)

| Item | When to buy | Cost | Notes |
|---|---|---|---|
| **3" × 3" × 2½" GI MS modular back box** (75 × 75 × 65 mm) | **BEFORE plaster** — any electrical supply store in Chitradurga (Anchor, Legrand, Indo Asian — all stock this) | ~₹100 | This is NOT supplied with the doorbell; it's a separate generic back box, sized to be **smaller than the doorbell's bracket** so it stays fully hidden behind the doorbell after install. |
| Silicone sealant tube | Before plaster | ~₹100 | For sealing around the conduit entry to the back box (since standard modular boxes aren't natively IP-rated, and the porch sees some humidity) |
| Outdoor LSZH UV-resistant Cat6 cable | Before plaster | ~₹40/m × ~7m = ~₹280 | Pulled through the conduit pre-plaster |
| **Hikvision DS-KV6113-WPE1(C) Video Doorbell PoE** (the actual doorbell) | Anytime before Phase 2 — but **order now** so you can verify the bracket dimensions before plaster covers your back box | ~₹8,000 ⚠️ (old Reolink price — confirm) | Order from I Secure India, Chitradurga. **Inspect on arrival** — confirm the DS-KABV6113-A mount + bracket footprint vs your back box. Then set aside until Phase 2. |
| In-house chime (Hikvision) | — | — | The DS-KV6113-WPE1(C) has no cheap plug-in wireless chime like the Reolink did. Chime is via Hik-Connect app push (free), a paired Hikvision DS-KH-series indoor station (separate ~₹6–10K), or Home Assistant playing a tone through the cavity speaker / Waveshare / any networked speaker — no separate chime device required. |
| RJ45 connectors (2 pieces) | Phase 2 | ~₹20 | One for each end of the Cat6 |
| Cat6 cable tester | Phase 2 | ~₹500 | Strongly recommended if your electrician isn't experienced with Cat6 |

**Important: NO separate conduit is needed for the chime.** The doorbell unit itself has a built-in speaker (visitors hear it at the door). And inside the house, any speaker connected to Home Assistant can play the chime — including your cavity speaker, future Waveshare, future dining hall speaker, etc. The bell-press signal travels over the existing Cat6 (the same conduit we already laid for the doorbell).

#### Can your electrician do this?

**Yes.** Every step uses standard electrician skills:
- Wall cutting / chasing — already doing this for the cavity + DB recess
- Conduit laying — already doing this throughout the foyer
- Cat6 termination + RJ45 crimping — standard Indian electrician skill

**One caveat:** if your electrician hasn't done Cat6 RJ45 termination before, ask them to bring a **Cat6 cable tester** (~₹500 — a small device that checks all 8 pins). Without testing, a bad crimp can be hard to debug later. Either insist on this, or have a separate Cat6-trained installer (smart-home installer) handle Phase 2 steps 3-5 + 9.

#### Critical errors to avoid

- ❌ Do NOT mount the back box flush with the PLASTER surface — it must be slightly recessed (~3 mm) so plaster can be applied around the rim cleanly. Otherwise plaster cracks at the rim within months.
- ❌ Do NOT use an indoor non-IP-rated back box. Even though the porch is roofed, condensation and humidity will rust an indoor box within a year.
- ❌ Do NOT skip the cable gland — water will run down the Cat6 jacket and into the back box during rain.
- ❌ Do NOT pull the Cat6 tight with no service loop — leave the full 300 mm tail inside the box for future re-termination if RJ45 fails.
- ❌ Do NOT terminate Cat6 outside in direct rain — do it inside the back box AFTER doorbell + bracket are mounted.

---

### 10.6 — Outdoor back box specs (Hikvision doorbell, CAM-1 spare, CAM-2 stub)

| Property | Value |
|---|---|
| Material | Weatherproof IP67 PVC or aluminium back box |
| Size | 4" × 4" (100 × 100 mm) face, ~60 mm deep |
| Mounting | Flush recessed into outer wall masonry; lip flush with finished plaster |
| Cable gland | M20 gland on bottom of box for Cat6 entry (prevents water ingress) |
| Cap (for unused boxes) | Blanking plate with gasket, screwed in place. Pull string left inside box for future cable pull. |

### 10.7 — Pre-plaster sign-off for Zones E + F (Porch + Staircase indoor)

- [ ] All 5 conduits routed from niche to their endpoints
- [ ] All conduit lengths verified (rough estimates above; measure actual on-site)
- [ ] Floor segment of C-Niche-Cavity-Data laid BEFORE tile contractor arrives (this is critical — once tiles are down, can't add the conduit)
- [ ] Weatherproof IP67 back boxes installed at:
  - Hikvision doorbell position (N wall 1'6" section, OUTSIDE face, 1450 mm FFL)
  - CAM-1 spare position (porch W wall, 1650 mm FFL) — capped
  - CAM-2 stub position (porch soffit NE corner, ~2700 mm FFL) — capped
- [ ] Indoor back box installed at Waveshare position (staircase S wall, 1500 mm FFL)
- [ ] Cat6 cables pulled through conduits where required (doorbell, foyer cavity, Waveshare) — using outdoor LSZH UV Cat6 for the porch + doorbell runs
- [ ] Pull strings inserted in all unused conduits (CAM-1 spare, CAM-2 stub)
- [ ] All conduit ends capped with masking tape
- [ ] Cable gland fittings ready for outdoor termination points
- [ ] Hikvision doorbell mounted and tested for face capture (wait until after plaster + porch finishing)
- [ ] Homeowner sign-off photographed for all 5 conduit routes + endpoints

---

## SECTION 11 — Complete conduit schedule (every run, master table)

This is the **single master list** of every conduit in the foyer welcome scope. Print this page and hand it to the electrician — they tick off each conduit as they lay it.

### 11.1 — Conduit colour code (recap)

| Colour | Used for | Size variants |
|---|---|---|
| **RED** PVC | 230V power (live wires) | 25 mm (heavy power) and 16 mm (light loads) |
| **GREY** PVC | Low voltage — Cat6, sensor wires, LED 24V secondary | 25 mm (Cat6, LV-25) and 16 mm (sensor, LED 24V, LV-16) |
| **BLUE** PVC | (Used elsewhere — sockets / AC / heavy power circuits) | Not used in foyer scope |

**If coloured PVC unavailable in Chitradurga,** the electrician should wrap each conduit end with coloured electrical tape (red, grey) AND label with permanent marker BEFORE plaster covers them. Once plastered, conduits are invisible — labelling is the only way to identify them later.

### 11.2 — Master conduit schedule

The 20 conduits in the foyer welcome scope, grouped by zone:

#### Zone A — East wall (DB-side)

| # | Conduit ID | Size | Colour | From | To | Length (~) | Cable inside |
|---|---|---|---|---|---|---|---|
| 1 | C-Main-Incomer | 25 mm | BLUE | Utility meter (outside) | DB | ~5 m | Single-phase mains (per BESCOM spec) |
| 2 | C-Earth | 16 mm | (any) | House earth pit | DB earth bus | ~3 m | 1× 4 sqmm Green/Yellow |
| 3 | C-DB-Foyer-Switch | 25 mm | RED | DB | Foyer Switch Panel on N wall | ~6 m | 3× 1.5 sqmm (Red L + Black N + Green/Yellow E) |
| 4 | C-DB-Cavity-Power | 25 mm | RED | DB | Cavity bottom-LEFT corner of back wall | ~3 m | 3× 2.5 sqmm (Red L + Black N + Green/Yellow E) |

#### Zone B — South feature wall (cavity)

| # | Conduit ID | Size | Colour | From | To | Length (~) | Cable inside |
|---|---|---|---|---|---|---|---|
| 5 | (same as #4) C-DB-Cavity-Power | 25 mm | RED | DB | Cavity bottom-LEFT | listed above | — |
| 6 | C-Niche-Cavity-Data | 25 mm | GREY | Staircase niche | Cavity bottom-RIGHT corner of back wall | ~12 m (floor route) | 1× outdoor LSZH UV Cat6 |
| 7 | C-Halo-24V | 16 mm | GREY | Halo driver (above false ceiling) | Cavity TOP-CENTRE of back wall | ~2 m | 2-core 0.75 sqmm 24V DC |
| 8 | C-Cavity-Ceiling-Speaker (provision) | 16 mm | GREY | Cavity TOP inner wall | Above false ceiling | ~2 m | Pull string only (future 2-core speaker wire) |

#### Zone C — North wall (Switch Panel side)

| # | Conduit ID | Size | Colour | From | To | Length (~) | Cable inside |
|---|---|---|---|---|---|---|---|
| 9 | (same as #3) C-DB-Foyer-Switch | 25 mm | RED | DB | Switch Panel | listed above | — |
| 10 | C-SW-Spots | 25 mm | RED | Switch Panel | 2× ceiling spotlight boxes | ~5 m | 3× 1.5 sqmm (switched L + N + E) |
| 11 | C-SW-Cove-Halo | 25 mm | RED | Switch Panel | Above false ceiling (splits to cove driver + halo driver) | ~5 m | 3× 1.5 sqmm (switched L + N + E) |
| 12 | C-SW-Shelf | 16 mm | RED | Switch Panel | Shelf driver location (Option 1 above ceiling OR Option 2 under shelf) | ~5 m (varies by option) | 3× 1.5 sqmm (switched L + N + E) |
| 13 | C-SW-Spare-4 (Gang 4) | 16 mm | RED | Switch Panel | Above false ceiling (capped) | ~3 m | Pull string only |
| 14 | C-SW-Porch-Ceiling | 16 mm | RED | Switch Panel | Porch ceiling fitting | ~4 m | 3× 1.5 sqmm (switched L + N + E) |
| 15 | C-SW-Porch-Wall | 16 mm | RED | Switch Panel | Outside near door, ~1900-2100 mm FFL (capped) | ~4 m | Pull string only |
| 16 | C-SW-Spare-7 (IF 7-gang installed) | 16 mm | RED | Switch Panel | Above false ceiling (capped) | ~3 m | Pull string only |
| 17 | C-SW-Spare-8 (IF 8-gang installed) | 16 mm | RED | Switch Panel | Above false ceiling (capped) | ~3 m | Pull string only |

#### Zone D — Foyer ceiling (driver-to-strip connections)

| # | Conduit ID | Size | Colour | From | To | Length (~) | Cable inside |
|---|---|---|---|---|---|---|---|
| 18 | C-Cove-24V | 16 mm | GREY (informal, can be loose wire inside cove pocket) | Cove driver | Cove strip start point | ~3 m (then strip extends ~10 m in cove pocket) | 2-core 1.5 sqmm 24V DC |
| 19 | C-Shelf-24V | 16 mm | GREY | Shelf driver location | Under-shelf LED strip | ~3 m (Option 1) or ~30 cm (Option 2) | 2-core 0.75 sqmm 24V DC |

#### Zone E — Porch (external)

| # | Conduit ID | Size | Colour | From | To | Length (~) | Cable inside |
|---|---|---|---|---|---|---|---|
| 20 | C-Niche-Doorbell | 25 mm | GREY | Staircase niche | Outside face of 1'6" N wall section, 1450 mm FFL | ~7 m (floor route) | 1× outdoor LSZH UV Cat6 |
| 21 | C-Niche-CAM1 (spare) | 25 mm | GREY | Staircase niche | Porch West wall, 1650 mm FFL (capped) | ~7 m (floor route) | Pull string only |
| 22 | C-Niche-CAM2 (stub) | 25 mm | GREY | Staircase niche | Porch soffit NE corner, ~2700 mm FFL (capped) | ~7 m (ceiling route — only viable option) | Pull string only |

#### Zone F — Staircase indoor

| # | Conduit ID | Size | Colour | From | To | Length (~) | Cable inside |
|---|---|---|---|---|---|---|---|
| 23 | C-Niche-Waveshare | 25 mm | GREY | Staircase niche | Staircase South wall, 1500 mm FFL | ~2 m | 1× outdoor LSZH UV Cat6 (cable pulled, ready for future Waveshare) |

### 11.3 — Conduit totals

| Conduit type | Total length | Notes |
|---|---|---|
| 25 mm RED PVC | ~17 m (DB-Foyer-Switch + Cavity-Power + SW-Spots + SW-Cove-Halo) | Buy a 30 m roll for cutting waste |
| 16 mm RED PVC | ~26 m (Earth + SW-Shelf + Spare-4 + Porch-Ceiling + Porch-Wall + Spare-7 + Spare-8) | Buy a 40 m roll |
| 25 mm GREY PVC (LV-25) | ~31 m (Cavity-Data + Doorbell + CAM1 + CAM2 + Waveshare) | Buy a 40 m roll |
| 16 mm GREY PVC (LV-16) | ~10 m (Halo-24V + Ceiling-Speaker provision + Cove-24V + Shelf-24V) | Buy a 15 m roll |
| 25 mm BLUE PVC | ~5 m (mains incomer only) | Buy a 10 m roll (per BESCOM requirements) |

### 11.4 — Critical conduit routing summary

```
   [Visual summary of all conduit routes]

         ┌──────────────────────────────────────────────────────┐
         │              PORCH (external)                          │
         │  CAM-1 spare  ◄────────────►  Hikvision doorbell      │
         │       ▲                              ▲                 │
         │       │ floor              │ floor   │                 │
         │       │ route               │ route                    │
         │   CAM-2 stub (ceiling route — porch soffit NE corner)  │
         ├──────────────────────────────────────────────────────┤
         │                       N wall                            │
         │                                                          │
         │              FOYER                          DB-East      │
         │                                              │           │
         │   ┌────────────────────┐                    │            │
         │   │  Cavity (S wall)   │                    │            │
         │   │  ◄── 3 conduits ─► │ ◄────────────── 25mm RED ────  │
         │   │  Power (DB) + Data │                  via wall chase │
         │   │  (niche, floor) +  │                                 │
         │   │  Halo (above       │                                 │
         │   │   ceiling)         │                                 │
         │   │  PLUS Conduit #4   │                                 │
         │   │  (cavity → false   │                                 │
         │   │   ceiling, for     │                                 │
         │   │   future speaker)  │                                 │
         │   └────────────────────┘                                 │
         │                                                          │
         │   Foyer Switch Panel on N wall ◄── 1 conduit from DB    │
         │                                                          │
         │   3 conduits via floor (Cavity Cat6 + Doorbell + CAM1)  │
         │   share the same East-going floor chase                 │
         │                                                          │
         ├──────────────────────────────────────────────────────┤
         │   LIVING / DINING                                       │
         │                                                          │
         │   Staircase niche ◄── origin of 5 external conduits     │
         │   ◄────── Waveshare (2m vertical)                       │
         │   Below: Beelink + PoE switch + router + UPS            │
         │                                                          │
         └──────────────────────────────────────────────────────┘
```

---

## SECTION 12 — Wire schedule (every wire, gauge, colour, length)

What goes inside each conduit. The electrician uses this to plan wire purchasing.

### 12.1 — Wire colour code (Indian standard, mandatory)

| Colour | Function | Where it goes |
|---|---|---|
| **RED** insulation | LIVE (phase) — 230V hot | Every live wire from MCB outward (UNTIL it passes through a switch) |
| **BLUE** insulation | Switched LIVE leg | Between switch and the load (e.g., between Gang 1 and the spotlight box) |
| **BLACK** insulation | NEUTRAL — return | Every switch board, every socket |
| **GREEN with YELLOW stripe** insulation | EARTH | Every switch, socket, metal back box, metal fitting |

In some Indian installs, "Red = Live, Black = Neutral" is unique to "Red = Live, Blue = switched live, Black = Neutral". Stick to this in the foyer wiring.

### 12.2 — Master wire schedule

#### Power wires (230V)

| For conduit | Wire | Colour | Length (~) | Total length budget |
|---|---|---|---|---|
| C-DB-Foyer-Switch | 1.5 sqmm | Red (L) + Black (N) + Green/Yellow (E) | 6 m each | 18 m (3-core) |
| C-DB-Cavity-Power | 2.5 sqmm | Red + Black + Green/Yellow | 3 m each | 9 m (3-core) |
| C-SW-Spots | 1.5 sqmm | Blue (switched L) + Black (N) + Green/Yellow (E) | 5 m each | 15 m |
| C-SW-Cove-Halo | 1.5 sqmm | Blue + Black + Green/Yellow | 5 m each | 15 m |
| C-SW-Shelf | 1.5 sqmm | Blue + Black + Green/Yellow | 5 m each | 15 m |
| C-SW-Porch-Ceiling | 1.5 sqmm | Blue + Black + Green/Yellow | 4 m each | 12 m |
| C-Earth (main earth) | 4 sqmm | Green/Yellow | 3 m | 3 m |

#### Low-voltage 24V DC wires (from drivers to LED strips)

| For conduit | Wire | Length (~) | Total |
|---|---|---|---|
| C-Halo-24V | 2-core 0.75 sqmm 24V DC | 2 m | 2 m |
| C-Cove-24V | 2-core 1.5 sqmm 24V DC | 3 m + 10 m strip | ~13 m |
| C-Shelf-24V | 2-core 0.75 sqmm 24V DC | 3 m (Option 1) or 0.3 m (Option 2) | 3 m |

#### Network cables (Cat6)

| For conduit | Wire | Length (~) | Notes |
|---|---|---|---|
| C-Niche-Cavity-Data | Outdoor LSZH UV-resistant Cat6 | 12 m | Includes 300 mm slack at each end |
| C-Niche-Doorbell | Outdoor LSZH UV-resistant Cat6 | 8 m | Includes service loop |
| C-Niche-Waveshare | Outdoor LSZH UV-resistant Cat6 | 3 m | Includes service loop |
| **Subtotal outdoor Cat6** | | **~23 m** | Buy a 30 m roll |

#### Spare conduits (pull string only — no cable now)

| Conduit | Pull string |
|---|---|
| C-SW-Spare-4 | Nylon twine 3 m |
| C-SW-Porch-Wall | Nylon twine 4 m |
| C-SW-Spare-7 (if installed) | Nylon twine 3 m |
| C-SW-Spare-8 (if installed) | Nylon twine 3 m |
| C-Cavity-Ceiling-Speaker | Nylon twine 2 m |
| C-Niche-CAM1 | Nylon twine 7 m |
| C-Niche-CAM2 | Nylon twine 7 m |
| **Subtotal pull string** | **~30 m** | Buy a 100 m roll (cheap insurance) |

### 12.3 — Total wire purchase summary

| Wire | Total budget | Buying recommendation |
|---|---|---|
| 1.5 sqmm Red | ~12 m | Standard 90 m coil — use across whole house |
| 1.5 sqmm Blue (switched live) | ~25 m | Standard 90 m coil |
| 1.5 sqmm Black | ~30 m | Standard 90 m coil |
| 1.5 sqmm Green/Yellow | ~30 m | Standard 90 m coil |
| 2.5 sqmm Red | ~3 m | Standard 90 m coil (used across house for sockets) |
| 2.5 sqmm Black | ~3 m | Standard 90 m coil |
| 2.5 sqmm Green/Yellow | ~3 m | Standard 90 m coil |
| 4 sqmm Green/Yellow | ~3 m | Standard 90 m coil (main earth) |
| 2-core 0.75 sqmm 24V | ~5 m | Buy 10 m of flexible LED extension cable |
| 2-core 1.5 sqmm 24V | ~13 m | Buy 15 m of flexible LED extension cable |
| Outdoor LSZH UV Cat6 | ~23 m | Buy 30 m of D-Link DCC-6OD-305 or Commscope outdoor Cat6 |
| Nylon pull string | ~30 m | Buy 100 m roll (cheap) |

### 12.4 — Wires INSIDE the cavity (short internal connections)

These don't go through any conduit — they're internal cavity wiring, all <30 cm long.

| Wire | Purpose | Length |
|---|---|---|
| 3.5 mm audio cable (TRRS to 3.5 mm aux) | RPi USB sound card → PAM8403 amp input | 30 cm |
| USB-A to micro-USB cable | RPi USB port → PAM8403 power | 30 cm |
| 2-core 1 sqmm speaker wire | PAM8403 amp output → Visaton FR 8 speaker terminals | 30 cm |
| CSI ribbon cable (15-pin) | RPi CSI port → Pi Camera Module 3 (bezel cam) | 25 cm (comes with camera) |
| Mini-HDMI to HDMI cable | RPi HDMI output → monitor HDMI input | 30 cm |
| USB-C cable | PoE splitter 5V output → RPi power input | 20 cm |
| RJ45 patch cable | PoE splitter RJ45 → USB OTG Ethernet adapter | 20 cm |
| 2-core 0.75 sqmm 24V DC | 24V wire from halo conduit → halo LED strip terminals | varies (cavity perimeter loops) |
| Power adapter cord (monitor) | Cavity Socket A → Samsung monitor power adapter | 50 cm |
| Optional USB charger (if Spare Socket B used) | Cavity Socket B → any USB device | varies |

---

## SECTION 13 — MCB plan (2 MCBs for foyer)

### 13.1 — MCB summary

The foyer welcome system uses **2 dedicated MCBs** at the main DB (decision locked: see Section 5 / 6 / Foyer-decision-history).

**📝 Note: electrician verification recommended.** The MCB selection below is the homeowner's plan based on load calculations. The on-site electrician should verify these selections against their experience with: (a) actual loads on similar installs, (b) local Indian Standards (IS 8623) for residential MCB sizing, (c) availability of preferred brands (Schneider vs ABB vs Legrand vs Indo Asian). The electrician has final discretion on MCB ratings, RCBO type, and exact brand — but the 2-MCB-for-foyer structure (Lights + Cavity) should remain regardless.

| MCB | Type | Rating | Protects |
|---|---|---|---|
| **B-Foyer-Lights** | 6 A MCB (B-curve) | 6 amps | All foyer + porch lighting: spots, cove, halo, shelf, porch ceiling, porch wall, future spares |
| **B-Foyer-Cavity** | 6 A MCB + 30 mA RCBO (leakage protection) | 6 amps + 30 mA leakage | Cavity sockets (Monitor Socket A + Spare Socket B) — and through them, all electronics in the cavity (RPi, monitor, amp, speaker, etc.) |

### 13.2 — Why 2 MCBs (not 1, not 3)

- **Why not 1 MCB:** if a single MCB serves all foyer loads, a fault in any one load (e.g., monitor's power supply shorts) trips the entire foyer — lights AND cavity go dark. You're left fumbling in the dark to troubleshoot. Bad design.
- **Why not 3 MCBs (lights + cavity + cove separately):** the cove and other lighting loads are electrically similar (all LED, low current). Combining them on one MCB is fine. 3 MCBs would use one more DB slot without functional benefit.
- **Why this 2-MCB split is right:** lights = mechanical fail (rare, low impact). Cavity = electronics fail (more likely, with RCBO for electrical safety). Different fault profiles, deserve separate MCBs.

### 13.3 — B-Foyer-Lights detail

| Property | Value |
|---|---|
| MCB | 6 A B-curve MCB (Schneider, ABB, Legrand, etc.) |
| RCBO | Not needed for lighting circuit (no wet/electronic loads) |
| Loads | 2× GU10 spots (14W total) + cove LED ~96W + halo LED ~10W + shelf LED ~11W + porch ceiling ~9W + porch wall (future, 0W now) = **~140W total** |
| Current draw | 140W ÷ 230V = **~0.6 A** (well below 6A rating; plenty of safety margin) |
| Wire size from MCB | 1.5 sqmm (standard for lighting) |
| Connected via conduit | C-DB-Foyer-Switch → Foyer Switch Panel → 4-7 outgoing branches |

### 13.4 — B-Foyer-Cavity detail

| Property | Value |
|---|---|
| MCB | 6 A B-curve MCB |
| RCBO | **YES — 30 mA RCBO** (mandatory for electronics + wet circuits; also protects against ground faults in case the monitor or RPi develops insulation issues) |
| Loads | Samsung monitor (25W typical) + RPi Zero 2W (via PoE — doesn't draw from this circuit) + halo LED (10W via halo driver primary) + cavity speaker amp (1W) + spare socket (variable 0-200W) = **~36W typical**, up to ~250W if heavy load on spare |
| Current draw | 36W ÷ 230V = **~0.16 A** typical; max ~1 A if spare socket heavily used |
| Wire size from MCB | 2.5 sqmm (heavier than lights — gives margin for future load on spare) |
| Connected via conduit | C-DB-Cavity-Power → directly to cavity socket box |

### 13.5 — DB layout (which slot each MCB occupies)

Inside the Schneider Acti9 48-way DB:

```
   [DB internal layout, simplified — only foyer-relevant slots shown]
   
   ╔═════════════════════════════════════╗
   ║         MAIN INCOMER MCB             ║  ← 63A or 100A main switch
   ╠═════════════════════════════════════╣
   ║   100 mA S-type RCCB                  ║  ← Master leakage protection
   ╠═════════════════════════════════════╣
   ║   B-Foyer-Lights   6A MCB            ║
   ╠═════════════════════════════════════╣
   ║   B-Foyer-Cavity   6A + 30mA RCBO    ║
   ╠═════════════════════════════════════╣
   ║   (other house circuits — bedroom,    ║
   ║    living, kitchen, etc.)             ║
   ╠═════════════════════════════════════╣
   ║   EARTH BUSBAR                        ║  ← All earth wires bond here
   ╚═════════════════════════════════════╝
```

DB total slots used by the foyer scope: **2** (out of 48). Plenty of room for the rest of the house circuits.

### 13.6 — Earth + safety

| Item | Spec |
|---|---|
| Main earth pit | Separate earth pit, copper plate, salt + charcoal fill, dedicated for the house (not shared with motor pit) |
| Earth wire from pit to DB | 4 sqmm green/yellow, via C-Earth conduit |
| Earth bonding | All metal back boxes, all metal switch plates, all socket earth terminals connect to the DB earth busbar via Green/Yellow earth wires through each conduit |
| Earth continuity test | Less than 1 ohm between any metal body and the earth bus — verify before plaster with multimeter |

---

## SECTION 14 — Switch board and socket schedule (every box, location, height, modules)

Every back box in the foyer welcome scope, in one table.

### 14.1 — Inside foyer (visible from foyer)

| # | Box | Location | Centre height (FFL) | Box size | Modules / contents | Purpose |
|---|---|---|---|---|---|---|
| 1 | **Foyer Switch Panel** | N wall, 1'6" section (between window West and door East), centred horizontally | **1200 mm (47¼")** | **6-gang GI MS, 335 × 75 × 65 mm** (default; 7 or 8 gang if it fits) | 6 smart-switch gangs (Spots, Cove+Halo, Shelf, Foyer-Spare, Porch-Ceiling, Porch-Wall) + 1 Sonoff Mini hidden behind plate | Master control for all foyer + porch lighting |

### 14.2 — Inside the cavity (hidden behind monitor)

| # | Box | Location | Centre height (FFL) | Box size | Modules / contents | Purpose |
|---|---|---|---|---|---|---|
| 2 | **Cavity Socket Panel** | Cavity back wall, centred horizontally, in pocket cut INTO back wall | **53" (1346 mm)** — below monitor centre | 3" × 3" × 2½" pocket cut INTO masonry beyond cavity back wall (75 × 75 × 65 mm GI MS box recessed in this pocket) | 2-module modular plate: Socket A (Monitor) + Socket B (Spare) + 1 Sonoff Mini behind Socket A wiring | 230V power for monitor + spare; remote on/off via Sonoff |

### 14.3 — On porch (outside, weather-exposed but roofed)

| # | Box | Location | Centre height (FFL) | Box size | Modules / contents | Purpose |
|---|---|---|---|---|---|---|
| 3 | **Hikvision doorbell back box** | Outside face of N wall 1'6" section, centred horizontally | **1450 mm (57⅛")** | 3" × 3" × 2½" GI MS modular (or per electrician's discretion) | None — back box only; the Hikvision doorbell mounts on its own bracket OVER this box | Holds Cat6 termination behind the doorbell |
| 4 | **CAM-1 spare back box** | Porch West wall (= Living E exterior wall) | **1650 mm (65")** | 4" × 4" IP67 outdoor box (capped, no plate yet) | Empty — pull string only | Future PoE face-capture camera |
| 5 | **CAM-2 stub back box** | Porch soffit NE corner (overhang ceiling) | **~2700 mm (~8'10")** | 4" × 4" IP67 outdoor box (capped, no plate yet) | Empty — pull string only | Future porch overview camera |
| 6 | **Porch ceiling light box** | Centre of porch ceiling (final position by homeowner decision) | ~10 ft FFL (porch ceiling level) | B-type ceiling rose box, 60 mm depth | LED fitting TBD (or pendant) | Porch overhead lighting |
| 7 | **Porch wall light box** (future provision) | Outside near main door, ~1900-2100 mm FFL (capped) | 1900-2100 mm | Standard wall box, capped | Empty — pull string only | Future porch wall sconce |

### 14.4 — Inside staircase area (indoor)

| # | Box | Location | Centre height (FFL) | Box size | Modules / contents | Purpose |
|---|---|---|---|---|---|---|
| 8 | **Waveshare back box** | Staircase South wall | **1500 mm (59")** | TBD (depends on Waveshare frame design — likely 6" × 6" or similar recessed box) | None — back box only; Waveshare touchscreen + Pi + frame designed later | Cat6 termination for future Waveshare indoor unit |

### 14.5 — Ceiling boxes (inside false ceiling)

| # | Box | Location | Position | Type | Contents | Purpose |
|---|---|---|---|---|---|---|
| 9 | Spotlight box #1 | False ceiling, 609 mm from N edge of foyer, 300 mm from W wall area | At false-ceiling level (9 ft FFL) | B-type, 60 mm depth | GU10 fitting with adjustable gimbal | Spotlight #1 grazing stone wall |
| 10 | Spotlight box #2 | False ceiling, 1218 mm from N edge of foyer, 300 mm from W wall area | At false-ceiling level | B-type, 60 mm depth | GU10 fitting with adjustable gimbal | Spotlight #2 grazing stone wall |

### 14.6 — Driver locations above false ceiling

| Driver | Location | Purpose |
|---|---|---|
| Cove LED driver | Above false ceiling, on a small shelf or zip-tied to slab anchor, accessible via inspection hatch | Converts 230V → 24V for cove strip |
| Halo LED driver | Same shelf as cove driver | Converts 230V → 24V for cavity halo strip |
| Walnut shelf LED driver (Option 1) | Same shelf as cove + halo | Converts 230V → 24V for shelf strip |
| Walnut shelf LED driver (Option 2) | Behind / under the walnut shelf on S wall | Converts 230V → 24V for shelf strip (Option 2 only) |

### 14.7 — Total back box count

| Box type | Count |
|---|---|
| Switch panel (6-8 gang) | 1 |
| Cavity socket panel (2-module) | 1 |
| Doorbell back box (modular) | 1 |
| Camera back boxes (capped, IP67 outdoor) | 2 (CAM-1 spare + CAM-2 stub) |
| Porch light boxes | 2 (ceiling + wall, the wall one capped) |
| Indoor Waveshare back box | 1 |
| Ceiling spotlight boxes | 2 |
| **Total back boxes** | **10** |

---

## SECTION 15 — Bill of Materials (line-item shopping list)

Everything to buy for the foyer welcome system, organised by category. Prices are approximate (Chitradurga / online retailers, mid-2026). Cross-reference [materials-checklist.md](materials-checklist.md) for the broader house material list.

### 15.1 — Conduits + accessories

| Item | Quantity | Where to buy | Est. cost |
|---|---|---|---|
| 25 mm RED PVC conduit (rigid, ISI marked) | 30 m roll | Local electrical store | ~₹400 |
| 16 mm RED PVC conduit | 40 m roll | Local electrical store | ~₹350 |
| 25 mm GREY PVC conduit (LV-25) | 40 m roll | Local electrical store | ~₹450 |
| 16 mm GREY PVC conduit (LV-16) | 15 m roll | Local electrical store | ~₹150 |
| 25 mm BLUE PVC conduit (mains feed) | 10 m | Local electrical store | ~₹150 |
| Conduit bends (25 mm) | 20 pieces | Local electrical store | ~₹150 |
| Conduit bends (16 mm) | 20 pieces | Local electrical store | ~₹100 |
| Conduit couplers (25 mm) | 15 pieces | Local electrical store | ~₹80 |
| Conduit couplers (16 mm) | 15 pieces | Local electrical store | ~₹60 |
| Conduit clamps / saddles | 50 pieces | Local electrical store | ~₹150 |
| Nylon pull string (100 m roll) | 1 roll | Local electrical store | ~₹150 |
| Masking tape (for capping conduit ends) | 2 rolls | Hardware store | ~₹80 |
| **Subtotal — Conduits** | | | **~₹2,270** |

### 15.2 — Wires

| Item | Quantity | Brand recommendation | Est. cost |
|---|---|---|---|
| 1.5 sqmm wire Red (90 m coil) | 1 coil | Polycab / Havells / Finolex | ~₹1,200 |
| 1.5 sqmm wire Blue (switched live) | 1 coil | Polycab / Havells / Finolex | ~₹1,200 |
| 1.5 sqmm wire Black | 1 coil | Polycab / Havells / Finolex | ~₹1,200 |
| 1.5 sqmm wire Green/Yellow | 1 coil | Polycab / Havells / Finolex | ~₹1,200 |
| 2.5 sqmm wire Red | 1 coil (use across house) | Polycab / Havells / Finolex | ~₹2,200 |
| 2.5 sqmm wire Black | 1 coil | Polycab / Havells / Finolex | ~₹2,200 |
| 2.5 sqmm wire Green/Yellow | 1 coil | Polycab / Havells / Finolex | ~₹2,200 |
| 4 sqmm wire Green/Yellow (main earth) | 5 m | Polycab / Havells | ~₹400 |
| 2-core 0.75 sqmm 24V cable | 10 m | Local LED supply | ~₹300 |
| 2-core 1.5 sqmm 24V cable (cove) | 15 m | Local LED supply | ~₹450 |
| **Outdoor LSZH UV-resistant Cat6** | 30 m | D-Link DCC-6OD-305 / Commscope / Belden (Amazon India) | ~₹1,200 |
| Indoor LSZH Cat6 (for cavity-internal patch) | 2 m | Any brand | ~₹50 |
| **Subtotal — Wires** | | | **~₹13,800** |

*Note: most wire coils above are shared with the whole-house wiring — the foyer scope uses only a fraction of each coil. Allocate ~20% of coil cost to foyer for a more accurate foyer-only number. Listed full coil cost above for purchase planning.*

### 15.3 — Back boxes + plates

| Item | Quantity | Brand recommendation | Est. cost |
|---|---|---|---|
| **6-gang GI MS modular back box** (335 × 75 × 65 mm) | 1 | Anchor / Legrand / Schneider | ~₹250 |
| (Upgrade option) 7- or 8-gang back box if it fits | 0 or 1 | Same brand | +₹100 |
| **2-module modular back box** (130 × 75 × 65 mm) — cavity socket | 1 | Anchor / Legrand | ~₹120 |
| **1-module GI MS modular back box** (75 × 75 × 65 mm) — Hikvision doorbell (electrician's discretion on exact box) | 1 | Anchor / Legrand | ~₹100 |
| 4×4 IP67 outdoor back box (CAM-1 spare + CAM-2 stub) | 2 | Hensel / OBO Bettermann / Polycab outdoor | ~₹600 |
| B-type ceiling rose box (60 mm depth) — 2× spotlights + porch ceiling | 3 | Local | ~₹150 |
| Standard wall box (porch wall future) | 1 | Local | ~₹80 |
| Waveshare back box (carpenter custom OR standard 6"×6") | 1 | Custom | ~₹200 |
| Modular plate 6-gang (Schneider Unica Pure or chosen brand) | 1 | Schneider / Aqara / Anchor (decision in finishing phase) | ~₹500-3000 |
| Modular plate 2-module (matching brand) | 1 | Same brand | ~₹150 |
| 5A sockets × 2 | 2 | Matching plate brand | ~₹200 |
| Modular cover plates / blanks | 4 | Matching brand | ~₹100 |
| **Subtotal — Back boxes + plates** | | | **~₹2,550-5,050** |

### 15.4 — MCBs + DB hardware

| Item | Quantity | Brand recommendation | Est. cost |
|---|---|---|---|
| 6A B-curve MCB | 2 (Foyer-Lights + Foyer-Cavity) | Schneider Acti9 / ABB / Legrand | ~₹500 |
| 30 mA RCBO (cavity protection) | 1 | Schneider Acti9 RCBO / ABB | ~₹2,000 |
| 100 mA S-type RCCB (main master leakage) | 1 (shared with whole house, may already exist) | Schneider | ~₹2,500 |
| DB enclosure (48-way Schneider Acti9) | 1 (already in main electrical plan) | Schneider Acti9 IEF48 | already planned |
| Copper earth busbar | 1 (in DB) | Schneider | already planned |
| MCB labels (Dymo or pre-printed) | 1 set | Local | ~₹150 |
| **Subtotal — MCBs + DB hardware** | | | **~₹5,150** |

### 15.5 — Smart hardware (Sonoff + Cat6 termination)

| Item | Quantity | Brand recommendation | Est. cost |
|---|---|---|---|
| Sonoff ZBMINI L2 (Foyer Switch Panel — supports 6+ gang setups) | 1 | iTead Sonoff (Amazon / Robu.in) | ~₹1,500 |
| Sonoff Mini R2 (Cavity socket — Monitor on/off) | 1 | iTead Sonoff (Amazon / Robu.in) | ~₹800 |
| RJ45 connectors (Cat6-rated) | 20 pieces | Local | ~₹100 |
| Cat6 cable tester | 1 | Amazon (any brand) | ~₹500 |
| Crimping tool (RJ45) | 1 (if electrician doesn't already have) | Amazon | ~₹400 |
| **Subtotal — Smart hardware** | | | **~₹3,300** |

### 15.6 — Welcome screen + cavity components

| Item | Quantity | Source | Est. cost |
|---|---|---|---|
| Samsung LS22F320GAWXXL monitor (21.5", IPS, VESA 100, dual HDMI, no speakers) — REVISED 2026-05-26 | 1 | Amazon India (Cocoblu/Appario seller) | ~₹6,499 ☑ ORDERED |
| VESA 100 slim fixed wall bracket (Speedio or equivalent, 15 mm standoff) | 1 | Amazon India | ~₹500 ☑ ORDERED |
| Raspberry Pi Zero 2W | 1 | Robu.in / Amazon | ~₹2,500 |
| Raspberry Pi Camera Module 3 (CAM-0, bezel) | 1 | Robu.in / Amazon | ~₹2,500 |
| PoE splitter (5V USB-C output) | 1 | TP-Link TL-PoE10R or UCTRONICS | ~₹1,000 |
| USB OTG Ethernet adapter (for Pi Zero 2W) | 1 | Amazon | ~₹400 |
| USB sound card (small dongle) | 1 | Amazon | ~₹400 |
| PAM8403 audio amplifier module | 1 | Robu.in | ~₹150 |
| Mini-HDMI to HDMI cable (30 cm) | 1 | Amazon | ~₹200 |
| 3.5 mm audio cable (30 cm) | 1 | Amazon | ~₹100 |
| 3M VHB heavy-duty mounting tape | 1 roll | Amazon | ~₹300 |
| Velcro strips | 1 pack | Local | ~₹100 |
| Silicone sealant tube | 1 | Local hardware | ~₹100 |
| Cable ties (small) | 1 pack | Local | ~₹100 |
| **Subtotal — Welcome screen + cavity** | | | **~₹17,350** |

### 15.7 — Audio (speaker)

| Item | Quantity | Source | Est. cost |
|---|---|---|---|
| Visaton FR 8 speaker driver (80 mm) | 1 | Amazon (Visaton India) | ~₹1,800 |
| MDF baffle (3½" × 3½" × ¼") — custom cut | 1 | Carpenter scrap | ~₹50 |
| 2-core speaker wire (1 sqmm, 1 m) | 1 m | Local | ~₹50 |
| **Subtotal — Audio** | | | **~₹1,900** |

### 15.8 — Lighting (LEDs + drivers + fittings)

| Item | Quantity | Source | Est. cost |
|---|---|---|---|
| GU10 LED bulb (7W, 2700K, CRI 90+, dimmable) | 2 | Philips / Wipro / Osram | ~₹1,000 |
| GU10 gimbal fitting (adjustable angle, 30° narrow flood) | 2 | Local lighting store | ~₹2,000 |
| 24V LED strip 2200K (5m roll, 4.8 W/m, 5050 SMD) — halo | 1 roll | Online: search "24V LED strip 2200K" (Mufasa / Amazon / AliExpress) | ~₹1,000 |
| 24V LED strip 2700K (5m roll, 6 W/m) — shelf | 1 roll | Local LED store | ~₹800 |
| 24V LED strip 2700K (10m roll, 9.6 W/m, CRI 90+) — cove | 1 roll | Local LED store | ~₹1,500 |
| Mean Well APV-12-24 LED driver (12W) | 2 (halo + shelf) | Amazon | ~₹1,200 |
| Mean Well APV-100-24 LED driver (100W) | 1 (cove) | Amazon | ~₹1,500 |
| LED strip connectors + corner clips | 1 set | Amazon | ~₹200 |
| **Subtotal — Lighting** | | | **~₹9,200** |

### 15.9 — Cameras + doorbell

| Item | Quantity | Source | Est. cost |
|---|---|---|---|
| **Hikvision DS-KV6113-WPE1(C) Video Doorbell PoE** | 1 | I Secure India, Chitradurga | ~₹8,000 ⚠️ (old Reolink price — confirm) |
| In-house chime (Hik-Connect app / paired DS-KH indoor station) — no plug-in chime like the Reolink | 0 | I Secure India | — |
| CAM-1 future (Hikvision DS-2CD2143G2-LU) | 0 (provision only) | future | ~₹15,000 (future) |
| CAM-2 future (Hikvision 2.8mm wide overview) | 0 (provision only) | future | ~₹12,000 (future) |
| **Subtotal — Cameras + doorbell (now)** | | | **~₹8,000** ⚠️ (doorbell price is old Reolink figure — confirm Hikvision price & re-total) |

### 15.10 — False ceiling + carpentry

| Item | Quantity | Source | Est. cost |
|---|---|---|---|
| Gypsum board 12.5 mm (for false ceiling) | Per sqft × foyer area | Local | included in false-ceiling contractor scope |
| GI grid + accessories | per spec | Local | included in false-ceiling contractor scope |
| Inspection hatch (300 × 300 mm) | 1 | Local | ~₹500 |
| Cove pocket framing | included in false-ceiling contractor scope | | |
| Walnut floating shelf (6 ft × 10" × 1¼") | 1 | Carpenter custom (walnut veneer on MDF or solid walnut) | ~₹4,500 |
| Hidden steel L-brackets for shelf | 4 | Local hardware | ~₹400 |
| Cupboard plywood facade (for starter cupboard) | 1 unit | Carpenter | ~₹3,000 |
| Cabinet hinges + lock | per design | Local | ~₹500 |
| **Subtotal — False ceiling + carpentry** | | | **~₹8,900** |

### 15.11 — Stone cladding

| Item | Quantity | Source | Est. cost |
|---|---|---|---|
| Rustic ledgestone slips (tobacco + sandstone + charcoal mix) | ~6 sqm (6 ft × 11 ft = 6.13 sqm) | Local stone supplier | ~₹15,000 (~₹2,500/sqm) |
| Extra stone slips for cavity reveal wrap | ~0.5 sqm extra | Same supplier | ~₹1,250 |
| MS polymer adhesive (high-bond) | 5 kg | Local hardware | ~₹1,500 |
| Mechanical anchor clips (for stones > 5 kg) | per spec | Local | ~₹500 |
| **Subtotal — Stone cladding** | | | **~₹18,250** |

### 15.12 — Future provisions (cost shown for reference only, NOT in current plan)

| Item | Cost (when added) |
|---|---|
| Waveshare 10.1" touchscreen | ~₹13,000 |
| Raspberry Pi 4 (4GB) for Waveshare | ~₹6,000 |
| PoE HAT for Pi 4 | ~₹2,000 |
| Waveshare mount frame (carpenter) | ~₹2,500 |
| Smart door lock (Yale / Hafele) | ~₹12,000-15,000 |
| Dining hall ceiling speaker | ~₹3,000 |
| **Future-add total** | **~₹38,500-41,500** |

### 15.13 — Labour estimates (foyer welcome scope only)

| Trade | Hours | Rate (~) | Cost |
|---|---|---|---|
| Electrician (cuts cavity + DB recess + conduits + wiring + termination) | 40 hours | ~₹200/hr | ~₹8,000 |
| Mason (plastering after, stone wall building) | included in main building contract | | |
| Painter (cavity matte black, side walls, ceiling, masking) | 8 hours | ~₹250/hr | ~₹2,000 |
| Stone cladder | 12 hours | ~₹400/hr | ~₹4,800 |
| Carpenter (shelf, cupboard facade, MDF baffle, optional VESA backing) | 6 hours | ~₹300/hr | ~₹1,800 |
| False-ceiling contractor (drop ceiling + cove + hatch + spot cut-outs) | per spec | | ~₹6,000 |
| Smart-home installer (Phase 11 commissioning) | 8 hours | ~₹500/hr | ~₹4,000 |
| **Subtotal — Labour** | | | **~₹26,600** |

### 15.14 — Grand total estimate (foyer welcome scope)

| Category | Cost |
|---|---|
| Conduits + accessories | ~₹2,270 |
| Wires (~20% of coils allocated to foyer) | ~₹2,760 |
| Back boxes + plates | ~₹2,550 |
| MCBs + DB hardware | ~₹5,150 |
| Smart hardware (Sonoff + Cat6 termination) | ~₹3,300 |
| Welcome screen + cavity components | ~₹17,350 |
| Audio (speaker) | ~₹1,900 |
| Lighting (LEDs + drivers + fittings) | ~₹9,200 |
| Cameras + doorbell (now) | ~₹8,000 |
| False ceiling + carpentry | ~₹8,900 |
| Stone cladding | ~₹18,250 |
| Labour | ~₹26,600 |
| **GRAND TOTAL — foyer welcome system** | **~₹1,06,230** |

**Excludes:** smart door lock, dining hall speaker, Waveshare hardware (all flagged in Section 18 for separate sessions).

---

## SECTION 16 — Phase-by-phase build order

The 11-phase sequence. Each phase has an owner, duration, deliverable, and sign-off requirement. Do not start the next phase until the prior phase signs off.

### 16.1 — Critical timeline

| Date | Event | Status |
|---|---|---|
| 2026-05-20 | Document v1.0 published, design locked | ✅ Done |
| 2026-05-21 to 22 | Final on-site walkthrough with electrician + carpenter | ✅ Done |
| **2026-05-23** | **Phase 1 starts: marking + sign-off** | ⏳ Imminent |
| 2026-05-23 to 24 | Phase 2: chasing + cavity cutting | |
| 2026-05-25 to 26 | Phase 3: conduit pulling | |
| 2026-05-27 to 28 | Phase 4: wire pulling + DB install | |
| 2026-05-29 to 31 | Phase 5: first plaster (rough coat) | |
| 2026-06-01 | Phase 6: cavity interior matte black | |
| 2026-06-01 | Phase 7: VESA backing + carpenter prep | |
| 2026-06-02 to 05 | Phase 8: stone cladding | |
| 2026-06-06 to 09 | Phase 9: false ceiling + cove + drivers | |
| 2026-06-10 to 12 | Phase 10: final paint | |
| 2026-06-13 to 15 | Phase 11: switch + socket fitting + smart-home commissioning | |
| **2026-06-15** | **Welcome system live + tested** | 🎯 Target |

**Calendar duration:** ~25 working days from Phase 1 to commissioning.

### 16.2 — Phase 1 — Marking + sign-off (Day 1)

| Property | Value |
|---|---|
| Owner | Electrician + Carpenter + Homeowner |
| Duration | 1 day (4-6 hours on-site) |
| Tools | Tape measure, chalk, spirit level, camera |
| What happens | On bare brick / block walls, mark in CHALK every: cavity outline, DB recess, switch box positions, socket box positions, conduit chase lines, spotlight ceiling positions on slab, halo conduit drop, cavity sub-pockets (socket + speaker), Hikvision doorbell back box position on outside face, CAM-1 spare position on porch W wall, CAM-2 stub position on porch soffit, Waveshare back box position. Take photos of every mark. |
| Deliverable | All marks chalked. Photographs of every wall. |
| Sign-off | Homeowner signs off in person before any cutting starts. NOTHING gets cut today. |

### 16.3 — Phase 2 — Wall chasing + cavity cutting (Day 2-3)

| Property | Value |
|---|---|
| Owner | Electrician |
| Duration | 2 days |
| Tools | Angle grinder, chisel + hammer, core drill, wall chaser |
| What happens | Cut the main cavity (22¾ × 14⅞ × 4"); cut the socket sub-pocket (3×3×2½"); cut the speaker sub-pocket (3" dia × 1"); cut the DB recess (15¾ × 23⅝ × 4"); cut the 6-gang switch panel pocket (335 × 75 × 65 mm) plus all other back box pockets; cut the Hikvision doorbell back box pocket on porch wall; cut all conduit chases (vertical and horizontal) per the conduit schedule |
| Deliverable | All cavities + back boxes cut to spec; all conduit chases cut |
| Sign-off | Cavities verified to dimension with tape measure; sub-pockets verified; chases verified at correct heights |

### 16.4 — Phase 3 — Conduit pulling (Day 4-5)

| Property | Value |
|---|---|
| Owner | Electrician |
| Duration | 2 days |
| Tools | Conduit bends, couplers, draw wire (fish tape) |
| What happens | Lay all 23 conduits per Section 11 schedule. Use coloured PVC where available, otherwise label with tape + permanent marker. Insert pull strings in every conduit. Cap all conduit ends with masking tape so plaster doesn't enter. Floor route conduits (Cavity-Data, Doorbell, CAM1) MUST be laid in floor screed before tiling. |
| Deliverable | All conduits in place; ends labelled; draw strings in; all caps fitted |
| Sign-off | Conduit count matches Section 11 list; each conduit labelled and verified |

### 16.5 — Phase 4 — Wire pulling + DB install (Day 6-7)

| Property | Value |
|---|---|
| Owner | Electrician |
| Duration | 2 days |
| Tools | Fish tape, multimeter, RJ45 crimper, Cat6 tester |
| What happens | Pull wires through conduits per Section 12 schedule. Every smart-switch box gets L+N+E (cap unused neutrals). Mount Schneider Acti9 48-way DB. Connect MCBs and RCBOs per Section 13 circuit list. Leave 300 mm tail of wires inside every switch box. Test earth continuity at every metallic body (< 1 ohm). Pull outdoor LSZH UV Cat6 through niche-to-cavity, niche-to-doorbell, niche-to-Waveshare conduits. |
| Deliverable | Wires labelled at both ends; earth continuity tested; tails inside boxes; Cat6 cables pulled |
| Sign-off | Wire schedule completed; MCBs labelled; Cat6 tester verifies all pulled cables |

### 16.6 — Phase 5 — First plaster (rough coat) (Day 8-10)

| Property | Value |
|---|---|
| Owner | Mason |
| Duration | 3 days (including 48-hour cure) |
| Tools | Plaster materials, trowels |
| What happens | Apply rough plaster coat over chased walls. Conduits and back boxes flush with finished plaster line. Plaster STOPS at: (a) cavity edge, (b) DB recess edge, (c) every switch and socket box rim. Cure 48 hours minimum. |
| Deliverable | Plaster level, no conduits visible, no boxes buried beyond rim |
| Sign-off | Plaster level checked with spirit level; box rims accessible |

### 16.7 — Phase 6 — Cavity interior matte black (Day 11)

| Property | Value |
|---|---|
| Owner | Painter |
| Duration | 1 day (1 hour work + dry time) |
| Tools | Brush, roller, matte black acrylic emulsion |
| What happens | Paint cavity interior matte black: BACK WALL (all of it) + 4 INNER WALLS in the DEEPER 70 mm portion (NOT the front 30 mm where stone goes). All 2 coats. Speaker pocket interior painted too. Socket pocket interior painted too. |
| Deliverable | Cavity interior fully matte black, no shiny spots, edges crisp |
| Sign-off | Visual check: no plaster bleed-through, no missed spots |

### 16.8 — Phase 7 — VESA backing + carpenter prep (Day 11, parallel with Phase 6)

| Property | Value |
|---|---|
| Owner | Carpenter |
| Duration | 1 day (in parallel with painter) |
| Tools | Drill, screws, rawl plugs |
| What happens | (Option A) Drill VESA pattern (75 × 75 mm) directly into cavity back wall masonry with rawl plugs. (Option B) Cut 8" × 4" × ½" BWP plywood, paint matte black, screw to back wall, then VESA bracket to ply. Cut MDF speaker baffle (3½" × 3½" × ¼") with 3⅛" hole, paint matte black. |
| Deliverable | VESA anchor ready; speaker baffle ready |
| Sign-off | VESA position verified (cavity centre, 1450 mm FFL); baffle ready for install |

### 16.9 — Phase 8 — Stone cladding (Day 12-15)

| Property | Value |
|---|---|
| Owner | Stone cladder |
| Duration | 4 days (including curing) |
| Tools | Tile saw, MS polymer adhesive, mechanical clips, mortar |
| What happens | Clad 6 ft × 11 ft S feature wall in rustic ledgestone mix. **PLUS** wrap stone slips (¾" / 20 mm thick) into the cavity reveal — first 30 mm depth on all 4 inner walls (top, bottom, left, right). Stone does NOT enter the deeper 70 mm of cavity or the back wall. Stone face flush with the cavity opening. |
| Deliverable | Stone cladding complete, reveal wrap done, no protrusion into deeper cavity, conduits accessible, no loose stones, mortar joints raked clean |
| Sign-off | Visual check: stone wrap depth uniform; no stone in back portion; halo strip mounting line (at 30 mm depth) still accessible |

### 16.10 — Phase 9 — False ceiling + cove + drivers (Day 16-19)

| Property | Value |
|---|---|
| Owner | Gypsum / POP contractor + Electrician |
| Duration | 4 days |
| Tools | GI grid, gypsum boards, inspection hatch hardware, drivers |
| What happens | Drop ceiling from 11 ft to 9 ft (2 ft drop). Build 100 mm × 75 mm cove pocket around full perimeter. Install 300 × 300 mm inspection hatch above W edge. Install 2× GU10 spotlight cut-outs. Install cove LED strip (~10 m) inside cove pocket. Install cove + halo + shelf drivers above hatch. Connect 24V wires from drivers to strips. |
| Deliverable | Ceiling level, cove pocket continuous, hatch operable, spotlight cut-outs clean, all drivers installed and labelled |
| Sign-off | Test each driver gets 230V when its switch panel gang is pressed; visual check on cove uniformity |

### 16.11 — Phase 10 — Final paint (Day 20-22)

| Property | Value |
|---|---|
| Owner | Painter |
| Duration | 3 days |
| Tools | Roller, brushes, masking tape, paint |
| What happens | N wall + Living-side walls (where they meet foyer): warm ivory #F2EBDD, premium washable matte emulsion, 2 coats. Ceiling (false ceiling face) + cove inside: soft snow #F8F4EC, flat emulsion. Sample 2 ft × 2 ft each surface BEFORE bulk paint. Mask the stone wall fully. Mask all switch and socket boxes. |
| Deliverable | Paint even, no roller marks under raking light, masking removed cleanly |
| Sign-off | Visual check; switch / socket boxes free of paint |

### 16.12 — Phase 11 — Switch + socket fitting + smart-home commissioning (Day 23-25)

| Property | Value |
|---|---|
| Owner | Electrician + Smart-home installer |
| Duration | 3 days |
| Tools | Screwdrivers, RJ45 tools, Hik-Connect app, HA dashboard, multimeter |
| What happens | Fit modular plates (Schneider Unica or chosen brand) on all switch boxes. Install Sonoff modules behind smart switches. Install 2× recessed GU10 gimbal spotlights. Mount VESA bracket + Samsung monitor in cavity. Insert RPi Zero 2W + PoE splitter + sound card + amp + speaker. Run cavity-internal wiring. Install bezel CAM-0 on monitor top. Mount Hikvision doorbell on outside face of 1'6" wall. Configure Frigate + CompreFace + Home Assistant. Train 3 family faces. Test welcome flow. |
| Deliverable | Welcome flow tested with 3 known faces; unknown person triggers idle screen; doorbell works; spotlights, cove, halo all dim and switch; speaker chimes; door-bell-on-Waveshare logic placeholder |
| Sign-off | Final acceptance walkthrough with homeowner; all features demonstrated; defect list addressed |

---

## SECTION 17 — Pre-plaster sign-off checklist (the master gate)

This is the critical checkpoint before Phase 5 (plaster). **NOTHING about the welcome system can be changed after plaster goes on.** Print this checklist; tick off each item on-site before the plaster crew arrives.

### 17.1 — Critical gates

Each zone must pass its sign-off before the plaster crew is allowed to start. If ANY zone fails its sign-off, plaster is delayed until fixed.

| Gate | Owner verifies | Photographs required |
|---|---|---|
| Zone A (East wall) | Electrician + Homeowner | Yes — DB recess + cupboard mark, all 5 outgoing DB conduits, all 5 incoming water-auto conduits |
| Zone B (Cavity) | Electrician + Homeowner | Yes — cavity dimensions, sub-pockets, all 3 conduit entries, stone reveal markings |
| Zone C (N wall) | Electrician + Homeowner | Yes — switch panel back box, all 5+ outgoing conduits, Hikvision doorbell back box on outside face |
| Zone D (Ceiling) | Electrician + Homeowner | Yes — driver shelf location, hatch position, spot positions |
| Zone E (Porch external) | Electrician + Homeowner | Yes — Hikvision doorbell + CAM-1 spare + CAM-2 stub back boxes, all 3 outdoor conduits |
| Zone F (Staircase indoor) | Electrician + Homeowner | Yes — Waveshare back box |

### 17.2 — Master pre-plaster checklist

**General (before any zone sign-off):**

- [ ] FFL chalk line drawn on every wall (so heights can be verified from the actual floor level, not raw slab)
- [ ] All conduit labels readable (tape + marker on every conduit end)
- [ ] All pull strings inserted in spare / empty conduits
- [ ] All conduit ends capped with masking tape
- [ ] All back boxes set with rims slightly recessed (so plaster goes around rim, not on top)

**Zone A — East wall (DB + starter cupboard):**

- [ ] DB recess cut: 400 × 600 × 100 mm, flush, position 1500 mm FFL bottom edge
- [ ] Starter cupboard mount position marked (Option 1 or 2 chosen on-site)
- [ ] Homeowner signed off on layout choice (Option 1 or 2)
- [ ] All 5 outgoing DB conduits routed and labelled
- [ ] All 5 incoming water-auto conduits terminated at cupboard back panel
- [ ] Draw strings in every conduit; ends capped
- [ ] DB shell mounting bracket / rawl plugs ready
- [ ] Earth wire (4 sqmm Green/Yellow) routed from earth pit to DB

**Zone B — South feature wall (Screen Cavity):**

- [ ] **Cavity cut to 22¾" × 14⅞" × 4" (580 × 380 × 100 mm)** — verify with tape measure
- [ ] Cavity centred on 6 ft feature wall (24⅝" from each side edge, ON ACTUAL MEASURED WIDTH)
- [ ] Bottom edge at 50½" (1280 mm) FFL — verified from FFL chalk line
- [ ] **Socket pocket** cut: 3" × 3" × 2½" deep, centred horizontally, centre at 53" FFL
- [ ] **Speaker pocket** cut: 3" diameter × 1" deep, centred horizontally, centre at 57⅛" FFL
- [ ] Conduit #1 (Power) hole: 1" diameter, bottom-LEFT corner, 1½" up + 2" in
- [ ] Conduit #2 (Data) hole: 1" diameter, bottom-RIGHT corner, 1½" up + 2" in
- [ ] Conduit #3 (Halo) hole: ⅝" diameter, top-CENTRE, ¾" down
- [ ] Conduit #4 (Ceiling Speaker provision) exit: ⅝" diameter, top wall, going up
- [ ] All 3 cavity-back-wall conduit stubs protrude 1-1½" into cavity, capped
- [ ] Stone cladder briefed on the 30 mm reveal depth specification
- [ ] Painter briefed: do NOT paint the front 30 mm of inner walls
- [ ] Cavity dimensions photographed
- [ ] Walnut shelf bracket positions chalked at 900 mm FFL on S wall

**Zone C — North wall (Switch Panel + door + window):**

- [ ] N wall total length verified (~9'6" / 2895 mm)
- [ ] Door opening cut to 3'2" wide × 7 ft tall
- [ ] Window opening cut to 3'6" wide × 5 ft tall (corner wrap confirmed)
- [ ] Vascal wall section confirmed (~1'4" East of door)
- [ ] 1'6" wall section between door and window confirmed
- [ ] **Foyer Switch Panel back box installed: 6-gang GI MS (or 7/8-gang if it fits), 335 × 75 × 65 mm**, centred horizontally, centre at 1200 mm FFL
- [ ] C-DB-Foyer-Switch conduit terminated at back box
- [ ] All outgoing conduits from switch panel routed (4 mandatory + 2 porch + spare slots)
- [ ] Draw strings in all conduits
- [ ] **Hikvision doorbell back box installed on OUTSIDE face of 1'6" section**, 1450 mm FFL, sized per electrician's discretion (default 75 × 75 × 65 mm)
- [ ] Cat6 cable pulled through C-Niche-Doorbell conduit, 300 mm tail in back box, capped

**Zone D — Foyer ceiling:**

- [ ] False ceiling drop confirmed at 2 ft (from 11 ft to 9 ft FFL)
- [ ] Cove pocket dimensions: 100 mm wide × 75 mm deep, around full perimeter
- [ ] Inspection hatch position marked: 300 × 300 mm, W edge
- [ ] 2× GU10 ceiling box positions chalked on raw slab (609 + 1218 mm from N edge, 300 mm from W wall)
- [ ] All ceiling-area conduits terminated at false ceiling level (C-SW-Spots, C-SW-Cove-Halo, C-Halo-24V drop to cavity, C-Cavity-Ceiling-Speaker provision exit)
- [ ] Driver shelf location marked above inspection hatch

**Zone E — Porch (external):**

- [ ] All 3 porch conduits routed from niche (C-Niche-Doorbell, C-Niche-CAM1, C-Niche-CAM2)
- [ ] **Floor segment of all 3 floor-route conduits laid BEFORE tile contractor arrives** ⚠️ CRITICAL
- [ ] Weatherproof back boxes installed:
  - Hikvision doorbell (outside 1'6" N wall section, 1450 mm FFL)
  - CAM-1 spare (porch W wall, 1650 mm FFL — capped)
  - CAM-2 stub (porch soffit NE corner, ~2700 mm FFL — capped)
- [ ] Pull strings in unused conduits (CAM-1, CAM-2)
- [ ] Cat6 pulled in C-Niche-Doorbell (300 mm tail in back box)
- [ ] All conduit ends capped with masking tape

**Zone F — Staircase indoor:**

- [ ] Waveshare back box installed at 1500 mm FFL on staircase S wall
- [ ] C-Niche-Waveshare conduit terminated at box
- [ ] Cat6 pulled through, 300 mm tail in box, capped

### 17.3 — Photographs to take BEFORE plaster

Take at least 25 photographs before plaster arrives. Store in `Home Interior and Automation/Inconstruction images/foyer-preplaster/` for permanent reference:

1. East wall — DB recess + cupboard area (3 angles)
2. East wall — outgoing DB conduits visible
3. South feature wall — cavity (front view)
4. South feature wall — cavity (close-up of each conduit entry hole)
5. South feature wall — cavity (close-up of socket pocket + speaker pocket)
6. South feature wall — walnut shelf bracket positions chalked
7. North wall — full elevation showing window + 1'6" section + door
8. North wall — switch panel back box position with tape measure showing centre at 1200 mm FFL
9. North wall outside — Hikvision doorbell back box at 1450 mm FFL
10. Porch — CAM-1 spare back box on porch W wall
11. Porch — CAM-2 stub back box on porch soffit
12. Floor — ALL 3 floor-route conduits visible before tile (Cavity, Doorbell, CAM1)
13. False ceiling area — all conduit ends at false ceiling level
14. Staircase niche — Waveshare conduit termination
15-25: details of any non-standard installation choices

### 17.4 — Homeowner sign-off form

```
   ────────────────────────────────────────────────────
   FOYER WELCOME SYSTEM — PRE-PLASTER SIGN-OFF FORM
   ────────────────────────────────────────────────────
   
   Project: Ganesh Prasad Home, Chitradurga
   Document version: 1.0
   Sign-off date: __________________
   
   I have verified the following:
   
   [ ] All zones above are checked off
   [ ] All photographs have been taken
   [ ] All conduit labels match the Section 11 master schedule
   [ ] All conduit ends are capped with masking tape
   [ ] All draw strings are in place
   [ ] FFL chalk line is visible on every wall
   [ ] DB + starter cupboard layout choice (Option 1 / Option 2) is decided
   [ ] Walnut shelf LED driver location choice (Option 1 / Option 2) is decided OR deferred to electrician's discretion
   [ ] 6-gang vs 7-gang vs 8-gang switch panel choice is decided
   [ ] Hikvision doorbell back box choice is finalised (or delegated to electrician)
   
   ☑ I AUTHORISE the plaster crew to begin Phase 5.
   
   Homeowner signature: ___________________________
   Date: ___________________________________________
   
   Electrician acknowledgement: ____________________
   Date: ___________________________________________
   
   ────────────────────────────────────────────────────
```

---

## SECTION 18 — Flagged open items (decide later, may need separate sessions)

These items are NOT covered in this plan. Some may need conduit provisioning RIGHT NOW (already done where applicable); others can be fully designed later. Listed here so they're not forgotten.

### 18.1 — Open: Smart door lock for "tap to unlock"

| Property | Value |
|---|---|
| What it is | An electronic door lock that can be remotely unlocked via Home Assistant (or via the Waveshare touchscreen "unlock" button) |
| Why deferred | Requires hardware selection (battery deadbolt vs electronic strike vs maglock); each has different conduit needs |
| What's needed now | Nothing — battery-powered smart deadbolts (Yale YDM7116, Hafele Catus) work without conduit. If you choose wired electronic strike or maglock, conduit must be laid before plaster — **but you haven't chosen yet**. |
| Recommendation | Defer to a separate session; choose battery smart deadbolt as default if undecided (no pre-plaster work needed) |
| Cost when added | ₹12,000-15,000 |

### 18.2 — Open: Dining hall speaker provision

| Property | Value |
|---|---|
| What it is | A mono in-ceiling speaker in the dining hall for ambient low-volume dinner music, controlled by Home Assistant. Foyer-architecture pattern (Pi + cheap Class-D amp + bare driver) — much cheaper than commercial in-ceiling speaker + standalone amp. |
| Status | **PROVISION LOCKED 2026-05-29 (foyer-pattern, Option B)** — conduit + Cat6 PoE, architecture supports both "shared screen Pi" and "dedicated speaker Pi" decisions at install time. Speaker + amp + Pi hardware deferred. |
| Architecture | **Mono — 1 in-ceiling speaker centered above the dining table.** Mono chosen over stereo for ambient dinner-music use case (equal sound for all diners, no sweet-spot issue). Speaker driven by a Pi running PAM8403 amp + USB sound card (foyer pattern). |
| Pre-plaster provision (TODAY) | **NEW conduit `C-Niche-DiningSpeaker`** — 25mm GREY PVC (LV-25, data conduit family), ~10m, from staircase niche → up niche wall → across GF slab ceiling chase → terminate at a capped ceiling junction box centered above the future dining table position. **1× indoor Cat6 + 1× pull-string** inside the conduit. PoE-capable (powers a future Pi at the ceiling if needed). Exact ceiling position defer to interior designer. |
| Future architecture options (decide at install time) | **(a) Shared screen Pi (cheapest, ~₹4,000)** — the dining screen's Pi Zero 2W (mounted behind the wall screen) drives BOTH the screen AND the speaker. Small audio cable runs from screen Pi through false ceiling void (~2-3m) to ceiling speaker. The C-Niche-DiningSpeaker conduit's Cat6 stays unused as a spare. **(b) Dedicated speaker Pi (~₹6,000)** — a second Pi Zero 2W lives in a small junction box near the ceiling speaker, powered by PoE on the C-Niche-DiningSpeaker Cat6. Independent of the screen Pi. Slightly more setup but cleaner failure isolation. |
| Future hardware (when installed) | **3" flush-mount commercial ceiling speaker** (JBL Control 12C, Polk RC60i, or comparable Indian brand, ~₹1,800-3,000) — same speaker spec as the foyer ceiling speaker installed 2026-05-22 (consistency across both ceiling-speaker locations) + **PAM8403 Class-D amp** (~₹200) + **USB sound card** (~₹150) + 2-core speaker wire ~3m from amp location to ceiling speaker (~₹100) + cabling (~₹200). Speaker is a fully-enclosed module with built-in back-can — recessed via standard ceiling-box, NO bare driver / MDF baffle / "void-as-enclosure" tricks (those were the OLD foyer cavity-speaker plan that was dropped 2026-05-22). |
| Cost today | **~₹500** (25mm grey conduit + 1× Cat6 + pull-string + capped junction box) |
| Cost when fully installed | **~₹4,000-6,000** depending on shared-Pi vs dedicated-Pi choice |
| Why we dropped the "WiiM/Fosi" path | Foyer welcome system already proved that a Pi Zero + PAM8403 + bare driver delivers genuinely acceptable ambient audio for ~₹2,500 in hardware. Premium WiiM/Polk path (~₹22K) was over-spec for "dinner background music" use case. |
| Trade-off vs WiiM premium path | Sound character is "clear voice + adequate music ambient" — not "premium music room". Standard 3" commercial flush-mount speaker is single-driver (or small 2-way), weaker on deep bass than premium in-ceiling. Saves ₹16K vs WiiM path. Genuinely the right choice for the use case. Same speaker model as foyer ceiling speaker = no extra brand/spec decisions to track. |

### 18.3 — RESOLVED 2026-05-25 v2.0: Waveshare indoor panels (Beelink-direct, no Pi)

| Property | Value |
|---|---|
| What it is | Waveshare 10.1" **HDMI** capacitive touchscreen on staircase S wall, driven **directly from Beelink** in the niche via HDMI 2 + USB-A (no Pi). USB ACR122U NFC reader behind walnut bezel. Plus a 2nd screen provisioned for future install on the dining hall E wall. |
| Status | **Hardware + mount + cabling LOCKED 2026-05-25 (v2.0).** Dashboard layout still deferred. Dining wall position + height defer to on-site marking. |
| Spec doc | [WAVESHARE_INDOOR_PANEL.md](WAVESHARE_INDOOR_PANEL.md) — full handout (15 sections, v2.0) |
| Key v1→v2 changes | (1) Pi 5 dropped — Beelink drives the HDMI screen directly via its 2nd HDMI port + a USB port. (2) NFC reader changed from GPIO PN532 to USB ACR122U (no Pi means no GPIO). (3) Existing Cat6 in `C-Niche-Waveshare` becomes a SPARE; HDMI + USB cables pulled alongside it. (4) **NEW** conduit `C-Niche-Dining` provisioned to dining hall E wall for future 2nd panel. Saves ~₹16K vs v1.0 Pi 5 plan. |
| What's needed now (URGENT — before plaster on 2026-05-30) | (a) Electrician pulls new HDMI + USB cables through existing staircase conduit alongside Cat6 (~30 min). (b) Electrician lays NEW `C-Niche-Dining` conduit (25mm GREY, ~7-8m) from niche → dining hall E wall via ceiling, with Cat6 + pull-string, terminating at a back box. (c) Homeowner walks dining hall with electrician on cable-pull day to mark wall position + height. |
| Total cost | ~₹20,250 today (staircase build + dining cable provision), ~₹38K lifetime (both screens fully built) |

### 18.4 — Open: Door grill on East jamb (outside)

| Property | Value |
|---|---|
| What it is | A traditional Indian-style decorative iron grill mounted on the vascal area (East of main door, outside face) |
| Why deferred | Style choice — homeowner preference; doesn't affect electrical |
| What's needed now | Nothing — purely decorative, installed during finishing phase |
| Recommendation | Decide during finishing phase based on overall facade aesthetic |

### 18.5 — Open: Aesthetic switch plate brand

| Property | Value |
|---|---|
| What it is | The face plate brand for all switch boxes (Foyer Switch Panel, Cavity Socket Panel, future Porch Wall) |
| Why deferred | Aesthetic decision; depends on overall foyer finishing palette |
| Recommendation options | (1) Schneider Unica Pure in champagne metallic (~₹3k); (2) Aqara H1 EU 6-gang touch panel in black glass (~₹7k); (3) Anchor Roma Urban chrome black (~₹2.5k) |
| When to decide | During finishing phase (Phase 11); doesn't affect conduit or back box work |

### 18.6 — Open: Walnut shelf LED driver location

| Property | Value |
|---|---|
| Decision | Option 1 (above false ceiling) vs Option 2 (under shelf) |
| Why deferred | Best decided on-site after shelf carpentry begins |
| Owner | Electrician + Carpenter |

### 18.7 — Open: Hikvision doorbell back box exact spec

| Property | Value |
|---|---|
| Decision | Final choice of back box brand/model |
| Why deferred | Electrician's experience with this brand of doorbell |
| Owner | Electrician |
| Constraint | Must be smaller than the Hikvision doorbell's mounting bracket footprint |

### 18.8 — Open: DB + starter cupboard final layout

| Property | Value |
|---|---|
| Decision | Arrangement Option 1 (DB recessed + Cupboard south of door) vs Option 2 (stacked vertically) |
| Why deferred | Best decided on-site with actual wall measurements after Phase 2 chasing |
| Owner | Electrician + Carpenter + Homeowner |

### 18.9 — Cross-references to other documents

| Document | What it covers |
|---|---|
| [conduits-and-cavities.md](conduits-and-cavities.md) | General conduit rules + whole-house conduit schedule |
| [water-automation-conduits.md](water-automation-conduits.md) | Water automation system conduits (5 of these terminate in the foyer DB cupboard) |
| [db-layout.md](db-layout.md) | DB internal circuit layout (whole house, including the 2 foyer MCBs) |
| [ground-floor-electrical.md](ground-floor-electrical.md) | All other ground-floor electrical items |
| [materials-checklist.md](materials-checklist.md) | Broader house materials list (this Section 15 is foyer subset) |
| [decisions/decision-log.md](../decisions/decision-log.md) | Locked design decisions across the project |

---

## END OF DOCUMENT

**Document version 1.0 — 2026-05-22**
**Foyer Welcome System — Master Electrician Plan**
**Project: Ganesh Prasad Home, Chitradurga**

**Total document scope:** 18 sections covering everything the electrician, mason, painter, carpenter, stone cladder, false-ceiling contractor, and smart-home installer need to deliver the foyer welcome system, from pre-plaster conduit laying through final commissioning.

**Critical next step:** Phase 1 — marking + sign-off — starts **2026-05-23 (tomorrow)**. Homeowner walks the site with the electrician + carpenter, chalk-marks every position per this document, takes photos, signs off. Phase 2 (cutting) starts immediately after sign-off.

**Total estimated cost:** ~₹1,06,230 (foyer welcome scope only — excludes smart lock, dining hall speaker, Waveshare hardware which are flagged in Section 18 for separate sessions).

**For any clarification during install:** reference this document by section number. If something on-site doesn't match a section, STOP and call the homeowner before proceeding.

---

*Generated as part of the home interior & automation project. Will be updated as decisions evolve and as on-site reality refines the plan. Last revised: 2026-05-22.*
