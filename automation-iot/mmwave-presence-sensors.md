# mmWave Presence Sensors — LOCKED 2026-05-30

> ✅ **LOCKED** as of 2026-05-30 (this prompt). Authoritative spec for all 7 mmWave presence sensors covering 3 bathrooms, 3 bedrooms, and 1 dining/living. Supersedes the earlier holding-file draft.

## 1. Why mmWave (not PIR)

Household has **adults + kids + elderly parents**. PIR fails on still bodies — elderly sleeping, kids sitting quietly, adult reading in bed. Bathroom shower = body mostly still behind curtain.

**mmWave detects breathing chest-rise of a still body.** Single failure mode (lights/fan off mid-shower) eliminated. This is the entire design driver.

## 2. Sensor selection (locked)

| Location | Sensor | Why | India price (~) |
|---|---|---|---|
| **Dining/Living (×1)** | **Aqara FP2** | Multi-zone (up to 30 zones) — only sensor that knows which spot of a big room is occupied; built-in lux; WiFi+Matter | ₹12,000–18,000 |
| **Bathrooms ×3 + Bedrooms ×3** | **Sonoff SNZB-06PR2** (24GHz mmWave + PIR fusion) | Native Zigbee 3.0 → joins existing Sonoff dongle directly; built-in lux; acts as Zigbee router (strengthens mesh); 1/4 the price of FP2 | ₹3,000–4,000 |
| **Staircase, Utility, Store** (future provision) | **Aqara P2 PIR** (battery) | Motion-only is fine — no one sits still on stairs or in storage | ₹3,500–5,000 |

**Aqara FP1E dropped:** FP1E needs an Aqara Zigbee 3.0 Hub officially (Z2M support is unofficial). SNZB-06PR2 is a cleaner fit for our locked Sonoff Zigbee dongle stack.

## 3. Power method (locked)

**All mmWave sensors require constant 5V USB-C.** Battery is impossible (radar always-on draw).

Standard component: **HLK-PM01** AC-to-DC buck converter module
- Input: 230V AC
- Output: 5V DC, 0.6A
- Size: 34 × 20 × 15mm
- Cost: ₹180–250
- Industrial-spec, 10+ year MTBF
- Source: Robu.in, Quartz Components, Amazon India

> **For the electrician:** "Buck converter / step-down module / 230V se 5V chota power adapter — looks like a small PCB, replaces a wall-wart but is hardwired inside the cavity."

## 4. Mount methods catalogue

Six methods documented in `pdfs/SENSOR_MOUNTING_METHODS.pdf` and `pdfs/JB_INSTALL_AND_NEW_APPROACHES.pdf`. Use this matrix to pick:

| # | Method | Best for |
|---|---|---|
| **1** | **JB Mount** (buck inside circular JB at sensor height) | Where existing chase + JB are present (GF master bathroom) |
| A | Direct adhesive on plate | Avoid — drilling plates is non-reversible |
| **B** | Bracket beside plate (USB cable along wall) | Default fallback for wall-mount when no JB |
| C | 3D-printed adapter | Aesthetic obsessives, not for first install |
| **D** | USB-A keystone at 7ft + sensor on bracket above | Cleanest minimal-cable wall mount |
| **E** | Buck inside 2M GI MS box at sensor height + sensor on bracket | Universal wall-mount; uses standard Sonoff-locked box format |

## 5. Locked sensor schedule (7)

