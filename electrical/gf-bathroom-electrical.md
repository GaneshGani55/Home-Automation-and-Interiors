# GF Common Bathroom — Complete Electrical Layout

**Room:** Ground Floor Common Bathroom
**Size:** 9'0" (E–W) × 4'6" (N–S) | **Ceiling:** 8ft flat RCC slab (attic above lintel)
**Circuits:** A1 (lighting + exhaust) · A2 (geyser)
**DB slots:** See [db-layout.md](db-layout.md)

> **Critical:** This bathroom has an attic above the 8ft lintel. ALL ceiling conduit runs happen in the attic. Core-drill downlight and exhaust fan holes from the attic side. Chase wall conduits before plastering.

---

## 1. Coordinate System Used in This Doc

```
         x = 0                               x = 9ft
         EAST WALL                           WEST WALL
  y=4.5  ┌───────────────────────────────────────┐
  NORTH  │                                       │
         │                  ROOM                 │
  SOUTH  │                                       │
  y=0    └───────────────────────────────────────┘
         ← door (y=0 to y=2.5ft, left corner)

Heights: z = 0 (floor) to z = 8ft (ceiling/lintel)
```

---

## 2. IP Zone Map (IEC 60364-7-701)

```
PLAN VIEW — IP ZONES
         WEST
    ┌────────────────────────────────┬──────────────┐
    │                                │              │
    │    ZONE 2                      │   ZONE 1     │
    │    (IP44 min)                  │   (IP65 min) │
    │    ← dry zone (5.5ft) →        │ ←shower 3.5ft│
    │                          [GLASS│PARTITION]    │
    │    WC         VANITY           │              │
    └────────────────────────────────┴──────────────┘
         EAST                                  WEST

  Zone 0 (IP67): Shower floor surface only
  Zone 1 (IP65): Shower zone — full ceiling + walls within shower enclosure
  Zone 2 (IP44): 0.6m outside Zone 1 boundary (≈ 2ft east of glass partition = up to x=3.5ft)
  Outside zones : Remainder of dry zone (vanity end) — IP20 acceptable, use IP44 for safety

ELEVATION — ZONE BOUNDARIES ON WEST WALL:
  8ft ─────────────────── CEILING / LINTEL
         [  NO SPACE  ]   (window top flush with lintel)
  4ft ─ ─ ─ ─ ─ ─ ─ ─ ─  Window sill (3ft wide window)
         [   WINDOW   ]   frosted glass
  0ft ─────────────────── FLOOR
```

---

## 3. Lighting & Point Schedule

### Fixed Coordinates

| ID | Point | Wall/Ceiling | x from East | y from South | z (height) | IP Rating | Wattage | Circuit |
|---|---|---|---|---|---|---|---|---|
| L1 | LED backlit mirror | North wall | 1.0ft (centre of vanity) | N wall (y=4.5ft) | 1.35m centre | IP44 | 15W | A1 via PIR |
| L2 | IP44 recessed downlight — dry zone | Ceiling | 3.0ft | 2.25ft (N-S centre) | 8ft (ceiling) | IP44 | 7W | A1 via PIR |
| L3 | IP65 recessed downlight — shower | Ceiling | 7.25ft | 2.25ft (N-S centre) | 8ft (ceiling) | IP65 ✱ | 7W | A1 via PIR |
| L4 | IP65 LED strip — upper niche | South wall | 7.25ft | y=0 (south wall) | 1.4m (niche centre) | IP65 ✱ | 5W | A1 via PIR |
| EF | IP65 exhaust fan | Ceiling | 8.0ft | 2.25ft (N-S centre) | 8ft (ceiling) | IP65 ✱ | 25W | A1 via manual |
| SW | Switch board | East wall | x=0 (east wall) | 3.25ft from south | 1.35m | — | — | A1 + A2 |
| GY | Geyser 15L | Attic above bathroom | attic | attic | attic level | — | 2000W | A2 |

✱ Mandatory IP65 — these are in Zone 1 (shower ceiling) or Zone 0 boundary.

> **L2 note:** Technically outside Zone 2 (>0.6m from partition), but specify IP44 anyway — it is cheap insurance and consistent spec.

---

## 4. Lighting Layout — Plan View

