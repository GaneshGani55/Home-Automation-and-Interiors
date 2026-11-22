# East guest room — mini home theatre (design locked 2026-11-22)

**Status: design LOCKED by Ganesh on 2026-11-22. Nothing bought yet.** Room = FF east bedroom (repo label "Bedroom 1 (East)", the guest room). Read with [interior-design/guest-room-east.md](../interior-design/guest-room-east.md) and [first-floor-electrical.md § 2](first-floor-electrical.md).

## 1. What it does, in plain words

- **Normal use:** movies stored on the home server (staircase niche) play on a projector, with sound from a soundbar. No laptop needed.
- **Override:** unplug the Fire Stick, plug a laptop into the same port, and the laptop plays on the projector and soundbar instead.
- **Internet at the desk is untouched:** the Cat6 keystone from the server (R-FF-3) stays free for a laptop.

The picture is on the **north wall above the desk**, watched from the bed. The projector hangs from the ceiling at the **south** end, above the bed head.

## 2. The idea that makes it simple

**One HDMI cable carries picture and sound together.** The soundbar sits in the middle of the line:

- **HDMI IN** — whatever is playing plugs in here (Fire Stick or laptop).
- **HDMI OUT** — goes on to the projector.

The soundbar takes the sound out and plays it, and passes the picture on. So its input never comes from the projector.

The server does **not** send video down a cable. It only stores the files. The Fire Stick fetches them over Wi-Fi (through the FF ceiling access point) and plays them.

## 3. The drawing

```
 Server (staircase niche) ──Cat6, existing──► FF ceiling access point
                                                    ┆ Wi-Fi
                                                    ▼
 ┌──────────── at the low 18M switch box, on the desk (N wall) ────────────┐
 │                                                                          │
 │  Fire Stick ───┐                                                         │
 │   (normal)     ├─► Soundbar HDMI IN                                      │
 │  Laptop ┄┄┄┄┄┄┄┘    Soundbar HDMI OUT ──HDMI──► Sender box (on the desk) │
 │   (swap in by hand)                                 │ short LAN patch    │
 │                                                     ▼                    │
 │                                  Keystone "PROJECTOR" in the 18M plate   │
 │                                                                          │
 │  Keystone "INTERNET" (R-FF-3 from the server) — stays free for a laptop  │
 └─────────────────────────────────────────────────────┬────────────────────┘
                                                       │ Cat6 from switch box
                                                       │ to projector (as laid)
                                                       ▼
 ┌──────────────────────── on the ceiling, south end ───────────────────────┐
 │   Receiver box (RJ45 plug goes in) ──short HDMI──► Projector             │
 └──────────────────────────────────────────────────────────────────────────┘
```

Words used above:

- **Sender box / receiver box** = the two halves of an "HDMI extender over Cat6". They turn the Cat6 into a long HDMI cable. That Cat6 is then **not** a network cable.
- **Keystone** = the snap-in network socket in the switch plate.
- **Jellyfin** = free media-server software. It runs on the server; the matching app runs on the Fire Stick.

## 4. Which part sits where

| Place | What sits there |
|---|---|
| Staircase niche | Server with Jellyfin installed. Nothing new to buy. |
| Desk at the low 18M switch box (N wall, ~2 ft / 700 mm) | Fire Stick (plugged into the soundbar), soundbar under the screen, its subwoofer on the floor nearby, extender **sender** box. |
| 18M plate | Two keystones: **INTERNET** (R-FF-3) and **PROJECTOR** (the run to the ceiling). Label both — they look identical, and PROJECTOR gives no internet. |
| Ceiling, south end | Projector on a mount, extender **receiver** box beside it. |

## 5. Cables already laid (as told by Ganesh — verify on site)

| Run | From → to | Use |
|---|---|---|
| R-FF-3 (existing) | Server niche → low switch box, N wall | Internet keystone. Unchanged. |
| **R-FF-3P (new)** | Low 18M switch box → projector point, ceiling at the S end | 1× Cat6, used as the HDMI extender link. Conduit size not confirmed. |
| **Speaker runs (new)** | Low 18M switch box → ceiling points | Finolex 1.5 sqmm speaker cable, several runs to ceiling points (Ganesh: the four corners). **Not used in stage 1** — cap and label them. |

## 6. For the electrician

