# Water Automation — Conduit Schedule (Electrician Handoff)

> **Hand this file to the electrician BEFORE plastering.** Every conduit listed here must be laid before walls are closed. Once plastered, retrofitting is wall-breaking work.
>
> Cross-reference: [conduits-and-cavities.md](conduits-and-cavities.md) for general conduit rules · [db-layout.md](db-layout.md) for DB circuits · [floor-plans-decoded.md](../floor-plans/floor-plans-decoded.md) for room dimensions.

---

## 0 — One-Page Cheat Sheet

### 0.1 The system in one diagram

```
                              ┌────────────────────────┐
                              │   Sintex 1500L         │
                              │   (terrace, SW corner) │
                              │   ╔══════════════════╗ │
                              │   ║ Ultrasonic +    ║ │
                              │   ║ high-level float ║ │
                              │   ╚════╤═══════╤═════╝ │
                              └────────┼───────┼──────┘
                                       │       │
                              ┌────────▼───────▼──────┐
                              │  Sintex JB (parapet)  │  ← ESP32 + PoE splitter
                              └────────┬───────┬──────┘
                                       │       │
                                       │       │ C-Sintex-2 (float, 220V)
                              C-Sintex-1       │ ↓ to DB cupboard
                              (Cat6 PoE)       │
                                       │       │
                                       ▼       ▼
   ┌────────────────────────────────────────────────────┐
   │                STAIRCASE NICHE                     │
   │  ┌──────────┐    ┌──────────────────────────────┐ │
   │  │ SERVER   │◄──►│  PoE switch / Cat6 backbone  │ │
   │  │ (HA)     │    └──────┬──────────────┬────────┘ │
   │  └──────────┘           │              │          │
   └─────────────────────────┼──────────────┼──────────┘
                  C-Sump-1   │              │   C-DB-Backup
                  (Cat6 PoE) │              │   (Cat6, future)
                             ▼              ▼
                  ┌──────────────────┐   ┌──────────────────────┐
                  │  Sump JB         │   │   DB CUPBOARD (foyer) │
                  │ (east external   │   │                       │
                  │  wall, ~1.2m)    │   │  ┌─────────────────┐  │
                  │  ESP32 + sensor  │   │  │ DB (existing)   │  │
                  └──────────┬───────┘   │  └─────────────────┘  │
                             │           │  ┌─────────────────┐  │
                             │ C-Sump-2  │  │ P1 starter      │  │
                             │ (float,   │  │ (Magnum PSP1H)  │  │
                             │  220V)    │  ├─────────────────┤  │
                             ▼           │  │ P2 starter      │  │
                  ┌──────────────────┐   │  │ (Magnum PSP1)   │  │
                  │   SUMP           │   │  ├─────────────────┤  │
                  │ (NE, outside)    │   │  │ Sonoff DUALR3   │  │
                  │                  │   │  └─────────────────┘  │
                  │  pressure probe  │   │                       │
                  │  low-level float │   │  Both float wires     │
                  └──────────────────┘   │  terminate here       │
                                          └────────┬─────────────┘
                                                   │
                                       C-Motor-P1  │  C-Motor-P2
                                       (4sqmm)     │  (2.5sqmm)
                                                   ▼
                                          ┌──────────────────┐
                                          │  Borewell motor  │
                                          │  + P2 in cage    │
                                          │  (east outside)  │
                                          └──────────────────┘
```

### 0.2 Five rules for this system

| # | Rule | Why |
|---|---|---|
| 1 | **Data and mains conduits never share** | Cat6 picks up 50Hz noise from 220V cables; safety code violation |
| 2 | **Parallel data + mains conduits separated by ≥50mm** | Minimum gap to keep induction acceptable |
| 3 | **Every conduit gets a pull-string left inside** | Lets future cables be added without breaking walls |
| 4 | **Horizontal terrace runs MUST be done before tiling/waterproofing** | Embed in screed; cannot retrofit under finished tile |
| 5 | **All JBs are IP65 minimum; outdoor JBs are IP66; cable glands required** | Monsoon + condensation eats non-sealed boxes |

### 0.3 Critical timing

| Phase | What must be ready |
|---|---|
| **Before plaster (~1 week)** | All 7 conduits laid + pull strings + JB mounting points marked |
| Before terrace tiling | C-Sintex-1 and C-Sintex-2 embedded in terrace screed |
| Before painting | JBs mounted, glands installed, conduit ends terminated |
| After paint, before move-in | Sensors + ESP32s + Sonoff installed, wiring completed |