```
PLAN VIEW (TOP DOWN) — 9ft × 4'6"
Scale: each [ ] ≈ 1ft

         x=0          x=3      x=5.5    x=7.25  x=9
  y=4.5  ┌────────────┬────────┬────────┬───────┬───┐  NORTH WALL
  NORTH  │            │        │        │       │   │
         │  VANITY    │  W C   │[glass] │       │[W]│  W=window on west wall
         │  +MIRROR   │        │partition│      │[I]│  sill@4ft, top@8ft
         │  [L1 north │        │        │       │[N]│
         │   wall]    │        │        │       │[D]│
         │            │        │        │       │[O]│
         │     [L2]   │        │  [L3]  │ [EF]  │[W]│
         │     ceil   │        │  ceil  │  ceil │   │
         │     3ft    │        │ 7.25ft │  8ft  │   │
         │            │        │        │       │   │
         │  ←─── DRY ZONE ────→│←─── SHOWER ───→   │
         │     (5.5ft)         │     (3.5ft)        │
  y=0    └────┬───────────────────────────────────  ┘  SOUTH WALL
  SOUTH  [DOOR]  [SW]                   ↑
         2.5ft    east wall,       [L4] niche LED
                  right of door    on south wall @ x=7.25ft
                  y=3.25ft         z=1.4m

  EAST WALL: door (y=0 to y=2.5ft) + switch box (y=2.5ft to y=4ft)
```

### Fixture Callout

```
L1  — LED backlit mirror (15W, IP44, 600×800mm)
      Power exit point: North wall, x=1.0ft, z=1.35m
      Mirror bottom edge: z=1.2m from floor
      Mirror top edge: z=2.0m from floor

L2  — IP44 recessed downlight (7W, 3000K, 75mm dia, white bezel)
      Core drill: ø75mm, ceiling at x=3.0ft, y=2.25ft
      Illuminates WC and transition zone

L3  — IP65 recessed downlight (7W, 3000K, 75mm dia, chrome bezel)
      Core drill: ø75mm, ceiling at x=7.25ft, y=2.25ft
      MUST be IP65 — inside shower Zone 1

L4  — IP65 LED strip (warm 3000K, 24V DC)
      Upper niche, south wall, x=7.25ft, z=1.4m centre
      Strip runs inside top edge of niche facing downward
      Driver: 24V 10W, hidden in attic or behind niche on south wall
      MUST be IP65 — inside shower Zone 1

EF  — IP65 exhaust fan (150mm dia, ceiling mount, 25W)
      Core drill: ø165mm, ceiling at x=8.0ft, y=2.25ft
      Duct: flexible 150mm duct, runs through attic → exit north or south external wall
      MUST be IP65 — inside shower Zone 1
```

---

## 5. Switch Board Detail

**Location:** East wall, right side of door frame, centred at y=3.25ft from south wall, z=1.35m

**Board type:** 4-module modular plate (Legrand Britzy / Schneider Unica / similar)

```
┌────────────────────────────────┐
│  [  PIR SWITCH  ]  [6A SW ]   │   ← Module positions
│   (2 modules)      exhaust fan │
│  [16A SW + NEON]  [  spare  ] │
│   geyser 16A       (blanked)  │
└────────────────────────────────┘
   z = 1.35m from floor
   y = 3.25ft from south wall on east wall
```

| Module | Device | Rating | Controls | Notes |
|---|---|---|---|---|
| 1–2 | PIR auto-off switch | 6A, 230V | L1 + L2 + L3 + L4 (all lights) | Set timer to 10 min; lux dial to MAX |
| 3 | 1-gang switch | 6A | EF (exhaust fan) | Manual — NOT on PIR |
| 4 | 1-gang switch + neon indicator | 16A | Geyser 15L (in attic) | Neon shows geyser is ON |

> **Why geyser switch here (inside bathroom door)?**
> Per IS 3043, the bathroom switch for a geyser must not be operable from within the shower zone or within reach of the shower. Placing it immediately right of the entry door — accessible from the dry zone and from outside the room — is standard Indian practice and acceptable. The switch is outside the Zone 1 and Zone 2 boundaries. ✅

---

## 6. Conduit Routing — Plan View

