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
- **Ground Floor:** Foyer (main entrance, N) → Living Area (TV unit, double-height) → Pooja (5'×5') → Dining → Kitchen with Utility + Store + Refrigerator zone → Master Bedroom (M.Bed) with wardrobes (12' top + 12'3" right) and attached Common Bathroom (9' × 4'6") → Stair landing on the W side. See [floor-plans/floor-plans-decoded.md](floor-plans/floor-plans-decoded.md).
- **First Floor:** Two Bedrooms (each ~13'-wide bay with attached toilet 8' × 5') along the south side, with right-side wardrobe (3' deep) and a Balcony on W → FF Living in the centre/lower-left → Stair continues to terrace → Cut-out double-height (16'9" × 11', no slab) on the lower-right → Front Balcony (11'9" × 7') on the lower-left. See [floor-plans/floor-plans-decoded.md](floor-plans/floor-plans-decoded.md).

## Workstreams (each has its own subfolder)
1. **Interior design** — style direction, palettes, room-by-room visual treatment. Image renders via `/banana` skill, saved to `interior-design/generated-images/`. **Master brief**: [interior-design/master-interior-spec.md](interior-design/master-interior-spec.md).
2. **Electrical layout** — switch/socket placement, lighting plan, circuiting, DB, conduits. Must be locked in **before** plastering/false-ceiling. **Field reference**: [electrical/conduits-and-cavities.md](electrical/conduits-and-cavities.md) and [pdfs/ELECTRICIAN_REFERENCE.pdf](pdfs/ELECTRICIAN_REFERENCE.pdf) (12-page printable handout).
3. **Furniture layout** — built-ins (wardrobes, TV unit, kitchen, pooja, dining), loose furniture, sizes.
4. **Home automation / IoT** — protocol (Matter / Zigbee / Wi-Fi / KNX), hubs, devices, scenes, network plan. **Wi-Fi backbone**: GF main router (staircase niche) + FF AP (FF Living wall, 2400mm) wired with Cat6 backhaul.
5. **Materials & finishes** — tiles, paint, wood, hardware, sanitaryware brand/SKU selection. **Master palette**: [materials-finishes/master-color-palette.md](materials-finishes/master-color-palette.md). **Printable interior brief**: [pdfs/INTERIOR_SUGGESTIONS.pdf](pdfs/INTERIOR_SUGGESTIONS.pdf) (24 pages with hex swatches).

## Tooling conventions
- **Image generation:** `/banana` skill only. Outputs → `interior-design/generated-images/`. Filename pattern: `<room>-<mood/style>-v<N>.png` (e.g. `living-warm-minimal-v2.png`).
- **Decisions:** every locked-in choice gets a one-liner in [decisions/decision-log.md](decisions/decision-log.md) with a date.
- **Open questions:** track in the relevant subfolder README under an **Open questions** heading — don't lose them in chat history.

## Known unknowns / to-confirm
- Civil status: is plastering / electrical chasing already done, or still to come? This gates how much can still change in the electrical layout.
- Exact kitchen width along N wall and final kitchen-to-dining depth split (kitchen target ~10ft, total zone 19'6").
- FF balcony (W side) final projection: stay at 3ft or expand?
- FF Bedroom 1 and 2 exact usable interior dimensions (to verify on-site).
- Budget envelope and timeline (not yet captured).
