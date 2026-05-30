# Electrical Layout

Complete electrical plan for the 2-floor home. Start with the DB layout, then dive into each floor.

> This is a **living document** — update it as decisions are made. Every file uses a consistent status system: ✅ CONFIRMED · 🔲 TBD · ⚠️ PENDING DECISION. When something moves from TBD to CONFIRMED, update the relevant file AND add a line to [../decisions/decision-log.md](../decisions/decision-log.md).

---

## Files

| File | What it covers |
|---|---|
| **★ [FOYER_MASTER_ELECTRICIAN_PLAN.md](FOYER_MASTER_ELECTRICIAN_PLAN.md)** ★ | **Authoritative foyer welcome system plan** (18 sections, ~17k words). Stone-clad feature wall + recessed monitor + Hikvision doorbell + cavity socket on back wall + halo LED + cavity speaker + 2 MCBs + 6-gang switch panel on N wall + Waveshare provisioning. PDF at [`../pdfs/FOYER_ELECTRICIAN_MASTER_PLAN.pdf`](../pdfs/FOYER_ELECTRICIAN_MASTER_PLAN.pdf). If anything in this folder conflicts with the foyer master plan, the master plan wins. |
| **[db-layout.md](db-layout.md)** | Distribution Board — MCB list, RCCB groups, DB sizing, wiring standards. **Read this first.** |
| **[conduits-and-cavities.md](conduits-and-cavities.md)** | Whole-house conduit + cavity reference. Part 1 (foyer cavity) is a summary; FOYER_MASTER_ELECTRICIAN_PLAN.md has full detail. |
| **[ground-floor-electrical.md](ground-floor-electrical.md)** | Room-by-room point schedule for GF: foyer (summary; full detail in foyer master plan), living, dining, kitchen, utility, MBR, bathroom, staircase, server niche, pooja |
| **[first-floor-electrical.md](first-floor-electrical.md)** | Room-by-room point schedule for FF: 2 bedrooms, 2 toilets, FF living, balconies, staircase to terrace |
| **[circuits-and-load.md](circuits-and-load.md)** | Master circuit registry, load estimation, wire/conduit procurement list |
| **[water-automation-conduits.md](water-automation-conduits.md)** | Water-level automation: 7-conduit pre-plaster schedule, JB specs, DB cupboard (co-located with main DB on East wall of foyer) |
| **[gf-bathroom-electrical.md](gf-bathroom-electrical.md)** | GF Common Bathroom — circuits, switch board, geyser, PIR |
| `low-voltage.md` | *(to create)* Cat6 drops, speaker wires, HDMI, doorbell, video intercom, CCTV |
| `automation-overlap.md` | *(to create)* Which points are smart vs dumb; neutral wire map for smart switches |

---

## Quick Reference — Key Decisions Already Made

| Decision | Value |
|---|---|
| **DB location (REVISED 2026-05-17)** | **East wall**, foyer, behind door swing (main door hinges East, swings against E wall) — supersedes earlier W-wall placement |
| DB size | 48-way (Schneider Acti9 IEF48) |
| DB brand | Schneider Acti9 (MCBs + RCCBs) |
| **Starter cupboard** | On East wall alongside or below DB — houses water automation P1 + P2 starters + Sonoff DUALR3 |
| Smart switch zones | Foyer, Living, Dining, Bedrooms × 3, Staircase, Balconies, Pooja, FF Living |
| Dumb switch zones | Kitchen, Utility, Store |
| Bathroom switches | PIR auto-off (standalone Legrand / Schneider PIR switch) |
| Wire brand | Finolex or Havells, FR-LSH |
| Server niche | Under staircase, GF, W wall — UPS + mini PC + network switch + 12-port Cat6 patch panel |
| **Foyer cavity (REVISED 2026-05-19)** | Raw cut 580×380×100mm; inner usable 540×340mm after 20mm stone reveal slips on front 30mm of all 4 inner walls. 2 sockets on **BACK wall** (not right wall): Monitor + Spare. 3 conduits enter back wall (Power + Data + Halo) + 1 exits top (ceiling speaker provision). |
| **Foyer Switch Panel** | **N wall** 1'6" section between corner window and main door, 6-gang at 1200mm FFL (electrician may upgrade to 7- or 8-gang if box fits) |
| **Foyer MCBs (REVISED 2026-05-18)** | 2 MCBs: B-Foyer-Lights (6A, all lighting incl. porch) + B-Foyer-Cavity (6A + 30mA RCBO, cavity sockets) |
| **Foyer face detection** | **Hikvision DS-KV6113-WPE1(C) Video Doorbell PoE** on outside of 1'6" N wall section (replaces dedicated CAM-1 install; CAM-1 conduit + back box provisioned only) |
| **🆕 Switch-box depth** | **65mm GI MS box at every smart-switch board** (Sonoff/Aqara relay sits behind plate) — 50mm only for dumb switches, sockets, geyser switches, AC sockets |
| **🆕 Wi-Fi backbone** | Main router in staircase niche (GF) + secondary AP on FF Living central wall (2400mm FFL) — wired Cat6 backhaul (run R-FF-1) |
| **🆕 Cat6 home-runs** | All Cat6 terminate at staircase niche 12-port patch panel: Hikvision doorbell + future cameras + foyer screen + FF router + BR1/BR2 study drops + Waveshare |

---

## Open Decisions (blocking further detail)

Before the electrician chases conduits, confirm these:

- [ ] **Number and location of ACs** — currently assumed 4 (Living, MBR, BR1, BR2). Confirm.
- [ ] **False ceiling** — GF Living and/or bedrooms? Drives cove lighting circuits.
- [ ] **Sanctioned load** — check with your EB (electricity board) what kW is allowed. Determines main MCB rating.
- [ ] **Geyser sizes** — 15L or 25L per bathroom?
- [ ] **Study table positions** in each bedroom — drives socket + Cat6 placement.
- [ ] **Chandelier in double-height void** — needs conduit from FF slab level.
- [ ] **Smart switch brand/series** — Wipro / Philips Wiz / Aqara / Schneider Wiser? Must decide before switch board boxes are fixed (modular frame size varies by brand).

---

## How to Evolve This Document

1. **New room decision made** → Update the relevant floor file's table row (change 🔲 to ✅).
2. **New circuit added** → Add a row to `circuits-and-load.md` AND a slot to `db-layout.md`.
3. **Smart switch brand chosen** → Create `automation-overlap.md` and map which switch boards need neutral wire.
4. **Conduit work starting** → Print / share `ground-floor-electrical.md` + `first-floor-electrical.md` with the electrician as the field reference.
5. **Any locked decision** → Log it in [../decisions/decision-log.md](../decisions/decision-log.md) with a date.
