# GF Common Bathroom — Lighting & Automation Spec

**Ceiling:** 8ft RCC — no false ceiling. Attic space above lintel gives top-down access for recessed fixtures.
**Automation:** PIR timer switch — lights auto-off when bathroom is unoccupied.
**Budget target:** ₹700–1,200 for the PIR switch itself.

---

## How It Works

```
Enter bathroom
     ↓
PIR detects motion → ALL lights ON instantly (mirror + downlights + niche LED)
     ↓
Use bathroom normally (PIR keeps detecting movement)
     ↓
Leave bathroom
     ↓
10 minutes of no motion → ALL lights turn OFF automatically
```

No app. No Wi-Fi. No hub. A single PIR timer wall switch does everything.
Exhaust fan has its own manual switch — stays on after you leave to clear moisture.

---

## Lighting Fixtures

Since there is no false ceiling, all fixtures go directly into (or onto) the 8ft RCC slab. The attic space above the lintel makes it easy for the electrician to run conduit and core-drill from above without breaking the bathroom ceiling.

| # | Fixture | Spec | Mounting | Location |
|---|---|---|---|---|
| L1 | LED backlit mirror | 3000K, 12–15W, IP44 | Wall-mount | North wall, above vanity, 1.2m from floor to bottom edge |
| L2 | IP65 recessed downlight | 3000K, 7W, white bezel | Recessed into RCC slab | Shower zone ceiling, centred |
| L3 | IP65 recessed downlight | 3000K, 7W, white bezel | Recessed into RCC slab | Dry zone (WC/vanity) ceiling, centred |
| L4 | LED strip (niche) | 3000K, IP65, 4–5W | Recessed in niche top edge | Upper storage niche, south wall shower zone |
| EF | Exhaust fan | 150mm, 30W | Ceiling or high west wall | Between dry and wet zones |

**Total switched load (L1–L4):** ~40W — well within 6A RCBO capacity.
**Exhaust fan:** On separate manual switch, not PIR-controlled.

---

## PIR Auto-Off Switch

**Device type:** PIR occupancy sensor + adjustable timer — replaces a standard wall switch.

| Spec | Value |
|---|---|
| Detection | 180° horizontal, 90° vertical — covers full 9×4.5ft room from the door position |
| Timer | Adjustable 1–30 min — **set to 10 minutes** |
| Load | 300–600W (our load is ~40W — well within limits) |
| Voltage | 230V AC |
| Mounting | Standard 2-module gang box (same size as normal switch) |

**Placement:** East wall, right of the door frame (dry zone, away from any splash). Standard switch height 4.5ft (1350mm) from floor. The PIR eye has clear line of sight diagonally across the full bathroom.

**Recommended brands:**
- Legrand Arteor PIR presence switch — ₹1,100–1,400
- Schneider Easy9 occupancy switch — ₹800–1,100
- Wipro occupancy switch — ₹700–900

**Settings to configure after installation:**
1. **Time dial (T):** Turn to 10 minutes. Lights stay on 10 min after last detected motion.
2. **Lux dial (L):** Turn to maximum (sun symbol). PIR activates regardless of ambient light level — important since the bathroom has a window.

---

## Wiring Schematic

```
DB (48-way)
 └─ RCBO 6A (GF Bathroom lighting circuit)
         │
         ▼
    PIR TIMER SWITCH (east wall, gang box)
         │  [load output]
         ▼
    Junction box in attic (above bathroom lintel)
         ├─── L1: LED mirror (via mirror's own driver)
         ├─── L2: IP65 downlight — shower zone
         ├─── L3: IP65 downlight — dry zone
         └─── L4: LED strip driver → niche LEDs

    Separate RCBO 6A (or same circuit, separate switch leg)
         └─── EF: Exhaust fan (manual switch, east wall, beside PIR switch)

    Separate RCBO 16A (already decided)
         └─── Geyser 15L
```

**Gang box on east wall (right of door):**
- Left position: PIR auto-off switch (controls L1–L4)
- Right position: Standard 6A switch (exhaust fan)

---

## Exhaust Fan

**Why separate manual switch (not on PIR):**
The exhaust fan should continue running for 5–10 minutes after the person leaves to clear residual moisture and odour. If it were on the PIR circuit, it would shut off with the lights.

**Placement:** High on the west wall (above the window, near the top) — furthest point from the door, creates a good cross-ventilation pull from entry door direction to the west wall exhaust. If west wall has no room above the window, use ceiling centre as fallback.

---

## Shower Zone Special Note — Window vs. Exhaust

The 3ft × 4ft frosted window on the west wall provides natural ventilation when open. However, in monsoon and rainy weather you cannot keep it open. The exhaust fan covers that gap. Wire the exhaust fan so it can be switched independently without affecting the bathroom lights.

---

## IP Ratings — Bathroom Zones (IS/IEC Standard)

```
Zone 0: Inside shower tray/area — IP67 minimum (submerged)
Zone 1: 2.25m above shower floor — IP65 minimum (water jets)
Zone 2: 0.6m outside Zone 1 — IP44 minimum (splash)
Outside zones: No IP requirement (standard fittings OK)
```

- L2 (shower ceiling downlight): Must be IP65 ✓
- L4 (niche LED strip): Must be IP65 ✓ (the niche is inside Zone 1)
- L1 (mirror): IP44 minimum — most LED mirrors are IP44 rated ✓
- L3 (dry zone downlight): IP44 minimum ✓
- PIR switch: Must be in Zone 2 or outside — east wall position is safe ✓
