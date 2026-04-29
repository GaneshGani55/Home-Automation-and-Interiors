# Circuit Registry & Load Calculation

> Master reference: every circuit in the house in one place.
> Update this file whenever a circuit is added, changed, or confirmed.
> Use this to verify DB sizing and to hand to your electrician.

---

## How to Read This

- **Circuit ID** matches the DB slot in [db-layout.md](db-layout.md) and the room files.
- **Estimated Load (W)** is the realistic running load (not the MCB trip rating).
- **Wire size** is the minimum — your electrician should not go below this.
- **Status:** ✅ CONFIRMED · 🔲 TBD · ⚠️ DECISION NEEDED

---

## Complete Circuit Table

| Circuit ID | Description | MCB | RCCB Group | Wire | Est. Load (W) | Status |
|---|---|---|---|---|---|---|
| GF-WET-01 | GF Bathroom — lights + exhaust + mirror | 6A | A | 1.5mm² | 40W | ✅ |
| GF-WET-02 | GF Bathroom — geyser | 20A | A | 2.5mm² | 2000W | ✅ |
| GF-WET-03 | Kitchen — lights + exhaust | 6A | A | 1.5mm² | 60W | ✅ |
| GF-WET-04 | Kitchen — counter sockets | 16A | A | 2.5mm² | 1500W | ✅ |
| GF-WET-05 | Kitchen — chimney | 16A | A | 2.5mm² | 250W | ✅ |
| GF-WET-06 | Kitchen — hob/cooktop | 20A | A | 4mm² | 3500W | ✅ |
| GF-WET-07 | Utility — washing machine | 16A | A | 2.5mm² | 2000W | ✅ |
| GF-WET-08 | Refrigerator (always-live) | 16A | A | 2.5mm² | 200W | ✅ |
| GF-LIV-01 | Foyer — ceiling spots + LED strips | 6A | B | 1.5mm² | 50W | ✅ |
| GF-LIV-02 | Foyer — screen socket + speaker | 6A | B | 1.5mm² | 60W | ✅ |
| GF-LIV-03 | Living — main ceiling lights | 6A | B | 1.5mm² | 80W | ✅ |
| GF-LIV-04 | Living — cove / accent | 6A | B | 1.5mm² | 60W | 🔲 TBD |
| GF-LIV-05 | Living — sockets (TV wall + general) | 16A | B | 2.5mm² | 400W | ✅ |
| GF-LIV-06 | Dining — lights + socket | 6A | B | 1.5mm² | 50W | ✅ |
| GF-LIV-07 | Staircase — lights (2-way) | 6A | B | 1.5mm² | 60W | ✅ |
| GF-LIV-08 | Pooja — lights + socket | 6A | B | 1.5mm² | 30W | ✅ |
| GF-BED-01 | Master Bedroom — lights | 6A | C | 1.5mm² | 60W | ✅ |
| GF-BED-02 | Master Bedroom — sockets | 16A | C | 2.5mm² | 300W | ✅ |
| FF-BED-01 | Bedroom 1 — lights | 6A | D | 1.5mm² | 60W | ✅ |
| FF-BED-02 | Bedroom 1 — sockets | 16A | D | 2.5mm² | 300W | ✅ |
| FF-BED-03 | Toilet 1 — lights + exhaust | 6A | D | 1.5mm² | 40W | ✅ |
| FF-BED-04 | Toilet 1 — geyser | 20A | D | 2.5mm² | 2000W | ✅ |
| FF-BED-05 | Bedroom 2 — lights | 6A | D | 1.5mm² | 60W | ✅ |
| FF-BED-06 | Bedroom 2 — sockets | 16A | D | 2.5mm² | 300W | ✅ |
| FF-BED-07 | Toilet 2 — lights + exhaust | 6A | D | 1.5mm² | 40W | ✅ |
| FF-BED-08 | Toilet 2 — geyser | 20A | D | 2.5mm² | 2000W | ✅ |
| FF-BED-09 | FF corridor + living — lights + socket | 6A | D | 1.5mm² | 50W | ✅ |
| FF-BED-10 | All balconies + terrace | 6A | D | 1.5mm² | 60W | ✅ |
| HVAC-01 | AC — Living Area | 20A RCBO | — | 4mm² | 1500W | ⚠️ Confirm |
| HVAC-02 | AC — Master Bedroom | 20A RCBO | — | 4mm² | 1500W | ⚠️ Confirm |
| HVAC-03 | AC — Bedroom 1 | 20A RCBO | — | 4mm² | 1500W | ⚠️ Confirm |
| HVAC-04 | AC — Bedroom 2 | 20A RCBO | — | 4mm² | 1500W | ⚠️ Confirm |
| SERVER-01 | Server niche — UPS input | 20A RCBO | — | 4mm² | 1000W | ✅ |
| SERVER-02 | Server niche — general sockets | 16A RCBO | — | 2.5mm² | 200W | ✅ |

