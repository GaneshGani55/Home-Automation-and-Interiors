# Waveshare Indoor Control Panels — Hardware + Mount Spec (v3.1)

**Scope:**
- **Screen 1 — Staircase South wall**, screen centered at **1500 mm FFL**, vertically aligned above the existing 2M light-switch box (~200 mm clear gap between switch and screen cavity) — fully designed below
- **Screen 2 — Dining hall E wall**, mounted on plywood under cantilever shelves (position + height defer to interior designer) — cable + back box provision only
**Architecture (hybrid, locked 2026-05-25 v3.0):**
- Staircase = **Beelink-direct** (HDMI + USB cables through existing 25 mm conduit, no Pi at panel)
- Dining = **Pi-at-screen, wired** (single Cat6 PoE, matching foyer welcome system pattern)
**Document version:** 3.1 — 2026-05-29 (v3.1 = cavity dims corrected + 1280×800 variant locked; v3.0 was hybrid architecture; v2.0 was Beelink-direct everywhere; v1.0 was Pi-5 thin client)
**Project:** Ganesh Prasad Home, Chitradurga

> **v3.1 correction (2026-05-29):** v2.0/v3.0 spec called for a "75×75 mm back box" at the staircase Waveshare position. **This was wrong** — a standard modular box is far too small to hold the 257.6 × 169.7 mm screen. v3.1 corrects this to a **custom 280 × 195 × 80 mm masonry cavity** (similar to the foyer Samsung monitor cavity, scaled smaller). Wall thickness is 9" (230 mm) → 150 mm of solid wall remains behind the cavity. Confirmed by homeowner: no back box was actually installed pre-plaster at this position; the cavity is a fresh masonry chase.

---

## SECTION 1 — Cheat sheet (read this before anything else)

| Trade | Job for Screen 1 (staircase) | Job for Screen 2 (dining hall provision only) |
|---|---|---|
| **Mason** | Chase a **280 × 195 × 80 mm rectangular cavity** in the 9" staircase South wall, **centered at 1500 mm FFL**, vertically aligned above the existing 2M light-switch box (~200 mm clear gap). Conduit `C-Niche-Waveshare` enters the cavity through a ~30 mm hole at the bottom of the cavity. Smooth-finish the cavity interior. | No masonry work on dining wall — back box only (see electrician row). |
| **Electrician** | Pull 1× HDMI cable + 1× USB cable through existing `C-Niche-Waveshare` conduit alongside the Cat6 (~30 min, tape new cables to existing Cat6 as pull guide). Cable ends terminate inside the new wall cavity with 200 mm service loop coiled. | Lay 1× new conduit `C-Niche-Dining` (25mm GREY) from niche → dining hall E wall via ceiling run (**~12m / 35-40 ft per electrician walk**). Pull **1× Cat6** + 1× pull-string for future Pi-at-screen install (architecture matches foyer welcome system). Cap back box on dining wall — **position + height defer to interior designer** (cantilever shelf mount). |
| **Carpenter** | Build recessed walnut bezel frame to suit the cavity (**~320 × 235 mm external**, 220 × 140 mm internal window for screen, 20-25 mm overhang on all four sides hides the masonry cut edge), magnetic-catch service hatch, vent slots top + bottom. **Wood: walnut recommended for foyer-shelf continuity, but carpenter's choice based on availability** (teak, sheesham, rubberwood all acceptable). | No carpentry needed yet — just an empty back box; future dining mount will be IDR plywood under cantilever shelf. |
| **Homeowner** | Mount Waveshare 10.1" HDMI screen (1280×800, with case) into carpenter sub-frame; plug HDMI + USB into Beelink HDMI 2 + USB-A; configure Beelink to run Chromium kiosk on HDMI-2 (one-time Linux setup, ~half a day). Stick NFC tags around house. | Pick exact wall position + screen height with interior designer once cantilever shelf design is finalised. |

**One-line summary:** Two cables (HDMI + USB) from Beelink in the niche carry image + touch directly to the screen. Beelink runs a second Chromium kiosk session on its 2nd HDMI output. No new computer; existing Beelink does everything.

---

## SECTION 2 — Architecture decision record (why no Pi)

| | v1.0 Plan (Pi 5 thin client) | v2.0 Plan (Beelink-direct) |
|---|---|---|
| Computer at screen | Raspberry Pi 5 (4 GB) | None — just a screen |
| Power to screen | PoE over Cat6 → PoE HAT → Pi → screen | USB-A from Beelink supplies 5V/600mA for screen + touch |
| Cable from niche to screen | 1× Cat6 (PoE) | 1× HDMI + 1× USB-A (+ existing Cat6 stays as spare) |
| Hardware cost | ~₹29,150 | ~₹14,850 |
| Software complexity | Pi runs Chromium kiosk pointing at HA on Beelink | Beelink runs Chromium kiosk on its 2nd HDMI output |
| Failure modes | Pi can fail independently; Beelink crash → Pi shows "reconnecting…" | Beelink crash → screen goes black for ~90s during boot |
| Scales to 2-3 screens | Same complexity per screen | 2 screens easy (Beelink has 2 HDMI); 3+ painful (port limits) |
| Right call for 1-2 screens? | **Over-engineered** | **Right-sized** |