1. **Power socket at the projector point** on the ceiling, two outlets: projector + receiver box. (D2 sockets circuit.)
2. **Projector Cat6:** keystone at the switch box end; crimped RJ45 plug at the ceiling end. **Same colour order both ends (T568B).** One unbroken run, no joints. Leave ~30 cm spare at the ceiling. Test with a LAN tester before the ceiling closes.
3. **Four power sockets at the desk:** Fire Stick, soundbar, subwoofer, sender box.
4. **Inside the 18M metal box:** keep the two Cat6 cables and keystones at one end, away from the 230 V wiring, with a partition if the box allows. (House rule: no power + low-voltage mixed.)
5. **Speaker cables:** label each at both ends (NE / NW / SE / SW), leave a 1 m coil at each ceiling point, test continuity, cap.
6. **If the conduit to the projector is 25 mm with space:** also pull a fibre (active optical) HDMI cable as a more reliable spare link. It is directional — "source" end at the switch box.

## 7. Check before mounting — still open

- [ ] **Measure the clear N-wall width** between the 12M board and the wardrobe end (estimated ~1.9 m, **not measured**). Picture width = that. Projector lens distance from the N wall = width × 1.64 (for the BenQ TH575 at its smallest zoom) → ~3.1 m for a 1.9 m picture.
- [ ] **Study light F64 conflict:** it is planned at 1800 mm on the N wall above the desk, which is inside the picture area. Move it or drop it before the wall is finished.
- [ ] **Fan:** the projector lens must hang **below** the fan-blade level, or the blades cut the beam. The fan stays at the room centre, so the projector cannot move closer to the screen.
- [ ] **Conduit size** of the switch box → projector run (decides item 6 above).
- [ ] **Speaker cable count and exact ceiling positions.**

## 8. Shopping list (prices seen 2026-11-21 — check before paying)

| # | Part | Product | Price |
|---|---|---|---|
| 1 | Streaming stick | [Amazon Fire TV Stick 4K Plus](https://www.amazon.in/All-New-Amazon-Fire-TV-Stick-4K-Plus/dp/B0F7Z6SDBQ) | ₹6,999 |
| 2 | Soundbar (must have HDMI IN **and** HDMI OUT) | [JBL Bar 2.1 Deep Bass MK2](https://in.jbl.com/Bar-2-1-Deep-Bass-MK2.html) | ₹21,000–24,000 |
| 3 | HDMI extender pair, 1080p | [MICROWARE HDMI Extender over Cat6, 60 m](https://www.amazon.in/Microware-Extender-Repeater-Transmitter-Projector/dp/B077T87FGS) | ₹854 |
| 4 | Projector, 1080p, 3800 lm, throw ratio 1.49–1.64 | [BenQ TH575](https://www.flipkart.com/benq-th575-3800-lm-1-speaker-remote-controller-low-latency-enhanced-game-mode-high-contrast-rec-709-color-standard-dual-hdmi-3d-auto-vertical-keystone-1-1x-zoom-1080p-dlp-gaming-projector/p/itm78d9bd07c859e) | ₹51,000–66,000 |
| 5 | Ceiling mount + 3 short HDMI cables + 0.5 m LAN patch cable | any | ~₹2,500 |

Total ≈ ₹82,000–1,00,000.

Why these:

- **Fire TV Stick 4K Plus, not the cheaper 4K Select:** the Select runs a newer system and Jellyfin on it was not confirmed.
- **Wi-Fi, not LAN, for the stick:** the projector is 1080p, and the FF access point is just outside the room, so Wi-Fi is enough. Fallback if it ever buffers: the [Amazon Ethernet Adapter](https://www.amazon.in/Amazon-Ethernet-Adapter-Fire-Stick/dp/B01M19P4GJ) (₹1,499) into the INTERNET keystone — no wall work.
- **No HDMI selector:** swapping the Fire Stick for the laptop by hand is enough.

## 9. How to use it

- **Server movies:** projector on, soundbar on, pick a movie in Jellyfin with the Fire Stick remote.
- **Laptop:** pull the Fire Stick out of the soundbar's HDMI IN, plug the laptop's HDMI cable in. Put the Fire Stick back afterwards.
- **Server movies without the Fire Stick:** open Jellyfin in the laptop's browser and plug the laptop in as above.

## 10. Later (stage 2, not planned yet)

The ceiling speaker cables are for passive speakers, which need an amplifier box (**AV receiver**) at the desk. If wanted later: the receiver replaces the soundbar in the same spot in the chain; add three front speakers + a subwoofer at the screen; use the two ceiling points above the bed as surrounds. Four ceiling corners alone are not enough — voices would come from the ceiling, not the screen.

**Considered and dropped:** driving the projector straight from the server over the server→room Cat6 (loses the internet keystone and leaves no remote in the room); Fire Stick at the projector (sound has no way back down to the soundbar).