---

## 1 — Master Conduit Schedule

| ID | Size | From | To | Cable Inside | Cable Spec | ~Length |
|---|---|---|---|---|---|---|
| **C-Sintex-1** | 20mm PVC (🩶 grey) | Server niche (staircase) | Sintex JB (terrace, SW corner parapet wall, ~1.2m AGL) | Cat6 UTP, single run | LSZH outdoor-rated Cat6 | **~42 ft (13m)** |
| **C-Sintex-2** | 16mm PVC | Sintex JB (terrace) | DB cupboard (foyer, east wall) | 2-core 1.5mm² flexible | 220V-rated, double-insulated | **~45 ft (14m)** |
| **C-Sump-1** | 20mm PVC (🩶 grey) | Server niche (staircase) | Sump JB (east external wall, ~1.2m AGL above manhole) | Cat6 UTP, single run | LSZH outdoor-rated Cat6 | **~25 ft (8m)** |
| **C-Sump-2** | 16mm PVC | Sump JB (east external wall) | DB cupboard | 2-core 1.5mm² flexible | 220V-rated, double-insulated | **~25 ft (8m)** |
| **C-DB-Backup** | 20mm PVC (🩶 grey) | Server niche (staircase) | DB cupboard | EMPTY — pull string only | Future Cat6 if ESP32 motor control desired | **~12 ft (4m)** |
| **C-Motor-P1** | 25mm PVC (🔵 blue) | DB cupboard | Borewell head (outside, location TBC) | 3-core 4mm² armoured | XLPE armoured submersible feeder | depends on borewell location; **likely existing run** — verify with electrician |
| **C-Motor-P2** | 25mm PVC (🔵 blue) | DB cupboard | P2 pump cage (east outside wall, immediately below where P1 starter would have gone) | 3-core 2.5mm² | PVC double-insulated | **~5 ft (1.5m)** |

**Total NEW conduit runs to lay: 7** (C-Motor-P1 may already exist).

---

## 2 — Conduit Details (Per Run)

### 2.1 C-Sintex-1 — Server → Sintex JB

**Purpose:** Carries Cat6 with PoE (data + 48V power) from server's PoE switch to the ESP32 in the Sintex JB.

**Routing:**
1. Start at staircase server niche, exit upward.
2. Run vertically through staircase shaft up to terrace level.
3. On terrace: exit shaft at FFL via a slab penetration (sealed).
4. Run horizontally embedded in terrace screed (under tile bed) from staircase exit point → SW corner.
5. Rise up the parapet wall (chase before painting) to JB position at ~1.2m AGL on the inner face of the parapet.
6. Terminate at Sintex JB with a 20mm rubber gland.

**Key points:**
- Use **outdoor-rated LSZH Cat6** for any segment exposed to terrace conditions, even though it's in conduit.
- Pull string left in conduit for future replacements.
- Slab penetration must be **sealed with fire-rated mastic** before terrace waterproofing layer is applied.

### 2.2 C-Sintex-2 — Sintex JB → DB cupboard

**Purpose:** Carries Sintex high-level float wire (220V, in series with both starter coils) from float (inside Sintex) down through JB to DB cupboard.

**Routing:**
1. Float cable enters Sintex JB through one of its bottom glands (transit only — does not terminate in JB; uses an internal in-line connector or terminal block to extend).
2. Continues from JB through C-Sintex-2 conduit, parallel to C-Sintex-1 (≥50mm separation).
3. Runs alongside C-Sintex-1 through terrace screed → down staircase shaft.
4. Exits staircase shaft at GF level, runs horizontally in chase to DB cupboard.
5. Terminates at a terminal block inside DB cupboard, jumpered in series with BOTH P1 and P2 contactor coil supplies.

**Key points:**
- **MUST be a separate conduit from C-Sintex-1.** Sharing with Cat6 is a code violation.
- 50mm minimum separation throughout the parallel run.
- Cable spec: 2-core 1.5mm² flexible, double-insulated, 220V-rated.

### 2.3 C-Sump-1 — Server → Sump JB

**Purpose:** Cat6 + PoE from server to sump JB's ESP32.

**Routing:**
1. Start at staircase server niche.
2. Run horizontally through wall chase at ceiling level to east external wall.
3. Exit external wall via sleeved penetration to outside.
4. Drop vertically along outside face of east wall to JB at ~1.2m AGL, sited directly above the sump manhole.
5. Terminate at sump JB with 20mm gland.

