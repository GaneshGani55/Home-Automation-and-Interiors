# Ground Floor — Electrical Layout

> ⚠️ **FOYER subsection updated 2026-05-22 (v1.1):** doorbell brand → Hikvision DS-KV6113-WPE1(C) (was Reolink); speaker → ceiling-mounted (was cavity); cavity socket → 8M with Cat6 keystone (was 2-module); switch panel → 18M vertical (was 6-gang); smart-switch boxes → 50mm + 2 modules (foyer panel exception 65mm). **Authoritative foyer spec: [FOYER_MASTER_ELECTRICIAN_PLAN.md](FOYER_MASTER_ELECTRICIAN_PLAN.md) (see revision summary at top of that doc).** Foyer subsection below kept for index purposes; if conflict, the master plan wins.
>
> Cross-reference: [../floor-plans/floor-plans-decoded.md](../floor-plans/floor-plans-decoded.md) for room dimensions.
> Circuit IDs here match [db-layout.md](db-layout.md).
> Cavity depth + Sonoff fitting rules: see [conduits-and-cavities.md § PART 0](conduits-and-cavities.md#part-0--electrician-one-page-cheat-sheet).
> **Status key:** ✅ CONFIRMED · 🔲 TBD · ⚠️ PENDING DECISION

> **🆕 ELECTRICIAN HEADS-UP for GF (REVISED 2026-05-23):**
> 1. **All smart-switch boxes use 65mm-deep GI MS boxes** (Sonoff ZBMINI R2 sits hidden behind plate). Dumb 50mm boxes only at: Kitchen, Utility, Store, geyser switches, all sockets, AC sockets.
> 2. **Apply the "+2M-per-Sonoff" plate-sizing rule everywhere.** 1 smart gang → 3M plate, 2 → 6M, 3 → 8M, 4 → 12M, 6 → 18M. See [conduits-and-cavities.md § 0.4b](conduits-and-cavities.md#04b--plate-size-sizing-rule-for-hidden-sonoff-boards-2m-per-sonoff). This is the rule the electrician agreed to follow on 2026-05-23.
> 3. **Smart-switch hardware locked**: all hidden Sonoff ZBMINI R2 behind Schneider Unica modular plates. Aqara H1 and Schneider Wiser dropped from spec.
> 4. **Staircase niche** is the data hub — it terminates: all Cat6 from cameras, all Cat6 from FF (router uplink + 2 study drops), Cat6 from foyer screen, foyer speaker, doorbell, contact sensor. Plan a **12-port keystone patch panel** at 700mm FFL on niche side wall.
> 5. **Every smart-switch board needs neutral** — black wire visible in tail bundle.
> 6. **Fans: Atomberg smart BLDC, "always-on Sonoff" pattern.** Each fan gang on the room board is a 1-module rocker with a hidden Sonoff ZBMINI R2; the rocker stays UP (relay closed) by default so the Atomberg fan has continuous power for its BLE/HA control. Wall rocker exists only as emergency cutoff for fan service. Atomberg handles speed via remote / HA.

---

## Room-by-Room Point Schedule

---

### 1. Foyer

> ⚠️ **REVISED 2026-05-22 — see [FOYER_MASTER_ELECTRICIAN_PLAN.md](FOYER_MASTER_ELECTRICIAN_PLAN.md) for authoritative full plan.** This subsection is a summary.

**Circuits:** B-Foyer-Lights (6A MCB, all foyer + porch lighting) + B-Foyer-Cavity (6A + 30mA RCBO, cavity sockets only).
**DB position:** **East wall** (revised 2026-05-17 from earlier West-wall plan; main door swings against E wall so DB is hidden when door is open). Starter cupboard for water automation co-locates on East wall (P1 + P2 starters + Sonoff DUALR3).
**Stone feature wall:** 6 ft wide × 11 ft tall, on the **South edge** of the foyer (East 6 ft of the 9.5 ft S edge; the West 3.5 ft is open passage to Living/Pooja).

| Point | Type | Location | Height from floor | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Ceiling spotlight 1 | Recessed GU10 gimbal, 7W 2700K | 300mm from W wall area, 609mm from N edge | False ceiling (9ft FFL) | B-Foyer-Lights (Gang 1) | Via smart switch | Grazes S feature wall stone |
| Ceiling spotlight 2 | Recessed GU10 gimbal, 7W 2700K | 300mm from W wall area, 1218mm from N edge | False ceiling (9ft) | B-Foyer-Lights (Gang 1) | Via smart switch | Grazes S feature wall stone |
| Cavity Socket A (Monitor) | 5A socket on cavity BACK wall in 3"×3"×2.5" pocket | Centre of back wall, in pocket cut INTO masonry | 53" (1346mm) FFL | B-Foyer-Cavity | Sonoff Mini (HA control) | Powers Samsung LS22F350 monitor; cord hidden in rear gap behind monitor |
| Cavity Socket B (Spare) | 5A socket beside Socket A on same plate | Same pocket | 53" FFL | B-Foyer-Cavity | Always-live | Spare for future / RPi backup |
| Halo LED strip | 24V 2200K LED strip on inner walls of cavity at 30mm depth step | All 4 inner walls behind stone reveal lip | Inside cavity | B-Foyer-Lights (Gang 2, linked with cove) | Via smart switch | Driver above false ceiling |
| Cove LED strip | 24V 2700K LED in cove pocket | Foyer false-ceiling perimeter | At cove (~9ft) | B-Foyer-Lights (Gang 2) | Via smart switch | ~10m perimeter |
| Walnut shelf under-LED | 24V 2700K LED strip | Under walnut shelf on S wall | At shelf (900mm FFL) | B-Foyer-Lights (Gang 3) | Via smart switch | Driver Option 1 (above false ceiling) or Option 2 (under shelf) |
| Cavity speaker | Visaton FR 8 (80mm driver, ~₹1,800) | Mounted to cavity back wall via MDF baffle | Centre 57⅛" FFL (in 3" dia × 1" pocket) | RPi USB power (PoE) | Via HA → RPi | Replaces ceiling speaker; "voice from screen" effect |
| Bezel camera (CAM-0) | Pi Camera Module 3 via CSI ribbon | Top-centre of monitor bezel | ~63" FFL | RPi CSI port | Via Frigate | Secondary close-range face check |
| **Hikvision DS-KV6113-WPE1(C) Video Doorbell PoE (REVISED)** | doorbell + camera + intercom | OUTSIDE face of 1'6" N wall section | 1450mm FFL | PoE (Cat6) | Via HA/Frigate | **Primary face detection** (replaces dedicated CAM-1 install) + doorbell + 2-way audio (chime via Hik-Connect app or paired indoor station) |
| CAM-1 spare (PROVISION ONLY) | Future PoE camera if needed | Porch W wall (= Living E exterior, NOT foyer wall) | 1650mm FFL | PoE (capped) | Future | Conduit + IP67 back box + pull string only; no camera now |
| CAM-2 stub (PROVISION ONLY) | Future overview camera | Porch soffit NE corner | ~2700mm FFL | PoE (capped) | Future | Conduit + back box + pull string only |
| **DB panel (REVISED)** | Schneider Acti9 48-way | **East wall**, behind door swing | Bottom edge 1500mm FFL | — | — | See db-layout.md |
| **Starter cupboard** | Wooden cupboard with hinged lockable plywood facade | East wall, alongside or below DB (electrician's choice on-site) | TBD on-site | — | — | Houses P1 + P2 motor starters + Sonoff DUALR3 for water automation |
| **Foyer Switch Panel (REVISED 2026-05-23)** | **18M VERTICAL GI MS, ~290×135×65mm (or 225×195×65mm)** — as cut on site | **N wall, 1'6" section** between corner window (W) and main door (E) | 1200mm FFL (centre) | B-Foyer-Lights | Smart — **6× Sonoff ZBMINI R2 hidden** behind Schneider Unica 18M plate | 6 gangs: Spots / Cove+Halo / Shelf / Spare / Porch Ceiling / Porch Wall (future). 12M of internal slack accommodates 6 hidden Sonoffs + neutral bus per electrician's "+2M-per-Sonoff" rule. Direct mode (NOT detach) — guests must be able to use foyer switches when HA is down. |
| **Waveshare back box (PROVISION)** | Cat6 termination for future indoor unit | Staircase South wall (above server niche) | 1500mm FFL | LV (Cat6 pulled) | Future | Hardware design deferred |

**Conduits from DB (East wall) — only 2:**
- **C-DB-Foyer-Switch** (25mm RED): DB → up E wall → false ceiling → across to N wall → drops to Foyer Switch Panel (carries L+N+E for all foyer + porch lighting)
- **C-DB-Cavity-Power** (25mm RED): DB → horizontal in E wall → SE corner → S wall → cavity bottom-LEFT corner of back wall (L+N+E for cavity sockets, direct, not switched at wall)

**Conduits from Foyer Switch Panel to loads:** C-SW-Spots (25mm), C-SW-Cove-Halo (25mm), C-SW-Shelf (16mm), C-SW-Spare-4 (16mm), C-SW-Porch-Ceiling (16mm), C-SW-Porch-Wall (16mm capped).

**Conduits from staircase niche → foyer + porch (all share the same FLOOR chase going East):**
- **C-Niche-Cavity-Data** (25mm GREY, floor route): Cat6 (PoE) to RPi inside cavity
- **C-Niche-Doorbell** (25mm GREY, floor route): Cat6 (PoE) to Hikvision doorbell on outside face of 1'6" N wall section
- **C-Niche-CAM1** (25mm GREY, floor route): pull string only, terminates at porch W wall back box
- **C-Niche-CAM2** (25mm GREY, false ceiling route — only viable for porch soffit destination): pull string only
- **C-Niche-Waveshare** (25mm GREY, short vertical run): Cat6 to staircase S wall

**Cavity-internal conduit (not from anywhere else):**
- 16mm GREY pull string going UP from cavity TOP wall into false ceiling — future ceiling speaker provision

⚠️ **CRITICAL TIMING:** all floor-route conduits (Cavity Data + Doorbell + CAM1 spare + shelf branch) MUST be laid in floor screed BEFORE the tile contractor arrives.

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
| **Ceiling fan (Atomberg BLDC)** | Atomberg Renesa/Studio+ smart BLDC, ~30W | Centre of room (or shifted clear of pendant if chandelier installed) | Ceiling | GF-LIV-03 (lights circuit, fans run on lighting feed) | Smart — **always-on Sonoff ZBMINI R2** behind fan rocker | Rocker stays UP by default; Sonoff relay closed; fan permanently powered for Atomberg BLE/HA control. Cutoff only for service. |
| Switch board 1 (REVISED) | **8M plate (4 gangs: main + cove + fan + spare; +4M slack)** | W wall, near foyer-living boundary | 1200mm | B3/B4 + GF-LIV-03 fan feed | Smart 4 hidden Sonoffs | Gang 1: main light. Gang 2: cove. Gang 3: fan (always-on). Gang 4: spare. Detach mode in HA for Gang 1+2 for scenes (movie/dinner/bright). |
| Switch board 2 (2-way) | **6M plate (2 gangs + 4M slack)** | Near staircase entry | 1200mm | B3 | Smart | 2-way partner with SB1 for main lights via Sonoff S2 traveler input (see staircase Section 9 below). |

**Confirmed + Open decisions:**
- ✅ False ceiling confirmed for Living Area — cove circuit B4 active.
- ⚠️ Chandelier in double-height void: decide yes/no. If yes, needs a conduit from DB run vertically to FF slab beam level, then pendant drop cord. Must be coordinated with false ceiling contractor.
- 📝 **Future Aqara upgrade**: if you want a glass-touch plate on SB1 later, cut a fresh 86×86×50 mm square cavity post-move-in. Not pre-plaster work.

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
| **Ceiling fan (Atomberg BLDC)** | Atomberg Renesa smart BLDC, ~30W | Centre of dining zone (offset from pendant) | Ceiling | GF-LIV-06 (lights circuit) | Smart — always-on Sonoff ZBMINI R2 | Rocker UP by default; emergency cutoff only. |
| Switch board (REVISED) | **8M plate (3 gangs: pendant + cove + fan; +5M slack)** | W side of dining entry | 1200mm | B6/B9 + fan feed | Smart 3 hidden Sonoffs | Pendant + cove + fan. Detach mode in HA for pendant+cove (dinner scene). |

> 📝 **Future Aqara upgrade**: pendant + cove gangs could be Aqara H1 2-gang glass plate. Requires cutting a fresh 86×86×50mm square cavity adjacent to the Sonoff board. Post-move-in change.

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
**Circuit:** C1 (lights), C2 (sockets), E3 (AC)
**Wardrobes:** 10'3" S wall + ~3' W-wall tail

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Main ceiling light | Recessed COB or surface LED | Ceiling centre | 11ft | C1 | Smart switch | |
| Bedside reading light L | Wall light or recessed spot | E wall, left side of headboard | 1400mm | C1 | Smart / dimmer | Align after final queen-bed centreline is marked |
| Bedside reading light R | Wall light or recessed spot | E wall, right side of headboard | 1400mm | C1 | Smart / dimmer | Align after final queen-bed centreline is marked |
| Wardrobe interior light | 5W LED strip or sensor light | Inside S-wall wardrobe + W-wall tail | — | C1 | Door sensor switch | Comes on when wardrobe opens |
| Bedside socket L | Double 5A + 1× USB-C | Left bedside | 600mm | C2 | No | |
| Bedside socket R | Double 5A + 1× USB-C | Right bedside | 600mm | C2 | No | |
| General socket | Double 5A | W-wall dressing or N-wall reading nook | 300mm | C2 | No | Dressing table / floor lamp / occasional use |
| AC point | 20A socket | High on N wall above door/nook, or as per AC spec | 1800mm | E3 | No (smart AC) | Dedicated RCBO E3 |
| **Ceiling fan (Atomberg BLDC)** | Atomberg Renesa smart BLDC, ~30W | Centre of room (clear of wardrobe area) | Ceiling | GF-BED-01 (lights circuit) | Smart — always-on Sonoff ZBMINI R2 | Rocker UP by default; emergency cutoff only. Atomberg BLE remote bedside-friendly. |
| Switch board (door) — REVISED | **12M plate (4 gangs: main + reading L + reading R + fan; +8M slack)** | Near bedroom door | 1200mm | C1 + fan feed | Smart 4 hidden Sonoffs | Main light + 2 bedside readings + fan. **Direct mode (not detach)** — bedside switches must work when HA is down for sleep/dark scenarios. |

> 📝 **Future Aqara upgrade**: bedside switches are the most-pressed in a bedroom. If you want a glass-touch panel at the bedside specifically, plan two 86×86×50mm square cavities at 1400mm FFL on bedside wall — post-move-in retrofit.

---

### 8. Common Bathroom (GF)
**Circuit:** A1 (lights + exhaust fan) · A2 (geyser 15L)
**Full detail → [gf-bathroom-electrical.md](gf-bathroom-electrical.md)**

> Layout corrected 2026-05-01: door on **East wall** (left corner, 2.5ft); all fixtures on **North wall** (E→W: Vanity → WC → Glass partition → Shower); ceiling **8ft** (attic above lintel); **no false ceiling**; switch board on east wall right of door.

| Point | Type | x from East | Height | Circuit | Notes |
|---|---|---|---|---|---|
| L1 LED mirror | IP44, 15W, backlit | x=1.0ft, north wall | 1.35m centre | A1 via PIR | Conduit stub behind mirror |
| L2 Downlight — dry zone | IP44, 7W, 3000K recessed | x=3.0ft, ceiling | 8ft ceiling | A1 via PIR | Core drill ø75mm from attic |
| L3 Downlight — shower | **IP65**, 7W, 3000K recessed | x=7.25ft, ceiling | 8ft ceiling | A1 via PIR | Zone 1 — IP65 mandatory |
| L4 Niche LED strip | **IP65**, 3000K, 24V | x=7.25ft, south wall | 1.4m centre | A1 via PIR | Inside shower — IP65 mandatory |
| EF Exhaust fan | **IP65**, 150mm, ceiling | x=8.0ft, ceiling | 8ft ceiling | A1 manual switch | Duct through attic to external wall |
| SW Switch board | 4-module: PIR + exhaust + geyser | East wall, right of door | 1.35m | A1 + A2 | y=3.25ft from south wall |
| GY Geyser 15L | 2000W | Attic above bathroom | attic | A2 (16A RCBO) | 16A switch + neon in SW board |

---

### 9. Staircase
**Circuit:** B7 / GF-LIV-07 (2-way control, GF bottom switch + FF landing switch)

> **2-way wiring approach (REVISED 2026-05-23):** Sonoff ZBMINI R2 hidden at GF bottom box ONLY. Top (FF landing) is a dumb rocker connected to bottom Sonoff's S2 input via a 2-wire **traveler**. No 230V at top box — just 2 signal wires. Both rockers physically toggle the relay, even when HA is down. See Section 5 in [conduits-and-cavities.md § 0.4](conduits-and-cavities.md#04-switch-box-cavity-depth--this-is-new-sonoff-compatibility).

| Point | Type | Location | Height | Circuit | Smart? | Notes |
|---|---|---|---|---|---|---|
| Staircase ceiling/wall lights | 3–4× step lights or wall-mounted luminaires | Along staircase wall | Staggered | B7 | Smart 2-way | Toggleable from either GF base or FF landing |
| Step lights (optional) | LED step nosing strips | Each step riser | Step level | B7 | With main circuit | Decorative; adds safety |
| Switch board GF (bottom) | **3M plate (1 gang + 2M slack)** — Sonoff ZBMINI R2 hidden | Base of stairs, GF | 1200mm | B7 | Smart — full Sonoff module here | L+N+E feed; L OUT to ceiling lights; S1 to bottom rocker; **S2 to top rocker via 2-wire traveler** |
| Switch board FF (top) | **1M plate** — dumb Schneider Unica rocker, NO module | FF landing | 1200mm | B7 (traveler only) | Dumb signaller | **No 230V** to this box. Only 2 traveler wires returning to bottom Sonoff's S2 input. |

---

### 10. Staircase Niche (Server Room)
**Circuit:** E5/E7 (UPS), E6/E8 (server sockets)
**Location:** Under stairs, W wall, GF

| Point | Type | Location | Height | Circuit | Box depth | Smart? | Notes |
|---|---|---|---|---|---|---|---|
| UPS socket | 16A 3-pin | Niche back wall | 300mm | E7 | 50mm | No | Powers UPS (which powers mini PC) |
| Server sockets | 4× 5A sockets (2 doubles) | Niche back wall | 400mm | E8 | 50mm | No | Mini PC, network switch, patch panel |
| Niche light | 1× 5W LED | Niche ceiling/top | — | B7 (share stair) | 50mm | Dumb toggle | Working light for maintenance |
| **🆕 Cat6 patch point — UPGRADED** | **Keystone wall plate (12-port)** | Niche side wall | 700mm | — | 50mm wall plate | — | All Cat6 home-runs terminate here. **12 ports** to handle: CAM-1, CAM-2, CAM-3, CAM-4, CAM-5, CAM-0 RPi, foyer screen, FF router (R-FF-1 ×2), BR1 study (R-FF-3), BR2 study (R-FF-2), spare |
| Speaker terminal | 2-port speaker terminal strip | Niche wall | 700mm | — | 50mm | — | Foyer speaker wire terminates here |

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

## GF Switch Board Summary (REVISED 2026-05-23 — +2M-per-Sonoff rule applied)

| Location | Plate size | Box (GI MS, mm) | Smart gangs | Hidden Sonoffs | HA mode |
|---|---|---|---|---|---|
| **Foyer Switch Panel (N wall 1'6")** | **18M vertical** | **~290×135×65 OR 225×195×65** (as cut on site) | 6 | 6× ZBMINI R2 | Direct |
| Living SB1 (W wall) | **8M** | 175×130×65 (or 225×86×65) | 4 (main + cove + fan + spare) | 4× ZBMINI R2 | Detach for main+cove; Direct for fan+spare |
| Living SB2 (2-way, stair side) | **6M** | 130×130×65 | 2 | 2× ZBMINI R2 | Direct (traveler pair with SB1 main light) |
| Dining | **8M** | 175×130×65 | 3 (pendant + cove + fan) | 3× ZBMINI R2 | Detach for pendant+cove; Direct for fan |
| Kitchen | 4M | 130×75×**50** | 0 (all dumb) | 0 | n/a |
| Utility | 1M | 75×75×**50** | 0 (dumb) | 0 | n/a |
| Store room | 1M | 75×75×**50** | 0 (dumb) | 0 | n/a |
| MBR door | **12M** | 225×130×65 | 4 (main + reading L + R + fan) | 4× ZBMINI R2 | Direct (bedside safety) |
| Bathroom (outside × 3) | 4M each | 130×75×**50** | 0 (PIR + geyser, all dumb) | 0 | n/a |
| Staircase base (GF) | **3M** | 86×86×65 | 1 (light, full Sonoff hidden) | 1× ZBMINI R2 | Direct |
| Staircase top (FF landing) | **1M** | 75×75×**50** | 0 (dumb, traveler only, NO 230V) | 0 | n/a |
| Pooja (outside entry) | **6M** | 130×130×65 | 2 (ceiling + niche) | 2× ZBMINI R2 | Direct |
| **GF Sonoff ZBMINI R2 subtotal** | | | **22 gangs** | **22 modules** | |
| Foyer cavity Monitor Socket | — (inside cavity socket pocket) | — | — | 1× Sonoff Mini (different model — Wi-Fi, switches cavity socket only) | HA |
| Water automation DB cupboard | — | — | — | 1× Sonoff DUALR3 (P1+P2 motor starters — see [water-automation-conduits.md](water-automation-conduits.md)) | HA |

> **Cavity-depth rule for the mason:** wherever a smart switch is planned (anything with a "Hidden Sonoff" count > 0), the GI MS box must be **65mm deep, not 50mm**. The wall plate matches the +2M rule plate-size column above — only the back box depth differs from dumb-switch boxes. **Buy 65mm GI boxes from your hardware shop and check the depth before sending to site.**
>
> **What goes inside each smart back box (electrician's final wiring):**
> 1. Incoming feed: L (red) + N (black) + E (green/yellow) from circuit conduit
> 2. Outgoing switched feed: 1× switched-L per gang to load (light/fan), plus shared N + E
> 3. **Wires capped with 300 mm tails** — Sonoff modules are installed by Ganesh after move-in
> 4. Schneider Unica plate with the modular rockers and blank inserts filling the slack modules
>
> **📝 Future Aqara upgrade option (any room):** if you ever want a glass-touch plate at a specific board, cut a new 86×86×50mm square cavity adjacent to (or replacing) the Sonoff board. Post-move-in retrofit. Not pre-plaster work — don't ask the mason to cut it now.

---

## GF Conduit Route Summary

| Run | Route | Size | Colour | Contents |
|---|---|---|---|---|
| DB → Foyer ceiling | W wall up, along ceiling | 25mm | 🔴 Red | B1 lighting |
| DB → Screen cavity | W wall up, across foyer | 25mm | 🔴 Red | B2 screen+speaker |
| DB → Living ceiling | W wall, ceiling | 25mm | 🔴 Red | B3 lighting |
| DB → Living sockets | Wall chase, skirting level | 25mm | 🔵 Blue | B5 power |
| DB → Kitchen ceiling | Ceiling run E direction | 25mm | 🔴 Red | A3 kitchen lights |
| DB → Kitchen counter | Wall chase | 25mm | 🔵 Blue | A4 counter sockets |
| DB → Hob | Direct short run | 25mm | 🔵 Blue | A6 hob |
| DB → Geyser (GF bath) | Through bathroom wall | 25mm | 🔵 Blue | A2 geyser |
| DB → Fridge niche | Along E wall | 25mm | 🔵 Blue | A8 fridge |
| DB → Washing machine | Through utility wall | 25mm | 🔵 Blue | A7 |
| DB → MBR | Chase through W wall | 25mm | 🔴 Red / 🔵 Blue | C1 (lights) + C2 (sockets) |
| DB → Staircase niche | Short run (niche is near DB) | 25mm | 🔵 Blue | E7+E8 server sockets |
| Staircase niche → Foyer | Chase wall/ceiling | 25mm×2 | ⚫ Grey | Cat6 + spare LV |
| Staircase niche → Foyer ceiling | Ceiling | 16mm | ⚫ Grey | Speaker wire |
| DB → all ACs | Individual chases | 25mm | 🔵 Blue | E1-E4 (1 per AC) |
| **🆕 Staircase niche → FF** (vertical bundle, see FF doc) | Through staircase wall | 5× 25mm + 3× 25mm + 1× 16mm | Mixed | Power circuits + 3× Cat6 LV-25 + LV-16 |
