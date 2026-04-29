# Ground Floor — Electrical Layout

> Cross-reference: [../floor-plans/floor-plans-decoded.md](../floor-plans/floor-plans-decoded.md) for room dimensions.
> Circuit IDs here match [db-layout.md](db-layout.md).
> **Status key:** ✅ CONFIRMED · 🔲 TBD · ⚠️ PENDING DECISION

---

## Room-by-Room Point Schedule

---

### 1. Foyer
**Circuit:** B1 (lights), B2 (screen/speaker), B10 (false ceiling cove — confirmed), DB on this wall
**Wall:** W wall (6ft wide × 11ft tall feature wall)

| Point | Type | Location | Height from floor | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Ceiling spotlight 1 | Recessed GU10, 7W warm white | 300mm from W wall, centered left | Ceiling (11ft) | B1 | Via smart switch | Stone-grazing angle |
| Ceiling spotlight 2 | Recessed GU10, 7W warm white | 300mm from W wall, centered right | Ceiling (11ft) | B1 | Via smart switch | Stone-grazing angle |
| Screen power socket | 6A 3-pin socket | Inside screen recess cavity | 1350mm (centre of cavity) | B2 | No | Hidden behind screen |
| Screen LED halo driver | 24V LED driver | Inside screen recess cavity | With screen socket | B2 | No | Powers amber halo strip |
| Foyer shelf LED strip | 24V LED strip under shelf | Under walnut shelf, full 6ft width | 900mm (shelf height) | B1 | Via smart switch | Warm 2700K, under-shelf wash |
| Speaker point | 2-core 1.5mm² speaker wire | Ceiling, above foyer centre | Ceiling | B2 | Via server | Terminate in ceiling rose |
| DB panel | 40-way flush-mount DB | W wall, right of foyer (behind door) | Bottom of DB at 1500mm | — | — | See db-layout.md |
| Switch board 1 | 4-gang modular (Schneider Unica or similar) | W wall, left of door, 1200mm | 1200mm | B1/B2 | Smart (2 gangs) | Gangs: foyer lights, screen, spare, spare |

**Conduits from DB → foyer:**
- 25mm conduit: lighting circuit B1 (DB → ceiling spotlight positions → shelf strip → switch board)
- 25mm conduit: B2 screen power + speaker wire (DB → screen cavity → ceiling speaker point)

**Conduits from staircase niche → foyer cavity:**
- 25mm: Cat6 (server → screen RPi)
- 25mm: spare (future)

---

### 2. Living Area
**Circuit:** B3 (main lights), B4 (cove/accent — TBD), B5 (sockets)
**Key feature:** Double-height void above — ceiling is open to FF slab cut-out edge at 22ft combined. Lights must be at 11ft GF ceiling level OR chandelier/pendant dropped from FF beam.

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Main ceiling light(s) | Recessed COB or pendant(s) — TBD style | Centred in non-void zone | 11ft ceiling | B3 | Smart | Count TBD pending false ceiling decision |
| Chandelier / statement pendant | 1× drop pendant into the double-height void | Centred over void | Drop from FF beam level | B3 | Smart dimmer | ⚠️ Must be fed from FF floor above — confirm conduit route |
| Cove lighting | LED strip in false ceiling cove | Perimeter of false ceiling | Ceiling | B4 | Smart dimmer | ✅ False ceiling confirmed for Living |
| TV wall cluster | 16A socket + 2× 5A socket + 1× Cat6 keystone | W wall, TV wall | 300mm | B5 | No | Cat6 via low-voltage conduit from staircase niche |
| General socket 1 | Double 5A + USB-A/C | N wall (near foyer entry) | 300mm | B5 | No | |
| General socket 2 | Double 5A + USB-A/C | E wall (opposite TV) or S wall | 300mm | B5 | No | |
| AC point | 16A or 20A socket | High on S wall or as per AC spec | 1800mm | E1 | No (smart AC) | Dedicated RCBO E1 |
| Switch board 1 | 4-gang modular | W wall, near foyer-living boundary | 1200mm | B3/B4 | Smart (2 smart gangs) | Main lights + cove |
| Switch board 2 (2-way) | 2-gang | Near staircase entry | 1200mm | B3 | Smart | 2-way with SB1 for main lights |

**Confirmed + Open decisions:**
- ✅ False ceiling confirmed for Living Area — cove circuit B4 active.
- ⚠️ Chandelier in double-height void: decide yes/no. If yes, needs a conduit from DB run vertically to FF slab beam level, then pendant drop cord. Must be coordinated with false ceiling contractor.

---