**Key points:**
- Sleeved penetration through external wall must slope **outward and downward** (so water cannot track inward along the conduit).
- Outdoor segment uses outdoor-rated Cat6.
- Pull string left.

### 2.4 C-Sump-2 — Sump JB → DB cupboard

**Purpose:** Sump low-level float wire (220V, in series with P2 coil only) from float (inside sump, on cable) up to JB (transit) and back into the home to DB cupboard.

**Routing:**
1. Float cable enters sump JB through bottom gland (transit — internal in-line connector or terminal block).
2. Continues from JB through C-Sump-2 conduit, parallel to C-Sump-1 (≥50mm separation).
3. Drops/runs back through external wall (separate sleeved penetration from C-Sump-1).
4. Inside the house: runs in wall chase to DB cupboard.
5. Terminates at a terminal block inside DB cupboard, jumpered in series with P2 contactor coil supply only.

**Key points:**
- Same separation rules as C-Sintex-2.
- 2-core 1.5mm² flexible, 220V-rated.

### 2.5 C-DB-Backup — Server → DB cupboard

**Purpose:** Empty conduit for future use. If WiFi-based motor control (current Sonoff design) becomes unreliable, a Cat6 can be pulled through this conduit to wire an ESP32-based motor controller in the DB cupboard.

**Routing:**
1. Start at staircase server niche.
2. Run horizontally through wall chase at ceiling level to foyer.
3. Down to DB cupboard at standard switch-board height (1200mm FFL or whatever the cupboard's cable entry is).
4. Terminate at a blanking plate inside DB cupboard with pull string left in conduit.

**Key points:**
- **No cable installed now.** Pull string only.
- Conduit ends sealed at both sides with caps to prevent debris ingress.
- Label both ends clearly: "WATER AUTOMATION — FUTURE Cat6".

### 2.6 C-Motor-P1 — DB cupboard → Borewell head

**Purpose:** Heavy AC power cable from P1 starter inside cupboard to the submersible motor in the borewell.

**Routing:**
1. Exits DB cupboard at floor level.
2. Through east wall (sleeved penetration with gland).
3. Outside: routed via existing outdoor cable trench/conduit (typically buried 300mm deep in soil) to the borewell head.
4. From borewell head, the submersible cable continues down inside the borewell casing to the motor (this segment is the existing in-bore cable).

**Key points:**
- **Verify with electrician if existing run can be reused.** P1 was previously planned outside; the cable run from the (formerly outdoor) starter to the borewell may still be usable. If the previous starter location is on the same east wall (just outside), the new run from inside the cupboard is just a few feet longer.
- Cable spec: 3-core 4mm² XLPE armoured (or whatever the existing cable was — match it).
- Earthing: connect motor frame earth to **dedicated motor earth pit** (separate from house earth pit, per electrical hardening notes).

### 2.7 C-Motor-P2 — DB cupboard → P2 cage

**Purpose:** AC power cable from P2 starter inside cupboard to P2 pump body in the outdoor cage.

**Routing:**
1. Exits DB cupboard at floor level.
2. Through east wall (sleeved penetration, gland on outside face).
3. Outside: short run down/across to the steel cage mounted on east wall.
4. Enters cage through a gland in the cage's side or top.
5. Terminates at P2 pump's terminal box (junction box on motor body).

**Key points:**
- Short run — ~5 ft.
- 3-core 2.5mm² PVC, double-insulated (no need for armoured at this short length above grade).
- Earthing: pump body earth → terminal box → cable's earth core → DB cupboard earth bar → motor earth pit.

---

## 3 — Junction Box Specifications

### 3.1 Sintex JB (terrace, parapet wall)

| Property | Spec |
|---|---|
| Type | Industrial polycarbonate, IP65 minimum (IP66 preferred for terrace) |
| Size | 200 × 200 × 100 mm |
| Mounting | Wall-mount, with sun shield if directly sun-exposed |
| Glands | 4× cable glands at bottom: 1× 20mm (C-Sintex-1 / Cat6), 1× 16mm (C-Sintex-2 / float in & out), 1× 12mm (sensor cable), 1× 12mm (float cable to tank) |
| Contents | WT32-ETH01 (ESP32 + Ethernet), PoE splitter (48→5V), 4-way terminal block (for sensor wires), 2-way terminal block (for float transit) |
| Power | From PoE only — no separate 230V at JB |
| Access | Hinged lid with gasket seal; tool-required to open (screw lid, not snap-fit) |

### 3.2 Sump JB (east external wall)

| Property | Spec |
|---|---|
| Type | Industrial polycarbonate, IP66 (outdoor, exposed) |
| Size | 200 × 200 × 100 mm |
| Mounting | Wall-mount at ~1.2m AGL, directly above sump manhole |
| Glands | 4× glands at bottom: 1× 20mm (C-Sump-1 / Cat6), 1× 16mm (C-Sump-2 / float in & out), 1× 12mm (sensor cable from sump), 1× 12mm (float cable from sump) |
| Contents | WT32-ETH01, PoE splitter, 3-way terminal block (pressure transducer wires), 2-way terminal block (float transit), 2-way low-voltage tap (float telemetry → ESP32 GPIO) |
| Power | From PoE only |
| Sun shield | Recommended — fibre cement sheet projecting 15cm above JB |

---

## 4 — DB Cupboard Requirements

> The DB cupboard is a new lockable enclosure in the foyer, adjacent to the existing DB. Houses both motor starters + Sonoff. See [db-layout.md](db-layout.md) for DB-internal circuit changes.

### 4.1 Cupboard physical specs

| Property | Spec |
|---|---|
| Type | Wooden / MDF / ply with hinged door |
| Internal size (minimum) | 600 × 400 × 250 mm |
| Door | Hinged with lock (child / tenant safety) |
| Ventilation | Slatted openings at top and bottom (~5% of door area) — starters dissipate heat |
| Cable entry | Bottom and back panels — provision for conduit entries from 7 runs above |
| Mounting | Wall-mounted, alongside DB, accessible without obstruction |

### 4.2 Cupboard interior layout

```
   ┌─────────────────────────────────────────┐
   │  Slatted vent (top)                     │
   ├─────────────────────────────────────────┤
   │                                          │
   │   ┌─────────────────┐                   │
   │   │  P1 starter     │                   │  ← Magnum PSP1H
   │   │  (existing)     │                   │     (1.5HP single-phase)
   │   │  Green/Red btns │                   │
   │   └─────────────────┘                   │
   │                                          │
   │   ┌─────────────────┐                   │
   │   │  P2 starter     │                   │  ← Magnum PSP1
   │   │  (new)          │                   │     (1HP single-phase)
   │   │  Green/Red btns │                   │
   │   └─────────────────┘                   │
   │                                          │
   │   ┌─────────────────┐                   │
   │   │ Sonoff DUALR3   │                   │  ← WiFi, 2 channels
   │   │  (Ch1=P1, Ch2=P2)│                  │     in series with coils
   │   └─────────────────┘                   │
   │                                          │
   │   ┌─────────────────┐                   │
   │   │ Terminal blocks │                   │  ← Float wire terminations
   │   │ — Sintex float  │                   │     + jumpers to coils
   │   │ — Sump float    │                   │
   │   └─────────────────┘                   │
   │                                          │
   ├─────────────────────────────────────────┤
   │  Slatted vent (bottom)                  │
   ├─────────────────────────────────────────┤
   │  Cable entries from below (7 conduits)  │
   └─────────────────────────────────────────┘
```

---

## 5 — Materials Checklist (for electrician)

### 5.1 Conduit + accessories

| Item | Qty | Notes |
|---|---|---|
| 20mm grey PVC conduit | ~80m (C-Sintex-1 13m + C-Sump-1 8m + C-DB-Backup 4m + spare) | ISI marked |
| 16mm PVC conduit | ~50m (C-Sintex-2 14m + C-Sump-2 8m + spare) | ISI marked |
| 25mm blue PVC conduit | ~30m (C-Motor-P1 + C-Motor-P2 + spare) | ISI marked, motor-power grade |
| Conduit bends, couplings, junctions | as needed | Same brand as conduit |
| Pull string (nylon twine) | 200m | Leave in every conduit |
| Slab/wall penetration sleeves | 4 (2 for east wall, 2 for terrace slab) | Plus fire-mastic for sealing |

### 5.2 Cables

| Cable | Qty | Notes |
|---|---|---|
| Outdoor LSZH Cat6 UTP | ~50m (C-Sintex-1 + C-Sump-1 + 20% slack) | UV-resistant outer jacket |
| 2-core 1.5mm² flexible 220V-rated | ~45m (C-Sintex-2 + C-Sump-2 + slack) | Double-insulated |
| 3-core 4mm² XLPE armoured | depends on borewell distance | C-Motor-P1; **verify existing cable first** |
| 3-core 2.5mm² PVC | ~5m + slack | C-Motor-P2 |

### 5.3 Junction boxes + glands

| Item | Qty |
|---|---|
| 200×200×100 IP65/IP66 enclosure | 2 (1 Sintex JB, 1 Sump JB) |
| 20mm cable gland | 2 (one per JB, for Cat6 entry) |
| 16mm cable gland | 2 (one per JB, for float cable transit) |
| 12mm cable gland | 4 (sensor and float cable tank exits) |
| Fibre cement sun shield | 1 (Sintex JB if direct sun) |

### 5.4 Inside DB cupboard

| Item | Qty | Notes |
|---|---|---|
| Magnum Pradhaan PSP1 starter (1HP, single-phase) | 1 | New for P2; ~₹3000 |
| Sonoff DUALR3 (WiFi smart switch, 2-ch) | 1 | ~₹1500; flash with Tasmota for MQTT |
| 4-way 220V terminal block | 1 | For float wire junction |
| Small DIN rail | 1 | If cupboard is large enough |
| Earthing busbar | 1 | All motor earths terminate here |

---

## 6 — Sequencing (Order of Operations)

| Step | Task | Dependencies |
|---|---|---|
| 1 | Mark conduit routes on walls (chalk/paint) | — |
| 2 | Chase wall channels for conduit | Step 1 |
| 3 | Lay all 7 conduits + pull strings | Step 2 |
| 4 | Drill terrace slab and east wall penetrations; install sleeves | Step 3 |
| 5 | Mount JB backplates (Sintex JB, Sump JB) | Step 4 |
| 6 | Plastering team takes over | Steps 1-5 must be complete |
| 7 | Terrace tiling/waterproofing (with C-Sintex-1/2 already embedded) | Steps 4 + 6 done |
| 8 | Paint completion | Step 7 |
| 9 | Install JBs on backplates, connect glands | Step 8 |
| 10 | Pull Cat6 + float cables through conduits | Step 9 |
| 11 | Mount DB cupboard + install starters + Sonoff | Step 9 (parallel) |
| 12 | Install sensors (ultrasonic in Sintex riser, pressure probe in sump) + floats | Step 10 |
| 13 | Wire and test | Step 12 |

---

## 7 — Electrician Acceptance Checklist

To be signed off by electrician before plastering:

- [ ] All 7 conduits routed per the table in §1
- [ ] All conduits have pull strings left inside
- [ ] Data conduits (20mm) and mains conduits (16mm/25mm) separated by ≥50mm in parallel runs
- [ ] No data and mains cables sharing the same conduit anywhere
- [ ] Slab + external wall penetrations sleeved and marked
- [ ] JB mounting points identified and backplates fixed
- [ ] DB cupboard cable entry positions match conduit endpoints
- [ ] Conduit ends sealed with caps to prevent debris during plastering
- [ ] Both ends of each conduit labelled with its ID (C-Sintex-1, C-Sump-2, etc.) using paint marker on a small ID tag — visible after plaster
- [ ] Conduit colour code matches scheme in [conduits-and-cavities.md](conduits-and-cavities.md): grey = data, blue = motor power, white/cream = float/control
- [ ] Photos taken of each conduit run before plastering (for future reference)

---

## 8 — Outstanding Items (Not Blocking Conduit Work)

These are decisions made AFTER conduits go in. Conduit work can proceed without them locked.

- Exact JB position on terrace parapet — confirm on-site once Sintex final position is known.
- Exact JB position on east external wall — confirm relative to sump manhole.
- Sensor brand specifics (DFRobot SEN0257 / JSN-SR04T) — locked; order placed when JBs are ready.
- Sonoff DUALR3 — order when DB cupboard ready.
- Starter for P2 (Magnum Pradhaan PSP1 1HP) — order with the pump (Crompton Mini Champ 1HP).
- Motor earth pit excavation — coordinate with civil; not in this electrician's scope unless agreed.

---

## 9 — References

- General conduit rules: [conduits-and-cavities.md](conduits-and-cavities.md)
- DB circuits + MCB additions: [db-layout.md](db-layout.md) — **NEEDS UPDATE for Type C MCBs (P1, P2)**
- Circuits + load: [circuits-and-load.md](circuits-and-load.md) — **NEEDS UPDATE: "Type C not needed here" is wrong now**
- System architecture: `automation-iot/water-level-system.md` (TODO — write this next)
- Decision log: [../decisions/decision-log.md](../decisions/decision-log.md)
