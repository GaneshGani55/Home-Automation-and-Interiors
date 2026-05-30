# mmWave Presence Sensors — Working Draft

> ⚠️ **HOLDING FILE — do NOT merge into `decisions/decision-log.md` yet.**
> Ganesh is finalising mmWave presence sensors in a separate session. This file only exists so the
> interactive conduit map can *show* the sensor locations. The authoritative spec lives in that other
> session; update here, not the decision log, until Ganesh says it's locked.

## Intent (as of 2026-05-29)
- Put mmWave presence sensors in **all 3 bedrooms**, **all 3 bathrooms**, and **one on the ceiling at the mid-point between the Dining and Living hall**.
- **Power is by wire — NOT PoE.** Already discussed one round with the electrician.
  - **Wall-mounted** sensors: 5V from a **USB female socket fed off the normal mains line** (a USB charger/outlet module).
  - **Ceiling-mounted** sensors: **230 → 5V buck converter** off the normal line.
- **No dedicated data conduit** is being chased for these. On the map they are shown as markers only
  ("there is a mmWave sensor here"), not as conduit runs.
- Sensor hardware model (Aqara FP2 / ESP32 + LD2410C / etc.) is **TBD** — owned by Ganesh's other session.
  Whatever the model, it reports presence to Home Assistant (Wi-Fi via the GF/FF ceiling APs) → HA drives
  the existing Sonoff relays for lighting.

## Sensor schedule (7) — DRAFT
| Ref | Room (physical) | Mount | Power |
|---|---|---|---|
| M1 | GF Master Bedroom | ceiling centre **(default — unconfirmed)** | buck 230→5V |
| M2 | GF Common Bathroom | wall | USB socket off mains |
| M3 | GF Dining/Living mid-ceiling | ceiling | buck 230→5V |
| M4 | FF west bedroom (balcony side) | ceiling | buck 230→5V |
| M5 | FF east bedroom | wall | USB socket off mains |
| M6 | FF west toilet (balcony bedroom's bath) | ceiling | buck 230→5V |
| M7 | FF east toilet | wall | USB socket off mains |

## Open / to confirm
- **M1 (GF Master Bedroom)** mount not given by Ganesh — defaulted to ceiling.
- **FF room labels:** floor-plans-decoded calls the **east** room Bedroom 1 and the **west/balcony** room
  Bedroom 2. Ganesh's instruction tied "ceiling" to "BR1 = west balcony room." If BR1 is actually the
  east room, M6/M7 (toilet mounts) flip. Confirm before locking.
- Bathroom note: bathrooms currently use **dumb PIR timer switches** (no Sonoff relay). If mmWave is meant
  to *drive* bathroom lights via HA, a Sonoff relay must be added to the bathroom lighting circuit. Pending
  Ganesh's other-session decision; does not block conduit work.