### 3. Dining Area
**Circuit:** B6 (main lights), B9 (cove/accent — false ceiling confirmed), E2 (AC)
**Location:** Along E wall, ~9'6" deep (after 10ft kitchen). False ceiling confirmed.

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Pendant / chandelier | 1× pendant (over dining table centre) | Centre of dining zone | Drop to ~2200mm | B6 | Smart dimmer | Warm 2700K, decorative |
| False ceiling cove | LED strip in cove perimeter | Inside false ceiling edge | Ceiling | B9 | Smart dimmer | Warm ambient |
| Recessed downlights | 2–3× recessed COB in false ceiling | Distributed in dining zone | False ceiling | B6 | Smart | Supplement pendant |
| AC point | 20A socket | High on W or N wall | 1800mm | E2 | No (smart AC) | Dedicated RCBO E2 |
| General socket | Double 5A | E wall | 300mm | B6 | No | Laptop / occasional use |
| Switch board | 3-gang smart | W side of dining entry | 1200mm | B6/B9 | Smart (2 smart gangs) | Pendant + cove |

---

### 4. Kitchen
**Circuit:** A3 (lights+exhaust), A4 (counter sockets), A5 (chimney), A6 (hob), A8 (fridge)
**Depth:** ~10ft (TBD exact). Along N wall.

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Main ceiling light | LED panel or recessed, 18W cool/neutral | Ceiling centre | 11ft | A3 | Dumb switch | Kitchen = dumb switch |
| Under-cabinet LED strip | 24V LED strip | Under wall cabinets above counter | 1600mm (under cabinet) | A3 | Dumb switch | Warm white, task lighting |
| Exhaust fan | 6" / 8" exhaust | Top of N or E wall | ~2400mm | A3 | Dumb switch | |
| Chimney | 16A socket | Above hob position, concealed | 1900mm | A5 | Dumb | Dedicated circuit |
| Hob / cooktop | 20A socket or direct hard-wired | Below counter at hob position | 150mm | A6 | Dumb | Dedicated; 4mm² wire |
| Counter socket 1 | 5A socket | Counter level, left zone | 1100mm | A4 | No | Mixer / toaster |
| Counter socket 2 | 5A socket | Counter level, centre | 1100mm | A4 | No | Microwave |
| Counter socket 3 | 5A socket | Counter level, right zone | 1100mm | A4 | No | OTG / misc |
| Counter socket 4 | 5A socket | Under-sink / RO purifier position | 300mm | A4 | No | RO water purifier |
| Refrigerator socket | 15A socket | Fridge niche (below store room) | 300mm | A8 | No | Always-live dedicated |
| Switch board | 4-gang dumb | Entry to kitchen, N wall | 1200mm | A3/A4 | Dumb | Lights + exhaust |

---

### 5. Utility (4ft × 5ft)
**Circuit:** A7

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Overhead light | 1× 9W LED | Ceiling | 11ft | A3 (share kitchen light circuit) | Dumb | |
| Washing machine socket | 16A 3-pin socket | W or N wall, at floor level | 300mm | A7 | No | Dedicated circuit |
| Switch board | 1-gang | Near utility door | 1200mm | A3 | Dumb | Light switch only |

---

### 6. Store Room (~4ft × 4ft)
**Circuit:** A3 (share kitchen lights)

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Overhead light | 1× 7W LED bulkhead | Ceiling | — | A3 | Dumb toggle | Simple on/off |

---

### 7. Master Bedroom (M.Bed)
**Circuit:** C1 (lights), C2 (sockets), E2 (AC)
**Wardrobes:** 12ft N wall + 12'3" W wall

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Main ceiling light | Recessed COB or surface LED | Ceiling centre | 11ft | C1 | Smart switch | |
| Bedside reading light L | Wall light or recessed spot | Left of bed, bedside | 1400mm | C1 | Smart / dimmer | |
| Bedside reading light R | Wall light or recessed spot | Right of bed, bedside | 1400mm | C1 | Smart / dimmer | |
| Wardrobe interior light | 5W LED strip or sensor light | Inside N-wall wardrobe | — | C1 | Door sensor switch | Comes on when wardrobe opens |
| Bedside socket L | Double 5A + 1× USB-C | Left bedside | 600mm | C2 | No | |
| Bedside socket R | Double 5A + 1× USB-C | Right bedside | 600mm | C2 | No | |
| General socket | Double 5A | S or E wall | 300mm | C2 | No | Study table / dressing table |
| AC point | 20A socket | High on S wall or as per AC spec | 1800mm | E2 | No (smart AC) | Dedicated RCBO E2 |
| Switch board (door) | 4-gang smart modular | Near bedroom door | 1200mm | C1 | Smart (2-3 gangs) | Main light, reading lights, master off |

---

