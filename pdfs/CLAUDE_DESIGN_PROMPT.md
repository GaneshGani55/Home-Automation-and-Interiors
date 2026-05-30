# Claude Design Prompt — Interactive Conduit Map (HTML/CSS/JS)

**How to use:** open https://claude.ai or claude.com in a browser, start a new chat with **Claude Sonnet 4.6 or Opus 4.7**, and paste the entire prompt below (everything between the `--- BEGIN PROMPT ---` and `--- END PROMPT ---` markers). Claude will return a single self-contained `conduit-map.html` file you can open in any browser and host on a phone for site reference.

Tested on Claude.ai web with Artifacts enabled — Claude renders the live HTML inline for you to preview.

---

--- BEGIN PROMPT ---

You are designing a single-page, mobile-friendly **interactive conduit map** for a residential electrician working on-site in Chitradurga, Karnataka, India. The electrician is **not tech-savvy** and **does not have patience for long text PDFs** — he ignored the previous handouts. The HTML must communicate every conduit visually first, with details revealed only on tap.

## What to produce

A **single HTML file** (with inline CSS and JS — no external dependencies, no CDN libraries except optional Tailwind CDN). Must work fully offline once loaded. Must work in mobile Safari + Android Chrome.

## The user story

1. Electrician opens the page on his phone.
2. He sees a **floor plan** (top-down 2D schematic) with **coloured conduit lines** drawn on top.
3. He can **tap any conduit line** → a side panel slides in with: conduit ID, size, what's inside, route description, status (pull now / pull string only), note/gotcha.
4. He can **switch floors** (Ground Floor / First Floor / Riser cross-section) using tabs at the top.
5. He can **filter by service** (Power / Data / LV-16 / Water) with toggle chips.
6. There's a **legend strip** at the top showing what each colour means.

## Visual style

- **Floor plan**: line-art SVG drawn fresh in the HTML (do not require image files). Rooms shown as labelled rectangles with door swings as arcs. Use real room proportions (see DIMENSIONS below). Wall lines `stroke: #333, stroke-width: 2`. Room labels in a neutral mid-grey.
- **Conduit lines**: thick coloured strokes (4-5 px) drawn as SVG `<path>` with right-angle bends. Provision conduits use `stroke-dasharray: 6,4`.
- **Numbered callout circles** at each destination: filled circle (live) or hollow circle (provision), with the ref label in the centre, and a short text label beside it.
- **Hubs**: yellow rectangles for "NICHE (data hub)", pink for "DB (power)", green for "DB CUPBOARD (water)", labelled clearly.
- **Side panel**: slides in from the right on tap, 350px wide on desktop, full-width modal on mobile.
- **Top bar**: project title + floor tabs + service filters + legend.
- Aesthetic: clean, almost industrial-drawing style. Pale-cream background `#FAF8F2`, dark ink `#1C1C1E`. Sans-serif (system font stack).
- Mobile: orientation-aware. Show "rotate to landscape for best view" hint if portrait on small screens.

## The orientation (critical)

Both floor plans drawn with:
- **TOP edge** = SOUTH wall (master bedroom S-wall window, FF bedroom S-wall windows)
- **BOTTOM edge** = NORTH wall (main entrance, foyer)
- **LEFT edge** = EAST (kitchen E-wall, exterior)
- **RIGHT edge** = WEST (TV wall, FF balcony)

Always show a small compass indicator (N arrow pointing DOWN) so the electrician isn't confused. Mention "main door is at the bottom".

## DIMENSIONS — Ground Floor

Building footprint is L-shaped. Approximate room positions (in arbitrary SVG units, used to lay out the plan):

| Room | Roughly where | Notes |
|---|---|---|
| Kitchen | top-left | ~10ft deep, E-wall window over sink |
| Master bedroom | top-right | 12'×12'3", wardrobe on S wall, bed against E wall |
| Common bath | middle-right area | 9' × 4'6", door from W |
| Dining | middle-left | open to kitchen + foyer |
| Staircase | middle (between dining and bath) | 22 risers UP to FF |
| Pooja | lower-left | 5' × 5' recessed |
| Foyer | bottom-left notch | 6'×4'9", main door, DB on E wall |
| Living | bottom-right | 16'11"×16'11", TV on W wall, void above |
| Parking | outside bottom-left | external area |