**Decision:** For 2 screens (staircase + future dining), Beelink-direct wins. If you ever genuinely need 3+ screens, migrate that single screen to a Pi thin-client at that time — the rest of the setup doesn't change.

---

## SECTION 3 — Screen 1 (staircase) bill of materials

All parts ordered by homeowner.

| # | Part | Model / spec | Vendor (India) | Cost (₹) |
|---|---|---|---|---|
| 1 | Touchscreen | **Waveshare 10.1inch HDMI LCD (B), with case** — 1280×800 IPS, 10-pt capacitive touch, HDMI in, micro-USB for touch + 5V power, includes back case. **Outline 257.6 × 169.7 × 22 mm**, active display 218.8 × 137.6 mm, ~600g. Confirmed locked **2026-05-29** (vs 1024×600 variant — chose 1280×800 for crisper dashboard text). | Robu.in (~₹11,750) / ElectroPi (~₹9,946) / Amazon.in (~₹10,000) | 9,946-11,752 |
| 2 | HDMI cable | **Slim flat HDMI 2.0**, 3 m, ~4 mm thick (fits inside 25 mm conduit alongside existing Cat6) | Amazon.in / Robu.in | 400 |
| 3 | USB-A to micro-USB cable | 3 m, certified data + power (touch + 5V for screen flow over this) | Amazon.in | 250 |
| 4 | NFC reader | **USB ACR122U** — plug-and-play in Linux via `pcscd` + `libnfc`. Mounts behind walnut bezel. | Amazon.in / Robu.in | 1,500 |
| 5 | NFC tags | **NTAG215 sticker tags, pack of 10** | Amazon.in | 250 |
| 6 | Mount frame | Recessed bezel + sub-frame with 4-magnet service hatch + vent slots, **premium hardwood — walnut recommended for foyer-shelf continuity, but carpenter's choice based on availability** (see § 5) | Local carpenter | 1,500-2,500 |
| 7 | USB extension (optional) | 2 m USB-A passive extension if cable run + Beelink port distance exceeds 5 m total. Likely not needed. | Amazon.in | 150 |
| 8 | Cabling kit | Velcro cable ties, heat-shrink, RJ45 plug to terminate the now-spare Cat6 | Local | 200 |
| | **Subtotal — Screen 1** | | | **~16,750** |

> **Why HDMI screen (not DSI like v1.0):** DSI is a Pi-only connector. Since Beelink uses standard HDMI, we need the HDMI variant of the same Waveshare panel. Same size, same resolution, same touch — different connector on the back. ~₹1,500 cheaper than the DSI version, because Pi-specific accessories are removed.

> **Why ACR122U USB NFC (not PN532 over I2C like v1.0):** I2C requires GPIO pins, which require a Pi. Since there's no Pi here, USB is the only option. ACR122U is the standard Linux-supported USB NFC reader.

---

## SECTION 4 — Screen 2 (dining hall) provision spec

This is **cable + back box only**. No screen, no carpentry today. Just keeps the option open for ~₹500.

### 4.1 — What gets installed now