### 8. Common Bathroom (GF)
**Circuit:** A1 (lights+exhaust), A2 (geyser)
**Door opens from West. Layout: Sink · Toilet · Shower (N→S along W wall)**

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Ceiling light | IP44 rated LED, 9W | Ceiling | — | A1 | PIR switch (outside door) | Auto-off PIR |
| Mirror light | IP44 LED strip or bar | Above mirror / sink | 1900mm | A1 | PIR | |
| Exhaust fan | 4" exhaust, IP44 | Top of wall, shower zone | ~2300mm | A1 | Runs with light | Wire to same PIR switch |
| Geyser | **15L** | Wall above shower/toilet | ~1800mm | A2 | No (manual switch outside) | Dedicated 20A circuit; switch OUTSIDE bathroom |
| PIR switch board | 1-gang PIR switch | Outside bathroom door, W side | 1200mm | A1 | PIR auto-off | Controls light + exhaust; 5-min delay |
| Geyser switch | 1-gang 20A switch with indicator | Outside bathroom, below PIR | 1200mm | A2 | No | MUST be outside bathroom (safety) |

> **Safety rule:** Geyser switch is ALWAYS outside the bathroom. Never inside.

---

### 9. Staircase
**Circuit:** B7 (2-way control, GF bottom switch + FF landing switch)

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Staircase ceiling/wall lights | 3–4× step lights or wall-mounted luminaires | Along staircase wall | Staggered | B7 | Smart 2-way | One switch GF bottom, one FF landing |
| Step lights (optional) | LED step nosing strips | Each step riser | Step level | B7 | With main circuit | Decorative; adds safety |
| Switch board GF | 1-gang smart | Base of stairs, GF | 1200mm | B7 | Smart | |
| Switch board FF | 1-gang smart | FF landing | 1200mm | B7 | Smart 2-way partner | |

---

### 10. Staircase Niche (Server Room)
**Circuit:** E5 (UPS), E6 (server sockets)
**Location:** Under stairs, W wall, GF

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| UPS socket | 16A 3-pin | Niche back wall | 300mm | E5 | No | Powers UPS (which powers mini PC) |
| Server sockets | 4× 5A sockets (2 doubles) | Niche back wall | 300mm | E6 | No | Mini PC, network switch, patch panel |
| Niche light | 1× 5W LED | Niche ceiling/top | — | B7 (share stair) | Dumb toggle | Working light for maintenance |
| Cat6 patch point | Keystone wall plate (6-port) | Niche side wall | 600mm | — | — | All Cat6 home-runs terminate here |
| Speaker terminal | 2-port speaker terminal strip | Niche wall | 600mm | — | — | Foyer speaker wire terminates here |

---

### 11. Pooja Room (5ft × 5ft)
**Circuit:** B8

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Ceiling light | 1× warm white LED panel, 12W | Ceiling | — | B8 | Smart (soft dimmer for ambience) | 2700K warm |
| Backlight / niche light | LED strip, warm amber | Behind idol niche / shelf | Niche height | B8 | Smart dimmer | Creates devotional glow |
| Socket | 1× 5A | Side wall | 300mm | B8 | No | Diya warmer / small appliance |
| Switch board | 2-gang smart | Outside pooja entry | 1200mm | B8 | Smart | Ceiling + niche light |

---

## GF Switch Board Summary

| Location | Board type | Gang count | Smart gangs |
|---|---|---|---|
| Foyer (W wall, near door) | Modular | 4 | 2 smart + 2 dumb |
| Living Area (W wall) | Modular | 4 | 3 smart |
| Living Area 2-way (stair side) | Modular | 2 | 2 smart |
| Dining | Modular | 2 | 1 smart |
| Kitchen | Modular (dumb only) | 4 | 0 |
| Utility | Modular | 1 | 0 |
| MBR door | Modular | 4 | 3 smart |
| Bathroom (outside) | PIR switch + geyser | 2 | PIR auto |
| Staircase base | Modular | 1 | Smart 2-way |
| Pooja (outside entry) | Modular | 2 | 2 smart |

---

## GF Conduit Route Summary

| Run | Route | Size | Contents |
|---|---|---|---|
| DB → Foyer ceiling | W wall up, along ceiling | 25mm | B1 lighting |
| DB → Screen cavity | W wall up, across foyer | 25mm | B2 screen+speaker |
| DB → Living ceiling | W wall, ceiling | 25mm | B3 lighting |
| DB → Living sockets | Wall chase, skirting level | 25mm | B5 power |
| DB → Kitchen ceiling | Ceiling run E direction | 25mm | A3 kitchen lights |
| DB → Kitchen counter | Wall chase | 25mm | A4 counter sockets |
| DB → Hob | Direct short run | 25mm | A6 hob |
| DB → Geyser (GF bath) | Through bathroom wall | 25mm | A2 geyser |
| DB → Fridge niche | Along E wall | 25mm | A8 fridge |
| DB → Washing machine | Through utility wall | 25mm | A7 |
| DB → MBR | Chase through W wall | 25mm | C1+C2 |
| DB → Staircase niche | Short run (niche is near DB) | 25mm | E5+E6 |
| Staircase niche → Foyer | Chase wall/ceiling | 25mm×2 | Cat6 + spare LV |
| Staircase niche → Foyer ceiling | Ceiling | 16mm | Speaker wire |
| DB → all ACs | Individual chases | 25mm | E1-E4 (1 per AC) |