## DIMENSIONS — First Floor

| Room | Roughly where | Notes |
|---|---|---|
| Bedroom 1 | top-left (E side) | bed against W wall, toilet at very top |
| Toilet 1 | top, attached to BR1 | sink-toilet-shower E to W |
| Bedroom 2 | top-right (W side) | bed against E wall, toilet at very top |
| Toilet 2 | top, attached to BR2 | sink-toilet-shower W to E |
| Wardrobe BR2 | right edge | 3ft deep |
| FF balcony (W) | far right | 3ft projection |
| FF Living | middle-lower-left | central area between bedroom doors |
| Cut-out (double-height void) | lower-right | NO SLAB — opens to GF Living below |
| Front balcony | lower-left | 11'9" × 7' |

## CONDUIT DATA (use exactly this)

```json
{
  "hubs": {
    "niche": { "floor": "GF", "x_pct": 35, "y_pct": 78, "label": "NICHE (data hub)", "fill": "#FFE650" },
    "db": { "floor": "GF", "x_pct": 12, "y_pct": 83, "label": "DB (power)", "fill": "#FFC8C8" },
    "db_cupboard": { "floor": "GF", "x_pct": 13, "y_pct": 88, "label": "DB CUPBOARD (water)", "fill": "#C8F0DC" },
    "riser_ff": { "floor": "FF", "x_pct": 55, "y_pct": 55, "label": "RISER (from GF)", "fill": "#FFE650" }
  },

  "conduits": [
    { "ref": "P1", "floor": "GF", "service": "power_light", "size": "25mm", "status": "live",
      "from": "DB", "to": "Foyer Switch Panel (N wall, 1200mm FFL)",
      "contents": "1.5sqmm L + N + E (feeds 6-gang foyer panel)",
      "note": "65mm-deep GI MS box. NEUTRAL must reach the panel - no exceptions." },
    { "ref": "P2", "floor": "GF", "service": "power_light", "size": "25mm", "status": "live",
      "from": "Foyer Switch Panel", "to": "2x foyer ceiling GU10 spotlights",
      "contents": "Switched live Gang 1 + N + E",
      "note": "GU10 7W 2700K, adjustable gimbals to angle 30deg toward stone wall." },
    { "ref": "P3", "floor": "GF", "service": "power_light", "size": "25mm", "status": "live",
      "from": "Foyer Switch Panel", "to": "False-ceiling cove driver + halo driver",
      "contents": "Switched live Gang 2 + N + E",
      "note": "Both drivers above false ceiling. Halo wraps cavity top." },
    { "ref": "P4", "floor": "GF", "service": "power_light", "size": "16mm", "status": "live",
      "from": "Foyer Switch Panel", "to": "Walnut shelf 24V driver",
      "contents": "Switched live Gang 3 + N + E",
      "note": "Floor route preferred." },
    { "ref": "P5", "floor": "GF", "service": "power_light", "size": "16mm", "status": "live",
      "from": "Foyer Switch Panel", "to": "Outside porch ceiling light",
      "contents": "Switched live Gang 5 + N + E",
      "note": "Through N wall. Outdoor IP44 fitting." },
    { "ref": "P6", "floor": "GF", "service": "power_light", "size": "25mm", "status": "live",
      "from": "DB", "to": "Living false ceiling, 4x recessed COB ceiling boxes (12W 2700K)",
      "contents": "1.5sqmm L + N + E", "note": "Stay in solid-slab zone, avoid the void area." },
    { "ref": "P7", "floor": "GF", "service": "power_light", "size": "25mm", "status": "live",
      "from": "DB", "to": "Chandelier ceiling rose box on FF beam (over void)",
      "contents": "1.5sqmm L + N + E", "note": "Chandelier hangs into double-height void from above." },
    { "ref": "P8", "floor": "GF", "service": "power_light", "size": "25mm", "status": "live",
      "from": "DB", "to": "Kitchen ceiling box + utility light",
      "contents": "1.5sqmm L + N + E", "note": "4000K cool/neutral panel for task area." },
    { "ref": "P9", "floor": "GF", "service": "power_light", "size": "25mm", "status": "live",
      "from": "DB", "to": "Dining pendant centre + 2x supplementary downlights",
      "contents": "1.5sqmm L + N + E", "note": "Pendant drop to 2100mm FFL. Confirm table position." },
    { "ref": "P10", "floor": "GF", "service": "power_light", "size": "25mm", "status": "live",
      "from": "DB", "to": "MBR ceiling + bedsides (E wall) + wardrobe driver (S+W walls)",
      "contents": "1.5sqmm L + N + E", "note": "Centre on bed after headboard line is marked." },
    { "ref": "P11", "floor": "GF", "service": "power_light", "size": "25mm", "status": "live",
      "from": "DB", "to": "GF Bath ceiling + mirror + exhaust + PIR outside door",
      "contents": "1.5sqmm L + N + E",
      "note": "PIR outside door at 1200mm FFL. Geyser switch BELOW at 1050mm." },
    { "ref": "P12", "floor": "GF", "service": "power_light", "size": "25mm", "status": "live",
      "from": "DB", "to": "Pooja ceiling spotlights + decorative strip",
      "contents": "1.5sqmm L + N + E", "note": "Confirm fixture spec on-site." },
    { "ref": "P13", "floor": "GF", "service": "power_light", "size": "25mm", "status": "live",
      "from": "DB", "to": "Step lights + mid-flight wall light + niche + landing",
      "contents": "1.5sqmm L + N + E", "note": "Step lights (3W each) on each riser left side." },

    { "ref": "H1", "floor": "GF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "DB", "to": "Foyer screen cavity (back wall) - 2x 5A sockets",
      "contents": "2.5sqmm L + N + E", "note": "Sonoff Mini R2 inside socket box switches Monitor only." },
    { "ref": "H2", "floor": "GF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "DB", "to": "TV wall (W wall of Living) - 3 boxes (16A + double 5A + Cat6 keystone)",
      "contents": "2.5sqmm L + N + E", "note": "All at 300mm FFL. Keystone box 150mm from power boxes." },
    { "ref": "H3", "floor": "GF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "DB", "to": "Living perimeter sockets (multiple boxes)",
      "contents": "2.5sqmm L + N + E", "note": "Skirting-level chase. Min 150mm from corners." },
    { "ref": "H4", "floor": "GF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "DB", "to": "Kitchen counter - 4x sockets at 1100mm FFL",
      "contents": "2.5sqmm L + N + E", "note": "Above counter, behind backsplash. Confirm with kitchen designer." },
    { "ref": "H5", "floor": "GF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "DB", "to": "Chimney socket above hob at 1900mm FFL",
      "contents": "2.5sqmm L + N + E", "note": "16A socket centred over hob." },
    { "ref": "H6", "floor": "GF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "DB", "to": "Hob position at 150mm FFL (floor screed route)",
      "contents": "4sqmm L + N + E (25A direct hardwire)",
      "note": "NO socket - direct hardwire. 25A MCB." },
    { "ref": "H7", "floor": "GF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "DB", "to": "Fridge niche socket at 300mm FFL",
      "contents": "2.5sqmm L + N + E", "note": "Confirm height after fridge model is picked." },
    { "ref": "H8", "floor": "GF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "DB", "to": "MBR bedside sockets (E wall) at 600mm FFL + utility",
      "contents": "2.5sqmm L + N + E", "note": "Flank the headboard." },
    { "ref": "H9", "floor": "GF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "DB", "to": "MBR AC socket at 1850mm FFL on N wall above door",
      "contents": "4sqmm L + N + E (20A RCBO)",
      "note": "Confirm AC manual for socket position relative to outdoor unit." },
    { "ref": "H10", "floor": "GF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "DB", "to": "Bath geyser outlet at 1850mm FFL inside bathroom",
      "contents": "2.5sqmm L + N + E (20A RCBO)",
      "note": "Geyser SWITCH (DP) outside door at 1050mm FFL." },

    { "ref": "D1", "floor": "GF", "service": "data", "size": "25mm", "status": "live",
      "from": "Niche", "to": "Foyer screen cavity (back wall, bottom-RIGHT)",
      "contents": "1x indoor Cat6 (UTP)",
      "note": "FLOOR route under screed (not ceiling). ~12m. Drops Cat6 to RPi behind foyer monitor." },
    { "ref": "D2", "floor": "GF", "service": "data", "size": "25mm", "status": "live",
      "from": "Niche", "to": "Main-door outside face (Hikvision DS-KV6113-WPE1(C) Video Doorbell PoE)",
      "contents": "1x outdoor LSZH UV-rated Cat6 (PoE)",
      "note": "Doorbell at 1450mm FFL, latch side. Shared floor route with D1+D3." },
    { "ref": "D3", "floor": "GF", "service": "data", "size": "25mm", "status": "provision",
      "from": "Niche", "to": "Porch W wall (future face-detection camera)",
      "contents": "PULL STRING ONLY - capped IP67 back-box, 1650mm FFL",
      "note": "DROPPED from base install (Hikvision doorbell handles face capture)." },
    { "ref": "D4", "floor": "GF", "service": "data", "size": "25mm", "status": "provision",
      "from": "Niche", "to": "Porch ceiling NE corner (future overview camera)",
      "contents": "PULL STRING ONLY", "note": "False-ceiling route only - soffit not reachable via floor." },
    { "ref": "D5", "floor": "GF", "service": "data", "size": "25mm", "status": "live",
      "from": "Niche", "to": "Staircase S wall, 1500mm FFL (Waveshare 10.1in panel)",
      "contents": "1x HDMI 2.0 (3m) + 1x USB-A->micro-USB (3m) + existing Cat6 spare",
      "note": "CUSTOM 280x195x80mm masonry cavity (not modular). Above existing 2M switch with ~200mm gap." },
    { "ref": "D6", "floor": "GF", "service": "data", "size": "25mm", "status": "live",
      "from": "Niche", "to": "Dining E wall (Waveshare dining panel)",
      "contents": "1x indoor Cat6 + 1x pull string",
      "note": "~12m / 35-40ft. Pi-at-screen pattern. Position TBD by interior designer." },
    { "ref": "D7", "floor": "GF", "service": "data", "size": "25mm", "status": "live",
      "from": "Niche", "to": "Ceiling JB above future dining table (mono speaker)",
      "contents": "1x indoor Cat6 (PoE-capable) + 1x pull string",
      "note": "Pi + PAM8403 + 3in ceiling speaker. ~10m." },
    { "ref": "D8", "floor": "GF", "service": "data", "size": "25mm", "status": "live",
      "from": "Niche", "to": "E-wall exterior at kitchen-utility junction, 2400-2600mm FFL",
      "contents": "1x outdoor LSZH UV Cat6 (PoE) + draw wire",
      "note": "Horizontal run 150mm below GF slab soffit. Confirm utility external door." },
    { "ref": "D9", "floor": "GF", "service": "data", "size": "25mm x 3", "status": "live",
      "from": "Niche", "to": "Vertical riser up staircase W wall -> FF (3 bundles)",
      "contents": "3x LV-25 conduits: (a) R-FF-1 2x Cat6, (b) R-FF-2 1x Cat6, (c) R-FF-3 1x Cat6. CAM-3+CAM-5 continue up.",
      "note": "Dedicated 150mm-wide chase channel." },

    { "ref": "L1", "floor": "GF", "service": "lv16", "size": "16mm", "status": "live",
      "from": "Foyer Switch Panel", "to": "Cove LED driver in false ceiling",
      "contents": "24V DC 2-core", "note": "Driver in false ceiling perimeter. Accessible via inspection hatch." },
    { "ref": "L2", "floor": "GF", "service": "lv16", "size": "16mm", "status": "live",
      "from": "Foyer Switch Panel", "to": "Halo driver above false ceiling near cavity top",
      "contents": "24V DC 2-core", "note": "Halo strip wraps cavity reveal. Amber 2200K." },
    { "ref": "L3", "floor": "GF", "service": "lv16", "size": "16mm", "status": "live",
      "from": "Foyer Switch Panel", "to": "Walnut shelf 24V driver",
      "contents": "24V DC 2-core", "note": "Shelf strip 6W/m, warm white." },
    { "ref": "L4", "floor": "GF", "service": "lv16", "size": "16mm", "status": "provision",
      "from": "Cavity TOP wall", "to": "Future ceiling speaker in foyer false ceiling",
      "contents": "PULL STRING ONLY", "note": "Conduit exits cavity TOP inner wall going up." },
    { "ref": "L5", "floor": "GF", "service": "lv16", "size": "16mm", "status": "provision",
      "from": "Niche", "to": "Main door frame TOP (concealed door contact sensor)",
      "contents": "PULL STRING ONLY", "note": "Future provision." },
    { "ref": "L6", "floor": "GF", "service": "lv16", "size": "16mm", "status": "live",
      "from": "MBR ceiling JB", "to": "S-wall wardrobe top rail LED driver",
      "contents": "24V DC 2-core", "note": "Door-activated sensor on each leaf." },
    { "ref": "L7", "floor": "GF", "service": "lv16", "size": "16mm", "status": "live",
      "from": "MBR ceiling JB", "to": "W-wall wardrobe tail LED driver",
      "contents": "24V DC 2-core", "note": "Tail of L-shaped wardrobe." },

    { "ref": "W1", "floor": "GF", "service": "water", "size": "20mm", "status": "live",
      "from": "Niche", "to": "Terrace SW parapet Sintex JB (~42ft)",
      "contents": "1x outdoor LSZH Cat6 (PoE for Sintex water-level sensor)",
      "note": "Embedded under terrace screed BEFORE tiling. IP65 JB 200x200x100mm." },
    { "ref": "W2", "floor": "GF", "service": "water", "size": "16mm", "status": "live",
      "from": "Niche", "to": "Terrace Sintex float -> DB cupboard (~45ft)",
      "contents": "2-core 1.5mm2 double-insulated", "note": "Parallel to W1, MIN 50mm separation." },
    { "ref": "W3", "floor": "GF", "service": "water", "size": "20mm", "status": "live",
      "from": "Niche", "to": "E external wall above manhole, sump JB (~25ft)",
      "contents": "1x outdoor LSZH Cat6 (PoE)", "note": "Sleeve through E wall, slope outward." },
    { "ref": "W4", "floor": "GF", "service": "water", "size": "16mm", "status": "live",
      "from": "Niche", "to": "Sump float -> DB cupboard (~25ft)",
      "contents": "2-core 1.5mm2", "note": "Parallel to W3, MIN 50mm separation." },
    { "ref": "W5", "floor": "GF", "service": "water", "size": "20mm", "status": "provision",
      "from": "Niche", "to": "DB cupboard (~12ft, future backup link)",
      "contents": "PULL STRING ONLY",
      "note": "Both ends capped + labelled WATER AUTOMATION - FUTURE Cat6." },
    { "ref": "W6", "floor": "GF", "service": "water", "size": "25mm", "status": "live",
      "from": "DB cupboard", "to": "Borewell head outside",
      "contents": "4sqmm armoured (16A Type C)", "note": "CONFIRM existing run can be repurposed." },
    { "ref": "W7", "floor": "GF", "service": "water", "size": "25mm", "status": "live",
      "from": "DB cupboard", "to": "P2 cage east outside wall (~5ft)",
      "contents": "2.5sqmm PVC (16A Type C)", "note": "Cage = lockable outdoor enclosure." },

    { "ref": "F1", "floor": "FF", "service": "power_light", "size": "25mm", "status": "live",
      "from": "Riser", "to": "BR2 ceiling + cove + bedsides + wardrobe driver",
      "contents": "1.5sqmm L + N + E", "note": "Centre on bed once headboard line is marked." },
    { "ref": "F2", "floor": "FF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "Riser", "to": "BR2 bedside + study sockets at 600mm FFL",
      "contents": "2.5sqmm L + N + E" },
    { "ref": "F3", "floor": "FF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "Riser", "to": "BR2 AC socket at 1850mm FFL",
      "contents": "4sqmm L + N + E (20A AC)" },
    { "ref": "F4", "floor": "FF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "Riser", "to": "T2 geyser outlet 1850mm FFL + DP switch outside door",
      "contents": "2.5sqmm L + N + E (20A geyser)" },
    { "ref": "F5", "floor": "FF", "service": "power_light", "size": "25mm", "status": "live",
      "from": "Riser", "to": "BR1 ceiling + bedsides + wardrobe driver",
      "contents": "1.5sqmm L + N + E" },
    { "ref": "F6", "floor": "FF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "Riser", "to": "BR1 bedside + study sockets at 600mm FFL",
      "contents": "2.5sqmm L + N + E" },
    { "ref": "F7", "floor": "FF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "Riser", "to": "BR1 AC socket at 1850mm FFL",
      "contents": "4sqmm L + N + E (20A AC)" },
    { "ref": "F8", "floor": "FF", "service": "power_heavy", "size": "25mm", "status": "live",
      "from": "Riser", "to": "T1 geyser + lights bundle",
      "contents": "2.5sqmm L + N + E + 1.5sqmm lights" },
    { "ref": "F9", "floor": "FF", "service": "power_light", "size": "25mm", "status": "live",
      "from": "Riser", "to": "FF Living ceiling + front balcony + corridor lights",
      "contents": "1.5sqmm L + N + E" },
    { "ref": "F10", "floor": "FF", "service": "data", "size": "25mm", "status": "live",
      "from": "Riser", "to": "FF Living central wall (router/AP) at 2400mm FFL",
      "contents": "2x Cat6 UTP (router + spare)",
      "note": "Wall plate Cat6 keystone x2 + 5A socket 300mm beside. Equidistant between BR1 and BR2." },
    { "ref": "F11", "floor": "FF", "service": "data", "size": "25mm", "status": "live",
      "from": "Riser", "to": "BR2 study wall, 700mm FFL",
      "contents": "1x Cat6 UTP + draw wire" },
    { "ref": "F12", "floor": "FF", "service": "data", "size": "25mm", "status": "live",
      "from": "Riser", "to": "BR1 study wall, 700mm FFL",
      "contents": "1x Cat6 UTP + draw wire" },
    { "ref": "F13", "floor": "FF", "service": "data", "size": "16mm", "status": "provision",
      "from": "FF AP", "to": "FF balcony soffit (future outdoor mesh AP)",
      "contents": "PULL STRING ONLY", "note": "Cap at IP67 keystone box at balcony soffit corner." },
    { "ref": "F14", "floor": "FF", "service": "data", "size": "25mm", "status": "provision",
      "from": "Riser", "to": "Front balcony NW corner soffit/parapet (CAM-3)",
      "contents": "PULL STRING + 1x outdoor Cat6",
      "note": "Elevated overview of compound, gate, driveway." },
    { "ref": "F15", "floor": "FF", "service": "data", "size": "25mm", "status": "provision",
      "from": "Riser", "to": "Continue UP to terrace level (CAM-5)",
      "contents": "PULL STRING + 1x outdoor UV-resistant Cat6",
      "note": "Use UV-rated conduit for last 500mm above roof. Parapet mount." }
  ]
}
```

