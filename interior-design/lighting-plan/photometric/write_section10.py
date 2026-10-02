#!/usr/bin/env python3
"""Regenerate § 10 "Photometric Verification — Double-Height Living Room" of
../../lighting-and-false-ceiling-design.md from tables.md + results.json (run photometric_living.py first).
The prose cites numbers through variables so the section always matches the last model run."""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
DOC = HERE.parent.parent / "lighting-and-false-ceiling-design.md"
tables = (HERE / "tables.md").read_text(encoding="utf-8")
R = json.loads((HERE / "results.json").read_text(encoding="utf-8"))

def grab(start, end=None):
    i = tables.index(start); j = tables.index(end, i) if end else len(tables)
    return tables[i:j].strip().replace("### ", "#### ")
def kv(scene, name):
    return next(k["total"] for k in R[scene]["keys"] if k["name"] == name)
def kd(scene, name, who):
    return next(k["contrib"].get(who, 0) for k in R[scene]["keys"] if k["name"] == name)
st = {sc: R[sc]["stats"] for sc in ("FULL", "EVENING", "MOVIE", "NIGHT")}
prev = R["sensitivity"]["Previous design: Bolt 12W over the landing + 470 lm bulbs"]
pkv = lambda name: next(k["total"] for k in prev["keys"] if k["name"] == name)
F, E, M, N = "FULL", "EVENING", "MOVIE", "NIGHT"
coffee, sofa, chair = "Coffee-table top", "N sofa, book held (reading plane)", "Accent chairs (south strip), seat"
r0 = lambda v: f"{v:.0f}"