| Ref | Room | Sensor | Mount Location | Method | Power | Notes |
|---|---|---|---|---|---|---|
| **M1** | GF Master Bedroom | SNZB-06PR2 | Ceiling centre | Method 1 ceiling-variant (buck in switch cavity → 2-core to ceiling) | 230→5V buck in MBR switch cavity | False ceiling planned; cavity decision in main spec |
| **M2** | GF Common Bathroom | SNZB-06PR2 | Wall — North wall middle, **7ft FFL**, on existing JB | **Method 1 (JB Mount)** | HLK-PM01 inside the existing circular JB on N-wall chase | LOCKED user choice — existing chase from hand-basin lighting extended up |
| **M3** | Dining / Living mid-ceiling | **Aqara FP2** | Ceiling centre between dining + living | Buck in nearest switch cavity (~8m run, use 1.0mm² 2-core) OR PoE from niche if adding ceiling AP/speaker later | 230→5V buck (default) | 25mm conduit with 1× Cat6 + 2× pull strings for future-proofing |
| **M4** | FF Bedroom 2 (W, balcony side) | SNZB-06PR2 | Ceiling centre | Buck in switch cavity → 2-core to ceiling | False ceiling present (cove circuit D11) | Use existing ceiling cavity space |
| **M5** | FF Bedroom 1 (E side) | SNZB-06PR2 | Ceiling — **NO false ceiling**, slab cast → wall mount at 7ft | **Method E or B** (Method E preferred — 2M GI box at 7ft) | HLK-PM01 inside the 2M GI box at sensor height | Updated from "wall" — needs Method E because no ceiling option |
| **M6** | FF Toilet 2 (W bedroom's bath) | SNZB-06PR2 | Ceiling | Buck in switch cavity → 2-core | Concrete slab — verify ceiling access; fall back to Method E if no access | TBD on site |
| **M7** | FF Toilet 1 (E bedroom's bath) | SNZB-06PR2 | Wall — 7ft FFL | **Method E** (buck inside 2M GI box at 7ft) | HLK-PM01 inside 2M GI box | Concrete slab done, no false ceiling |

## 6. Pre-plaster work for the electrician

Per sensor location:
1. Cut a sensor cavity at intended sensor mount point (86×86×40mm for ceiling, 2M GI MS box at 7ft FFL for wall, OR use existing circular JB for M2)
2. Run 20mm PVC conduit from the room's switch cavity (where Sonoff ZBMINI + HLK-PM01 live) to the sensor cavity
3. Drop a nylon pull-string inside the conduit
4. For Method E: cut the 2M GI MS box at 7ft FFL on the wall facing the entry door

**Future-provision rooms (utility, store, WIC):** Cut the cavity + conduit + pull-string NOW. No sensor, no buck, no wiring. Cap with a blank Schneider insert. Install sensor + HLK-PM01 in 30 min any time after move-in.

## 7. Wiring inside the JB / switch cavity / 2M GI box

```
              230V from MCB / room lighting circuit
                          │
              ┌───────────┴───────────┐
              │                       │
       Wago 221 (3-port)        Wago 221 (3-port)
       L branch                 N branch
              │                       │
       ┌──────┴──────┐         ┌─────┴───────┐
       ▼             ▼         ▼             ▼
   Sonoff       HLK-PM01    Sonoff       HLK-PM01
   ZBMINI        AC-L       ZBMINI        AC-N
   relay L       input      relay N       input
   (existing)   (new)       (existing)   (new)
                  │                         │
                  │                         │
                  ▼                         ▼
              ┌──────────────────────────────┐
              │      HLK-PM01 DC OUT         │
              │   +5V (red)   GND (black)    │
              └──────┬────────────┬──────────┘
                     │            │
              2-core 0.75mm² (red + black)
              through 20mm PVC conduit to sensor
                     │            │
                     ▼            ▼
              ┌──────────────────────┐
              │  USB-C connector or  │
              │  sacrificed USB-C    │
              │  cable (bare end)    │
              └──────────┬───────────┘
                         │
                 plugs into sensor
```

## 8. Bill of materials (locked)

| Item | Qty | Source | Unit (₹) | Total (₹) |
|---|---|---|---|---|
| Aqara FP2 | 1 | dbgtechstore.in | 12,130 | 12,130 |
| Sonoff SNZB-06PR2 (24G mmWave) | 6 | iTead direct / AliExpress | 3,500 | 21,000 |
| HLK-PM01 buck converter | 7 (install) + 3 (future) | Robu.in | 200 | 2,000 |
| 2-core 0.75mm² flexible copper (50m roll) | 1 | Local electrical | — | 800 |
| Wago 221-413 (3-port lever) | 30 pcs | Amazon India | 15 | 450 |
| USB-A→C cable (for sacrifice) | 7 | Local mobile shop | 80 | 560 |
| Heat-shrink tubing assorted | 1 pack | Amazon India | 150 | 150 |
| Cat6 cable for dining ceiling | 12m | Local network shop | 15 | 180 |
| **TOTAL** | | | | **~₹37,270** |

Plus the existing ZBMINI + 65mm GI MS boxes already locked in the smart-switch spec.

## 9. Pairing + HA integration (post-install)

1. **Sonoff SNZB-06PR2:** Press pairing button → Zigbee2MQTT discovers it on the existing Sonoff dongle. Map presence → existing Sonoff ZBMINI in HA automation.
2. **Aqara FP2:** WiFi setup via Aqara app → expose to HA via Matter (HA Matter integration is mature). Draw zones in Aqara app: sofa / dining table / walkway. Each zone reports occupancy independently.

## 10. Decision provenance

- 2026-05-30 · automation · mmWave sensor lock-in (this prompt with Claude) · supersedes 2026-05-01 GF bath PIR decision
- 2026-05-23 · automation · Sonoff Zigbee 3.0 stack locked → made native-Zigbee Sonoff sensors preferable to WiFi-only Aqara
- 2026-05-29 · holding draft → 2026-05-30 final lock

See: `decisions/decision-log.md`, `electrical/gf-bathroom-electrical.md`, `pdfs/MMWAVE_SENSOR_MASTER.pdf`.