## Colour code (use exactly)

| Service | Colour | Hex | Real PVC |
|---|---|---|---|
| `power_light` | RED | `#DC1E1E` | 25mm RED |
| `power_heavy` | BLUE | `#1E5ADC` | 25mm BLUE |
| `data` | ORANGE | `#EB6E14` | 25mm GREY (orange used for visibility) |
| `lv16` | PURPLE | `#8C5AC8` | 16mm GREY |
| `water` | GREEN | `#1E8C64` | 20/16mm GREY |

## Behaviour requirements

1. **Tap-to-detail.** Tapping a conduit line or its numbered circle opens the side panel populated with that conduit's `ref`, `size`, `from -> to`, `contents`, `note`, and `status` badge. Tap outside to close.
2. **Filters.** Toggle chips at top: `Power (light)`, `Power (heavy)`, `Data`, `LV-16`, `Water`. Tap one to show only that service. Tap again to clear. Allow multi-select.
3. **Floor tabs.** Three tabs: `Ground Floor`, `First Floor`, `Riser (vertical)`. Riser tab shows a stylized cross-section of the staircase wall with all bundles going up GF -> FF -> terrace.
4. **Search.** Small search box top-right that filters conduits by ref (e.g. type "P5") or by destination keyword (e.g. "geyser").
5. **Status legend.** Solid line = pull cable now. Dashed = pull string only (provision). Make this visible in the top legend strip.
6. **Print view.** A "Print" button that hides the side panel and chrome, showing just the floor plan + cheat sheet, A3 landscape friendly. CSS `@media print` rules.
7. **Self-locating.** Tap a conduit in the side panel detail → the line flashes/highlights on the plan (animate stroke-width briefly).

