# Conduit Map — how it works & how to edit

An interactive, mobile-first **conduit map** for the on-site electrician. It draws the Ground Floor, First Floor, a vertical Riser cross-section and the Terrace as line-art SVG, with the **automation / low-voltage / water / data** conduits drawn on top. Tap a line for its detail; tap a dark **component box** for a step-by-step install guide.

> **This file is for whoever maintains the map next — a person or another AI model/session.** Read it before editing. The map is a *view*; the real decisions live in the `electrical/` + `automation-iot/` docs (see [§7 Source of truth](#7-source-of-truth--keep-them-in-sync)).

---

## 1. Who it's for & what it shows
- Audience: a **non-tech-savvy electrician** in Chitradurga who ignored long PDFs. Everything is visual-first, detail-on-tap.
- Scope: **automation-focused.** All conduits are present, but it opens pre-filtered to the automation services (data, LV-16, water, presence) + components. The plain lighting/socket power runs are one tap away.
- Orientation (critical, drawn this way on purpose): **TOP = South, BOTTOM = North (main door), LEFT = East, RIGHT = West.** A compass shows it on every plan.

## 2. Files & how it's served
```
conduit-map/
├── index.html              ← shell: top bar, panels, ALL CSS, SVG container. Loads app.js.
├── app.js                  ← EVERYTHING: data + drawing + interaction. ~900 lines. Edit here.
├── assets/
│   ├── img/                ← reference images shown inside install guides (.jpg)
│   └── pdf/                ← full PDFs linked from guides
├── conduit-map-offline.html ← GENERATED single-file copy (images inlined as base64). Do not hand-edit.
├── build_offline.py        ← regenerates conduit-map-offline.html
└── README.md               ← this file
```
- **Hosted (primary):** GitHub Pages → `https://ganeshgani55.github.io/Home-Automation-and-Interiors/conduit-map/` (repo `GaneshGani55/Home-Automation-and-Interiors`, branch `main`, pushing to `conduit-map/` auto-rebuilds Pages in ~1 min).
- **Offline (backup):** `conduit-map-offline.html` is fully self-contained — AirDrop/WhatsApp it; it works with no internet on site.

## 3. The golden rule for editing
**Almost every change is a data edit in `app.js`.** The drawing/interaction code rarely needs touching. Find the right `const` (see §5), change the data, then [rebuild + deploy](#8-rebuild--deploy). Run `node --check app.js` after every edit.

## 4. Coordinate system
- SVG `viewBox` is `0 0 1000 1085`. All `[x, y]` are in these units.
- Because of the orientation: **smaller y = South (top), larger y = North (bottom); smaller x = East (left), larger x = West (right).**
- "Move it north" = increase `y`. "Move it west" = increase `x`.

## 5. Data model (every `const` in `app.js`)
| Const | What it is | Shape |
|---|---|---|
| `SVC` | service types → colour + PVC label | `{ key: {label, color, pvc} }` |
| `SVC_ORDER` | order of the filter chips | array of `SVC` keys |
| `DEFAULT_ACTIVE` | which layers are ON at load | array of keys (+ `"components"`) |
| `CONDUITS` | **the conduit list** | see schema below |
| `HUB` / `NODE` | named origin points (Server, DB, DB cupboard, Riser, Foyer panel, etc.) | `{ NAME: [x,y] }` |
| `CO` | screen coordinates per conduit ref | `{ ref: {o,d,via?} }` |
| `MMWAVE` | mmWave presence sensors (markers only, no conduit) | see schema |
| `DEVICES` | the dark **component boxes** that open guides | `{id, floor, svc, label, xy}` |
| `GUIDES` | the step-by-step install guides | keyed by device `id`, see schema |
| `ROOMS` / `ENV` / `VOID_FF` | room rectangles + outer wall outline + the FF void | geometry |
| `RISER_BUNDLES` | the bundles shown on the Riser tab | `{n, svc, top, txt}` |
| `drawTerrace()` | the Terrace tab is **hand-drawn** in this function, not data-driven | edit inline |

**`CONDUITS` entry:**
```js
{ ref:"D1", floor:"GF",          // floor: "GF" | "FF"
  service:"data",                 // a key in SVC
  size:"25mm", status:"live",     // status: "live" (solid) | "provision" (dashed, pull-string)
  from:"Server", to:"Foyer screen cavity ...",
  contents:"1x indoor Cat6 (UTP)",
  note:"short site note",
  explain:"WHY it exists / what connects where / can it reuse a conduit" }
```
Every conduit also needs an entry in **`CO`**: `{ o:HUB.X (or [x,y]), d:[x,y], via?:[[x,y],...] }`. `o`=origin, `d`=destination (the dot + ref label land at `d`). `via` is optional explicit waypoints used to **hug the wall boundary** (e.g. the Sintex float `W2`).

**`DEVICES` entry:** `{ id:"NICHE-SERVER", floor:"GF"|"FF"|"TERRACE", svc:"data", label:"Server", xy:[x,y] }`. The `id` must match a `GUIDES` key.

**`GUIDES` entry (the install guide):**
```js
"NICHE-SERVER": {
  title, sub, glyph, svc,         // svc picks the icon colour
  badge:"Pull cable now",
  inside:[ ... ],                 // what's in the box (bullet list)
  power:"how it's powered",
  mount:"how/where it mounts",
  sensor:"sensor/wiring detail",  // optional
  steps:[ ... ],                  // ordered step-by-step
  imgs:["jb-internals.jpg"],      // files in assets/img/
  pdf:"WATER_AUTOMATION.pdf",     // file in assets/pdf/
  related:["W3","W4"]             // conduit refs — tappable, flash on the plan
}
```

## 6. Common edit recipes

### A. Change a device's hardware — *the Beelink → custom PC example*
The decision "swap the Beelink EQ12 for a custom-build PC" must show up here. Hardware names are **prose inside the guides**, so:
1. In `app.js`, search **`Beelink`** — it appears in ~5 spots: `GUIDES["NICHE-SERVER"].inside` and `.steps`, `GUIDES["WAVESHARE-STAIR"].power` and `.steps`, and `CONDUITS` D5 `.explain`. Replace the model text (e.g. `"Beelink EQ12 mini-PC — Home Assistant + Frigate NVR + CompreFace"` → `"Custom mini-ITX PC (Intel ___, 16GB) — Home Assistant + Frigate + CompreFace"`). Keep the *role* description.
2. Update the BOM: **`electrical/materials-checklist.md` § 8 (Server / Home Hub)**.
3. Log it: add a dated line to **`decisions/decision-log.md`**.
4. `node --check app.js`, then [rebuild + deploy](#8-rebuild--deploy).
> Same pattern for any device (cameras, router, Sonoff, panels, sump/Sintex ESP32, etc.): the user-facing text is in `GUIDES` / `CONDUITS`; the canonical spec is in the matching `electrical/*.md`. Update **both**.

### B. Edit an existing conduit (route text, contents, note)
Find it in `CONDUITS` by `ref`, edit the fields. No `CO` change unless you're moving it.

### C. Move where a conduit ends on the plan
Edit `CO[ref].d` (and/or `.o`). Use [§4](#4-coordinate-system) for direction. To make a run follow the walls, add `via:[[x,y],...]`.

### D. Add a new conduit
Add an entry to `CONDUITS` **and** a matching `CO[ref]`. If it should open a guide, add the ref to some `GUIDES[...].related`.

### E. Add a component box + its install guide
Add to `DEVICES` (give it an `id`, `floor`, `svc`, `label`, `xy`) and add a `GUIDES[id]` with the same id. Drop any images into `assets/img/` and reference them in `imgs`.

### F. Add an mmWave sensor / change its spot
Add/edit `MMWAVE` (it draws a radar marker; no conduit line — these are wired-5V per the electrician).

### G. Recolour or rename a service / add a new service type
Edit `SVC` (and `SVC_ORDER` / `DEFAULT_ACTIVE` if it's a new key).

## 7. Source of truth — keep them in sync
The map **duplicates** data from the project docs so it can stand alone on a phone. When a decision changes, update the map **and** its source doc **and** the decision log:
| Map area | Canonical source doc |
|---|---|
| All conduit runs | `electrical/conduits-and-cavities.md` |
| Foyer welcome system | `electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md` |
| Water JBs / sump / Sintex / floats / starters | `electrical/water-automation-conduits.md` |
| Waveshare panels | `electrical/WAVESHARE_INDOOR_PANEL.md` |
| Hardware / BOM (server, cameras, Sonoff, router) | `electrical/materials-checklist.md` |
| mmWave presence sensors | `automation-iot/mmwave-presence-sensors.md` |
| Every locked decision (dated) | `decisions/decision-log.md` |

## 8. Rebuild & deploy
```bash
cd conduit-map
node --check app.js                 # 1. must print nothing / exit 0
python3 build_offline.py            # 2. regenerate the offline single-file copy
cd ..
git add conduit-map                 # 3. stage ONLY this folder
git commit -m "Conduit map: <what changed>"
git push origin main                # 4. GitHub Pages auto-rebuilds (~1 min)
```
Then load the Pages URL (hard-refresh) to confirm. To preview locally: `python3 -m http.server` inside `conduit-map/` and open `index.html`.

## 9. Conventions & gotchas
- **Filter model:** chips **toggle** (multi-select — e.g. Data + Water). Presets: **Automation** / **All** / **None** (None = bare floor plan). **Components** is its own independent layer (so you can view Data wiring without the boxes).
- **Don't rename the code identifiers** `HUB.NICHE`, the device id `NICHE-SERVER`, or the GUIDES key `"NICHE-SERVER"` — they're internal wiring. The *visible* word is already "Server" everywhere; "niche" was removed because it confused the electrician.
- **"Fridge alcove"** is a real room recess — not the server. Don't auto-replace it with "Server".
- Conduit IDs on the map read `C-Server-*`; the older PDFs still say `C-Niche-*`. Same runs — update the master docs when convenient.
- Don't hand-edit `conduit-map-offline.html` (it's generated). Don't commit unrelated files — stage `conduit-map` only.
- After any data edit, **re-run `build_offline.py`** so the offline copy doesn't drift from the hosted one.
