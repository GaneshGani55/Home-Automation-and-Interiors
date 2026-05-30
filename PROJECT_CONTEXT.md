# Project Context

## What this project is
Ganesh is designing the **interiors and home-automation system** for a two-storey residential home. The build/architectural shell appears largely fixed (floor plans exist in both AutoCAD and an updated hand-redraw). Ongoing work is interiors, electrical, furniture, automation/IoT, and finishes.

## House at a glance
- **Two floors:** Ground Floor + First Floor.
- **Site orientation (confirmed):** main entrance faces **North**; the long axis runs roughly North–South. Handwritten sheets are drawn with S at top, N at bottom, E at left, W at right.
- **Footprint:** roughly **32'2" × 17'11"** at the widest, with a stepped (L-shape) plan at both floors. AutoCAD sheet labels a notional 30' × 40' grid; treat handwritten dimensions as the live ones.
- **Notable feature:** a **double-height cut-out** above the Ground-Floor living area (no slab on First Floor at that location) — a key visual/lighting feature for interior design.
- **Ceiling heights:** Ground Floor = **11ft**, First Floor = **10ft**.
- **Wall thicknesses:** structural/external = **9"**, partition walls = **4"**.
- **Vertical circulation:** internal staircase, 22 risers; First-Floor flight continues up to terrace.

## Floors — quick summary
- **Ground Floor:** Foyer (main entrance, N) → Living Area (TV unit, double-height) → Pooja (5'×5') → Dining → Kitchen with Utility + Store + Refrigerator zone → Master Bedroom (M.Bed) with L-wardrobe on S wall (10'3") + W-wall tail (~3'), and attached Common Bathroom (9' × 4'6") → Stair landing on the W side. See [floor-plans/floor-plans-decoded.md](floor-plans/floor-plans-decoded.md).
- **First Floor:** Two Bedrooms (each ~13'-wide bay with attached toilet 8' × 5') along the south side, with right-side wardrobe (3' deep) and a Balcony on W → FF Living in the centre/lower-left → Stair continues to terrace → Cut-out double-height (16'9" × 11', no slab) on the lower-right → Front Balcony (11'9" × 7') on the lower-left. See [floor-plans/floor-plans-decoded.md](floor-plans/floor-plans-decoded.md).

## Workstreams (each has its own subfolder)
1. **Interior design** — style direction, palettes, room-by-room visual treatment. Image renders via `/banana` skill, saved to `interior-design/generated-images/`. **Master brief**: [interior-design/master-interior-spec.md](interior-design/master-interior-spec.md).
2. **Electrical layout** — switch/socket placement, lighting plan, circuiting, DB, conduits. Must be locked in **before** plastering/false-ceiling. **Field reference**: [electrical/conduits-and-cavities.md](electrical/conduits-and-cavities.md) and [pdfs/ELECTRICIAN_REFERENCE.pdf](pdfs/ELECTRICIAN_REFERENCE.pdf) (12-page printable handout). **Foyer-specific master plan** (2026-05-22): [electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md](electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md) and [pdfs/FOYER_ELECTRICIAN_MASTER_PLAN.pdf](pdfs/FOYER_ELECTRICIAN_MASTER_PLAN.pdf) (44-page printable with vector diagrams).
3. **Furniture layout** — built-ins (wardrobes, TV unit, kitchen, pooja, dining), loose furniture, sizes.
4. **Home automation / IoT** — protocol (Matter / Zigbee / Wi-Fi / KNX), hubs, devices, scenes, network plan. **Wi-Fi backbone (locked 2026-05-29 v2 — ceiling-mounted APs)**: GF main router (TP-Link AX55, staircase niche) + **GF ceiling AP** on GF false ceiling between dining/living (new conduit `R-GF-1`) + **FF ceiling AP** on FF false ceiling (existing `R-FF-1` cable continues up from wall position to ceiling). Both APs PoE-only, model placeholder "Ubiquiti UniFi U6-Lite or equivalent". Original wall-mounted FF AP plan at 2400mm FFL is superseded. **Foyer welcome system** (face detection via Hikvision doorbell → Frigate/CompreFace on Beelink → welcome screen): fully designed; see foyer master plan.
5. **Materials & finishes** — tiles, paint, wood, hardware, sanitaryware brand/SKU selection. **Master palette**: [materials-finishes/master-color-palette.md](materials-finishes/master-color-palette.md). **Printable interior brief**: [pdfs/INTERIOR_SUGGESTIONS.pdf](pdfs/INTERIOR_SUGGESTIONS.pdf) (24 pages with hex swatches).

## Tooling conventions
- **Image generation:** `/banana` skill only. Outputs → `interior-design/generated-images/`. Filename pattern: `<room>-<mood/style>-v<N>.png` (e.g. `living-warm-minimal-v2.png`).
- **Decisions:** every locked-in choice gets a one-liner in [decisions/decision-log.md](decisions/decision-log.md) with a date.
- **Open questions:** track in the relevant subfolder README under an **Open questions** heading — don't lose them in chat history.

## Known unknowns / to-confirm
- ~~Civil status: is plastering / electrical chasing already done, or still to come?~~ **RESOLVED 2026-05-22**: Electrical chasing + cavity cutting starts 2026-05-23 (Phase 1 marking). Plaster begins ~2026-05-30. Foyer electrical fully locked; see [electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md](electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md). Other rooms still in design.
- Exact kitchen width along N wall and final kitchen-to-dining depth split (kitchen target ~10ft, total zone 19'6").
- FF balcony (W side) final projection: stay at 3ft or expand?
- FF Bedroom 1 and 2 exact usable interior dimensions (to verify on-site).
- Budget envelope and timeline (not yet captured). Foyer welcome scope estimated ~₹1,06,230 (per FOYER master plan § 15).
- Open foyer items still to decide (NOT blocking plaster): smart door lock (battery deadbolt = no conduit needed, wired = conduit needed pre-plaster).
- ~~Dining hall speaker provision~~ **RESOLVED 2026-05-29 (foyer-pattern, Option B)**: Mono ceiling speaker provisioned via NEW conduit `C-Niche-DiningSpeaker` (**25mm grey, ~10m, niche → dining ceiling centered above table) + 1× Cat6 (PoE-capable) + pull-string** + capped junction box. Architecture mirrors foyer audio chain (Pi + PAM8403 amp + Visaton FR 8). Install-time choice: shared dining-screen Pi drives BOTH screen + speaker (saves ~₹2K) OR dedicated Pi Zero at ceiling on PoE. ~₹500 today, ~₹4-6K future.
- ~~Waveshare full hardware design~~ **RESOLVED 2026-05-29 v3.1**: Hybrid architecture. **Staircase**: 280 × 195 × 80 mm custom masonry cavity (NOT a modular back box — v3.1 correction) at 1500 mm FFL on S wall, vertically aligned above existing 2M light switch (~200 mm gap). Waveshare 10.1" HDMI LCD (B) with case, 1280×800, driven Beelink-direct via HDMI + USB through existing conduit. USB ACR122U NFC behind walnut bezel (~320 × 235 mm external, 220 × 140 mm cutout). **Dining (~12m run, E wall near breakfast counter)**: Pi-at-screen wired pattern matching foyer welcome system — single Cat6 in new `C-Niche-Dining` conduit. Dining position + height defer to interior designer (cantilever shelf mount). Dashboard layout still deferred. ~₹18,500-21,700 today, ~₹34-41K lifetime for both screens. See [electrical/WAVESHARE_INDOOR_PANEL.md](electrical/WAVESHARE_INDOOR_PANEL.md).
