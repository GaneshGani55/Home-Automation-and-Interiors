# Project guide for agents

Two-storey home **interior + automation** project. Start a session by reading `PROJECT_CONTEXT.md` and `README.md`. Treat handwritten floor plans as canonical (see `floor-plans/`). Log every locked decision in `decisions/decision-log.md`.

## ⚠️ Keep the conduit map in sync (it is a downstream view)

`conduit-map/` is an **interactive conduit map handed to the on-site electrician** (hosted on GitHub Pages + an offline copy). It **duplicates** data from `electrical/*.md` and `automation-iot/*.md` so it can run offline on a phone — so it does **not** update itself when those docs change.

**Whenever you change any of the following, update the map in the *same* change:**
- a conduit run (route / contents / size / status),
- a device or hardware choice (server, cameras, router, Sonoff, panels, sump/Sintex ESP32, etc.),
- an automation / sensor decision (mmWave, floats, presence, etc.),
- a position or routing on a floor.

**Steps:**
1. Edit the matching data in `conduit-map/app.js` — conduit text → `CONDUITS`; device/hardware blurbs → `GUIDES`; endpoint positions → `CO`; sensors → `MMWAVE`; rooms → `ROOMS`/`ENV`.
2. `node --check conduit-map/app.js` → `python3 conduit-map/build_offline.py`.
3. Commit + push `conduit-map/` (GitHub Pages redeploys in ~1 min).

**Before editing the map, read [`conduit-map/README.md`](conduit-map/README.md)** — it has the full data schema, edit recipes, the source-of-truth doc mapping, and the deploy flow.

**Worked example:** deciding to swap the Beelink server for a custom-build PC means updating `electrical/materials-checklist.md` §8 + `decisions/decision-log.md` **and** the ~5 `Beelink` mentions in `conduit-map/app.js` (the Server guide's *inside*/*steps*, the Waveshare guide's *power*/*steps*, conduit D5's *explain*), then rebuild + redeploy.

> If the map and a source doc ever disagree, the source doc wins — fix the map to match.