## Required floor plan elements

Draw the rooms as SVG `<rect>` with stroke. Label each room with a `<text>` inside. Include:

**GF**: Kitchen, Master Bedroom, Common Bath, Dining, Staircase (with numbered step grid 1-22), Pooja, Foyer, Living Hall (mark the void boundary), Parking (outside), Utility, Store room, Fridge niche.

**FF**: Bedroom 1, Bedroom 2, Toilet 1, Toilet 2, FF Living, Front Balcony, W Balcony, Wardrobe BR2, Cut-out (double-height void — show as hatched area).

**Riser tab**: stylized column with 4 horizontal lines marking GROUND, GF SLAB, FIRST FLOOR, TERRACE. 11 vertical bundles (use the data above) shown as coloured arrows going up. Right-side legend listing each bundle.

## Anti-requirements (do NOT do these)

- Do NOT use 3D rendering, three.js, or pseudo-isometric views. Top-down 2D only.
- Do NOT load external images, fonts, or JS libraries except optional Tailwind CDN.
- Do NOT use animations that distract during scrolling.
- Do NOT show all 45 conduits at once initially — that was the failure mode of the original PDFs. Default load shows all, but the filters and tap-to-detail are the primary interaction.
- Do NOT use emojis.
- Do NOT include the project-management chatter (no "this is generated by Claude" banners). The electrician should see only the conduit map.