```
CONDUIT ROUTING (ATTIC VIEW, LOOKING DOWN)

         x=0                                      x=9
  y=4.5  ┌────────────────────────────────────────────┐
         │                                            │
         │      JB (junction box in attic)            │
         │         at x=4.5ft, y=2.25ft              │
         │               ●                            │
         │         ╔═════╝ (20mm conduit)             │
         │ ╔═══════╝  (run A — to switch wall)        │
         │ ║ [down east wall chase to SW @ 1.35m]     │
         │ ║                                          │
         │ ║         ╔════════╗ (run B — L2 drop)     │
         │ ║         ║        ║                       │
         │ ║         ▼        ▼ (run C — L3 drop)     │
         │ ║      [L2 core]  [L3 core]  [EF core]     │
         │ ║      x=3.0ft   x=7.25ft   x=8.0ft       │
         │ ║                  ║                       │
         │ ║         ╔════════╝ (run D — to south wall│
         │ ║         ║  niche L4, down south wall)    │
         │ ║     ╔═══╝ (run E — to north wall L1      │
         │ ║     ║     mirror, down north wall)        │
  y=0    └─╫─────╫────────────────────────────────────┘
            ║     ║
            ║     ▼
            ║  [L1 north wall chase, exit z=1.35m]
            ▼
         [SW east wall chase, exit z=1.35m]

INCOMING FROM DB:
  DB (foyer west wall) → through MBR zone → attic above bathroom
  25mm conduit carrying: 3-core 1.5mm² (A1) + 3-core 2.5mm² (A2) together
  Enter attic at north-east corner of bathroom ceiling
  Reach Junction Box in attic at x=4.5ft, y=2.25ft
```

### Conduit Run Summary

| Run | Route | Conduit | Cable | Notes |
|---|---|---|---|---|
| Incoming | DB → MBR zone → attic above bathroom | 25mm PVC | 1.5mm² 3-core (A1) + 2.5mm² 3-core (A2) | Shared conduit to bathroom entry, then split at JB |
| Run A | Attic JB → down east wall chase → SW | 20mm PVC | 1.5mm² 3-core (lighting) + 2.5mm² 3-core (geyser) | Chase east wall before plastering |
| Run B | Attic JB → core drill ceiling → L2 | 16mm PVC flex | 1.5mm² 3-core | Core drill ø75mm at x=3.0ft, y=2.25ft |
| Run C | Attic JB → core drill ceiling → L3 | 16mm PVC flex | 1.5mm² 3-core | Core drill ø75mm at x=7.25ft, y=2.25ft; IP65 fitting |
| Run D | Attic JB → core drill ceiling → EF | 20mm PVC | 1.5mm² 3-core | Core drill ø165mm at x=8.0ft, y=2.25ft; IP65 fitting |
| Run E | Attic JB → down north wall chase → L1 | 16mm PVC | 1.5mm² 3-core | Chase north wall, exit at x=1.0ft, z=1.35m |
| Run F | Attic JB → down south wall chase → L4 | 16mm PVC | 1.5mm² 2-core (LED driver output is DC, use separate DC cable from driver) | Chase south wall, exit at x=7.25ft, z=1.2m; driver in attic or at niche back |
| Geyser | SW geyser module → up east wall chase → attic → geyser | 20mm PVC | 2.5mm² 3-core | Separate from lighting cable; geyser in attic above bathroom |

---

## 7. Conduit Routing — Elevation Views

### East Wall Elevation (what the electrician chases)

```
  z=8ft ────── LINTEL / CEILING ──────────────────
                │
                │ (attic above — conduit enters from top)
                │
  z=4.5ft ─────┼──── [conduit enters wall chase here from attic]
                │
                │  20mm PVC chase in east wall
                │  (carries A1 lighting 1.5mm² + A2 geyser 2.5mm²)
                │
  z=1.35m ─────┼──── [SWITCH BOX exits here]
                │      4-module board
                │      PIR + exhaust switch + geyser switch
                │
  z=0 ──────── FLOOR ─────────────────────────────

  East wall section: chase is on the right side of the door frame
  (between door frame edge and north wall, ≈ 2ft width available)
```

### North Wall Elevation (mirror conduit)

```
  z=8ft ──────────────────────────────────────────
                │
                │ (conduit comes from attic, runs down north wall)
                │
  z=2.0m ──────┼──── (mirror top edge)
                │
  z=1.35m ─────┼──── [L1 POWER EXIT POINT — flush socket or stub]
                │      60mm-deep conduit box, 1 x 6A socket (concealed)
                │      or direct conduit stub — connect to mirror driver
                │
  z=1.2m ──────┼──── (mirror bottom edge)
                │
  z=0 ──────── FLOOR ─────────────────────────────

  Position: x=1.0ft from east wall on north wall
  Mirror is wall-hung — mirror driver/transformer sits inside mirror housing
  Conduit stub exits flush behind mirror
```

### South Wall Elevation (niche LED)

