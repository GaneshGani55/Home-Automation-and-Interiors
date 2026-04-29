# Home Automation & IoT

Whole-home automation plan: protocol, hubs, devices, scenes, networking.

> The electrical layout ([../electrical/](../electrical/)) and the automation plan are tightly coupled — every "smart" switch/socket point must be flagged on the electrical drawing too. Always update both.

## Files (to add as we go)
- `protocol-decision.md` — Matter / Zigbee / Z-Wave / Wi-Fi / KNX trade-off and final pick
- `device-list.md` — every smart device by room (switches, sensors, locks, cameras, curtains, ACs, geysers, fans, lights)
- `scenes-and-automations.md` — Good morning, Movie, Goodnight, Away, etc.
- `network-plan.md` — router placement, AP coverage, VLANs, Cat6 drops (cross-link to electrical)
- `voice-and-app.md` — Alexa / Google / Apple Home / dedicated app stack

## Open questions / decisions to lock
- **Protocol:** Matter-first vs Zigbee hub vs KNX (wired) vs Wi-Fi only. Driver: future-proofing vs cost vs reliability.
- **Hub strategy:** single hub (e.g. Home Assistant on a mini PC) vs vendor cloud (Aqara, Hue, Wipro/Syska, Tata Power EZ).
- **Switch ecosystem:** smart switches (retrofit modular) vs smart relays behind dumb switches. Driver: WAF (wife-acceptance-factor), aesthetics, neutral wire availability.
- **Voice front-end:** Alexa vs Google Home vs Apple HomeKit (or all three via Matter).
- **Camera/security:** which rooms, indoor vs outdoor, NVR vs cloud.
- **Curtains/blinds:** motorized, where? (FF bedrooms, double-height living window are likely candidates.)
- **Climate:** smart AC IR blasters vs native smart ACs; geyser scheduling.
- **Network backbone:** how many APs, where, wired backhaul via Cat6 to each AP.

## Constraint checks
- **Neutral wire** at every switch board → confirm with electrical.
- **Cat6 drops** behind every TV, AP location, study, and at least one drop per bedroom.
- **Hub location** needs power + Ethernet + central RF position (often near the DB or stair).
