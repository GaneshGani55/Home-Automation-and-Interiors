# Electrical Layout

Complete electrical plan for the 2-floor home. Start with the DB layout, then dive into each floor.

> This is a **living document** — update it as decisions are made. Every file uses a consistent status system: ✅ CONFIRMED · 🔲 TBD · ⚠️ PENDING DECISION. When something moves from TBD to CONFIRMED, update the relevant file AND add a line to [../decisions/decision-log.md](../decisions/decision-log.md).

---

## Files

| File | What it covers |
|---|---|
| **[db-layout.md](db-layout.md)** | Distribution Board — MCB list, RCCB groups, DB sizing, wiring standards. **Read this first.** |
| **[ground-floor-electrical.md](ground-floor-electrical.md)** | Room-by-room point schedule for GF: foyer, living, dining, kitchen, utility, MBR, bathroom, staircase, server niche, pooja |
| **[first-floor-electrical.md](first-floor-electrical.md)** | Room-by-room point schedule for FF: 2 bedrooms, 2 toilets, FF living, balconies, staircase to terrace |
| **[circuits-and-load.md](circuits-and-load.md)** | Master circuit registry, load estimation, wire/conduit procurement list |
| `low-voltage.md` | *(to create)* Cat6 drops, speaker wires, HDMI, doorbell, video intercom, CCTV |
| `automation-overlap.md` | *(to create)* Which points are smart vs dumb; neutral wire map for smart switches |

---

## Quick Reference — Key Decisions Already Made

| Decision | Value |
|---|---|
| DB location | West wall, foyer, behind door swing |
| DB size | 40-way (Schneider Acti9 IEF40) |
| DB brand | Schneider Acti9 (MCBs + RCCBs) |
| Smart switch zones | Foyer, Living, Dining, Bedrooms × 3, Staircase, Balconies, Pooja |
| Dumb switch zones | Kitchen, Utility, Store |
| Bathroom switches | PIR auto-off (standalone Legrand / Schneider PIR switch) |
| Wire brand | Finolex or Havells, FR-LSH |
| Server niche | Under staircase, GF, W wall — UPS + mini PC + network switch |
| Foyer screen | 6A socket + Cat6 in wall cavity; 2× ceiling spotlight circuit |

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