| Item | Spec |
|---|---|
| Conduit ID | `C-Niche-Dining` |
| Conduit type | 25 mm GREY PVC (LV-25) — same colour family as other data conduits |
| Route | Staircase niche (GF) → vertical up niche wall → at GF slab level branch east through ceiling chase (long horizontal run across kitchen/dining ceiling) → drop down into dining hall E wall → terminate at back box |
| Length | **~12 m / 35-40 feet total** (per electrician's site walk; longer than initial estimate due to ceiling-route distance) |
| Cable pulled | **1× indoor Cat6** (cap both ends) + **1× pull-string** for future supplementary pulls. **Architecture refined 2026-05-25 v3.0: dining screen will use Pi-at-screen pattern (matching foyer welcome system) — single Cat6 carries both PoE power and Ethernet data to a small Pi behind the screen. No HDMI extender needed.** |
| Back box | Standard 3" × 3" × 2½" GI MS modular box, recessed in dining E wall |
| Height of back box | **Defer to interior designer** — homeowner is planning to mount the screen on plywood attached to cantilever kitchen shelves; final height + exact wall position determined by interior designer's shelf design |
| Position on wall | **E wall of dining hall, near breakfast counter / kitchen-dining partition** (confirmed 2026-05-25). Exact mounting point under cantilever shelf TBD by interior designer. |
| Cap | Back box covered with a blank plate matching house switch finish until screen is installed |

### 4.2 — Decision deferred to on-site discussion

When the electrician arrives to pull this cable (target: before plaster on 2026-05-30), homeowner walks the dining hall with him and chalk-marks:

1. **Wall section** — confirm the E side has a solid masonry section long enough to host a back box (vs an open arch / window / door)
2. **Height** — final FFL based on dining table sightline + future buffet/sideboard plan
3. **Pull-string slack** — leave 500 mm of slack inside the back box so the exact box position can shift by ±300 mm later without re-pulling

### 4.3 — When the dining screen is actually installed (future, separate session)

**Architecture: Pi-at-screen, wired (matching foyer welcome system pattern).** A small Pi sits behind the screen, gets both PoE power and Ethernet data through the single Cat6 from the niche, renders the HA dashboard locally, drives the Waveshare via short HDMI cable. No long-distance signal extenders.

Hardware needed at that time (NOT ordered today):

| Item | Cost (₹) |
|---|---|
| Waveshare 10.1" HDMI LCD (B), with case | 11,500 |
| Raspberry Pi (Zero 2W ~₹2,000 OR Pi 4 (2GB) ~₹4,500 — pick at install time based on performance need) | 2,000-4,500 |
| **PoE HAT (for Pi 4) OR PoE-to-USB-C splitter with Ethernet passthrough (for Pi Zero 2W)** | 1,500-2,200 |
| microSD 32 GB (SanDisk Extreme A2) | 500 |
| Short HDMI cable (Pi to screen, ~30cm) + short USB cable (touch from screen to Pi, ~30cm) | 400 |
| Interior-designer-built plywood mount under cantilever shelf (carpenter framework provided by IDR, not separate spec) | included in IDR scope |
| **Subtotal — Screen 2 (when installed)** | **~16,000-19,100** |

But again: **none of that is ordered today.** Today we just lay the conduit + 1 Cat6 cable.

**Pi-at-dining vs Beelink-direct-at-staircase — why two different architectures:**
- **Staircase (~2m run, conduit already done):** Beelink can drive HDMI + USB cables directly. Saves Pi cost. Wired HDMI is rock-solid at 2m.
- **Dining (~12m run):** Beelink-direct would need HDMI-over-Cat6 extender chain (₹5K extra, finicky). Pi-at-screen with single Cat6 PoE is cheaper AND more reliable. Also matches foyer welcome system pattern for architectural consistency at the longer-distance panels.

---

## SECTION 5 — Mount frame for Screen 1 (carpenter spec)

Carried over largely unchanged from v1.0. The mount design is independent of what's behind the screen.

### 5.1 — Material and finish

- **Wood choice: carpenter's discretion**, with **walnut as the recommendation** (same supplier and grain direction as the foyer floating shelf, for visual continuity through GF).
- Acceptable alternatives if walnut is unavailable or impractical: **teak, sheesham (Indian rosewood), rubberwood** — all premium hardwoods, all hold magnets and machining cleanly. Cost impact: ₹800-2,500 depending on wood.
- Finish: matte polyurethane, 2 coats. No high-gloss (kills the screen contrast with reflections).
- Grain runs horizontal (long axis of the bezel).
- **Final wood decision at carpenter purchase time** based on local availability.

### 5.2 — Dimensions (v3.1, locked 2026-05-29)

The mount lives in a **280 × 195 × 80 mm masonry cavity**. Walnut bezel sits on the wall surface around the cavity opening with a generous overhang to hide the masonry edge.

```
                          ┌──────── 320 mm ────────┐
                  ┌───────┴───────────────────────┴───────┐
                  │ ▓▓▓▓▓▓ vent slot row ▓▓▓▓▓▓          │ 25 mm top bezel
                  ├───────────────────────────────────────┤
                  │     ┌─────────────────────────┐       │
                  │     │                          │       │
                  │     │   Screen window          │       │
                  │     │   (active display area)  │       │
              235 │     │   218.8 × 137.6 mm       │       │ 50 mm side bezel
              mm  │     │   1280 × 800 px          │       │ (25 mm overhang
                  │     │                          │       │  + 25 mm reveal)
                  │     │                          │       │
                  │     └─────────────────────────┘       │
                  ├───────────────────────────────────────┤
                  │ ▓▓▓▓▓▓ vent slot row ▓▓▓▓▓▓          │ 25 mm bottom bezel
                  └───────────────────────────────────────┘
                                                      • ← NFC tap dot
                                                        (ACR122U behind bezel,
                                                         marked with brass inlay)
```

| Element | Dimension | Notes |
|---|---|---|
| **Wall cavity (masonry chase)** | **280 × 195 × 80 mm** | Custom mason work, NOT a standard back box. Smooth-finished interior. Located on staircase S wall, centered at 1500 mm FFL. |
| Screen outline (with case) | 257.6 × 169.7 × 22 mm | Waveshare 10.1" HDMI LCD (B) — fits inside cavity with ~11 mm side clearance, ~13 mm top/bottom |
| Active display area | 218.8 × 137.6 mm | The visible screen window the carpenter cuts in the bezel |
| Bezel cutout window | **220 × 140 mm** | Matches active display + 1 mm tolerance each side |
| Bezel external footprint (W × H) | **~320 × 235 mm** | 20-25 mm overhang beyond cavity edge on all 4 sides — hides the masonry cut; carpenter can adjust ±10 mm based on visual proportion |
| Bezel projection from wall | 3-5 mm max | Subtle shadow line; near-flush look |
| Cavity depth | 80 mm | Holds screen (22) + sub-frame (~10) + cable plug clearance (~20) + service loop slack (~25) |
| Wall remaining behind cavity | 150 mm | 9" wall = 230 mm minus 80 mm cavity. Plenty of structural margin. |
| NFC tap marker | 6 mm brass inlay dot, lower-right bezel | Visual cue + "tap here" hint |
| Position vs existing 2M switch | Cavity bottom ~200 mm above switch top | Vertical alignment for "control zone" visual coherence |

### 5.3 — Service hatch (still important)

Even without a Pi to fail, the screen itself can fail, the HDMI cable can fail, or the NFC reader can fail. The mount must allow the **entire screen + reader assembly to pop forward**:

- 4× **hidden neodymium magnetic catches** at corners (10×10×3 mm magnets in walnut sub-frame, matching strike plates mortared into the masonry cavity walls or fixed to a thin plywood liner)
- 200 mm service loop on **both** HDMI and USB cables coiled inside the cavity, so unit can slide forward 150 mm without unplugging
- Recessed finger-notch in bottom bezel OR hidden suction-cup pad for pulling the unit out

### 5.4 — Ventilation

Screen + NFC reader generate maybe ~6W (down from ~17W in the Pi 5 plan). Heat is **much less of a problem** now, but slots stay in the design for:
- Convection of warm air from the screen's backlight
- Long-term reliability (electronics enclosed without airflow age faster)

- Top bezel: 6 horizontal slots, ~30 × 3 mm
- Bottom bezel: matching slots
- Same angled-cut for aesthetic concealment as v1.0

### 5.5 — Joinery

- Walnut bezel = mitred frame, 4 pieces, 45° corners, glued + biscuit-joined
- Sub-frame = 9 mm plywood, walnut-veneered on visible reveal
- Screen mounts to sub-frame via 4× M3 brass standoffs (Waveshare HDMI panel has VESA-style mount holes at the back)
- ACR122U reader sticks to inside of bezel with adhesive pad, USB cable routed along bottom edge of sub-frame to exit at the back

---

## SECTION 6 — Cable & electrical (electrician spec)

### 6.1 — Existing cable in `C-Niche-Waveshare`

Currently: 1× outdoor LSZH UV-resistant Cat6, both ends coiled, capped. This was the original PoE plan that we're no longer using.

**Decision:** Leave Cat6 in place. Terminate both ends with RJ45 plugs and label as **"SPARE — staircase panel position"**. Future-proofs the conduit if you ever want to migrate to Pi-thin-client architecture, or use the line for a wired sensor / camera at the screen location.

### 6.2 — New cables to pull through `C-Niche-Waveshare`

| Cable | Length | Both-ends termination |
|---|---|---|
| Slim flat HDMI 2.0, 3 m | Niche end → Beelink HDMI 2 port. Panel end → screen HDMI input. | Standard HDMI A connectors at both ends |
| USB-A to micro-USB, 3 m | Niche end → Beelink USB-A 2.0 port. Panel end → screen micro-USB (touch + 5V power upstream) | Standard USB-A → micro-USB |

**How to pull:**
1. Tape both new cables to the existing Cat6 at the niche end using insulation tape
2. Pull from the panel end — all 3 cables come through together
3. Coil 200 mm of service loop on each cable inside the wall cavity, 500 mm at the niche end
4. Verify HDMI cable not kinked anywhere (kinks degrade signal)

**Cavity preparation order:**
1. Mason chases the 280 × 195 × 80 mm cavity in the staircase S wall (do this **before plaster** — 2026-05-30 deadline)
2. Conduit `C-Niche-Waveshare` enters the cavity through a small ~30 mm hole at the bottom of the cavity
3. Cavity interior gets smooth plaster finish OR a 6 mm plywood liner painted matte black (carpenter's choice; black plywood liner is cleaner and gives the magnets a flat strike surface)
4. After plaster, electrician pulls HDMI + USB through the conduit, terminates inside the cavity with service loop

**Conduit fill check:** 25 mm conduit ID ≈ 21 mm usable. Cables: HDMI ~5 mm + USB ~4 mm + Cat6 ~6 mm = 15 mm total diameter. Well within 40% fill rule. Easy.

### 6.3 — New cable run for `C-Niche-Dining`

| ID | C-Niche-Dining |
|---|---|
| Type | 25 mm GREY PVC (LV-25) |
| From | Staircase server niche, top of niche, joins existing data conduit bundle |
| Route | Vertical up niche wall → horizontal east at GF slab level through ceiling chase → down into dining hall E wall → terminate at back box (height per § 4.2) |
| To | Dining hall E side wall back box, height defer to on-site |
| Length | ~7-8 m, verify on-site |
| Cables pulled now | 1× indoor Cat6 + 1× pull-string |
| Back box | 3" × 3" × 2½" GI MS modular, recessed, capped with blank plate |

### 6.4 — Beelink-side connections

In the niche:

| Beelink port | Connects to | Purpose |
|---|---|---|
| HDMI 1 | (Leave free, or occasional service monitor) | For when you SSH into Beelink in person |
| **HDMI 2** | Staircase screen, via new HDMI cable in `C-Niche-Waveshare` | Screen output |
| USB-A port (any) | Staircase screen, via new USB cable | Touch input + 5V power for screen |
| USB-A port (any) | ACR122U NFC reader, via USB extension if needed | NFC tap input |

Beelink port count check (typical EQ12 has 4× USB-A + 1-2× USB-C):
- Zigbee dongle: 1× USB-A
- Touch USB for staircase: 1× USB-A
- NFC reader USB: 1× USB-A
- Backup external drive (occasional): 1× USB-A
- USB-C: free

OK — fits. No port pressure today. When dining screen is added later, that's +1 HDMI (uses HDMI 1, no more spare) + 1 USB-A (still fits with the 4 used today).

### 6.5 — No PoE budget impact

Since Beelink drives the screen directly, the niche PoE switch (TL-SG1210P) doesn't power the panel. PoE budget unchanged from foyer plan:
- Hikvision doorbell: ~6W
- CAM-3, CAM-5 (future): ~12W
- FF Wi-Fi 6 AP: ~12W
- **Headroom: 33W** (was 16W in v1.0 — gained back by removing Pi PoE load)

---

## SECTION 7 — Beelink software setup (homeowner / installer, one-time)

This is the part that's new compared to v1.0. Pi-based v1.0 had a self-contained Pi running its own kiosk. v2.0 needs Beelink to run a second kiosk session on its 2nd HDMI output, while continuing to run all its existing services (Home Assistant, Frigate, etc.).

### 7.1 — Recommended Beelink OS

**Ubuntu Server 24.04 LTS** (already planned). Server edition, no desktop installed by default.

### 7.2 — Adding a minimal kiosk session

We don't want to install full GNOME — too heavy. Instead, install a minimal X11 stack + a tiling window manager + Chromium:

```bash
# Install minimal X + Openbox window manager + Chromium
sudo apt install --no-install-recommends \
  xserver-xorg xinit openbox chromium-browser \
  unclutter xdotool xinput

# Configure Xorg to use HDMI-2 only for kiosk session
# (HDMI-1 stays free for occasional troubleshooting monitor)
```

Create a systemd service `/etc/systemd/system/staircase-kiosk.service`:

```
[Unit]
Description=Staircase panel Chromium kiosk
After=network-online.target home-assistant.service

[Service]
Type=simple
User=kiosk
Environment=DISPLAY=:1
ExecStartPre=/usr/bin/xinit -- :1 vt7
ExecStart=/usr/bin/chromium-browser \
  --kiosk \
  --no-first-run \
  --disable-translate \
  --disable-features=TranslateUI \
  --disable-restore-session-state \
  --noerrdialogs \
  http://localhost:8123/lovelace/staircase
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable staircase-kiosk
sudo systemctl start staircase-kiosk
```

After this, Beelink's HDMI-2 boots straight into Home Assistant dashboard at every reboot.

### 7.3 — Touch input mapping

Beelink's X server auto-detects USB touch devices. To force the staircase USB touch to route to HDMI-2 only (not HDMI-1):

```bash
xinput map-to-output "Waveshare USB Touch" HDMI-2
```

Put this in `~/.xinitrc` or as an Xorg `90-touch.conf` so it runs on every X start.

### 7.4 — NFC reader integration

ACR122U works out-of-the-box with `pcscd` + `libnfc`:

```bash
sudo apt install pcscd libnfc-bin libnfc-examples python3-pyscard

# Test
nfc-list  # should show the ACR122U
```

A small Python service reads tag UIDs and posts to Home Assistant:

```python
# /opt/nfc-listener.py — runs as systemd service
from smartcard.System import readers
import requests, time

HA_URL = "http://localhost:8123/api/events/tag_scanned"
HA_TOKEN = "..."  # long-lived access token

r = readers()[0]
conn = r.createConnection()
while True:
    try:
        conn.connect()
        uid = conn.transmit([0xFF, 0xCA, 0x00, 0x00, 0x00])[0]
        uid_hex = ''.join(f'{b:02x}' for b in uid)
        requests.post(HA_URL,
            headers={"Authorization": f"Bearer {HA_TOKEN}"},
            json={"tag_id": uid_hex})
    except Exception:
        time.sleep(0.5)
```

HA Tag integration triggers scenes based on UID. Same UX as v1.0.

### 7.5 — Screen sleep / wake schedule

Beelink can blank HDMI-2 on schedule via `xset` or `cec-utils`:

```bash
# Blank HDMI-2 at 23:00
0 23 * * * /usr/bin/xset -display :1 dpms force off

# Wake at 06:00
0 6 * * * /usr/bin/xset -display :1 dpms force on
```

Or — better — have HA control display power based on presence sensors or doorbell-rings (instant wake when bell rings at 2 AM).

---

## SECTION 8 — Install steps (Screen 1 only)

### 8.1 — Pre-plaster (URGENT — by 2026-05-30)

1. **Mason** chases the **280 × 195 × 80 mm cavity** in the staircase South wall, centered at 1500 mm FFL, vertically aligned above the existing 2M switch box (~200 mm clear gap).
2. **Electrician** confirms conduit `C-Niche-Waveshare` enters the bottom of the new cavity through a ~30 mm hole.
3. Cavity interior gets smooth plaster OR a 6 mm matte-black plywood liner (carpenter's call — black plywood is cleaner and provides flat strike surfaces for the magnets).

### 8.2 — Cable pull (electrician, before or after plaster)

1. Tape HDMI + USB cables to existing Cat6, pull all 3 from niche end through `C-Niche-Waveshare`. ~30 min.
2. At cavity end, leave 200 mm service loop coiled inside the cavity. Cap cables with dust plugs until carpenter is ready.
3. At niche end, plug HDMI into Beelink HDMI 2 port, USB into any Beelink USB-A port.
4. **Test:** boot Beelink → expect to see Ubuntu login on a desk monitor connected to HDMI 1. Verify HDMI 2 detected by `xrandr` (will say "disconnected" until screen is at the other end).

### 8.3 — Carpenter mount build (off-site, after plaster)

1. Carpenter takes final cavity measurements on-site (cavities may end up 270-285 mm wide, 188-200 mm tall — masonry tolerances).
2. Build walnut bezel + sub-frame off-site sized to the actual cavity (typically ~320 × 235 mm external bezel, 220 × 140 mm internal cutout for screen window).
3. Fit 4 neodymium magnets at sub-frame corners.
4. Attach Waveshare screen + ACR122U NFC reader to sub-frame on bench.
5. Deliver finished assembly to site.

### 8.4 — Final wall install

1. Plug HDMI + USB cables into back of screen at the wall.
2. Slide sub-frame into the cavity, magnets engage with strike plates on the cavity wall.
3. Power on Beelink → Beelink boots → Chromium kiosk autostarts on HDMI 2 → screen lights up with HA dashboard within ~90s of Beelink boot.
4. Test touch — tap a few cards on the dashboard, confirm responsive.
5. Test NFC — `nfc-list` on Beelink should detect the reader; tap an NTAG215 tag → UID appears.

### 8.4 — Software commissioning (Beelink-side)

1. Install minimal X + Openbox + Chromium (per § 7.2)
2. Create kiosk user, systemd service for kiosk
3. Configure touch input mapping
4. Install NFC listener service
5. Set screen sleep schedule
6. Build HA dashboard (deferred to separate dashboard session)
7. Register 5 NTAG215 tags with HA Tag integration, attach scenes

---

## SECTION 9 — NFC tag programming

Carried over from v1.0. NFC tags are independent of the brain architecture.

| Tag # | Location | Action |
|---|---|---|
| 1 | Master bedroom — bedside table | **Goodnight scene** (all lights off, fans medium, water motors locked) |
| 2 | Sofa armrest, GF Living | **Movie scene** (cove dim 20%, halo off, TV power on) |
| 3 | Foyer cavity shelf (walnut) | **Arm Away** (alarm armed, lights off, doorbell records) |
| 4 | Kitchen counter near fridge | **Disarm Home** (kitchen + dining lights on, water motors enabled) |
| 5 | Master bedroom — wardrobe handle | **Wake scene** (curtains open, warm dim lights) |

Spare tags (5 in pack) for future scenes or replacements.

Bezel reader (ACR122U) is always-on (~0.5W draw). Tap any tag → reader reads UID → Python service posts to HA → HA fires the scene → screen highlights the scene name briefly + soft chime through cavity speaker.

---

## SECTION 10 — Maintenance & serviceability

**Screen fails:** Pull magnetic-catch frame forward 150 mm (cables have service loop). Unscrew 4× M3 standoffs holding screen to sub-frame. Disconnect HDMI + USB at the screen end. Swap screen. **~30 min.**

**HDMI cable fails:** Pull frame forward, unplug from screen, pull old cable out from niche end, pull new cable through conduit (tape to existing USB cable as guide). **~45 min.**

**ACR122U NFC reader fails:** Cheap (~₹1,500), accessible behind bezel. Pull frame, swap reader, plug back into Beelink USB. **~15 min.**

**Beelink fails:** Bigger problem — replace Beelink (separate hardware, see project context). All screens, HA, Frigate, etc. go offline until Beelink is replaced. Hold a backup-image of Beelink's OS + HA config on an external drive.

**Spares to stock:**
- 1× spare Waveshare 10.1" HDMI screen (₹11,500) — only if uptime really matters
- 1× spare slim HDMI cable + USB cable (~₹650)
- 1× spare ACR122U (~₹1,500) — small, worth having

---

## SECTION 11 — Cost roll-up

| Category | Cost (₹) |
|---|---|
| **Screen 1 — staircase, today (v3.1 lock)** | |
| Waveshare 10.1" HDMI LCD (B) + case (1280×800), per multi-site survey 2026-05-29 | 9,946-11,752 |
| HDMI + USB cables, NFC reader (ACR122U), NTAG215 tags, misc cabling kit | 2,750 |
| Carpenter mount frame (walnut bezel + sub-frame + magnetic catches + finish; materials + labour) | 4,000-5,000 |
| **Mason labour for 280×195×80 mm cavity chase** (new in v3.1) | 800-1,200 |
| Electrician labour (pull 2 new cables through existing conduit; test) | 500 |
| **Subtotal Screen 1** | **~18,000-21,200** |
| | |
| **Screen 2 — dining hall, provision only today** | |
| `C-Niche-Dining` conduit (~12m) + **1× Cat6** + back box + pull-string | 500 |
| **Subtotal Screen 2 (today)** | **~500** |
| | |
| **TOTAL TODAY** | **~₹18,500-21,700** |
| | |
| **Future cost when dining screen is installed (Pi-at-screen architecture)** | |
| Screen 2 hardware + Pi + PoE HAT + microSD + short cables + IDR plywood mount (in IDR scope) | ~16,000-19,100 |
| **Future spend** | **~₹16,000-19,100** |
| | |
| **Lifetime total (both screens fully built)** | **~₹34,500-40,800** |

**Vs prior iterations:**
- v1.0 (Pi 5 plan) was ~₹33,750 for just the staircase screen
- v2.0 (Beelink-direct everywhere) was ~₹20,250 today
- **v3.1 (current)** ~₹18,500-21,700 today — wider cost range because we lock realistic web-checked pricing on both ends and add the mason cavity labour

---

## SECTION 12 — Visual map

```
                          STAIRCASE SOUTH WALL          DINING HALL E WALL (future)
                          (looking west)                 (looking east into kitchen)
   ┌──────────────────────────────┐                  ┌──────────────────────────────┐
   │                                │                  │                                │
   │     ┌──────────────────┐       │                  │                                │
   │     │ WALNUT BEZEL      │       │                  │                                │
   │     │ 320 × 235 mm      │       │                  │     ┌───────────────────┐     │
   │     │   ┌───────────┐   │       │                  │     │ Future dining     │     │
   │     │   │ Cavity    │   │       │                  │     │ screen — back box │     │
   │     │   │ 280×195   │   │ ← 1500│                  │     │ provisioned at    │     │
   │     │   │ × 80mm    │   │   mm  │                  │     │ TBD height        │     │
   │     │   │ deep      │   │   FFL │                  │     │ (cap blank for    │     │
   │     │   └───────────┘   │       │                  │     │  now)             │     │
   │     │  • NFC tap dot    │       │                  │     │                   │     │
   │     └──────────────────┘       │                  │     └───────────────────┘     │
   │           │                     │                  │                                │
   │      ~200mm clear gap            │                  │                                │
   │           ↓                     │                  │                                │
   │     ┌──────────────────┐       │                  │                                │
   │     │ Existing 2M switch│       │                  │                                │
   │     │ box (staircase    │  ←1200│                  │                                │
   │     │ light, 2-way)     │   mm  │                  │                                │
   │     └──────────────────┘       │                  │                                │
   │                                │                  │                                │
   │     ┌──────────────────┐       │                  │                                │
   │     │ SERVER NICHE     │       │                  │                                │
   │     │ - Beelink EQ12   │       │                  │                                │
   │     │ - HDMI 2 → cable │       │                  │                                │
   │     │   up to screen   │       │                  │                                │
   │     │ - USB-A → cable  │       │                  │                                │
   │     │   up to screen   │       │                  │                                │
   │     │ - HDMI 1 stays   │       │                  │                                │
   │     │   free (future   │       │                  │                                │
   │     │   dining screen) │       │                  │                                │
   │     │ - TP-Link PoE    │       │                  │                                │
   │     │   switch         │       │                  │                                │
   │     │ - Router + UPS   │       │                  │                                │
   │     └──────────────────┘       │                  │                                │
   └──────────────────────────────┘                  └──────────────────────────────┘
              ↑                                                   ↑
              │  C-Niche-Waveshare conduit (25mm GREY)             │  C-Niche-Dining conduit
              │  cables inside:                                    │  (NEW, 25mm GREY, 7-8m)
              │   - HDMI 3m (NEW)                                  │  cable inside:
              │   - USB 3m (NEW)                                   │   - Cat6 (capped)
              │   - Cat6 (existing, now SPARE)                     │   - pull-string
              │                                                    │
              └────────── Beelink in niche ────────────────────────┘
```

---

## SECTION 13 — Install timing in the overall project phase plan

| Phase | Description | Status / when |
|---|---|---|
| Pre-plaster (DONE) | `C-Niche-Waveshare` conduit + Cat6 + staircase back box | ✓ |
| **Pre-plaster (NEW, urgent)** | Lay `C-Niche-Dining` conduit + Cat6 + dining back box. **Must be done before plaster on 2026-05-30.** | ⏳ |
| Plaster + paint | Walls close | per foyer plan Phase 7-8 |
| Carpenter frame build | Walnut bezel + sub-frame off-site | Phase 9 (parallel with foyer shelf) |
| Beelink software setup | One-time Linux config (X + Chromium kiosk + NFC listener) | Anytime after Beelink is up |
| Screen install on wall | Plug cables, slide into magnetic frame | Phase 11 |
| NFC tag programming | Stick 5 NTAG215 tags, attach HA scenes | Phase 12 |
| HA dashboard build | **Separate session**, post-move-in | Future |
| Dining screen install | When you decide to add it | Future session |

---

## SECTION 13.5 — Purchase-time decisions (homeowner discretion)

Items locked in scope but with flexibility on the final pick at order/install time:

| Item | Locked? | Purchase-time decision |
|---|---|---|
| **Wood for mount frame** | In scope | Walnut recommended; teak / sheesham / rubberwood acceptable. Final pick at carpenter purchase time based on local stock + price. |
| **NFC reader (ACR122U + NTAG215 tags, ~₹1,750)** | In scope | Can be dropped at order time if homeowner decides the tap-to-scene convenience isn't worth ₹1,750. Touchscreen still does everything NFC does, just one more tap. Decision deferred to purchase time. |
| **USB extension cable (₹150)** | In scope (safety) | Drop if total cable run from Beelink USB port to screen is < 5m on the bench. Trivial. |
| **Pi Zero 2W vs Pi 4 (for future dining screen)** | Architecture locked (Pi-at-screen) | Pick the specific Pi model at dining install time. Pi 4 if you want headroom for future use cases; Pi Zero 2W if you want cheapest viable. |

---

## SECTION 14 — Open / deferred

### 14.1 — Home Assistant dashboard layout (DEFERRED)

Cards, screens, navigation flow for the 7 use cases (water tank, doorbell video, lights, music, future unlock, CCTV grid, NFC scenes). Pure HA dashboard work. Best done live with screen on the wall.

### 14.2 — Dining hall screen position (DEFERRED to on-site)

Exact wall section + height to be marked by homeowner + electrician on the day `C-Niche-Dining` is pulled.

### 14.3 — Voice / microphone add-on (DEFERRED, not currently selected)

If you ever want voice control: USB conference mic (Jabra Speak 410) plugged into Beelink → HA Voice Assistant. No hardware change to mount.

### 14.4 — Bezel camera (DEFERRED, not currently selected)

If you ever want bezel-mounted video intercom: small USB camera + USB cable through `C-Niche-Waveshare` → Beelink. Carpenter would need to add a hole in top bezel.

### 14.5 — Migration path to Pi-per-screen (DEFERRED, only relevant if 3+ screens ever wanted)

If years from now you want 3+ screens and Beelink port count becomes a constraint, migrate any single screen to Pi-thin-client architecture by:
1. Adding a Pi 4 + PoE HAT at the panel
2. Re-using the existing Cat6 in `C-Niche-Waveshare` (currently capped as SPARE) for PoE
3. Removing HDMI + USB cables (or leaving them capped as spare)
4. Pi runs Chromium kiosk pointing at HA on Beelink — same UX, different brain

Cost to migrate one screen later: ~₹7,000 in Pi parts. Trivial future option.

---

## SECTION 15 — Cross-references

| Document | What it covers |
|---|---|
| [FOYER_MASTER_ELECTRICIAN_PLAN.md § 10 + 18.3](FOYER_MASTER_ELECTRICIAN_PLAN.md) | Original staircase Cat6 stub + deferred design (now resolved by this v2.0 doc) |
| [conduits-and-cavities.md](conduits-and-cavities.md) | Conduit schedule — needs update for new `C-Niche-Dining` |
| [../decisions/decision-log.md](../decisions/decision-log.md) | 2026-05-25 decision lock |
| [../PROJECT_CONTEXT.md](../PROJECT_CONTEXT.md) | Project-wide context |
| [../automation-iot/README.md](../automation-iot/README.md) | Whole-home automation overview |

---

## END OF DOCUMENT v2.0

**Scope:** Staircase screen fully designed for Beelink-direct install. Dining hall screen position provisioned via Cat6 stub for future install.

**Critical next step:** Electrician lays `C-Niche-Dining` conduit + cable + back box **before plaster on 2026-05-30**. Homeowner walks the dining hall with electrician that day to mark wall position + height.

**For any clarification during install:** reference this document by section number.

*Generated as part of the home interior & automation project. Last revised: 2026-05-25. Supersedes v1.0 Pi 5 plan.*
