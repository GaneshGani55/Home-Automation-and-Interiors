# First Floor — Electrical Layout

> Cross-reference: [../floor-plans/floor-plans-decoded.md](../floor-plans/floor-plans-decoded.md) for room dimensions.
> Circuit IDs here match [db-layout.md](db-layout.md).
> Cavity depth + Sonoff fitting rules: see [conduits-and-cavities.md § PART 0](conduits-and-cavities.md#part-0--electrician-one-page-cheat-sheet).
> **Status key:** ✅ CONFIRMED · 🔲 TBD · ⚠️ PENDING DECISION

> **🆕 ELECTRICIAN HEADS-UP for FF:**
> 1. **All smart-switch boxes on FF use 65mm-deep GI MS boxes** (Sonoff relay sits behind the switch). The dumb 50mm box does not work.
> 2. **A Wi-Fi access point goes on FF Living wall** at 2400mm FFL — see new section "FF Router / AP Wall Plate" below.
> 3. **Two extra Cat6 drops** go to BR1 and BR2 study walls at 700mm FFL.
> 4. **Every smart-switch board needs neutral** — visible black wire in tail bundle, even if today's switch is dumb.

---

## Room-by-Room Point Schedule

---

### 1. FF Living / Central Corridor
**Circuit:** D9 (lights + sockets) · NETWORK runs R-FF-1 (router/AP), R-FF-4 (balcony AP option)
**Location:** Central zone connecting both bedrooms, staircase landing, and front balcony. Beam runs along the cut-out edge.

| Point | Type | Location | Height | Circuit | Box depth | Smart? | Notes |
|---|---|---|---|---|---|---|---|
| Ceiling light(s) | 2–3× recessed LED, 9W | Ceiling, avoiding beam line | 10ft | D9 | 60mm circular | Smart switch | Warm 2700K |
| Socket | Double 5A | Wall near staircase | 300mm | D9 | 50mm | No | Charging / occasional use |
| Staircase top switch | 1-gang smart | FF landing, near stair top | 1200mm | B7 (stair circuit) | **65mm** | Smart 2-way partner | Partners with GF base switch |
| Switch board | 2-gang smart | Central wall | 1200mm | D9 | **65mm** | Smart | FF corridor lights |
| **🆕 Router/AP wall plate** | 2× Cat6 keystone | **FF Living central wall** between BR1 & BR2 doors | **2400mm** | LV-25-AP | 50mm wall plate | — | Run R-FF-1 from staircase niche; primary FF Wi-Fi 6 access point |
| **🆕 Router power socket** | Single 5A | 300mm to side of router plate | 2400mm | D9 | 50mm | No | For non-PoE APs / PoE injector / power adapter |

---

### 2. Bedroom 1 (East side)
**Circuit:** D1 (lights), D2 (sockets), E3 (AC) · NETWORK run R-FF-3 (Cat6 to study)
**Toilet attached:** Toilet 1 (8ft × 5ft, SINK · TOILET · SHOWER layout)

| Point | Type | Location | Height | Circuit | Box depth | Smart? | Notes |
|---|---|---|---|---|---|---|---|
| Main ceiling light | Recessed COB, 12W | Ceiling centre | 10ft | D1 | 60mm circular | Smart switch | |
| Bedside reading light L | Wall light / recessed | Left bedside wall | 1400mm | D1 | **65mm** | Smart / dimmer | |
| Bedside reading light R | Wall light / recessed | Right bedside wall | 1400mm | D1 | **65mm** | Smart / dimmer | |
| Wardrobe light | 5W LED strip or sensor | Inside wardrobe | — | D1 | — | Door sensor | |
| Study table light | 1× recessed spot or wall track | Above study zone | 1800mm | D1 | **65mm** | Smart | ⚠️ Study location TBD (per AutoCAD note: study table required) |
| Bedside socket L | Double 5A + 1× USB-C | Left bedside | 600mm | D2 | 50mm | No | |
| Bedside socket R | Double 5A + 1× USB-C | Right bedside | 600mm | D2 | 50mm | No | |
| Study socket | Double 5A + **🆕 Cat6 keystone (R-FF-3)** | Study wall | 700mm | D2 + LV | 50mm | No | Laptop + wired internet drop from staircase niche |
| General socket | Double 5A | S or W wall | 300mm | D2 | 50mm | No | |
| AC point | 20A socket | High on W or S wall | 1800mm | E3 | 50mm | No (smart AC) | Dedicated RCBO E3 |
| Switch board (door) | 4-gang smart | Near bedroom door, inside | 1200mm | D1 | **65mm (4-gang = 230×75×65)** | Smart (3 gangs) | Main light, reading L+R, master off |

---

### 3. Toilet 1 (Bedroom 1 Attached)
**Circuit:** D3 (lights+exhaust), D4 (geyser)
**Layout:** SINK · TOILET · SHOWER (E→W)

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Ceiling light | IP44 LED, 9W | Ceiling | 10ft | D3 | PIR (inside) | Auto-off PIR inside bath is fine for attached toilet |
| Mirror / vanity light | IP44 LED bar | Above sink mirror | 1900mm | D3 | With ceiling PIR | |
| Exhaust fan | 4" exhaust, IP44 | Shower zone, top of wall | ~2200mm | D3 | Runs with light | Linked to PIR |
| Geyser | **15L** | Wall above shower | ~1800mm | D4 | Switch outside bath | Dedicated D4 circuit; 20A switch outside |
| Geyser switch | 1-gang 20A with indicator | Just outside toilet door | 1200mm | D4 | No | ALWAYS outside bathroom |

---

### 4. Bedroom 2 (West side)
**Circuit:** D5 (lights), D11 (false ceiling cove — confirmed), D6 (sockets), E4 (AC) · NETWORK run R-FF-2 (Cat6 to study)
**Wardrobe:** 3ft deep along W wall. Toilet attached: Toilet 2 (8ft × 5ft, SHOWER · TOILET · SINK layout). **False ceiling confirmed for this room.**

| Point | Type | Location | Height | Circuit | Box depth | Smart? | Notes |
|---|---|---|---|---|---|---|---|
| Main ceiling light | Recessed COB, 12W | Ceiling centre | 10ft | D5 | 60mm circular | Smart switch | |
| Bedside reading light L | Wall light / recessed | Left bedside wall | 1400mm | D5 | **65mm** | Smart / dimmer | |
| Bedside reading light R | Wall light / recessed | Right bedside wall | 1400mm | D5 | **65mm** | Smart / dimmer | |
| Wardrobe light | 5W LED strip or sensor | Inside W-wall wardrobe (3ft deep) | — | D5 | — | Door sensor | |
| False ceiling cove | LED strip in cove perimeter | Inside false ceiling edge | False ceiling | D11 | driver box in FC | Smart dimmer | ✅ Confirmed |
| Study table light | 1× spot or wall track | Above study zone | 1800mm | D5 | **65mm** | Smart | ⚠️ Study location TBD |
| Bedside socket L | Double 5A + 1× USB-C | Left bedside | 600mm | D6 | 50mm | No | |
| Bedside socket R | Double 5A + 1× USB-C | Right bedside | 600mm | D6 | 50mm | No | |
| Study socket | Double 5A + **🆕 Cat6 keystone (R-FF-2)** | Study wall | 700mm | D6 + LV | 50mm | No | Laptop + wired internet drop from staircase niche |
| General socket | Double 5A | N or E wall | 300mm | D6 | 50mm | No | |
| AC point | 20A socket | High on E or S wall | 1800mm | E4 | 50mm | No (smart AC) | Dedicated RCBO E4 |
| Switch board (door) | 4-gang smart | Near bedroom door, inside | 1200mm | D5 | **65mm (4-gang = 230×75×65)** | Smart (3 gangs) | Main light, reading L+R, master off |

---

### 5. Toilet 2 (Bedroom 2 Attached)
**Circuit:** D7 (lights+exhaust), D8 (geyser)
**Layout:** SINK · TOILET · SHOWER (W→E)

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Ceiling light | IP44 LED, 9W | Ceiling | 10ft | D7 | PIR (inside) | |
| Mirror / vanity light | IP44 LED bar | Above sink mirror | 1900mm | D7 | With PIR | |
| Exhaust fan | 4" exhaust, IP44 | Shower zone top | ~2200mm | D7 | Runs with light | |
| Geyser | **15L** | Wall above shower | ~1800mm | D8 | Switch outside bath | Dedicated D8 circuit; 20A switch outside |
| Geyser switch | 1-gang 20A with indicator | Just outside toilet door | 1200mm | D8 | No | ALWAYS outside |

---

### 6. Front Balcony (N side, 11'9" × 7'0")
**Circuit:** D10 (balcony circuit shared with W balcony)

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Ceiling / wall light | IP65 rated LED, 9W | Ceiling of balcony slab edge | 10ft | D10 | Smart schedule | On at sunset, off at 11pm |
| Weatherproof socket | 16A IP44 socket with cover | Side wall | 300mm | D10 | No | Outdoor use: string lights, cleaning |
| Switch board | 1-gang smart | Inside, near balcony door | 1200mm | D10 | Smart | |

---

### 7. West Balcony / Top Balcony (3ft projection from last column)
**Circuit:** D10 (shared with front balcony)

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Wall light | IP65 LED, 7W | Outer wall above door | 2200mm | D10 | Smart schedule | |
| Weatherproof socket | 5A IP44 socket | Wall | 300mm | D10 | No | |

---

### 8. Staircase to Terrace (FF → Terrace)
**Circuit:** B7 (continues from GF staircase circuit)

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Stair lights FF flight | Wall-mounted or step lights | Along FF stair to terrace | Staggered | B7 | On with staircase circuit | |
| Terrace landing light | IP65 bulkhead LED | Near terrace door/opening | 2200mm | D10 (share balcony) | Smart | |
| Terrace socket (prep) | 16A IP65 socket | Near terrace entry | 300mm | D10 | No | Future: terrace garden, events |

---

## FF Switch Board Summary

| Location | Board type | Gang count | **Box depth** | Smart gangs |
|---|---|---|---|---|
| FF corridor | Modular | 2 | **65mm** | 2 smart |
| FF staircase top (2-way) | Modular | 1 | **65mm** | Smart 2-way |
| Bedroom 1 (inside door) | Modular | 4 | **65mm** | 3 smart |
| Bedroom 1 geyser switch (outside toilet) | 20A switch | 1 | 50mm | No |
| Bedroom 2 (inside door) | Modular | 4 | **65mm** | 3 smart |
| Bedroom 2 geyser switch (outside toilet) | 20A switch | 1 | 50mm | No |
| Front balcony | Modular | 1 | **65mm** | Smart |
| **🆕 FF Router/AP wall plate** | Cat6 ×2 keystone wall plate | — | 50mm wall plate | — (data only) |
| **🆕 FF Router power socket** | 1-gang 5A | 1 | 50mm | No |
| **🆕 BR1 study Cat6 plate** | Cat6 keystone wall plate | — | 50mm wall plate | — |
| **🆕 BR2 study Cat6 plate** | Cat6 keystone wall plate | — | 50mm wall plate | — |

> **Why 65mm for smart switch boxes?** Sonoff ZBMINI R2 / Aqara T1 relay modules sit *behind* the switch plate. They are ~22mm thick; combined with wire-bending room and switch terminals, 50mm is too tight (cables get crushed, plate doesn't sit flush). 65mm GI MS box gives clean fit + future flexibility. Same plate face, same modular accessories — only the wall hole is deeper. **Tell your mason explicitly when chasing.**

---

## FF Conduit Route Summary

| Run | Route | Size | Colour | Contents |
|---|---|---|---|---|
| DB (GF) → FF via staircase | Chase in staircase wall, vertical run | 25mm × 3 | 🔴 Red / 🔵 Blue | D1+D2, D5+D6, D9 lighting+sockets |
| DB → FF geysers | Separate vertical chase | 25mm × 2 | 🔵 Blue | D4 (T1 geyser), D8 (T2 geyser) |
| DB → FF bathroom lights | With bedroom conduit | 25mm | 🔴 Red | D3, D7 |
| DB → FF AC circuits | Separate vertical chases | 25mm × 2 | 🔵 Blue | E3, E4 (one per AC) |
| **🆕 R-FF-1** Staircase niche → FF Living wall (router/AP) | Vertical → FF slab → branch to FF Living central wall | **25mm LV-25** | ⚫ Grey | **2× Cat6** + draw wire — terminate at 2400mm FFL |
| **🆕 R-FF-2** Staircase niche → BR2 study wall | Vertical → FF slab → branch into BR2 wall | **25mm LV-25** | ⚫ Grey | **1× Cat6** + draw wire — terminate at 700mm FFL |
| **🆕 R-FF-3** Staircase niche → BR1 study wall | Vertical → FF slab → branch into BR1 wall | **25mm LV-25** | ⚫ Grey | **1× Cat6** + draw wire — terminate at 700mm FFL |
| **🆕 R-FF-4** (optional) FF Living AP → Front Balcony soffit | Through partition → balcony soffit | 16mm LV-16 | ⚫ Grey | 1× Cat6 outdoor + draw wire (cap until needed) |
| Staircase niche → CAM-3, CAM-5 | Vertical staircase wall (existing bundle) | 25mm × 2 | ⚫ Grey | Cat6 each — see conduits-and-cavities.md |
| DB → balconies | Via FF ceiling | 16mm | 🔴 Red | D10 balcony circuit |

> **Note on vertical runs:** All GF DB → FF circuits travel vertically through the staircase wall (the most direct chase path). Bundle them in separate conduits — do NOT mix power and lighting in the same conduit, and **never** mix any 230V power conduit with the LV-25 grey (Cat6) conduits.
>
> **🆕 Staircase wall chase capacity:** The staircase wall now needs to carry **5× P-25/P-25H + 3× LV-25 (grey) + 1× LV-16** = 9 conduits vertically. Cut a **150mm-wide × 60mm-deep chase** in the staircase wall to accommodate this neatly. Mason and electrician must coordinate so the chase is wide enough on first cut — opening it twice doubles labour.

---

## Open Decisions (FF)

- [ ] **AC in FF bedrooms** — confirmed conceptually (2 ACs), but confirm brand and unit position. Split AC outdoor units typically go on terrace or on W/E wall externally. Mark outdoor unit mounting brackets + drain pipe route now.
- [ ] **Geyser size** — 15L (single person) or 25L (family shared) per bathroom? Drives geyser bracket position and conduit sizing.
- [ ] **Study table position** in each bedroom — drives socket + Cat6 + reading light placement.
- [ ] **False ceiling in bedrooms** — if yes, cove lighting prep needed in each bedroom (add to D1, D5).
- [ ] **Window seat lighting** — AutoCAD plan noted a window seat with wardrobe on S wall of BR1. If built, add a reading/task light there.