---

## Load Estimation (for sanctioned load / EB application)

| Category | Circuits | Est. Simultaneous Load |
|---|---|---|
| Lighting (all floors) | 12 circuits | ~600W |
| Kitchen appliances | 4 circuits | ~4,000W (rarely all at once) |
| Bathroom geysers (3×) | 3 circuits | ~6,000W (rarely all 3 together) |
| ACs (4×, assume 2 running) | 4 circuits | ~3,000W |
| General sockets | 5 circuits | ~1,000W |
| Server / UPS | 2 circuits | ~1,200W |
| **Realistic peak load** | | **~8,000–10,000W** |
| **Sanctioned load to apply for** | | **10 kW (single phase max in most areas) or 3-phase 15kW** |

> **Talk to your electricity board (BESCOM / TNEB / MSEDCL etc.) about sanctioned load before the DB is energised.** For a 2-floor home with 4 ACs and a kitchen, 10kW single-phase is usually sufficient. If denied, 3-phase is the fallback — but that changes the DB design.

---

## Wire & Conduit Procurement Guide

| Item | Qty (estimate) | Brand | Notes |
|---|---|---|---|
| 1.5mm² FR wire (red/black/green) | ~300m | Finolex / Havells | Lighting circuits |
| 2.5mm² FR wire | ~250m | Finolex / Havells | Socket circuits |
| 4mm² FR wire | ~80m | Finolex / Havells | ACs, hob, server UPS |
| 25mm PVC conduit | ~150m | AKG / Precision | Power runs |
| 16mm PVC conduit | ~60m | AKG / Precision | Low-voltage / lighting branch |
| Cat6 UTP cable | ~100m | D-Link / Systimax | LV network runs |
| 2-core speaker wire (1.5mm²) | ~15m | Any shielded | Foyer speaker |
| 40-way DB enclosure | 1 | Schneider Acti9 IEF40 | |
| 63A DP MCB (main) | 1 | Schneider Acti9 iC60N | |
| 40A RCCB 30mA × 4 | 4 | Schneider Acti9 iID | Groups A, B, C, D |
| 6A MCB × 12 | 12 | Schneider Acti9 iC60N | Lighting circuits |
| 16A MCB × 8 | 8 | Schneider Acti9 iC60N | Socket circuits |
| 20A MCB × 3 | 3 | Schneider Acti9 iC60N | Geysers |
| 20A RCBO × 5 | 5 | Schneider Acti9 iC60N-H | ACs + server (E1–E5) |
| 16A RCBO × 1 | 1 | Schneider Acti9 iC60N-H | Server sockets (E6) |

> All MCBs above are **Type B** (standard residential). **Type C** is for motors (not needed here). Stick to one brand throughout — mixing brands in a DB is messy and can cause incompatibility.

---

## Evolution Log

> Append a line here every time the circuit list changes. Keeps a history for the electrician.

| Date | Change | Who |
|---|---|---|
| 2026-04-27 | Initial circuit list created from floor plan + confirmed decisions | Claude |