```
  z=8ft ──────────────────────────────────────────
                │
                │ (conduit comes from attic, runs down south wall)
                │
  z=1.6m ──────┼──── [LED NICHE UPPER — conduit exits here]
                │      ← upper niche top edge is at z=1.5m
                │      LED strip clips inside niche top
                │      IP65 driver box mounts on south wall above niche
                │      OR driver in attic (cleaner)
                │
  z=1.4m ──────┼──── (niche centre)
                │
  z=1.3m ──────┼──── (niche bottom edge)
                │      [LOWER NICHE — no wiring needed]
                │
  z=0 ──────── FLOOR ─────────────────────────────

  Position: x=7.25ft from east on south wall
  Entire south wall section shown is INSIDE shower Zone 1
  ALL wiring here must be IP65; use IP65 rated conduit boxes
```

---

## 8. Complete Circuit Wiring Diagram

```
230V SUPPLY FROM DB
        │
        ├── RCBO 6A 30mA (A1) ─────────────────────────────────┐
        │                                                        │
        └── RCBO 16A 30mA (A2) ─── Geyser 15L (in attic) ─────┘
                                    (2000W, 2.5mm² cable)

A1 CIRCUIT — LIGHTING + EXHAUST:

  RCBO 6A (A1) in DB
       │
       │ 3-core 1.5mm² FRLS (Line, Neutral, Earth)
       │
  [JUNCTION BOX — in attic above bathroom]
       │
       ├──── Line → PIR SWITCH (module 1-2, east wall) → load output ─┐
       │                                                               │
       │     ┌─────────────────────────────────────────────────────── ┘
       │     │
       │     ├── L1 (LED mirror, north wall)          [15W, IP44]
       │     ├── L2 (recessed downlight, dry zone ceiling) [7W, IP44]
       │     ├── L3 (recessed downlight, shower ceiling)   [7W, IP65]
       │     └── L4 (LED strip driver → niche strip)       [5W, IP65]
       │
       └──── Line → MANUAL SWITCH (module 3, east wall) → EF [25W, IP65]

  Neutral and Earth from JB run to ALL fixtures directly (not through switch)

A2 CIRCUIT — GEYSER:

  RCBO 16A (A2) in DB
       │
       │ 3-core 2.5mm² FRLS
       │
  [16A SWITCH + NEON, module 4, east wall]
       │
  [15L Geyser in attic]
  (2000W load)

EARTH CONTINUITY:
  All metal fixture bodies connected to Earth (green/yellow wire)
  Earth wire runs from DB → JB → every fixture
  Continuity must be tested before plastering
```

---

## 9. DB Panel Schedule — Bathroom Circuits

| DB Slot | Circuit ID | RCBO | Load | Wire | Protected by |
|---|---|---|---|---|---|
| TBD | A1 | 6A, 30mA RCBO | Bathroom lighting + exhaust (54W total) | 1.5mm² 3-core FRLS | RCBO own RCD (30mA) |
| TBD | A2 | 16A, 30mA RCBO | Geyser 15L (2000W) | 2.5mm² 3-core FRLS | RCBO own RCD (30mA) |

> Both bathroom circuits get their own 30mA RCD protection via combined RCBO (not just MCB). This is mandatory for wet areas per IS 3043.

---

## 10. Cable & Conduit Bill of Quantities

### Conduit

| Item | Size | Est. Length | Notes |
|---|---|---|---|
| PVC conduit (rigid, heavy duty) | 25mm | 8m | Incoming run from DB to attic |
| PVC conduit (rigid) | 20mm | 6m | East wall chase (Run A) + geyser run (Run G) |
| PVC conduit (rigid) | 16mm | 10m | North wall chase + south wall chase + ceiling flex stubs |
| Conduit boxes (deep 60mm) | — | 6 nos | At each fixture exit point |
| Conduit coupling, bends, clamps | — | lot | As needed |
| Junction box IP55 | 100×100mm | 1 no | In attic |
| Exhaust fan duct (flexible aluminium) | 150mm dia | 3m | Attic to external wall vent |
| Duct louvre/grille (external wall) | 150mm | 1 no | Where duct exits outside |

### Cable

| Item | Spec | Est. Length | Notes |
|---|---|---|---|
| FRLS 3-core | 1.5mm², Havells/Finolex | 25m | A1 lighting circuit — all runs |
| FRLS 3-core | 2.5mm², Havells/Finolex | 8m | A2 geyser circuit |
| DC cable (LED strip) | 2-core 0.75mm² | 2m | 24V from driver to niche strip |
| Earth wire (extra) | 4mm² green/yellow | 5m | Bonding at geyser and shower mixer |

### Fixtures

