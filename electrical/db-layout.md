# Distribution Board (DB) Layout

> ⚠️ **Note 2026-05-22:** the blanket "65mm-deep boxes everywhere for smart switches" mandate (2026-05-06) has been **relaxed** to "depth-as-needed + 2 extra modules per Sonoff" — see [FOYER_MASTER_ELECTRICIAN_PLAN.md § revision summary](FOYER_MASTER_ELECTRICIAN_PLAN.md). General rule: standard 50mm box + 2 extra modules. Exception: high-density boards (e.g., Foyer Switch Panel with 6 Sonoffs in one box) still need 65mm + 2M-per-Sonoff per master plan § 8.5.
>
> **What is a DB?** The DB (Distribution Board) is the metal/plastic box on your wall that houses all the MCBs and RCCBs. Every electrical circuit in the house originates here. Think of it as the brain of your home's electrical system.
>
> **MCB** (Miniature Circuit Breaker) = protects each circuit from overload and short circuit. Like a smart resettable fuse. Rated in Amps (6A, 16A, 20A, 32A).
>
> **RCCB** (Residual Current Circuit Breaker) = detects current leaking to earth (e.g., someone getting a shock). Trips in ~30ms at 30mA. **Life-safety device.** Does NOT protect against overload — must always have MCBs downstream.
>
> **RCBO** = MCB + RCCB combined in one unit. More expensive, ideal for critical circuits (server, geysers).
>
> **Rule of thumb:** RCCB covers a group of circuits. MCBs sit on the "output" side of each RCCB and protect individual circuits.

---

## DB Location
- **Floor:** Ground Floor
- **Wall:** **East wall**, foyer (behind door swing — main door hinges on East jamb and swings against E wall, so door panel covers DB when open)
- **Height:** Bottom of DB at **1500mm FFL**
- **DB size:** **48-way** flush-mount Schneider Acti9 IEF48 (per 2026-04-27 decision; 42 confirmed circuits + 6 spare)
- **Recess dimensions:** 400 × 600 × 100 mm
- **Adjacent:** **Starter cupboard** for water automation (P1 + P2 starters + Sonoff DUALR3) — surface-mounted alongside or below DB on same East wall. Layout (side-by-side vs stacked) chosen on-site by electrician + carpenter; see [FOYER_MASTER_ELECTRICIAN_PLAN.md § 6](FOYER_MASTER_ELECTRICIAN_PLAN.md).

## Recommended DB Brand
**Schneider Electric Acti9** or **Legrand DX³** series. Both are widely available in India, have standardised components, and electricians are trained on them. Avoid off-brand DB boxes — the MCBs and RCCBs inside them are what matter, and these two brands have the best quality in India at reasonable cost.

---

## DB Single-Line Diagram (text form)

```
INCOMING MAINS (230V, 50Hz, Single Phase)
         │
    ┌────┴────┐
    │  MAIN   │  ← 63A DP MCB (Double Pole — disconnects L+N together)
    │  MCB    │     Schneider Acti9 iC60N or equivalent
    └────┬────┘
         │
    ┌────┴──────────────────────────────────────────┐
    │                                               │
  RCCB                                        RCCB
  GROUP A                                    GROUP B
  (Wet Areas)                                (Living + GF Power)
  40A / 30mA                                 40A / 30mA
    │                                               │
  MCBs A1–A8                                  MCBs B1–B6
    │                                               │
  RCCB                                        RCCB
  GROUP C                                    GROUP D
  (FF Bedrooms)                              (FF Wet Areas)
  40A / 30mA                                 40A / 30mA
    │                                               │
  MCBs C1–C5                                  MCBs D1–D5
    │
  DEDICATED MCBs (no RCCB — ACs, Server)
  E1–E6  (each is an RCBO = MCB + RCCB in one)
```

---

## MCB Register — Complete List

> **Status key:** ✅ CONFIRMED · 🔲 TBD · ⚠️ PENDING DECISION
> Update this table as decisions are made. Add circuit number to the conduit/chase drawing when each circuit is confirmed.

### GROUP A — Wet Areas (RCCB 40A/30mA)