section = f"""## 10. Photometric Verification — Double-Height Living Room

**Status: PARTIALLY VERIFIED (model, not measurement). Updated 2026-10-02 for the accepted design.** The track spots are calculated from TISVA's own published lumens and optics; the recessed downlights, the Avia spot and all LED strips are calculated from *estimated* lumens because TISVA publishes none for those products (basis stated for every number). No site measurement exists yet. The living room is **not** declared "photometrically verified" until TISVA supplies Rega Plus and Lumelace data or a lux meter confirms the key points after installation (§ 10.13). What the model shows robustly across the whole uncertainty range tested in § 10.5: no downlights are needed in the 21 ft void; the earlier Bolt 12 W over the half landing was over-bright (now replaced by an Avia 7 W aimed at the stair wall — accepted); the curtain pelmet strip lights only the top metre.

Two changes from this check were **accepted on 2026-10-02 and are built into the tables below**: (1) F37 half-landing fixture = Avia 7 W black surface spot aimed at the stair feature wall (was Bolt 12 W); (2) pendant smart bulbs = 806 lm class, tunable, set to 3000 K (was 470 lm). The previous design is kept as a comparison row in the sensitivity table.

Reproduce: `python3 interior-design/lighting-plan/photometric/photometric_living.py` then `python3 interior-design/lighting-plan/photometric/write_section10.py` (positions come from `lighting-data.js`; outputs: `tables.md`, `results.json`, heatmaps, section drawing, and this section).

### 10.1 Seven words that are not the same thing

| Quantity | Unit | What it is | Living-room example (from the tables below) |
|---|---|---|---|
| Electrical power | W | What the fixture draws from the wall. Says nothing about light by itself. | Axios head 20 W; Rega Plus 12 W; strip 10 W/m |
| Luminous flux | lm (lumen) | Total light leaving the fixture in all directions. | Axios 20 W = **1600 lm** (TISVA); Rega Plus 12 W ≈ 900 lm (estimate) |
| Luminous intensity | cd (candela) | Light per unit solid angle in one direction; the beam's "punch". Same lumens into a narrow beam = higher candela. | Axios 1600 lm: 24° optic ≈ 7,400 cd on axis, 60° optic ≈ 1,250 cd |
| Beam angle | ° | Full cone angle where intensity has fallen to 50 % of the on-axis value. Set by the optic (reflector/lens), not by the LED. | Rega 38° (inferred), Axios 15/24/38/60 selectable, Spotlit 120° |
| Illuminance | lx (lux = lm/m²) | Light landing on a surface. **This is what a room "feels" like.** Depends on candela, distance² and angle. | Coffee table ≈ {r0(kv(F,coffee))} lx FULL, ≈ {r0(kv(E,coffee))} lx EVENING |
| CRI | — | How truthfully colours appear under the light (100 = daylight). | Rega Plus and Avia >90 (price list); Axios >80 (catalogue); Lumelace not published |
| Colour temperature | K | Warm (2700–3000 K) to cool (6500 K). Mood, not brightness. | Whole living 3000 K; smart bulbs set to 3000 K |

A COB ("chip on board") is only the LED package; it can sit behind a 15° lens or a 120° diffuser. "COB downlight" tells you nothing about the beam.

### 10.2 Geometry and assumptions

Positions are the ones in `lighting-data.js` (same as the ceiling map). Heights above the GF finished floor:

| Light | Where | Height of the light source | Really at 21 ft? |
|---|---|---|---|
| F38, F39 Rega Plus 12 W | south-strip false ceiling, x 12 & 15 ft, y 23.3 ft | **2.74 m (9 ft)** | no |
| F40, F41, F42 Axios Pro 20 W on the 1 m track | underside of the EAST edge beam, x 10.1 ft | track at 3.35 m (11 ft); optical centre ≈ **3.15 m** (body is 25.5 cm tall, TISVA) | no |
| S10 beam-edge LED profile | underside of the S + E edge beams | **3.35 m (11 ft)** | no |
| Pendant cluster (10 globes modelled) | hung from the roof slab through the void lid, x 18.7, y 31.4 ft | globes **2.6 m to 5.3 m**; anchor 6.25 m | anchor yes; light sources no |
| S20 curtain pelmet strip | recessed pelmet in the void lid, N wall | **6.10 m (20 ft)** | **yes** |
| S11 TV-unit strips | vertical reveals of the TV unit | 0.4–5.5 m (modelled at 1.6 m, 50 % of flux into the room) | no |
| F37 Avia 7 W (accepted) | FF-landing slab soffit, aimed at the stair feature wall above flight 1 (aim point x 23 ft, 2.6 m) | 3.25 m above GF floor = **1.4 m above the landing** | no |
| F31–F36 Spotlit Pro 2 W | stair wall, 0.3 m above alternate treads | 0.3–1.9 m | no |
| F6–F9 Rega Plus 7 W (passage/hall) | 9 ft false ceiling outside the living | 2.74 m | no |

Only the pelmet strip and the pendant anchor are at the top of the void. Nothing is recessed at 21 ft.

Other assumptions: room per § 4.6 (void 16.6 × 11 ft, strip 7.1 × 3.9 ft); receiving planes = floor (0 m), coffee table and seats (0.45 m), book in hand (0.75 m), TV wall (vertical, x = 27 ft), curtain (vertical, y = 36.8 ft), stair treads at their real heights (flight 1 rises 0 → 1.83 m west; flight 2 rises 1.83 → 3.51 m east), half landing 1.83 m. Night-time, curtains drawn, no daylight. New fixtures, clean (no maintenance factor; multiply by ≈ 0.8 for a 5-year-old installation). Reflectances: floor polished blond-ivory tile 0.50, ivory walls 0.60, curtain 0.45, TV stone/teak wall 0.42, open east side 0.30, lid ceiling 0.80. Scenes: **FULL** everything 100 %; **EVENING** coves 40 %, pendant 30 %, floor lamp on, downlights/track off; **MOVIE** TV strips 15 %, beam line 20 %; **NIGHT walk** passage/hall/stair lights only.

### 10.3 Fixture data and where each number comes from

| Fixture | W | lm | peak cd (model) | beam | CRI | CCT | mount | data basis |
|---|---:|---:|---:|---|---|---|---|---|
| Axios Pro 20 W track spot `823TKL2030094` | 20 | **1600** | 3,000 (38°) / 7,400 (24°) / 1,250 (60°) | 15/24/38/60° selectable | >80 | 3000 K | track under beam, 11 ft | **TISVA Architectural Catalogue 2023 p.59** (lumens, beam options, CRI, size). No polar curve published → intensity shape = Gaussian at the chosen optic with a 0.91 peak factor (the factor TISVA's own Fugl data shows: documented 1812 lx at 1 m vs 1995 lx for an ideal Gaussian). |
| Rega Plus 12 W `806DLR12338912` | 12 | **900 (est. 850–950)** | ≈ 1,700 | 38° (inferred from code pattern) | >90 (price list) | 3000 K | recessed, 9 ft | **Estimate.** Not in the 2023 catalogue; the May-25 price list gives W, CCT, finish, CRI only. Lumens from TISVA's consistent 79–81 lm/W on COB downlights (Orrin 13 W 1050 lm, Galaxy Pro 12 W 960 lm, GVO 12 W 950 lm) less ~10 % for CRI>90 chips. Intensity shape **fitted to TISVA's published Orrin 13 W polar curve and illuminance table** (deep-recessed analogue); soft case uses the Orrin 7.5 W fit. |
| Rega Plus 7 W `806DLR733892` | 7 | 520 (est.) | ≈ 600 | 38° (inferred) | >90 | 3000 K | recessed, 9 ft | Estimate; shape fitted to Orrin 7.5 W (600 lm, peak 1227 cd/klm, catalogue p.37–38). |
| Avia 7 W surface spot `806DLA7338992` (half landing, accepted) | 7 | 520 (est.) | ≈ 1,060 | 36° (assumed) | >90 (price list) | 3000 K | landing soffit, aimed at the wall | Estimate: Avia is not in the 2023 catalogue; 7 W × ~75 lm/W; beam assumed. |
| Lumelace 24 V 10 W/m `816LS50302420` | 10/m | 900/m raw → **630/m effective** in an opal profile (est.) | Lambertian line | 120° | **not published** | 3000 K | profiles at 11 ft (S10), 6.1 m (S20), TV unit (S11) | Catalogue p.75 lists W/m, CCT, IP, voltage only. 80–110 lm/W is the normal range for 2835 strips; 0.70 diffuser transmission assumed. |
| Pendant smart bulbs (accepted spec) | 10 × ~8 | 806 each → ×0.75 opal globe | 48 cd per globe (isotropic) | 360° | 80–90 | tunable, set to 3000 K | 2.6–5.3 m | Bulb lumens = manufacturer data (Philips Hue White Ambiance / IKEA Trådfri E27 806 lm); globe transmission estimated. |
| Spotlit Pro 2 W `806DL23120R` | 2 | 140 (est.) | ≈ 42 | 120° (price list) | n/a | 3000 K | stair wall | Estimate (~70 lm/W). Dimensions only in the 2020 MRP booklet. |
| Floor lamp (decor) | ~9 | 800 bulb, 60 % out of shade | — | wide | — | 3000 K | 1.5 m | Estimate. |

Documented photometric data used for calibration (TISVA Architectural Catalogue 2023, public PDF): Orrin 7.5 W = 600 lm, 38°, polar peak ≈ 1227 cd/klm, 398 lx average in a Ø 0.76 m beam at 1 m; Orrin 13 W = 1050 lm, 38°, polar ≈ 3181 cd/klm ring max, 1071 lx in Ø 0.58 m at 1 m, 119 lx in Ø 1.73 m at 3 m; Fugl 7.5 W = 430 lm, 25°, 1812 lx at 1 m on axis; Veros Pro 10 W = 900 lm, 24°; Axios Pro 10/20/30 W = 800/1600/2400 lm. No IES/LDT files are published for any TISVA product.

### 10.4 Method

Direct illuminance at a point: E = I(α) · cos i / d², where I(α) is the fixture's intensity at angle α off its aiming axis, i the angle between the surface normal and the incoming ray, d the distance. Point sources: Gaussian intensity profiles (core half-angle = beam/2; a second, wide Gaussian "skirt" where TISVA's Orrin data shows one), normalised so the integral equals the fixture lumens. LED strips: Lambertian line sources in 50 mm segments. Pendant globes: isotropic. Indirect (inter-reflected) light: room-cavity flux balance E_ind = Φ·ρ·f / (A·(1−ρ)) with the surfaces in § 10.2, area-weighted ρ = {R[F]['rho']:.2f}, enclosure factor f = 0.65 for the open east side and stair well; applied uniformly (×0.8 on vertical surfaces). Grid: 0.5 ft over the living, strip, passage, hall, flights and landing.

{grab("### Calibration", "### Lux at the important points")}

The fitted shapes reproduce TISVA's published beam averages within +9 to +15 % (model slightly brighter), so the Rega-class numbers below lean about 10 % high.

### 10.5 Results — lux grid

![FULL scene floor lux heatmap](lighting-plan/photometric/living-lux-heatmap-full.png)

![EVENING scene floor lux heatmap](lighting-plan/photometric/living-lux-heatmap-evening.png)

![Previous design, for comparison](lighting-plan/photometric/living-lux-heatmap-full-previous.png)

{grab("### Lux at the important points", "### Floor-grid statistics")}

{grab("### Floor-grid statistics", "### Sensitivity")}

**Brightest and darkest.** FULL: the brightest living cell is under the two Rega downlights in the south strip (≈ {r0(st[F]['max'])} lx; the accent-chair seat sees ≈ {r0(kv(F,chair))} lx because both fixtures hit it). The brightest *vertical* spot is the Avia pool on the stair feature wall (≈ {r0(kv(F,'Stair feature wall above flight 1 (x 23 ft, 2.6 m) — Avia pool'))} lx, a deliberate accent). Darkest living cells are the two north corners at ≈ {r0(kv(F,'NW corner floor'))} lx. EVENING: {r0(st[E]['min'])}–{r0(st[E]['max'])} lx across the room, seating {r0(kv(E,'N sofa, seat'))}–{r0(kv(E,coffee))} lx, corners ≈ {r0(kv(E,'NW corner floor'))} lx. MOVIE: {r0(st[M]['min'])}–{r0(st[M]['max'])} lx. NIGHT walk: passage {r0(kv(N,'Passage threshold, floor'))}, stair base {r0(kv(N,'Stair base (tread 1)'))}, seating {r0(kv(N,'N sofa, seat'))} lx, half landing {r0(kv(N,'Half landing centre'))} lx.

**Is the variation intentional?** Yes. A residential layered scheme is *supposed* to have a 2–3× range between the lit task pools (chairs, coffee table, stair wall) and the quiet edges; the min/avg uniformity of {st[F]['u_min_avg']:.2f}–{st[E]['u_min_avg']:.2f} in the two main scenes is high for a home (offices aim for ≥ 0.6 on the task area only) and comes from the large bounce component in the void. The min/max of {st[F]['u_min_max']:.2f} in FULL is driven by the deliberately strong reading pool over the accent chairs. NIGHT's {st[N]['u_min_avg']:.2f} is by design: the walkway and stairs are lit, the seating is not.

{grab("### Sensitivity", "### Beam angle")}

What the sensitivity table says: the two things nobody can verify yet (Rega Plus lumens and intensity shape) move the *chair pool* by ±10 % and the void seating by < 1 %; halving the indirect estimate still leaves ≈ {r0(kd(F,coffee,'pendant cluster')+kd(F,coffee,'S10 beam-edge profile')+kd(F,coffee,'S20 pelmet strip')+R[F]['indirect']/2)} lx at the coffee table in FULL. The accepted bulb change lifts the void seating by ≈ {r0(kv(F,coffee)-pkv(coffee))} lx and the mid-curtain by ≈ {r0(kv(F,'Curtain, 3.2 m')-pkv('Curtain, 3.2 m'))} lx; the accepted landing change takes the half landing from ≈ {r0(pkv('Half landing centre'))} lx to ≈ {r0(kv(F,'Half landing centre'))} lx. The conclusions do not hinge on the unknowns.

### 10.6 Vertical surfaces

| Surface | FULL | EVENING | Who lights it |
|---|---:|---:|---|
| TV screen centre (1.1 m) | ≈ {r0(kv(F,'TV screen centre (wall x=27, 1.1 m)'))} lx | ≈ {r0(kv(E,'TV screen centre (wall x=27, 1.1 m)'))} | F41 spill {r0(kd(F,'TV screen centre (wall x=27, 1.1 m)','F41'))}, pendant {r0(kd(F,'TV screen centre (wall x=27, 1.1 m)','pendant cluster'))}, beam line, bounce. In MOVIE {r0(kv(M,'TV screen centre (wall x=27, 1.1 m)'))} lx → no contrast loss. |
| TV feature panel, 2.5 m | ≈ {r0(kv(F,'TV feature panel, 2.5 m'))} lx | ≈ {r0(kv(E,'TV feature panel, 2.5 m'))} | **F41 24° head = {r0(kd(F,'TV feature panel, 2.5 m','F41'))} lx** at 5.3 m throw — a clear 1.7 m pool on the stone; pendant {r0(kd(F,'TV feature panel, 2.5 m','pendant cluster'))}. |
| TV feature panel, 4.5 m | ≈ {r0(kv(F,'TV feature panel, 4.5 m'))} lx | ≈ {r0(kv(E,'TV feature panel, 4.5 m'))} | pendant, tail of F41, pelmet spill, bounce. The upper third of the 20 ft panel reads darker than its middle — acceptable (eye is on the TV/console zone). |
| Curtain, 1.5 m (seated eye level) | ≈ {r0(kv(F,'Curtain, 1.5 m (eye level, seated view)'))} lx | ≈ {r0(kv(E,'Curtain, 1.5 m (eye level, seated view)'))} | pendant {r0(kd(F,'Curtain, 1.5 m (eye level, seated view)','pendant cluster'))} (it hangs 1.65 m from the curtain), **F42 60° head {r0(kd(F,'Curtain, 1.5 m (eye level, seated view)','F42'))}**, beam line, bounce. |
| Curtain, 3.2 m | ≈ {r0(kv(F,'Curtain, 3.2 m'))} lx | ≈ {r0(kv(E,'Curtain, 3.2 m'))} | pendant {r0(kd(F,'Curtain, 3.2 m','pendant cluster'))}, **F42 {r0(kd(F,'Curtain, 3.2 m','F42'))}**. |
| Curtain, 5.5 m (under the pelmet) | ≈ {r0(kv(F,'Curtain, 5.5 m (top, under pelmet)'))} lx | ≈ {r0(kv(E,'Curtain, 5.5 m (top, under pelmet)'))} | **S20 pelmet strip {r0(kd(F,'Curtain, 5.5 m (top, under pelmet)','S20 pelmet strip'))}**, F42 {r0(kd(F,'Curtain, 5.5 m (top, under pelmet)','F42'))}. |
| Stair feature wall (grooved plaster), 1.2 m above tread 6 | ≈ {r0(kv(F,'Stair feature wall (y=17.5), 1.2 m above tread 6'))} lx | ≈ {r0(kv(E,'Stair feature wall (y=17.5), 1.2 m above tread 6'))} | F37 Avia {r0(kd(F,'Stair feature wall (y=17.5), 1.2 m above tread 6','F37'))}, F40 {r0(kd(F,'Stair feature wall (y=17.5), 1.2 m above tread 6','F40'))}, pendant; plus the Spotlit foot-lights graze it strongly near each unit. |
| Stair feature wall above flight 1 — the Avia aim point (2.6 m) | ≈ {r0(kv(F,'Stair feature wall above flight 1 (x 23 ft, 2.6 m) — Avia pool'))} lx | ≈ {r0(kv(E,'Stair feature wall above flight 1 (x 23 ft, 2.6 m) — Avia pool'))} | **F37 Avia {r0(kd(F,'Stair feature wall above flight 1 (x 23 ft, 2.6 m) — Avia pool','F37'))} lx** — the accepted change turns the landing light into a wall accent. |
| Flight 2, living-facing side/riser face | ≈ {r0(kv(F,'Flight 2 riser face, mid (seen from living)'))} lx | ≈ {r0(kv(E,'Flight 2 riser face, mid (seen from living)'))} | pendant {r0(kd(F,'Flight 2 riser face, mid (seen from living)','pendant cluster'))}, **beam line {r0(kd(F,'Flight 2 riser face, mid (seen from living)','S10 beam-edge profile'))}**, F40 {r0(kd(F,'Flight 2 riser face, mid (seen from living)','F40'))} — the stair reads as a lit sculpture from the sofa, mostly from the void frame and pendant, not from the spot. |

How the track spots and the void frame contribute: the three Axios heads are the only sources that put *directional* light on the vertical surfaces ({r0(kd(F,'TV feature panel, 2.5 m','F41'))} lx on the TV panel, {r0(kd(F,'Curtain, 3.2 m','F42'))} lx on the mid-curtain, ≈ 50 lx raking across the upper treads); the beam-edge profile is a 6.3 m, ≈ 3,900 lm line of soft light at 11 ft that gives ≈ {r0(R[F]['e10'])} lx on the floor directly below it (≈ 95 for an endless line; the 5 m length loses the tails), 30–50 lx everywhere in the void, and 100+ lx on the stair's living-facing face, i.e. it behaves like four hidden downlights spread into a line. The pelmet strip lights only the top ≈ 1 m of curtain ({r0(kd(F,'Curtain, 5.5 m (top, under pelmet)','S20 pelmet strip'))} lx at 5.5 m, {r0(kd(F,'Curtain, 3.2 m','S20 pelmet strip'))} lx at 3.2 m) because a strip parallel to a plane 76 mm away reaches it at grazing incidence (cos i → 0); tilting the profile toward the fabric was tested and does not change the 3.2 m value (§ 10.5). The curtain's visible glow below the header therefore comes from the pendant and the 60° head, and from pleat ridges catching the grazing light (not captured by a plane-illuminance model).

### 10.7 Distance and the inverse-square law

{grab("### Inverse-square", "### Fixture")}

Why: illuminance from a small source falls with the *square* of distance because the same candela spreads over an area that grows with d². Going from 9 ft to 21 ft is 2.3× the distance → 1/5.4 of the lux (18 %) and a footprint 5.4× larger in area. So a downlight recessed in the void lid would deliver about 40 lx in a 4.4 m pool per 900 lm fixture; matching the 225 lx a 9 ft fixture gives would take five or six of them, 21 ft up, with the LED visible from every seat. That is the quantitative reason the void is lit from the pendant (sources at 2.6–5.3 m), the beam edge (3.35 m) and the wall-wash heads (3.15 m) instead.

Limits of the rule: (1) it is exact only for a point source; a fixture is "point-like" beyond about five times its own size (Rega Ø 90 mm → fine past 0.5 m; a 6.3 m LED line is *not* a point — its illuminance falls roughly with 1/d near the line and only approaches 1/d² far away, which is why the strip is a stronger ambient source than its 630 lm/m suggests); (2) real reflectors and lenses make intensity depend on angle, so off-axis points get I(α), not the on-axis candela — the cos i term matters as much as d² for the wall-aimed heads (incidence 79° on the treads from F40 leaves only 50 lx of 3,000 cd); (3) inter-reflection adds a near-uniform floor ({r0(R[F]['indirect'])} lx in FULL here) that the direct formula ignores; (4) lumen depreciation and dirt remove 15–25 % over years.

### 10.8 Beam angle

{grab("### Beam angle", "### Inverse-square")}

The footprint is Ø = 2·d·tan(θ/2): doubling the distance doubles the diameter and quarters the lux. 15° is a torch for a basin, idols or a painting; 24° carries a usable pool over 4–5 m (the TV panel from the east beam); 36–38° is the general downlight class (a 1.8 m pool from a 9 ft ceiling, which sets the ≈ 1.2–1.8 m spacing rule); 60° washes a 3–4 m-wide surface from mid distance (the curtain head); 120° is a spread with no visible pool (foot-lights, panels). The beam angle is a property of the optic: the same 1600 lm Axios head has 7,400 cd on axis with the 24° lens and 1,250 cd with the 60° lens. When ordering the three Axios heads, the optic must be stated: **F40 stair 38°, F41 TV panel 24°, F42 curtain 60°** (accepted 2026-10-02).

### 10.9 Living-room conclusions

- **A. Sufficient for comfortable living?** Yes. In FULL the whole seating zone sits at ≈ {r0(kv(F,'N sofa, seat'))}–{r0(kv(F,coffee))} lx (centre {r0(kv(F,'Living centre (void), floor'))}, coffee table {r0(kv(F,coffee))}, sofa {r0(kv(F,'N sofa, seat'))}–{r0(kv(F,sofa))}, return {r0(kv(F,'E return sofa, seat'))}), the corners at ≈ {r0(kv(F,'NW corner floor'))} lx; EVENING gives {r0(kv(E,'N sofa, seat'))}–{r0(kv(E,coffee))} lx at the seats with ≈ {r0(kv(E,'NW corner floor'))} lx corners; MOVIE {r0(st[M]['min'])}–{r0(st[M]['max'])} lx. Sustained reading on the sofa (300 lx on the page) is met by the table/floor lamp, as intended in a layered scheme, not by the ceiling.
- **B. Is 100–150 lx a reasonable ambient target?** Yes, as the *relaxed-ambient* level. The dimmable layers span it: FULL lands above it, EVENING (as defined) below it, and a "guests" setting of coves ≈ 70 % + pendant ≈ 50 % + track on lands inside it. Keep 100–150 as the target for the default evening-with-guests scene, 50–80 for lounging, 200+ for cleaning/bright.
- **C. Whole floor or selected areas?** Selected areas. Treat it as the target on the seating/coffee-table plane; the floor at the edges should be lower (here ≈ 60 % of centre), otherwise the room loses its hierarchy and the void reads flat. Uniformity 0.4–0.6 is right for a home.
- **D. Are the two Rega Plus 12 W in the south strip sufficient?** Yes — more than: they put ≈ 360 lx direct on the accent-chair seats (≈ {r0(kv(F,chair))} lx total), a proper reading pool, and {r0(kv(F,'Passage threshold, floor'))} lx at the passage threshold. They are not meant to light the void and do not (≈ 20 lx at the coffee table). If the FULL scene feels harsh there, the 7 W version (`806DLR733892`) would give ≈ 350 lx at the seat; a dimmable alternative is Orrin 7.5 W DIM with a Zigbee TRIAC dimmer. Not changed.
- **E. Add general downlights to the 21 ft void?** No. Per § 10.7 each would add ≈ 40 lx in a 4.4 m pool, be visible from every seat, and need a scaffold to clean; the void already reaches {r0(kv(F,'N sofa, seat'))}–{r0(kv(F,coffee))} lx in FULL without them.
- **F. If more light is ever wanted, what works best?** In order: (1) the pendant bulbs at full (already the 806 lm class); (2) the beam-edge line at 100 % (it is on a dimmer); (3) a fourth Axios head 24° aimed at the coffee table for a games/reading scene — but it adds ≈ 350 lx in a 1.7 m pool ({r0(next(k['total'] for k in R['sensitivity']['(rejected) + 4th Axios head 24° aimed at the coffee table']['keys'] if k['name']==coffee))} lx total), too much for everyday, so only as a switchable extra; (4) wall washing (the three heads) — raises *perceived* brightness most per watt because the eye reads vertical surfaces; (5) more downlights — the worst option here.
- **G. Glare risks.** (1) **Resolved:** the earlier Bolt 12 W over the half landing (≈ 925 lx direct, a bare 900 lm COB 1.4 m above a climber's head) is replaced by the Avia 7 W aimed at the stair wall; the landing now sits at ≈ {r0(kv(F,'Half landing centre'))} lx from the wall pool, the foot-light and bounce, and the LED points away from the climber. (2) F42 (60°) is aimed at the curtain above the N sofa; its aperture is in the periphery of someone on that sofa at ≈ 35–40° above the eye line — keep the aim point at ≥ 2.4 m on the curtain and keep the 60° (lowest-intensity) optic; ask for a honeycomb louvre if TISVA offers one for Axios. (3) The two Rega over the chairs are deep-recessed black-reflector units (the Orrin-class cut-off is > 40°): low glare, bright pool. (4) Pendant globes: ≈ 2,700 cd/m² luminance with 806 lm bulbs in Ø 150 mm opal globes — comfortable (opal globes get uncomfortable above ≈ 5,000); use Ø 150–200 mm globes, not smaller. (5) Beam-edge profile: a thin 10 W/m line in a 20 mm opal profile is ≈ 10,000 cd/m² — bright if stared at; use a 30 mm-wide profile and run it at 60–70 % normally. (6) TV: {r0(kv(F,'TV screen centre (wall x=27, 1.1 m)'))} lx vertical on the screen in FULL would wash out dark scenes — but MOVIE drops it to {r0(kv(M,'TV screen centre (wall x=27, 1.1 m)'))} lx, as designed.
- **H. Dark zones?** None in FULL/EVENING: the darkest living cells (north corners) are ≈ 60 % of the centre. NIGHT deliberately leaves the seating at {r0(kv(N,'N sofa, seat'))} lx while the walkway and stairs are at 80–120.

### 10.10 Limitations

No IES/LDT file exists for any TISVA product; Rega Plus, Avia, Lumelace and Spotlit lumens are estimates (basis in § 10.3) and Rega's intensity shape is borrowed from Orrin; Axios has documented lumens but an assumed Gaussian shape; smart-bulb globe transmission assumed; furniture shadows, people and the sofa itself are ignored (floor under the sofa is irrelevant); the indirect term is a single-number cavity estimate (±40 %) applied uniformly; vertical-surface indirect factor 0.8 assumed; no maintenance factor (×0.8 after 5 years); no daylight (the 8 ft double-height window dominates by day); the pelmet model is a plane-illuminance model and under-represents the visible glow on pleated fabric; positions of coffee table, sofas and chairs are from the furniture plan and may move.

### 10.11 Changes from this check

**Accepted 2026-10-02 and applied to the design, the map and the buy list:**
1. **F37 half landing: Bolt 12 W → Avia 7 W black surface spot (`806DLA7338992`, ₹850) aimed at the stair feature wall** above the upper treads of flight 1 (aim point ≈ 2.6 m above GF floor). Landing ≈ {r0(pkv('Half landing centre'))} → ≈ {r0(kv(F,'Half landing centre'))} lx; wall pool ≈ {r0(kd(F,'Stair feature wall above flight 1 (x 23 ft, 2.6 m) — Avia pool','F37'))} lx; saves ₹1,100.
2. **Pendant bulbs: 806 lm class, tunable white set to 3000 K** (Philips Hue White Ambiance E27 or IKEA Trådfri E27 806 lm class; ~12 for the living cluster). +{r0(kv(F,coffee)-pkv(coffee))} lx at the coffee table, +{r0(kv(F,'Curtain, 3.2 m')-pkv('Curtain, 3.2 m'))} lx on the mid-curtain.
3. **Axios optics specified for ordering: F40 38°, F41 24°, F42 60°**, F42 aim point ≥ 2.4 m on the curtain.

**Kept as installation guidance:** pelmet strip = header glow only (top ≈ 1 m of curtain), mounted 150 mm off the fabric; beam-edge profile 30 mm opal, dimmer default 60–70 %. **Rejected:** a fourth track head on the coffee table (too much); downlights in the void lid (§ 10.7); swapping the strip downlights to 7 W (fine either way; 12 W kept for the reading pool). **Still to ask the TISVA dealer for:** Rega Plus datasheet or IES (lumens, beam, polar), Avia lumens/beam, Lumelace lm/m and CRI, Axios polar — then re-run the script with the new numbers in `P`/`SHAPES` and the verification becomes "full".

### 10.12 Which numbers are which

- **Measured:** none — no site measurement exists yet.
- **From TISVA documentation:** Axios Pro 20 W = 1600 lm, 15/24/38/60° optics, CRI>80, 25.5 cm body (Architectural Catalogue 2023 p.59); Orrin 7.5/13/20 W lumens, polar curves and illuminance tables (p.37–40) and Fugl on-axis lux (p.31–32) used for calibration; Lumelace 10 W/m 24 V 3000 K IP20 (p.75, no lumens); Rega Plus and Avia wattage/CCT/finish/CRI>90, Spotlit 120° (Product list May-25).
- **Calculated:** every lux value, candela peak, footprint, uniformity, indirect term, in `results.json`/`tables.md` (script above).
- **Estimated:** Rega Plus lumens (900/520) and 38° beam; Rega intensity shape (fitted to Orrin); Avia 520 lm / 36°; Lumelace 630 lm/m effective; Spotlit 140 lm; smart-bulb globe transmission 0.75; floor-lamp output; all reflectances and the 0.65 enclosure factor; the 0.91 Gaussian peak factor; coffee-table/sofa positions.

### 10.13 Verify on site (₹1,500 lux meter or a phone app, after dark, curtains drawn)

Measure at: coffee-table top, N sofa seat, accent-chair seat, floor under the TV, half landing, stair base; in FULL and EVENING. Expected (model): {r0(kv(F,coffee))} / {r0(kv(F,'N sofa, seat'))} / {r0(kv(F,chair))} / {r0(kv(F,'TV viewing area, floor (W side)'))} / {r0(kv(F,'Half landing centre'))} / {r0(kv(F,'Stair base (tread 1)'))} lx and {r0(kv(E,coffee))} / {r0(kv(E,'N sofa, seat'))} / {r0(kv(E,chair))} / {r0(kv(E,'TV viewing area, floor (W side)'))} / {r0(kv(E,'Half landing centre'))} / {r0(kv(E,'Stair base (tread 1)'))} lx. If readings are within ±30 % the model is confirmed; set the EVENING and GUESTS scene levels from the meter, not from the model.

![N–S section through the void](lighting-plan/photometric/living-section.svg)

{grab("### Fixture", "### Indirect-light budget")}

{grab("### Indirect-light budget")}
"""

doc = DOC.read_text(encoding="utf-8")
i = doc.index("## 10. Photometric Verification")
doc = doc[:i] + section.rstrip() + "\n"
DOC.write_text(doc, encoding="utf-8")
print("§10 regenerated:", len(section)//1024, "KB")