| Item | Spec | Qty |
|---|---|---|
| PIR timer switch | Legrand/Schneider, 6A, 180°, adjustable timer | 1 |
| 6A 1-gang switch | Modular | 1 (exhaust fan) |
| 16A 1-gang switch + neon | Modular, 16A rated | 1 (geyser) |
| 4-module plate + frame | Matching brand to above | 1 set |
| IP44 recessed downlight | 7W, 3000K, 75mm, white | 1 (L2, dry zone) |
| IP65 recessed downlight | 7W, 3000K, 75mm, chrome or white | 1 (L3, shower zone) |
| IP65 exhaust fan | 150mm, ceiling mount, 30W max | 1 |
| IP65 LED strip (warm) | 3000K, 24V, 5W/m, min IP65 | 0.6m (for niche) |
| 24V LED driver (IP65) | 10W, 24V DC output | 1 (for niche strip) |
| 6A concealed socket or conduit stub | Behind mirror | 1 |
| RCBO 6A 30mA | A1 slot in DB | 1 |
| RCBO 16A 30mA | A2 slot in DB | 1 |

---

## 11. Installation Sequence

Do these IN ORDER — each step gates the next:

```
Step 1 — CONDUIT CHASING (before plastering)
  □ Chase east wall: 20mm conduit, from top (lintel level) down to switch box height (1.35m)
  □ Chase north wall: 16mm conduit, from top down to x=1.0ft, exit at 1.35m (mirror point)
  □ Chase south wall: 16mm conduit, from top down to x=7.25ft, exit at 1.5m (niche LED point)
  □ Confirm all conduit boxes are set flush in wall — call mason to fill and level

Step 2 — WIRING PULL (after chasing, before plastering)
  □ Pull 1.5mm² FRLS cable through all lighting conduits
  □ Pull 2.5mm² FRLS cable through geyser conduit
  □ Leave 300mm tail at every outlet point
  □ Label each cable tail: L1, L2, L3, L4, EF, GY

Step 3 — PLASTERING (by mason)
  □ Plaster walls — conduits and boxes are embedded, cable tails stick out
  □ Conduit box faces flush with plaster surface

Step 4 — CORE DRILLING (after plastering, before tiling)
  □ L2: ø75mm core drill at x=3.0ft, y=2.25ft on ceiling
  □ L3: ø75mm core drill at x=7.25ft, y=2.25ft on ceiling
  □ EF: ø165mm core drill at x=8.0ft, y=2.25ft on ceiling
  □ Run conduit stubs in attic from JB to each hole

Step 5 — WATERPROOFING (by civil team)
  □ Waterproof floor and lower walls — conduit boxes are already protected by being above WP line
  □ NICHE BOXING: Contractor builds niche boxes in south wall at this stage (before tiling)
  □ Niche must have conduit stub for LED strip cable at top-back

Step 6 — TILING (by tile contractor)
  □ Tiles go over conduit chase areas — boxes must be accessible (no tile over them)
  □ Niche interior tiled
  □ Cut tile carefully around L3 and EF core drill positions — fixtures sit flush in holes

Step 7 — FIXTURE INSTALLATION (by electrician)
  □ Fit PIR switch, exhaust switch, geyser switch in east wall board
  □ Fit L2 (dry zone downlight) in ceiling
  □ Fit L3 (IP65 downlight) in ceiling
  □ Fit EF (exhaust fan) in ceiling, connect duct to attic run
  □ Fit LED mirror on north wall, connect to conduit stub
  □ Fit IP65 LED strip in niche, connect driver (driver in attic or behind niche)
  □ Install geyser in attic, connect A2 cable

Step 8 — EARTH CONTINUITY + RCD TEST
  □ Test earth continuity at every metallic fixture with clamp meter (< 1Ω)
  □ Test RCD trip time on RCBO A1 and A2 (should trip < 30ms at 30mA)
  □ Test PIR switch: walk in, lights ON; leave, wait 10 min, lights OFF
  □ Test geyser switch + neon indicator

Step 9 — SIGN-OFF
  □ Electrician sign-off sheet (to be kept)
  □ Log completion in decisions/decision-log.md
```

---

## 12. Open Items Before Electrician Starts

- [ ] **Exhaust fan duct exit wall:** Which wall is external — north or south? Confirm so duct is routed correctly through attic.
- [ ] **Geyser exact position in attic:** Needs access hatch in attic for future servicing — decide hatch location before masonry is complete.
- [ ] **Mirror brand:** Confirm brand/model before electrician sets conduit exit (some mirrors use a plug socket, others need a direct hardwire terminal — affects conduit box type).
- [ ] **DB slot numbers** for A1 and A2 — confirm with [db-layout.md](db-layout.md).