| Slot | Circuit ID | Circuit Name | MCB Rating | Wire Size | Status |
|------|-----------|---|---|---|---|
| A1 | GF-WET-01 | GF Common Bathroom — lights + exhaust + mirror light | 6A | 1.5mm² | ✅ |
| A2 | GF-WET-02 | GF Common Bathroom — geyser (dedicated) | 20A | 2.5mm² | ✅ |
| A3 | GF-WET-03 | Kitchen — lights + exhaust fan | 6A | 1.5mm² | ✅ |
| A4 | GF-WET-04 | Kitchen — counter sockets (4× 5A) | 16A | 2.5mm² | ✅ |
| A5 | GF-WET-05 | Kitchen — chimney (dedicated) | 16A | 2.5mm² | ✅ |
| A6 | GF-WET-06 | Kitchen — hob / cooktop (dedicated) | 20A | 4mm² | ✅ |
| A7 | GF-WET-07 | Utility — washing machine (dedicated) | 16A | 2.5mm² | ✅ |
| A8 | GF-WET-08 | Refrigerator (dedicated, always-live) | 16A | 2.5mm² | ✅ |

> Refrigerator gets its own always-live circuit so a tripped circuit elsewhere doesn't spoil food.

---

### GROUP B — GF Living, Dining, Foyer Power (RCCB 40A/30mA)

| Slot | Circuit ID | Circuit Name | MCB Rating | Wire Size | Status |
|------|-----------|---|---|---|---|
| B1 | **B-Foyer-Lights** | Foyer + porch — all lighting (2× GU10 spots + cove + cavity halo + walnut shelf LED + porch ceiling + porch wall future) via 6-gang Switch Panel on N wall | 6A | 1.5mm² | ✅ Revised 2026-05-18: consolidates old B1 + B10 + porch lights into one MCB |
| B2 | **B-Foyer-Cavity** | Foyer cavity — 2× 5A sockets (Monitor + Spare), Sonoff-switched. 230V direct to cavity, not through wall switch. | 6A + **30mA RCBO** | 2.5mm² | ✅ Revised 2026-05-18: RCBO mandatory for electronics |
| B3 | GF-LIV-03 | Living Area — main ceiling lights (smart) | 6A | 1.5mm² | ✅ |
| B4 | GF-LIV-04 | Living Area — cove / false ceiling accent lighting | 6A | 1.5mm² | ✅ False ceiling confirmed for Living |
| B5 | GF-LIV-05 | Living Area — sockets (TV wall + general) | 16A | 2.5mm² | ✅ |
| B6 | GF-LIV-06 | Dining Area — main lights + sockets | 6A | 1.5mm² | ✅ |
| B9 | GF-LIV-09 | Dining Area — false ceiling cove / accent | 6A | 1.5mm² | ✅ False ceiling confirmed |
| B10 | ~~GF-LIV-10~~ | ~~Foyer — false ceiling cove (above stone wall)~~ — **MERGED into B1 (B-Foyer-Lights) 2026-05-18.** Slot B10 now SPARE. | — | — | ⚠️ Slot reassigned |
| B7 | GF-LIV-07 | Staircase — lights (2-way, GF bottom to FF top) | 6A | 1.5mm² | ✅ |
| B8 | GF-LIV-08 | Pooja room — lights + socket | 6A | 1.5mm² | ✅ |

---

### GROUP C — GF Master Bedroom (RCCB 40A/30mA)

| Slot | Circuit ID | Circuit Name | MCB Rating | Wire Size | Status |
|------|-----------|---|---|---|---|
| C1 | GF-BED-01 | Master Bedroom — lights (smart) | 6A | 1.5mm² | ✅ |
| C2 | GF-BED-02 | Master Bedroom — sockets (bedside × 2 + general) | 16A | 2.5mm² | ✅ |

---

### GROUP D — FF Bedrooms + Wet Areas (RCCB 40A/30mA)

| Slot | Circuit ID | Circuit Name | MCB Rating | Wire Size | Status |
|------|-----------|---|---|---|---|
| D1 | FF-BED-01 | Bedroom 1 — lights (smart) | 6A | 1.5mm² | ✅ |
| D2 | FF-BED-02 | Bedroom 1 — sockets (bedside × 2 + study + general) | 16A | 2.5mm² | ✅ |
| D3 | FF-BED-03 | Toilet 1 — lights + exhaust | 6A | 1.5mm² | ✅ |
| D4 | FF-BED-04 | Toilet 1 — geyser (dedicated) | 20A | 2.5mm² | ✅ |
| D5 | FF-BED-05 | Bedroom 2 — lights (smart) | 6A | 1.5mm² | ✅ |
| D6 | FF-BED-06 | Bedroom 2 — sockets (bedside × 2 + study + general) | 16A | 2.5mm² | ✅ |
| D7 | FF-BED-07 | Toilet 2 — lights + exhaust | 6A | 1.5mm² | ✅ |
| D8 | FF-BED-08 | Toilet 2 — geyser (dedicated) | 20A | 2.5mm² | ✅ |
| D9 | FF-BED-09 | FF Living / corridor — lights + sockets | 6A | 1.5mm² | ✅ |
| D10 | FF-BED-10 | Balconies (FF front + FF W side) — lights + weatherproof sockets | 6A | 1.5mm² | ✅ |