## Code quality

- Single HTML file, ≤ 1000 lines including data.
- All conduit positions computed from a small lookup table mapping `hub + destination_key` to `(x_pct, y_pct)` percentages of the SVG viewport. The conduit list data uses descriptive `from`/`to` text — you choose the destination coordinates from your interpretation of the floor plan you draw.
- Comment any non-obvious bit of CSS or JS.
- The HTML must render correctly when saved to disk and opened with `file://` URL.

## Deliverable

A complete `<html>...</html>` file. Render it as an Artifact so I can preview it inline.

After rendering, also briefly tell me: (1) how many conduits you ended up rendering per service; (2) any conduit whose route you guessed because the description was ambiguous, so I can correct.

--- END PROMPT ---

## After Claude generates the HTML

1. Click "Download" or "Copy" the HTML artifact.
2. Save it as `pdfs/conduit-map.html` in this repo.
3. Open it in any browser to verify it works offline.
4. **Test on a phone** before showing the electrician — open it in mobile Safari/Chrome and check the tap interactions work.
5. If you want to AirDrop or share it: zip the single HTML file (it's self-contained) and message it to the electrician.

## Iterating

If Claude's first attempt has issues (wrong room positions, missing conduits, ugly colour mix), reply in the same chat with specific corrections — e.g.:
> "The Master Bedroom should be in the top-RIGHT not top-left of the GF plan. Move the bed against the LEFT wall of MBR (which is the E wall)."

Claude can edit the artifact in place.

## Updating the conduit list later

When new conduits get added (or the spec changes), edit the `conduits` JSON block in this prompt and re-run. The structure is stable — only the data changes.

The source-of-truth markdown for the conduit data is:
- `electrical/conduits-and-cavities.md` PART 2
- `electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md`
- `electrical/water-automation-conduits.md` (or PART 0.7)