---

### GROUP E — Dedicated Heavy Circuits (each is an RCBO = MCB+RCCB combined)

> ACs and the server get their own RCBO so a trip affects only that one load — not a whole RCCB group.

| Slot | Circuit ID | Circuit Name | RCBO Rating | Wire Size | Status |
|------|-----------|---|---|---|---|
| E1 | HVAC-01 | AC — Living Area | 20A | 4mm² | ✅ Point confirmed |
| E2 | HVAC-02 | AC — Dining Area | 20A | 4mm² | ✅ Point confirmed |
| E3 | HVAC-03 | AC — Master Bedroom | 20A | 4mm² | ✅ Point confirmed |
| E4 | HVAC-04 | AC — Bedroom 1 (FF) | 20A | 4mm² | ✅ Point confirmed |
| E5 | HVAC-05 | AC — Bedroom 2 (FF) | 20A | 4mm² | ✅ Point confirmed |
| E6 | HVAC-06 | AC — FF Living / corridor | 20A | 4mm² | ✅ Point confirmed (install later if needed) |
| E7 | SERVER-01 | Server niche — UPS input (dedicated) | 20A | 4mm² | ✅ |
| E8 | SERVER-02 | Server niche — general sockets (mini PC, switch, etc.) | 16A | 2.5mm² | ✅ |

---

### SPARE SLOTS (future use)

| Slot | Notes |
|---|---|
| F1–F4 | Reserved. Label these "SPARE" physically in the DB. Pull a neutral to each spare slot now. |

---

## DB Summary

| Group | RCCB | MCB Count | Purpose |
|---|---|---|---|
| A | 40A/30mA | 8 | Wet areas + kitchen |
| B | 40A/30mA | 10 | GF living, foyer, dining (incl. 2 cove circuits) |
| C | 40A/30mA | 2 | GF master bedroom |
| D | 40A/30mA | 10 | FF bedrooms + bathrooms |
| E | RCBO each | 8 | 6 ACs + 2 server (dedicated) |
| F | — | 4 | Spare |
| **Total** | **1 main + 4 RCCB** | **42 ways** | Use a **40-way DB + 1 extension** or a 48-way DB |

> ⚠️ Circuit count grew to 42 with all AC points confirmed. Upgrade to a **48-way DB** (Schneider Acti9 IEF48) — only ₹500 more than the 40-way but avoids being cramped.

> **Recommended DB box:** Schneider Acti9 40-way flush-mount (IEF40). Gives 40 slots + spare. About ₹3,500–5,000 for the enclosure; MCBs and RCCBs are bought separately.

---

## Wiring Standards (follow throughout)

| Item | Standard |
|---|---|
| Lighting circuits | 1.5mm² FR-LSH (fire-retardant) wire, 6A MCB |
| Power/socket circuits | 2.5mm² FR-LSH wire, 16A MCB |
| AC / geyser / heavy loads | 4mm² FR-LSH wire, 20A MCB |
| Conduit | 25mm PVC for power runs; 16mm PVC for lighting/LV |
| Earthing | Green/yellow wire to every socket, every switch board |
| Neutral colour | Black (Indian standard) |
| Live colour | Red |
| Earth colour | Green/yellow |
| Wire brand | Finolex / Havells / RR Kabel (all tier-1 Indian brands) |

---

## Open Decisions (update when resolved)

- [x] **ACs** — points in ALL rooms confirmed: Living, Dining, MBR, BR1, BR2, FF Living = 6 RCBO slots (E1–E6). Install AC units later as needed; point is pre-wired.
- [x] **False ceiling** — confirmed for: Living Area (GF), Dining (GF), Foyer (GF), one bedroom (TBD which one — see below). Cove lighting circuit B4 confirmed for Living. Add cove circuits for Dining + Foyer to Group B.
- [ ] **Which bedroom gets false ceiling?** User said "only one room" on FF. Confirm: Bedroom 1 or Bedroom 2 (or Master Bedroom on GF)?
- [ ] **Microwave + toaster points** — confirm kitchen appliance count for socket planning.
- [ ] **Water purifier / RO point** — needs a 5A socket under the kitchen sink or counter.
- [ ] **CCTV / NVR power** — if any cameras are non-PoE, each needs a nearby 5A socket.
- [ ] **Outdoor / porch light** — add if entrance needs a separate porch light over the main door.
- [ ] **Main MCB amperage** — confirm with your electricity board what sanctioned load is (typically 32A or 40A for a 2-floor home). Size the main DP MCB to that.
