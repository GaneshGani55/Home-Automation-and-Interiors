/* ============================================================
   Conduit Map — Automation focus
   Source of truth: electrical/conduits-and-cavities.md,
   FOYER_MASTER_ELECTRICIAN_PLAN.md, water-automation-conduits.md,
   WAVESHARE_INDOOR_PANEL.md, automation-iot/mmwave-presence-sensors.md
   ============================================================ */

/* SERVICE META (colour = real PVC conduit colour code) */
const SVC = {
  power_light:{label:"Power (light)", color:"#DC1E1E", pvc:"25mm RED"},
  power_heavy:{label:"Power (heavy)", color:"#1E5ADC", pvc:"25mm BLUE"},
  data:       {label:"Data",          color:"#EB6E14", pvc:"25mm GREY"},
  lv16:       {label:"LV-16",         color:"#8C5AC8", pvc:"16mm GREY"},
  water:      {label:"Water",         color:"#1E8C64", pvc:"20/16mm GREY"},
  presence:   {label:"Presence (mmWave)", color:"#C81E78", pvc:"wired 5V — no conduit"}
};
/* Automation services are listed first; power is toggled on when needed. */
const SVC_ORDER = ["data","lv16","water","presence","power_light","power_heavy"];
/* Filter active on load (automation-first). Components are an independent layer. */
const DEFAULT_ACTIVE = ["data","lv16","water","presence","components"];

/* ============================================================
   CONDUIT DATA
   ============================================================ */
const CONDUITS = [
 {ref:"P1",floor:"GF",service:"power_light",size:"25mm",status:"live",from:"DB",to:"Foyer Switch Panel (N wall, 1200mm FFL)",contents:"1.5sqmm L + N + E (feeds 6-gang foyer panel)",note:"65mm-deep GI MS box. NEUTRAL must reach the panel - no exceptions."},
 {ref:"P2",floor:"GF",service:"power_light",size:"25mm",status:"live",from:"Foyer Switch Panel",to:"2x foyer ceiling GU10 spotlights",contents:"Switched live Gang 1 + N + E",note:"GU10 7W 2700K, adjustable gimbals to angle 30deg toward stone wall."},
 {ref:"P3",floor:"GF",service:"power_light",size:"25mm",status:"live",from:"Foyer Switch Panel",to:"False-ceiling cove driver + halo driver",contents:"Switched live Gang 2 + N + E",note:"Both drivers above false ceiling. Halo wraps cavity top."},
 {ref:"P4",floor:"GF",service:"power_light",size:"16mm",status:"live",from:"Foyer Switch Panel",to:"Walnut shelf 24V driver",contents:"Switched live Gang 3 + N + E",note:"Floor route preferred."},
 {ref:"P5",floor:"GF",service:"power_light",size:"16mm",status:"live",from:"Foyer Switch Panel",to:"Outside porch ceiling light",contents:"Switched live Gang 5 + N + E",note:"Through N wall. Outdoor IP44 fitting."},
 {ref:"P6",floor:"GF",service:"power_light",size:"25mm",status:"live",from:"DB",to:"Living false ceiling, 4x recessed COB ceiling boxes (12W 2700K)",contents:"1.5sqmm L + N + E",note:"Stay in solid-slab zone, avoid the void area."},
 {ref:"P7",floor:"GF",service:"power_light",size:"25mm",status:"live",from:"DB",to:"Chandelier ceiling rose box on FF beam (over void)",contents:"1.5sqmm L + N + E",note:"Chandelier hangs into double-height void from above."},
 {ref:"P8",floor:"GF",service:"power_light",size:"25mm",status:"live",from:"DB",to:"Kitchen ceiling box + utility light",contents:"1.5sqmm L + N + E",note:"4000K cool/neutral panel for task area."},
 {ref:"P9",floor:"GF",service:"power_light",size:"25mm",status:"live",from:"DB",to:"Dining pendant centre + 2x supplementary downlights",contents:"1.5sqmm L + N + E",note:"Pendant drop to 2100mm FFL. Confirm table position."},
 {ref:"P10",floor:"GF",service:"power_light",size:"25mm",status:"live",from:"DB",to:"MBR ceiling + bedsides (E wall) + wardrobe driver (S+W walls)",contents:"1.5sqmm L + N + E",note:"Centre on bed after headboard line is marked."},
 {ref:"P11",floor:"GF",service:"power_light",size:"25mm",status:"live",from:"DB",to:"GF Bath ceiling + mirror + exhaust + PIR outside door",contents:"1.5sqmm L + N + E",note:"PIR outside door at 1200mm FFL. Geyser switch BELOW at 1050mm."},
 {ref:"P12",floor:"GF",service:"power_light",size:"25mm",status:"live",from:"DB",to:"Pooja ceiling spotlights + decorative strip",contents:"1.5sqmm L + N + E",note:"Confirm fixture spec on-site."},
 {ref:"P13",floor:"GF",service:"power_light",size:"25mm",status:"live",from:"DB",to:"Step lights + mid-flight wall light + niche + landing",contents:"1.5sqmm L + N + E",note:"Step lights (3W each) on each riser left side."},

 {ref:"H1",floor:"GF",service:"power_heavy",size:"25mm",status:"live",from:"DB",to:"Foyer screen cavity (back wall) - 2x 5A sockets",contents:"2.5sqmm L + N + E",note:"Sonoff Mini R2 inside socket box switches Monitor only."},
 {ref:"H2",floor:"GF",service:"power_heavy",size:"25mm",status:"live",from:"DB",to:"TV wall (W wall of Living) - 3 boxes (16A + double 5A + Cat6 keystone)",contents:"2.5sqmm L + N + E",note:"All at 300mm FFL. Keystone box 150mm from power boxes."},
 {ref:"H3",floor:"GF",service:"power_heavy",size:"25mm",status:"live",from:"DB",to:"Living perimeter sockets (multiple boxes)",contents:"2.5sqmm L + N + E",note:"Skirting-level chase. Min 150mm from corners."},
 {ref:"H4",floor:"GF",service:"power_heavy",size:"25mm",status:"live",from:"DB",to:"Kitchen counter - 4x sockets at 1100mm FFL",contents:"2.5sqmm L + N + E",note:"Above counter, behind backsplash. Confirm with kitchen designer."},
 {ref:"H5",floor:"GF",service:"power_heavy",size:"25mm",status:"live",from:"DB",to:"Chimney socket above hob at 1900mm FFL",contents:"2.5sqmm L + N + E",note:"16A socket centred over hob."},
 {ref:"H6",floor:"GF",service:"power_heavy",size:"25mm",status:"live",from:"DB",to:"Hob position at 150mm FFL (floor screed route)",contents:"4sqmm L + N + E (25A direct hardwire)",note:"NO socket - direct hardwire. 25A MCB."},
 {ref:"H7",floor:"GF",service:"power_heavy",size:"25mm",status:"live",from:"DB",to:"Fridge niche socket at 300mm FFL",contents:"2.5sqmm L + N + E",note:"Confirm height after fridge model is picked."},
 {ref:"H8",floor:"GF",service:"power_heavy",size:"25mm",status:"live",from:"DB",to:"MBR bedside sockets (E wall) at 600mm FFL + utility",contents:"2.5sqmm L + N + E",note:"Flank the headboard."},
 {ref:"H9",floor:"GF",service:"power_heavy",size:"25mm",status:"live",from:"DB",to:"MBR AC socket at 1850mm FFL on N wall above door",contents:"4sqmm L + N + E (20A RCBO)",note:"Confirm AC manual for socket position relative to outdoor unit."},
 {ref:"H10",floor:"GF",service:"power_heavy",size:"25mm",status:"live",from:"DB",to:"Bath geyser outlet at 1850mm FFL inside bathroom",contents:"2.5sqmm L + N + E (20A RCBO)",note:"Geyser SWITCH (DP) outside door at 1050mm FFL."},

 {ref:"D1",floor:"GF",service:"data",size:"25mm",status:"live",from:"Niche",to:"Foyer screen cavity (back wall, bottom-RIGHT)",contents:"1x indoor Cat6 (UTP)",note:"FLOOR route under screed (not ceiling). ~12m.",explain:"Cat6 (floor route under the screed) from the niche to the foyer screen cavity. It powers (PoE) and feeds the Raspberry Pi behind the welcome monitor. Shares one floor chase with D2 + D3 - no separate break."},
 {ref:"D2",floor:"GF",service:"data",size:"25mm",status:"live",from:"Niche",to:"Main-door outside face (Hikvision DS-KV6113-WPE1(C) video doorbell, PoE)",contents:"1x outdoor LSZH UV-rated Cat6 (PoE)",note:"Doorbell at 1450mm FFL, latch side. Shared floor route with D1+D3. Updated 2026-05-22: Hikvision DS-KV6113-WPE1(C) replaces the earlier Reolink TC541.",explain:"Outdoor Cat6 (PoE) to the video doorbell. ONE cable both powers the doorbell and carries its video back to the server for face detection - no power needed at the door."},
 {ref:"D3",floor:"GF",service:"data",size:"25mm",status:"provision",from:"Niche",to:"Porch W wall (future face-detection camera, CAM-1)",contents:"PULL STRING ONLY - capped IP67 back-box, 1650mm FFL",note:"DROPPED from base install (doorbell handles face capture).",explain:"Spare conduit for a future dedicated face camera if the doorbell's face detection ever proves unreliable. Pull-string only now; a Cat6 can be drawn later - no wall break."},
 {ref:"D4",floor:"GF",service:"data",size:"25mm",status:"live",from:"Niche",to:"Living Hall N wall, MIDDLE (overview camera, CAM-2)",contents:"1x outdoor Cat6 (PoE) - conduit route chosen on site",note:"Moved 2026-05-30: was porch ceiling NE corner; now mid of the Living Hall NORTH wall. Technician picks the conduit route.",explain:"Overview camera relocated to the middle of the Living Hall north (entrance-facing) wall - it watches the porch / main approach. Conduit route is left to the technician: pull from the niche, or tap the nearest data run, whatever is cleanest on site."},
 {ref:"D5",floor:"GF",service:"data",size:"25mm",status:"live",from:"Niche",to:"Staircase S wall, 1500mm FFL (Waveshare 10.1in panel)",contents:"1x HDMI 2.0 (3m) + 1x USB-A->micro-USB (3m) + existing Cat6 spare",note:"CUSTOM 280x195x80mm masonry cavity (not modular). Above existing 2M switch with ~200mm gap.",explain:"Two cables (HDMI + USB) from the Beelink in the niche carry picture + touch straight to the staircase panel - no computer at the screen. The old Cat6 in this conduit is kept as a labelled spare."},
 {ref:"D6",floor:"GF",service:"data",size:"25mm",status:"live",from:"Niche",to:"Dining E wall (Waveshare dining panel)",contents:"1x indoor Cat6 + 1x pull string",note:"~12m / 35-40ft. Pi-at-screen pattern.",explain:"Cat6 from the niche to the dining wall panel. A small Pi behind the screen gets PoE power + data on this ONE cable and renders the Home Assistant dashboard. The interior designer will try to fit this screen into the cantilevered kitchen shelves, so box height/position is kept flexible (500mm slack)."},
 {ref:"D7",floor:"GF",service:"data",size:"25mm",status:"live",from:"Niche",to:"Dining ceiling JB (mono speaker)",contents:"1x indoor Cat6 (PoE-capable) + 1x pull string",note:"Pi + PAM8403 + 3in ceiling speaker. ~10m. This is the LOW-voltage speaker run via the niche.",explain:"Cat6 from the niche to a ceiling junction box above the dining table for a mono ceiling speaker. PoE-capable, so a small Pi/amp can sit at the ceiling - or the dining panel's Pi can drive it (see D11)."},
 {ref:"D9",floor:"GF",service:"data",size:"25mm x 3",status:"live",from:"Niche",to:"Vertical riser -> FF -> Terrace (3 bundles)",contents:"3x LV-25: R-FF-1 (2x Cat6), R-FF-2, R-FF-3. CAM-3, CAM-5 and the Sintex run continue UP to terrace.",note:"Dedicated 150mm-wide chase channel up the staircase wall.",explain:"The vertical data spine. 3 grey conduits up the staircase wall carry ALL First-Floor and Terrace data - FF APs, the two study drops, the balcony + terrace cameras, and the Sintex tank sensor run all continue up here. See the Riser and Terrace tabs for what reaches the top."},
 {ref:"D10",floor:"GF",service:"data",size:"25mm",status:"live",from:"Niche",to:"GF false-ceiling AP, central JB above dining/living junction (R-GF-1)",contents:"1x Cat6 UTP (PoE) + draw wire",note:"Ubiquiti UniFi U6-Lite or equiv. PoE only - no socket. Primary GF Wi-Fi 6.",explain:"Cat6 (PoE) from the niche to the GF ceiling Wi-Fi AP above the dining/living junction. One cable powers the AP and backhauls it - no socket needed in the ceiling."},
 {ref:"D11",floor:"GF",service:"lv16",size:"16mm",status:"live",from:"Dining panel (Pi)",to:"Dining ceiling speaker JB",contents:"Short AV / control link (2-core or 3.5mm)",note:"NEW 2026-05-30.",explain:"Lets the dining panel's Raspberry Pi play and control audio on the dining ceiling speaker. Short hop - can be pulled through the false-ceiling void between the panel and the speaker JB, so no wall break is needed."},
 {ref:"D12",floor:"GF",service:"data",size:"25mm",status:"live",from:"Server",to:"TV unit (W wall of Living)",contents:"1x Cat6 (UTP)",note:"Wired network point behind the TV unit.",explain:"Cat6 from the server to the TV unit on the W wall of the Living Hall - a wired drop behind the TV for a smart-TV / streaming box / console, so the main screen doesn't depend on Wi-Fi."},

 {ref:"L1",floor:"GF",service:"lv16",size:"16mm",status:"live",from:"Foyer Switch Panel",to:"Cove LED driver in false ceiling",contents:"24V DC 2-core",note:"Driver in false ceiling perimeter. Accessible via inspection hatch.",explain:"24V DC from the foyer panel (Gang 2) to the cove LED driver hidden in the false ceiling. The driver converts 230V->24V; this 2-core only carries the low-voltage OUTPUT to the strip. Runs inside the foyer panel's existing ceiling chase - no extra wall break."},
 {ref:"L2",floor:"GF",service:"lv16",size:"16mm",status:"live",from:"Foyer Switch Panel",to:"Halo driver above false ceiling near cavity top",contents:"24V DC 2-core",note:"Halo strip wraps cavity reveal. Amber 2200K.",explain:"24V to the amber halo strip that frames the screen cavity. Driven from the same panel gang as the cove; the driver sits above the false ceiling near the cavity top."},
 {ref:"L3",floor:"GF",service:"lv16",size:"16mm",status:"live",from:"Foyer Switch Panel",to:"Walnut shelf 24V driver",contents:"24V DC 2-core",note:"Shelf strip 6W/m, warm white.",explain:"24V DC to the under-strip driver of the walnut floating shelf, switched by foyer panel Gang 3. Floor route preferred so the shelf gets a hidden feed."},
 {ref:"L4",floor:"GF",service:"lv16",size:"16mm",status:"live",from:"Foyer screen cavity (amp)",to:"Foyer ceiling speaker (centre, between the 2 spotlights)",contents:"2-core speaker wire",note:"FIXED - not future. Speaker sits in the MIDDLE of the foyer ceiling, between the two GU10 spotlights.",explain:"Carries audio from the PAM8403 amp INSIDE the screen cavity up to the foyer ceiling speaker. The cavity Pi plays sound -> amp -> this 2-core -> ceiling speaker. Pull it up through the cavity's TOP conduit into the false ceiling, then across to the centre point between the two spotlights."},
 {ref:"L5",floor:"GF",service:"lv16",size:"16mm",status:"provision",from:"Niche",to:"Main door frame TOP (concealed door-contact sensor)",contents:"PULL STRING ONLY",note:"Future provision - pull-string now.",explain:"For a FUTURE hidden magnetic door-contact sensor at the top of the main-door frame. It simply tells Home Assistant whether the door is OPEN or SHUT - two thin wires, one reed switch on the frame + a magnet on the door leaf. HA uses it for the 'Away' alarm and the welcome logic (e.g. only greet when the door actually opens). Just a pull-string today; a thin 2-core can be drawn later through THIS 16mm conduit, or piggy-backed on the adjacent doorbell conduit, so no wall-breaking later."},
 {ref:"L6",floor:"GF",service:"lv16",size:"16mm",status:"live",from:"MBR ceiling JB",to:"S-wall wardrobe top rail LED driver",contents:"24V DC 2-core",note:"Door-activated sensor on each leaf.",explain:"24V to the master-bedroom S-wall wardrobe top-rail LED. A small door sensor on each leaf turns the strip on when the wardrobe opens."},
 {ref:"L7",floor:"GF",service:"lv16",size:"16mm",status:"live",from:"MBR ceiling JB",to:"W-wall wardrobe tail LED driver",contents:"24V DC 2-core",note:"Tail of L-shaped wardrobe.",explain:"24V to the W-wall wardrobe tail LED (the short return of the L-shaped wardrobe). Same door-sensor idea as L6."},

 {ref:"W1",floor:"GF",service:"water",size:"20mm",status:"live",from:"Niche",to:"Terrace SW Sintex JB (up the riser)",contents:"1x outdoor LSZH Cat6 (PoE)",note:"Up the staircase riser to the terrace, then embedded under terrace screed BEFORE tiling to the SW corner. See the Terrace tab.",explain:"Cat6 (data + 48V PoE) from the niche, up the riser, across the terrace to the Sintex tank JB at the SW corner. It powers the tank's ESP32 and carries the ultrasonic water-level reading back to the server. Sensor run only - the float is separate (W2)."},
 {ref:"W2",floor:"GF",service:"water",size:"16mm",status:"live",from:"Terrace Sintex HIGH float",to:"DB starter cupboard",contents:"2-core 1.5mm2 double-insulated",note:"Comes DOWN the riser, then around to the cupboard. Parallel to W1, MIN 50mm separation on the shared legs.",explain:"The Sintex HIGH-level float is a hardware safety cut-off: tank full -> stop BOTH motors. Its 2-core runs from the tank straight to the DB starter cupboard and sits in series with both motor coils, so it works even if the server/Wi-Fi are down. It does NOT need to pass through the server - route it the shortest safe way to the cupboard."},
 {ref:"W3",floor:"GF",service:"water",size:"20mm",status:"live",from:"Niche",to:"Sump JB (porch W wall, 300mm AGL)",contents:"1x outdoor LSZH Cat6 (PoE)",note:"Sleeve through the wall sloping outward. JB beside the manhole (cover hinges W).",explain:"Cat6 (data + 48V PoE) from the niche to the sump JB on the porch. Powers the sump ESP32 and reads the pressure-probe water level. Sensor run only - the float is separate (W4)."},
 {ref:"W4",floor:"GF",service:"water",size:"16mm",status:"live",from:"Sump LOW float",to:"DB starter cupboard",contents:"2-core 1.5mm2",note:"Short run from the sump JB around to the cupboard. Parallel to W3, MIN 50mm separation.",explain:"The sump LOW-level float stops the booster pump running dry. Its 2-core goes from the sump JB to the DB starter cupboard, in series with the P2 (booster) coil ONLY. Like the Sintex float it's a mechanical failsafe - no reason to route it via the server; take it straight around the walls to the cupboard."},
 {ref:"W5",floor:"GF",service:"water",size:"20mm",status:"provision",from:"Niche",to:"DB starter cupboard (future backup link)",contents:"PULL STRING ONLY",note:"Both ends capped + labelled WATER AUTOMATION - FUTURE Cat6.",explain:"Spare conduit between the niche and the cupboard. If the Wi-Fi link to the motor controller ever proves unreliable, a Cat6 can be pulled here later for a wired ESP32 motor controller - no wall break."},
 {ref:"W6",floor:"GF",service:"water",size:"25mm",status:"live",from:"DB starter cupboard",to:"Borewell head outside",contents:"4sqmm armoured (16A Type C)",note:"CONFIRM existing run can be repurposed.",explain:"Purely the POWER feed to RUN the borewell motor - 4sqmm armoured from the P1 starter in the cupboard out to the borewell head. No data or sensor in this conduit."},
 {ref:"W7",floor:"GF",service:"water",size:"25mm",status:"live",from:"DB starter cupboard",to:"Sump (submersible booster motor)",contents:"3-core 2.5mm2",note:"The sump motor is a SUBMERSIBLE sitting INSIDE the sump - cable goes into the sump, not to an outdoor cage.",explain:"POWER feed to RUN the sump booster pump from the P2 starter. Per the electrician the pump is submerged inside the sump, so this power cable goes to the sump itself."},

 {ref:"F1",floor:"FF",service:"power_light",size:"25mm",status:"live",from:"Riser",to:"BR2 ceiling + cove + bedsides + wardrobe driver",contents:"1.5sqmm L + N + E",note:"Centre on bed once headboard line is marked."},
 {ref:"F2",floor:"FF",service:"power_heavy",size:"25mm",status:"live",from:"Riser",to:"BR2 bedside + study sockets at 600mm FFL",contents:"2.5sqmm L + N + E",note:""},
 {ref:"F3",floor:"FF",service:"power_heavy",size:"25mm",status:"live",from:"Riser",to:"BR2 AC socket at 1850mm FFL",contents:"4sqmm L + N + E (20A AC)",note:""},
 {ref:"F4",floor:"FF",service:"power_heavy",size:"25mm",status:"live",from:"Riser",to:"T2 geyser outlet 1850mm FFL + DP switch outside door",contents:"2.5sqmm L + N + E (20A geyser)",note:""},
 {ref:"F5",floor:"FF",service:"power_light",size:"25mm",status:"live",from:"Riser",to:"BR1 ceiling + bedsides + wardrobe driver",contents:"1.5sqmm L + N + E",note:""},
 {ref:"F6",floor:"FF",service:"power_heavy",size:"25mm",status:"live",from:"Riser",to:"BR1 bedside + study sockets at 600mm FFL",contents:"2.5sqmm L + N + E",note:""},
 {ref:"F7",floor:"FF",service:"power_heavy",size:"25mm",status:"live",from:"Riser",to:"BR1 AC socket at 1850mm FFL",contents:"4sqmm L + N + E (20A AC)",note:""},
 {ref:"F8",floor:"FF",service:"power_heavy",size:"25mm",status:"live",from:"Riser",to:"T1 geyser + lights bundle",contents:"2.5sqmm L + N + E + 1.5sqmm lights",note:""},
 {ref:"F9",floor:"FF",service:"power_light",size:"25mm",status:"live",from:"Riser",to:"FF Living ceiling + front balcony + corridor lights",contents:"1.5sqmm L + N + E",note:""},
 {ref:"F10",floor:"FF",service:"data",size:"25mm",status:"live",from:"Riser",to:"FF Living CEILING AP, central JB between BR1 & BR2 doors (R-FF-1)",contents:"2x Cat6 UTP (router uplink + spare) + draw wire",note:"Updated 2026-05-29: moved from 2400mm wall plate to ceiling junction box. PoE-only AP (UniFi U6-Lite); 5A socket dropped."},
 {ref:"F11",floor:"FF",service:"data",size:"25mm",status:"live",from:"Riser",to:"BR2 study wall, 700mm FFL",contents:"1x Cat6 UTP + draw wire",note:""},
 {ref:"F12",floor:"FF",service:"data",size:"25mm",status:"live",from:"Riser",to:"BR1 study wall, 700mm FFL",contents:"1x Cat6 UTP + draw wire",note:""},
 {ref:"F14",floor:"FF",service:"data",size:"25mm",status:"provision",from:"Riser",to:"Front balcony NW corner soffit/parapet (CAM-3)",contents:"PULL STRING + 1x outdoor Cat6",note:"Elevated overview of compound, gate, driveway."},
 {ref:"F15",floor:"FF",service:"data",size:"25mm",status:"provision",from:"Riser",to:"Continue UP to terrace level (CAM-5)",contents:"PULL STRING + 1x outdoor UV-resistant Cat6",note:"Use UV-rated conduit for last 500mm above roof. Parapet mount."}
];

/* ============================================================
   ENDPOINT COORDINATES (viewBox 1000 x 1085)
   ============================================================ */
const HUB = { DB:[88,935], NICHE:[900,730], DBCUP:[88,978], RISER:[800,705] };
const NODE = { FOYERPANEL:[185,990], MBRJB:[750,205], CAVTOP:[185,905], FFAP:[490,648] };

const CO = {
 P1:{o:HUB.DB,d:[185,988]}, P2:{o:NODE.FOYERPANEL,d:[150,945]}, P3:{o:NODE.FOYERPANEL,d:[120,930]},
 P4:{o:NODE.FOYERPANEL,d:[235,945]}, P5:{o:NODE.FOYERPANEL,d:[270,1040]}, P6:{o:HUB.DB,d:[745,720]},
 P7:{o:HUB.DB,d:[760,855]}, P8:{o:HUB.DB,d:[210,205]}, P9:{o:HUB.DB,d:[210,520]},
 P10:{o:HUB.DB,d:[770,230]}, P11:{o:HUB.DB,d:[770,500]}, P12:{o:HUB.DB,d:[148,812]}, P13:{o:HUB.DB,d:[700,700]},
 H1:{o:HUB.DB,d:[200,914]}, H2:{o:HUB.DB,d:[928,800]}, H3:{o:HUB.DB,d:[650,985]}, H4:{o:HUB.DB,d:[112,150]},
 H5:{o:HUB.DB,d:[85,80]}, H6:{o:HUB.DB,d:[145,118]}, H7:{o:HUB.DB,d:[448,345]}, H8:{o:HUB.DB,d:[585,300]},
 H9:{o:HUB.DB,d:[700,418]}, H10:{o:HUB.DB,d:[835,452]},
 D1:{o:HUB.NICHE,d:[210,914]}, D2:{o:HUB.NICHE,d:[205,1010]}, D3:{o:HUB.NICHE,d:[490,1038]},
 D4:{o:HUB.NICHE,d:[745,1000]}, D5:{o:HUB.NICHE,d:[618,618]}, D6:{o:HUB.NICHE,d:[68,470]},
 D7:{o:HUB.NICHE,d:[210,560]}, D9:{o:HUB.NICHE,d:[845,720]}, D10:{o:HUB.NICHE,d:[470,700]},
 D11:{o:[80,470],d:[210,560]}, D12:{o:HUB.NICHE,d:[928,825]},
 L1:{o:NODE.FOYERPANEL,d:[235,905]}, L2:{o:NODE.FOYERPANEL,d:[258,918]}, L3:{o:NODE.FOYERPANEL,d:[110,918]},
 L4:{o:NODE.CAVTOP,d:[185,950]}, L5:{o:HUB.NICHE,d:[210,1006]}, L6:{o:NODE.MBRJB,d:[750,72]}, L7:{o:NODE.MBRJB,d:[928,200]},
 W1:{o:HUB.NICHE,d:[845,660]}, W2:{o:[920,72],via:[[75,72],[75,985]],d:[130,985]}, W3:{o:HUB.NICHE,d:[505,1042]},
 W4:{o:HUB.DBCUP,d:[505,1058]}, W5:{o:HUB.NICHE,d:[150,975]}, W6:{o:HUB.DBCUP,d:[60,1042]}, W7:{o:HUB.DBCUP,d:[520,1062]},
 F1:{o:HUB.RISER,d:[700,400]}, F2:{o:HUB.RISER,d:[560,348]}, F3:{o:HUB.RISER,d:[700,255]},
 F4:{o:HUB.RISER,d:[650,128]}, F5:{o:HUB.RISER,d:[260,400]}, F6:{o:HUB.RISER,d:[440,348]},
 F7:{o:HUB.RISER,d:[260,255]}, F8:{o:HUB.RISER,d:[300,128]}, F9:{o:HUB.RISER,d:[250,770]},
 F10:{o:HUB.RISER,d:[490,648]}, F11:{o:HUB.RISER,d:[700,612]}, F12:{o:HUB.RISER,d:[270,612]},
 F14:{o:HUB.RISER,d:[110,1000]}, F15:{o:HUB.RISER,d:[762,730]}
};

/* mmWave presence sensors — markers only (no conduit drawn). */
const MMWAVE = [
 {ref:"M1",floor:"GF",room:"GF Master Bedroom",mount:"Ceiling (centre)",powerShort:"Ceiling - buck 230->5V",
  power:"Ceiling mount: a 230->5V buck converter off the bedroom lighting line (permanent L+N).",
  mountNote:"Ceiling centre of the master bedroom, clear of the wardrobe path.",xy:[800,300]},
 {ref:"M2",floor:"GF",room:"GF Common Bathroom",mount:"Wall",powerShort:"Wall - USB off mains",
  power:"Wall mount: 5V from a USB female socket fed off the normal mains line.",
  mountNote:"High on a dry-zone wall (east, by the door) with clear sight across the room. Keep out of shower Zone 1/2.",xy:[645,500]},
 {ref:"M3",floor:"GF",room:"Dining / Living mid-ceiling",mount:"Ceiling",powerShort:"Ceiling - buck 230->5V",
  power:"Ceiling mount: a 230->5V buck converter off the normal line.",
  mountNote:"Ceiling mid-point between Dining and Living, near the GF ceiling-AP junction box (D10).",xy:[430,655]},
 {ref:"M4",floor:"FF",room:"FF west bedroom (balcony side)",mount:"Ceiling",powerShort:"Ceiling - buck",
  power:"Ceiling mount: a 230->5V buck converter off the normal line.",
  mountNote:"Ceiling centre of the west bedroom (the one with the balcony).",xy:[705,430]},
 {ref:"M5",floor:"FF",room:"FF east bedroom",mount:"Wall",powerShort:"Wall - USB off mains",
  power:"Wall mount: 5V from a USB female socket off the normal mains line.",
  mountNote:"High wall corner with a clear view of the bed / room.",xy:[265,430]},
 {ref:"M6",floor:"FF",room:"FF west toilet",mount:"Ceiling",powerShort:"Ceiling - buck",
  power:"Ceiling mount: a 230->5V buck converter off the normal line.",
  mountNote:"Ceiling, dry zone, clear of the shower.",xy:[675,150]},
 {ref:"M7",floor:"FF",room:"FF east toilet",mount:"Wall",powerShort:"Wall - USB off mains",
  power:"Wall mount: 5V from a USB female socket off the normal mains line.",
  mountNote:"High dry-zone wall corner.",xy:[325,150]}
];

/* Device / install-guide markers (tag pinned on the plan -> opens a guide). */
const DEVICES = [
 {id:"JB-SUMP",      floor:"GF",   svc:"water", label:"Sump JB",        xy:[505,1040]},
 {id:"DB-CUPBOARD",  floor:"GF",   svc:"water", label:"DB cupboard",    xy:[150,975]},
 {id:"NICHE-SERVER", floor:"GF",   svc:"data",  label:"Server",         xy:[900,770]},
 {id:"FOYER-CAVITY", floor:"GF",   svc:"data",  label:"Foyer screen",   xy:[205,915]},
 {id:"AP-GF",        floor:"GF",   svc:"data",  label:"GF ceiling AP",  xy:[470,705]},
 {id:"WAVESHARE-STAIR",floor:"GF", svc:"data",  label:"Stair panel",    xy:[650,600]},
 {id:"WAVESHARE-DINING",floor:"GF",svc:"data",  label:"Dining panel",   xy:[140,455]},
 {id:"CAM-DOORBELL", floor:"GF",   svc:"data",  label:"Doorbell",       xy:[210,1010]},
 {id:"CAM-N",        floor:"GF",   svc:"data",  label:"Living N cam",   xy:[745,982]},
 {id:"SMART-SWITCH", floor:"GF",   svc:"power_light", label:"Smart switch box", xy:[630,890]},
 {id:"AP-FF",        floor:"FF",   svc:"data",  label:"FF ceiling AP",  xy:[490,692]},
 {id:"CAM-3",        floor:"FF",   svc:"data",  label:"CAM-3",          xy:[120,998]},
 {id:"CAM-5R",       floor:"TERRACE",svc:"data",  label:"CAM-5",        xy:[640,790]}
];

/* ============================================================
   INSTALL GUIDES (keyed by device id)
   glyph = short tag shown in the header icon; color from service
   ============================================================ */
const GUIDES = {
 "JB-SUMP":{
  title:"Sump JB — sensor hub", sub:"Porch W wall · 300mm AGL · IP66", glyph:"JB", svc:"water",
  badge:"Pull cable now",
  inside:["WT32-ETH01 (ESP32 + Ethernet) — the local sensor brain","PoE splitter (48V → 5V) — powers the ESP32","3-way terminal block — pressure transducer wires","2-way terminal block — float wire transit to DB cupboard","2-way LV tap — float telemetry to an ESP32 GPIO ('sump low' status)"],
  power:"PoE only. One Cat6 (C-Sump-1 / W3) from the niche carries data + 48V. NO 230V at this box. The PoE splitter drops 48V → 5V to the ESP32; the ESP32's 5V rail feeds the sensor.",
  mount:"Surface-mount IP66 box on the porch W wall at 300mm AGL (1 ft), BESIDE the manhole — not above it (the cover hinges on the W side and lies flat against this wall when open). 4 glands at the bottom: M20 Cat6 (C-Sump-1), M16 float (C-Sump-2), M12 pressure probe, M12 low-float.",
  sensor:"DFRobot SEN0257 hydrostatic pressure probe, suspended through a manhole gland ~10cm above the sump floor. Drill the side-of-sump glands BEFORE waterproofing; sensor + float cables run up the W wall in a short surface conduit into the JB bottom glands.",
  steps:["Fix the IP66 box backplate at 300mm AGL beside the manhole.","Land C-Sump-1 Cat6 → PoE splitter; take its 5V to the WT32-ETH01.","Pressure-probe cable → 3-way block → ESP32 ADC. Keep this analog run under 30cm.","Low-level float: 2 wires in series into C-Sump-2 (to DB cupboard, P2 coil) for dry-run cutoff, PLUS a parallel LV tap to an ESP32 GPIO for 'sump low' telemetry.","Seal every gland; fit the gasket lid (screw lid, not snap-fit)."],
  imgs:["sump-jb-mount.jpg","sump-cross.jpg","jb-internals.jpg"], pdf:"WATER_AUTOMATION.pdf", related:["W3","W4"]
 },
 "JB-SINTEX":{
  title:"Sintex JB — tank sensor hub", sub:"Terrace SW parapet · ~1.2m AGL · IP66", glyph:"JB", svc:"water",
  badge:"Pull cable now",
  inside:["WT32-ETH01 (ESP32 + Ethernet)","PoE splitter (48V → 5V)","4-way terminal block — ultrasonic sensor wires","2-way terminal block — high-level float transit to DB cupboard"],
  power:"PoE only, via C-Sintex-1 (W1) Cat6 from the niche. No 230V at the JB.",
  mount:"On the SW parapet inner face at ~1.2m AGL. Add a sun shield if directly exposed. 4 bottom glands (Cat6, float, sensor, float-to-tank). The horizontal terrace run for W1/W2 MUST be embedded under the screed BEFORE tiling/waterproofing.",
  sensor:"JSN-SR04T ultrasonic on a 30cm PVC riser screwed into the tank cap (30cm clears the 25cm dead-zone + 10cm air-gap at full). Sensor in an acrylic enclosure at the riser top, cable exits sideways. Camsco vertical SS high-level float (NC, ~95% level) runs via C-Sintex-2 (W2) to the DB cupboard, in series with BOTH motor coils — a mechanical, server-independent failsafe.",
  steps:["Embed C-Sintex-1 + C-Sintex-2 under the terrace screed before tiling (50mm apart).","Mount the IP66 box on the SW parapet; land Cat6 → PoE splitter → 5V to ESP32.","Drill the Sintex cap, fit the 30cm PVC riser, mount the JSN-SR04T on top.","Run the ultrasonic cable into the JB 4-way block → ESP32 (keep analog <30cm).","Transit the high-level float through the JB into C-Sintex-2 down to the DB cupboard."],
  imgs:["sintex-jb-mount.jpg","sintex-riser.jpg","jb-internals.jpg"], pdf:"WATER_AUTOMATION.pdf", related:["W1","W2"]
 },
 "DB-CUPBOARD":{
  title:"DB starter cupboard", sub:"Foyer E wall, beside DB · lockable + vented", glyph:"DB", svc:"water",
  badge:"Pull cable now",
  inside:["P1 starter — Magnum Pradhaan PSP1H (1.5HP, borewell submersible)","P2 starter — Magnum Pradhaan PSP1 (1HP, sump booster)","Sonoff DUALR3 Pro (Wi-Fi, 2 channels — one per motor)","Float terminal blocks + coil jumpers","Earth busbar (all motor earths land here)"],
  power:"Mains-fed. Motor feeds leave via C-Motor-P1 (W6, 4sqmm armoured → borewell) and C-Motor-P2 (W7, 2.5sqmm → P2 cage on the east outside wall).",
  mount:"New lockable, ventilated enclosure, ≥600 × 400 × 250mm internal, adjacent to the existing DB. Hinged door with lock; slatted vents top + bottom; 7 conduit entries from below/back.",
  sensor:"Failsafe wiring: Sintex high-level float in series with BOTH contactor coils (full tank → both motors stop). Sump low-level float in series with P2's coil only (dry-run protection). Both fire even if Sonoff/Wi-Fi/server are all down. Manual green/red starter buttons are preserved as the ultimate override.",
  steps:["Build the lockable, vented cupboard beside the DB on the E wall.","Mount P1 + P2 starters and the Sonoff DUALR3 Pro.","Wire one Sonoff channel in series with each starter's coil supply (tap, don't bypass).","Land both float pairs on the terminal block; jumper Sintex float to both coils, sump float to P2 only.","Bring C-Motor-P1 + C-Motor-P2 out to the borewell and the P2 cage."],
  imgs:["water-overview.jpg"], pdf:"WATER_AUTOMATION_VISUAL_v2.pdf", related:["W6","W7","W5","W2","W4"]
 },
 "NICHE-SERVER":{
  title:"Server niche (the brain)", sub:"Staircase · HA + Frigate + PoE backbone", glyph:"HA", svc:"data",
  badge:"Pull cable now",
  inside:["Beelink EQ12 mini-PC — Home Assistant + Frigate NVR + CompreFace","1TB SSD (HA storage + NVR), APC UPS","TP-Link TL-SG1210P PoE switch (8× PoE) — powers cameras / APs / JBs","TP-Link Archer AX55 router (GF Wi-Fi 6)","Sonoff Zigbee 3.0 USB dongle — coordinator for the 45 Sonoff relays","12-port Cat6 keystone patch panel"],
  power:"20A UPS socket at 300mm FFL; 2× double 5A at 400mm. Everything out of here is LV / PoE — this is the hub every data + camera + JB Cat6 returns to.",
  mount:"Niche shelving; Cat6 patch panel + speaker terminal strip at 700mm FFL on the side wall. This is the origin hub for all D-series (data), W1/W3 (water sensors) and the FF riser bundle.",
  steps:["Terminate every incoming Cat6 onto the 12-port patch panel.","Patch the PoE switch to: doorbell, CAM-3/4/5, GF + FF ceiling APs, Sintex + Sump JBs.","Uplink the router; Beelink runs HA + Frigate + CompreFace.","Plug in the Zigbee dongle — it coordinates all hidden Sonoff relays.","Sit everything on the UPS so a power blip doesn't drop the brain."],
  imgs:["staircase-spine.jpg"], pdf:"FOYER_ELECTRICIAN_MASTER_PLAN.pdf", related:["D9","D10","D5","W1","W3"]
 },
 "FOYER-CAVITY":{
  title:"Foyer welcome screen", sub:"S feature wall · stone cavity 580×380×100mm", glyph:"TV", svc:"data",
  badge:"Pull cable now",
  inside:["Samsung LS22F320GAW 21.5\" monitor (VESA 100, no speakers)","Raspberry Pi Zero 2W + PoE splitter (5V)","Pi Camera Module 3 (CAM-0) on the top bezel — CSI ribbon","Visaton FR 8 speaker + PAM8403 amp + USB sound card","Sonoff Mini R2 (Wi-Fi) inside the socket box — switches the Monitor socket","Halo 24V amber LED around the cavity reveal"],
  power:"Cavity has 2× 5A sockets on the BACK wall (C-DB-Cavity-Power / H1, from the DB on the E wall). The Pi is PoE-powered: the cavity Cat6 (D1, floor route from the niche) → PoE splitter → 5V to the Pi. Halo 24V from the driver above the false ceiling.",
  mount:"Monitor on a VESA 100 bracket, centre 1450mm FFL, on the back wall. Socket pocket centre 1346mm; 3\"dia×1\" speaker pocket; matte-black inside; stone wraps the front 30mm of the reveal.",
  sensor:"Face capture: Hikvision DS-KV6113-WPE1(C) PoE doorbell on the outside N wall at 1450mm → Frigate → CompreFace match → HA wakes the screen. CAM-0 bezel Pi-cam is a secondary close-range check.",
  steps:["Cut the 580×380×100mm cavity, centred on the 6ft feature wall; paint matte black.","Bring POWER (H1) to bottom-LEFT and DATA (D1) to bottom-RIGHT of the back wall; HALO (16mm) to top-centre.","Mount the VESA bracket at 1450mm; fit the 2× 5A socket plate (Sonoff Mini R2 inside, switching Monitor only).","Behind the monitor: Pi + PoE splitter + amp + sound card on the back wall; speaker into its pocket.","Run the stone reveal + halo; commission the welcome flow with the doorbell."],
  imgs:["foyer-stone.jpg","foyer-xray.jpg"], pdf:"FOYER_ELECTRICIAN_MASTER_PLAN.pdf", related:["H1","D1","D2","P1","L2"]
 },
 "AP-GF":{
  title:"GF ceiling Wi-Fi AP", sub:"False ceiling, dining/living junction · PoE", glyph:"AP", svc:"data",
  badge:"Pull cable now",
  inside:["Ubiquiti UniFi U6-Lite (or equivalent) Wi-Fi 6 AP","Fed by 1× Cat6 (R-GF-1 / D10) from the niche"],
  power:"PoE only — the AP draws ~12W over the Cat6 from the niche PoE switch. No socket needed.",
  mount:"Ceiling junction box, flush in the false ceiling, centred above the open dining/living junction. Primary GF Wi-Fi 6 for dining, living, foyer and the master bedroom.",
  steps:["Run R-GF-1 (D10) from the niche, up the niche wall, east across the GF false-ceiling void.","Terminate at a capped ceiling JB at the central dining/living position.","After ceiling work, clip the AP to the JB and patch its Cat6 to a PoE port in the niche."],
  imgs:["wifi-ap.jpg"], pdf:"ELECTRICIAN_REFERENCE.pdf", related:["D10"]
 },
 "AP-FF":{
  title:"FF ceiling Wi-Fi AP", sub:"FF Living false ceiling, central · PoE", glyph:"AP", svc:"data",
  badge:"Pull cable now",
  inside:["Ubiquiti UniFi U6-Lite (or equivalent) Wi-Fi 6 AP","Fed by 2× Cat6 (R-FF-1 / F10) — uplink + spare"],
  power:"PoE only (R-FF-1). The old 2400mm wall plate + 5A socket are dropped — ceiling-mount, PoE-fed.",
  mount:"Ceiling JB in the FF Living false ceiling, central between the BR1 and BR2 doors for balanced coverage.",
  steps:["Carry R-FF-1 up the staircase riser, then east to the central FF Living ceiling.","Terminate 2× Cat6 at a ceiling JB.","Mount the AP after ceiling work; patch one Cat6 to a niche PoE port (keep the 2nd as spare)."],
  imgs:["wifi-ap.jpg"], pdf:"ELECTRICIAN_REFERENCE.pdf", related:["F10","F11","F12"]
 },
 "CAM-DOORBELL":{
  title:"Video doorbell (face capture)", sub:"Outside N wall · 1450mm FFL · PoE", glyph:"DR", svc:"data",
  badge:"Pull cable now",
  inside:["Hikvision DS-KV6113-WPE1(C) PoE video doorbell (doorbell + camera + 2-way intercom)","3\"×3\"×2.5\" GI back box, recessed so it hides behind the bracket"],
  power:"PoE via D2 (outdoor LSZH UV Cat6), floor route shared with the cavity Cat6 (D1).",
  mount:"Latch side of the main door, 1450mm FFL, 150–200mm from the frame.",
  sensor:"RTSP stream → Frigate → CompreFace face match → Home Assistant → foyer welcome screen. Replaces the earlier Reolink TC541 (updated 2026-05-22).",
  steps:["Recess the small GI box on the outside N wall at 1450mm.","Pull D2 outdoor Cat6 (floor route) to the box; weatherproof the entry with silicone.","Mount the doorbell bracket over the box; patch its Cat6 to a niche PoE port.","Add it to Frigate; train CompreFace on family faces."],
  imgs:["foyer-xray.jpg"], pdf:"FOYER_ELECTRICIAN_MASTER_PLAN.pdf", related:["D2","D3"]
 },
 "CAM-N":{
  title:"Living N-wall camera", sub:"Mid Living Hall N wall · overview · PoE", glyph:"CN", svc:"data",
  badge:"Pull cable now",
  inside:["Hikvision ColorVu 4MP, 2.8mm, IP67, PoE","Fed by D4 outdoor Cat6 (PoE)"],
  power:"PoE via D4. One Cat6 powers the camera and carries its video to the server.",
  mount:"Centre of the Living Hall NORTH (entrance-facing) wall — covers the porch and the main approach. Replaces the earlier porch-ceiling position (CAM-2).",
  sensor:"Overview / context camera, not a face camera. Feeds Frigate for motion + general CCTV.",
  steps:["Pick the conduit route on site (from the niche, or tap the nearest data run) — left to the technician.","Land a Cat6 at a flush / IP-rated box at the middle of the Living N wall.","Mount the camera, aim out over the porch / approach; patch to a niche PoE port."],
  imgs:["wifi-ap.jpg"], pdf:"ELECTRICIAN_REFERENCE.pdf", related:["D4"]
 },
 "CAM-3":{
  title:"CAM-3 — Front balcony bird's-eye", sub:"FF balcony NW soffit · PoE", glyph:"C3", svc:"data",
  badge:"Pull string now",
  inside:["Hikvision ColorVu 4MP, 2.8mm, IP67, PoE (installed later)","Conduit + 1× outdoor Cat6 + draw wire now (F14)"],
  power:"PoE via F14 (riser → FF corridor ceiling → balcony soffit).",
  mount:"NW corner of the front balcony soffit/parapet, ~5500mm above ground — elevated overview of compound, gate and driveway.",
  steps:["Carry F14 up the riser, north along the FF corridor ceiling, into the balcony soffit.","Terminate at an IP67 back box at the NW corner; leave the draw wire.","Fit the camera when commissioning the NVR."],
  imgs:["wifi-ap.jpg"], pdf:"ELECTRICIAN_REFERENCE.pdf", related:["F14"]
 },
 "CAM-5R":{
  title:"CAM-5 — Terrace exit", sub:"Parapet by stair exit · UV conduit · PoE", glyph:"C5", svc:"data",
  badge:"Pull string now",
  inside:["Hikvision ColorVu 4MP, 2.8mm, IP67, PoE (installed later)","Conduit + 1× outdoor UV Cat6 + draw wire now (F15)"],
  power:"PoE via F15 — the riser bundle continued up to terrace level.",
  mount:"Parapet beside the FF→terrace stair exit, ~2500mm above terrace floor. Use UV-rated conduit for the last 500mm above the roof line.",
  steps:["Continue the riser up to terrace level beside the stair exit.","Terminate at an IP67 UV-rated back box on the parapet.","Fit the camera later; it watches terrace access + neighbourhood overview."],
  imgs:["staircase-spine.jpg"], pdf:"ELECTRICIAN_REFERENCE.pdf", related:["F15"]
 },
 "WAVESHARE-STAIR":{
  title:"Staircase control panel", sub:"S wall · 1500mm FFL · 280×195×80 cavity", glyph:"WS", svc:"data",
  badge:"Pull cable now",
  inside:["Waveshare 10.1\" HDMI LCD (B), 1280×800, with case","ACR122U USB NFC reader behind the bezel","Walnut bezel (~320×235mm) + magnetic service hatch"],
  power:"Beelink-direct — no Pi, no PoE. HDMI + USB run through the existing C-Niche-Waveshare conduit (D5); 5V to the screen comes over the USB from the Beelink. The existing Cat6 stays as a labelled SPARE.",
  mount:"Custom 280×195×80mm masonry cavity in the 9\" staircase S wall, centred at 1500mm FFL, ~200mm above the existing 2M light switch. Walnut bezel overhangs to hide the cut; 4 magnets for a pop-forward service hatch; vent slots top + bottom.",
  steps:["Mason chases the 280×195×80mm cavity (before plaster, 2026-05-30).","Conduit enters the cavity bottom via a ~30mm hole; smooth-finish or black-ply liner.","Tape HDMI + USB to the existing Cat6 and pull all three; leave 200mm service loops.","Niche end: HDMI → Beelink HDMI-2, USB → Beelink USB-A.","Carpenter builds the bezel; mount the screen; Beelink runs a Chromium kiosk on HDMI-2."],
  imgs:["waveshare-1.jpg","waveshare-2.jpg","waveshare-3.jpg","waveshare-4.jpg","waveshare-5.jpg","waveshare-6.jpg"],
  pdf:"WAVESHARE_INSTALL_GUIDE.pdf", related:["D5"]
 },
 "WAVESHARE-DINING":{
  title:"Dining panel (provision)", sub:"Dining E wall · Cat6 + back box only", glyph:"WS", svc:"data",
  badge:"Pull string now", live:false,
  inside:["Today: 1× Cat6 + pull-string + capped 3\"×3\"×2.5\" back box (C-Niche-Dining / D6)","Future: Waveshare 10.1\" + a small Pi behind the screen (Pi-at-screen)"],
  power:"Future: Pi-at-screen, wired — a single Cat6 PoE powers AND drives a Pi behind the screen (matches the foyer pattern). No HDMI extender. Today: just lay the cable.",
  mount:"E wall of the dining hall near the breakfast counter / kitchen-dining partition. Height + exact position defer to the interior designer (plywood under the cantilever shelf). Leave 500mm slack so the box can shift ±300mm later.",
  steps:["Lay C-Niche-Dining (~12m): niche → up the wall → east through the GF ceiling chase → down the dining E wall.","Pull 1× indoor Cat6 + 1× pull-string; cap the back box with a blank plate.","Also drop a short link (D11) from this panel to the dining ceiling-speaker JB so the panel's Pi can drive + control the speaker.","On the day, walk the dining hall with the electrician to mark the exact wall section + height. The interior designer will try to fit the screen into the cantilevered kitchen shelves, so keep it flexible."],
  imgs:["dining-xray.jpg"], pdf:"WAVESHARE_INSTALL_GUIDE.pdf", related:["D6","D7","D11"]
 },
 "SMART-SWITCH":{
  title:"Smart switch box (Sonoff)", sub:"65mm GI box · neutral required · all smart boards", glyph:"SW", svc:"power_light",
  badge:"Pre-plaster rule",
  inside:["Sonoff ZBMINI R2 (Zigbee) hidden behind a Schneider Unica plate","The physical rocker (still works if HA is down)","Neutral bus + earth bonding in the box"],
  power:"Lighting circuit. Every smart board MUST get permanent L + N + E. Plate size = smart gangs + 2M slack per hidden Sonoff. The homeowner fits the Sonoff later — the electrician just leaves 300mm L/N/E tails, capped + labelled.",
  mount:"65mm-deep GI MS box (NOT 50mm — too tight for the relay + bent wires). Applies at: Foyer, Living ×2, Dining, MBR, Pooja, Staircase ×2, FF Living, BR1, BR2, balconies.",
  sensor:"This is where the mmWave presence sensors tie in: HA reads presence, then switches THIS relay. So the neutral + 65mm box here is what makes presence-based lighting possible later.",
  steps:["At every smart-switch location use a 65mm-deep GI box.","Pull a NEUTRAL to every board (black wire visible in the tail bundle).","Leave 300mm L/N/E tails, capped, labelled with the circuit ID.","Size the Unica plate with +2M slack per Sonoff so the modules sit flush."],
  imgs:["foyer-xray.jpg"], pdf:"ELECTRICIAN_REFERENCE.pdf", related:["P1"]
 }
};

/* ============================================================
   FLOOR PLAN GEOMETRY  [x1,y1,x2,y2,label,sublabel?]
   ============================================================ */
const ROOMS = {
 GF:[
  [60,60,360,360,"Kitchen"],
  [360,60,520,190,"Utility"],
  [360,190,520,300,"Store"],
  [360,300,520,380,"Fridge"],
  [60,380,360,690,"Dining"],
  [560,60,940,430,"Master Bedroom","12' x 12'3\""],
  [560,430,940,575,"Common Bath","9' x 4'6\""],
  [560,610,860,700,"",""],
  [860,610,940,790,"Landing"],
  [60,720,235,905,"Pooja","5' x 5'"],
  [60,905,300,1005,"Foyer"],
  [540,615,940,1005,"Living Hall","16'11\" x 16'11\""],
  [40,1008,540,1075,"Porch","main door + sump (W wall)"]
 ],
 FF:[
  [180,60,470,230,"Toilet 1","sink-toilet-shower"],
  [60,230,470,620,"Bedroom 1"],
  [530,60,820,230,"Toilet 2","shower-toilet-sink"],
  [530,230,880,620,"Bedroom 2"],
  [880,230,940,560,"Wd"],
  [880,560,940,720,"W Balcony"],
  [60,620,470,1005,"FF Living"],
  [640,660,880,755,"",""],
  [60,840,340,1020,"Front Balcony","11'9\" x 7'"]
 ]
};
const ENV = {
 GF:"M60,60 H940 V790 H940 V1005 H540 V615 H475 V1005 H235 V905 H60 V60 Z",
 FF:"M60,60 H940 V820 H560 V1020 H60 Z"
};
const VOID_FF=[560,820,940,1020];

/* ---------- render helpers ---------- */
const NS="http://www.w3.org/2000/svg";
function el(tag,attrs){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);return e;}
function txt(x,y,s,cls){const t=el("text",{x,y,class:cls});t.textContent=s;return t;}

function drawPlan(floor,g){
  g.appendChild(el("path",{d:ENV[floor],class:"wall","stroke-width":"3"}));
  if(floor==="FF"){
    const[vx1,vy1,vx2,vy2]=VOID_FF;
    g.appendChild(el("rect",{x:vx1,y:vy1,width:vx2-vx1,height:vy2-vy1,fill:"#F2EEDF",stroke:"#C9C3B2","stroke-width":1}));
    const hg=el("g",{class:"voidhatch"});
    for(let i=-((vy2-vy1));i<(vx2-vx1);i+=14){
      hg.appendChild(el("line",{x1:vx1+Math.max(0,i),y1:vy1+Math.max(0,-i),x2:vx1+Math.min(vx2-vx1,i+(vy2-vy1)),y2:vy1+Math.min(vy2-vy1,(vx2-vx1)-i)}));
    }
    g.appendChild(hg);
    g.appendChild(txt((vx1+vx2)/2,(vy1+vy2)/2-8,"CUT-OUT","rsub"));
    g.appendChild(txt((vx1+vx2)/2,(vy1+vy2)/2+8,"DOUBLE-HEIGHT VOID","rsub"));
  }
  ROOMS[floor].forEach(r=>{
    const[x1,y1,x2,y2,label,sub]=r;
    g.appendChild(el("rect",{x:x1,y:y1,width:x2-x1,height:y2-y1,class:"wall"}));
    if(label){
      g.appendChild(txt((x1+x2)/2,(y1+y2)/2,label,"rlabel"));
      if(sub)g.appendChild(txt((x1+x2)/2,(y1+y2)/2+16,sub,"rsub"));
    }
  });
  if(floor==="GF") drawStair(g,560,610,860,700,22,"UP",true);
  if(floor==="FF"){ drawStair(g,640,660,880,755,12,"UP TERRACE",false);
    g.appendChild(txt(760,650,"to terrace","rsub")); }
  const doors = floor==="GF"
   ? [[475,955,40,"M475,995 A40,40 0 0,1 435,955"],
      [560,455,34,"M560,489 A34,34 0 0,1 594,455"]]
   : [[470,640,40,"M470,600 A40,40 0 0,0 510,640"],
      [530,640,40,"M530,600 A40,40 0 0,1 490,640"]];
  doors.forEach(d=>g.appendChild(el("path",{d:d[3],class:"door"})));
}
function drawStair(g,x1,y1,x2,y2,n,label,up){
  g.appendChild(el("rect",{x:x1,y:y1,width:x2-x1,height:y2-y1,class:"wall"}));
  const step=(x2-x1)/n;
  for(let i=1;i<n;i++) g.appendChild(el("line",{x1:x1+step*i,y1:y1,x2:x1+step*i,y2:y2,class:"step"}));
  g.appendChild(txt((x1+x2)/2,y1-8,label,"rsub"));
}

function drawHubs(floor,g){
  const list = floor==="GF"
    ? [["NICHE",HUB.NICHE,"#FFE650","SERVER",90,26],
       ["DB",HUB.DB,"#FFC8C8","DB",58,24],
       ["DBCUP",HUB.DBCUP,"#C8F0DC","DB CUPBD",78,22]]
    : [["RISER",HUB.RISER,"#FFE650","RISER",78,26]];
  list.forEach(h=>{
    const[,c,fill,lab,w,ht]=h;
    const grp=el("g",{class:"hub"});
    grp.appendChild(el("rect",{x:c[0]-w/2,y:c[1]-ht/2,width:w,height:ht,rx:3,fill}));
    grp.appendChild(txt(c[0],c[1]+3.5,lab,""));
    g.appendChild(grp);
  });
  if(floor==="GF"){
    [["FOYERPANEL",NODE.FOYERPANEL,"PANEL"],["MBRJB",NODE.MBRJB,"MBR JB"]].forEach(nd=>{
      const grp=el("g",{class:"node"}),c=nd[1];
      grp.appendChild(el("rect",{x:c[0]-22,y:c[1]-9,width:44,height:18,rx:2}));
      grp.appendChild(txt(c[0],c[1]+3,nd[2],""));
      g.appendChild(grp);
    });
  }
  if(floor==="FF"){
    const c=NODE.FFAP,grp=el("g",{class:"node"});
    grp.appendChild(el("rect",{x:c[0]-20,y:c[1]-9,width:40,height:18,rx:2}));
    grp.appendChild(txt(c[0],c[1]+3,"AP",""));
    g.appendChild(grp);
  }
}

function routeD(o,d,jit){
  // horizontal trunk sits BETWEEN origin and destination (clamped) so a run never
  // dips past its endpoint — e.g. foyer-panel LV lines no longer loop down to the porch.
  let my=(o[1]+d[1])/2 + jit*0.45;
  const lo=Math.min(o[1],d[1])-6, hi=Math.max(o[1],d[1])+6;
  my=Math.max(lo,Math.min(hi,my));
  return `M${o[0]},${o[1]} L${o[0]},${my} L${d[0]},${my} L${d[0]},${d[1]}`;
}

function drawConduits(floor,g){
  const list=CONDUITS.filter(c=>c.floor===floor);
  list.forEach((c,i)=>{
    const co=CO[c.ref]; if(!co)return;
    const color=SVC[c.service].color;
    const jit=((i%9)-4)*9;
    const grp=el("g",{class:"cond"+(c.status==="provision"?" prov":""),"data-ref":c.ref});
    // co.via = explicit waypoints (used to hug the wall boundary, e.g. the Sintex float W2)
    const dpath=co.via ? "M"+[co.o,...co.via,co.d].map(p=>p[0]+","+p[1]).join(" L") : routeD(co.o,co.d,jit);
    grp.appendChild(el("path",{class:"hit",d:dpath}));
    grp.appendChild(el("path",{class:"ln",d:dpath,stroke:color}));
    grp.appendChild(el("circle",{class:"dot",cx:co.d[0],cy:co.d[1],r:11,
      fill:c.status==="provision"?"#FAF8F2":color,stroke:color}));
    const tref=txt(co.d[0],co.d[1],c.ref,"ref");
    tref.setAttribute("fill",c.status==="provision"?color:"#fff");
    grp.appendChild(tref);
    const right = co.d[0]<880;
    const lab=txt(co.d[0]+(right?16:-16),co.d[1]+4,shortLabel(c.to),"lab");
    lab.setAttribute("text-anchor",right?"start":"end");
    lab.setAttribute("fill","#1C1C1E");
    grp.appendChild(lab);
    grp.addEventListener("click",e=>{e.stopPropagation();select(c.ref);});
    g.appendChild(grp);
  });
}
function shortLabel(to){
  let s=to.split("(")[0].split(" - ")[0].split(" -> ")[0].trim();
  return s.length>26?s.slice(0,25)+"…":s;
}

/* mmWave presence markers (icon only, no conduit line) */
function drawMmwave(floor,g){
  MMWAVE.filter(m=>m.floor===floor).forEach(m=>{
    const[x,y]=m.xy;
    const grp=el("g",{class:"mw","data-ref":m.ref});
    grp.appendChild(el("circle",{cx:x,cy:y,r:17,fill:"transparent"}));
    grp.appendChild(el("circle",{class:"halo",cx:x,cy:y,r:11}));
    grp.appendChild(el("path",{class:"ring",d:`M ${x-7} ${y-1} A 8 8 0 0 1 ${x+7} ${y-1}`}));
    grp.appendChild(el("path",{class:"ring",d:`M ${x-4} ${y} A 5 5 0 0 1 ${x+4} ${y}`}));
    grp.appendChild(el("circle",{class:"core",cx:x,cy:y+2,r:2.4}));
    grp.appendChild(txt(x,y+24,m.ref,""));
    grp.addEventListener("click",e=>{e.stopPropagation();openMmwave(m.ref);});
    g.appendChild(grp);
  });
}

/* device / install-guide tag markers */
function drawDevices(floor,g){
  DEVICES.filter(d=>d.floor===floor).forEach(d=>{
    const G=GUIDES[d.id]||{}; const col=SVC[d.svc]?SVC[d.svc].color:"#1C1C1E";
    const[cx,cy]=d.xy; const w=d.label.length*5.7+26, h=19, x=cx-w/2, y=cy-h/2;
    const grp=el("g",{class:"dev","data-id":d.id});
    grp.appendChild(el("rect",{x:x-4,y:y-4,width:w+8,height:h+8,rx:6,fill:"transparent"}));
    grp.appendChild(el("rect",{class:"tag",x,y,width:w,height:h,rx:5,fill:"#2F2C28"}));
    grp.appendChild(el("circle",{class:"gear",cx:x+11,cy:cy,r:3.4}));
    grp.appendChild(el("circle",{cx:x+11,cy:cy,r:1.6,fill:col}));
    const t=txt(cx+7,cy+3.4,d.label,"lab"); grp.appendChild(t);
    grp.addEventListener("click",e=>{e.stopPropagation();openDeviceAt(d.id);});
    g.appendChild(grp);
  });
}

/* ============================================================
   RISER cross-section view
   ============================================================ */
const RISER_BUNDLES=[
 {n:"R-FF-1",svc:"data",top:"FF",txt:"2x Cat6 -> FF ceiling AP"},
 {n:"R-FF-2",svc:"data",top:"FF",txt:"1x Cat6 -> BR2 study"},
 {n:"R-FF-3",svc:"data",top:"FF",txt:"1x Cat6 -> BR1 study"},
 {n:"CAM-3",svc:"data",top:"TERR",txt:"Cat6 -> balcony cam"},
 {n:"CAM-5",svc:"data",top:"TERR",txt:"Cat6 -> terrace parapet cam"},
 {n:"FF-PL",svc:"power_light",top:"FF",txt:"FF lighting feed"},
 {n:"FF-PH",svc:"power_heavy",top:"FF",txt:"FF power feed"},
 {n:"FF-AP",svc:"data",top:"FF",txt:"Router / AP feed"},
 {n:"W1",svc:"water",top:"TERR",txt:"Sintex sensor Cat6 (PoE)"},
 {n:"W2",svc:"water",top:"TERR",txt:"Sintex float 2-core"},
 {n:"SPARE",svc:"lv16",top:"FF",txt:"Pull string (spare)"}
];
function drawRiser(g){
  const L=140,R=620,levels=[
    {y:120,t:"TERRACE"},{y:320,t:"FIRST FLOOR"},{y:620,t:"GF SLAB"},{y:920,t:"GROUND (Niche)"}
  ];
  levels.forEach(lv=>{
    g.appendChild(el("line",{x1:L-40,y1:lv.y,x2:R+40,y2:lv.y,stroke:"#333","stroke-width":2}));
    g.appendChild(txt(L-44,lv.y-7,lv.t,"rsub")).setAttribute("text-anchor","end");
  });
  g.appendChild(el("rect",{x:L-12,y:120,width:R-L+24,height:800,fill:"#F4F0E2",stroke:"#E3DECF","stroke-width":1}));
  g.appendChild(txt((L+R)/2,108,"STAIRCASE RISER CHASE  (GF Niche → FF → Terrace)","rsub"));
  const n=RISER_BUNDLES.length, gap=(R-L)/(n-1);
  RISER_BUNDLES.forEach((b,i)=>{
    const x=L+gap*i, color=SVC[b.svc].color, topY=b.top==="TERR"?130:330;
    const grp=el("g",{class:"cond"+(b.n==="SPARE"?" prov":""),"data-rref":b.n});
    grp.appendChild(el("line",{class:"ln",x1:x,y1:910,x2:x,y2:topY,stroke:color,"stroke-width":5}));
    grp.appendChild(el("path",{d:`M${x},${topY-2} l-6,12 l6,-4 l6,4 z`,fill:color}));
    grp.appendChild(el("circle",{cx:x,cy:920,r:5,fill:color}));
    g.appendChild(grp);
  });
  const lx=R+70;
  g.appendChild(txt(lx,150,"BUNDLES (left → right)","rlabel")).setAttribute("text-anchor","start");
  RISER_BUNDLES.forEach((b,i)=>{
    const yy=180+i*44, color=SVC[b.svc].color;
    g.appendChild(el("rect",{x:lx,y:yy-12,width:15,height:15,rx:3,fill:color}));
    const t1=txt(lx+24,yy,b.n,"");t1.setAttribute("font-size","13");t1.setAttribute("font-weight","700");t1.setAttribute("fill","#1C1C1E");
    g.appendChild(t1);
    const t2=txt(lx+24,yy+16,b.txt,"rsub");t2.setAttribute("text-anchor","start");
    g.appendChild(t2);
  });
}

/* ============================================================
   TERRACE (roof) view — Sintex JB + what reaches the top
   ============================================================ */
function drawTerrace(g){
  g.appendChild(el("rect",{x:120,y:150,width:760,height:780,class:"wall","stroke-width":3}));
  const par=el("rect",{x:142,y:172,width:716,height:736,fill:"none",stroke:"#C9C3B2","stroke-width":1.5});
  par.setAttribute("stroke-dasharray","6,5"); g.appendChild(par);
  g.appendChild(txt(500,138,"TERRACE (roof level)","rlabel"));
  g.appendChild(txt(500,922,"parapet wall","rsub"));
  // corner tags (orientation: S top, N bottom, E left, W right)
  g.appendChild(txt(170,196,"SE","rsub")); g.appendChild(txt(830,196,"SW","rsub"));
  g.appendChild(txt(170,892,"NE","rsub")); g.appendChild(txt(830,892,"NW","rsub"));
  // stair exit from FF + riser arrival
  g.appendChild(el("rect",{x:600,y:710,width:130,height:95,class:"wall"}));
  g.appendChild(txt(665,700,"stair up from FF","rsub"));
  const ax=662,ay=722;
  function tl(x1,y1,x2,y2,color,dash,wd){
    const p=el("path",{d:`M${x1},${y1} L${x1},${y2} L${x2},${y2}`,fill:"none",stroke:color,
      "stroke-width":wd||4,"stroke-linecap":"round","stroke-linejoin":"round"});
    if(dash)p.setAttribute("stroke-dasharray","7,5"); g.appendChild(p);
  }
  tl(ax,ay,790,318,SVC.water.color,false,5);      // W1 sensor TERMINATES at the tank JB
  tl(ax-24,ay,648,790,SVC.data.color,true,4);     // CAM-5 to parapet
  // W2 float DEPARTS the tank back down the riser to the DB cupboard
  const w2=el("path",{d:"M828,316 L860,316 L860,650 L700,650",fill:"none",stroke:SVC.water.color,
    "stroke-width":4,"stroke-dasharray":"7,5","stroke-linecap":"round","stroke-linejoin":"round"});
  g.appendChild(w2);
  g.appendChild(txt(745,395,"W1 ↑","rsub")); g.appendChild(txt(885,470,"W2 ↓","rsub"));
  g.appendChild(txt(610,775,"CAM-5","rsub"));
  g.appendChild(el("circle",{cx:ax,cy:ay,r:6,fill:"#1C1C1E"}));
  g.appendChild(txt(ax,ay+20,"riser arrives (D9 + W1 + CAM-5)","rsub"));
  // Sintex tank at the SW corner (top-right) — TAPPABLE, opens the Sintex JB guide
  const tank=el("g",{class:"dev","data-id":"JB-SINTEX"});
  tank.appendChild(el("circle",{cx:800,cy:262,r:58,fill:"#EAF4EF",stroke:SVC.water.color,"stroke-width":2}));
  tank.appendChild(txt(800,250,"SINTEX","rsub"));
  tank.appendChild(txt(800,265,"1500L","rsub"));
  const jb=txt(800,286,"⊙ Sintex JB",""); jb.setAttribute("font-size","10"); jb.setAttribute("font-weight","700"); jb.setAttribute("fill",SVC.water.color);
  tank.appendChild(jb);
  tank.addEventListener("click",e=>{e.stopPropagation();openGuide("JB-SINTEX");});
  g.appendChild(tank);
  // mini legend
  g.appendChild(txt(250,470,"W1 = Sintex sensor Cat6 (PoE) — terminates at the tank JB","rsub")).setAttribute("text-anchor","start");
  g.appendChild(txt(250,492,"W2 = Sintex float — departs down to the DB cupboard","rsub")).setAttribute("text-anchor","start");
  g.appendChild(txt(250,514,"CAM-5 = terrace parapet camera","rsub")).setAttribute("text-anchor","start");
  g.appendChild(txt(250,540,"Tap the tank for the full Sintex JB install guide","rsub")).setAttribute("text-anchor","start");
}

/* ============================================================
   STATE + INTERACTION
   ============================================================ */
let floor="GF", active=new Set(DEFAULT_ACTIVE), selRef=null, query="";

/* Filter model (mobile-friendly):
   - tap a service/Components chip = SOLO it (show only that). Tap it again = back to Automation.
   - "Automation" preset = the 4 automation layers. "All" preset = everything incl. power. */
function buildChips(){
  const c=document.getElementById("chips"); c.innerHTML="";
  const mk=(html,cls)=>{const b=document.createElement("button");b.className="chip"+(cls||"");b.innerHTML=html;return b;};
  const auto=mk("Automation"); auto.dataset.key="preset-auto";
  auto.onclick=()=>{active=new Set(DEFAULT_ACTIVE);syncChips();apply();};
  const all=mk("All"); all.dataset.key="preset-all";
  all.onclick=()=>{active=new Set();syncChips();apply();};
  const none=mk("None"); none.dataset.key="preset-none";
  none.onclick=()=>{active=new Set(["__none__"]);syncChips();apply();};
  c.appendChild(auto); c.appendChild(all); c.appendChild(none);
  SVC_ORDER.forEach(k=>{
    const b=mk(`<span class="sw" style="background:${SVC[k].color}"></span>${SVC[k].label}`);
    b.dataset.svc=k;
    b.onclick=()=>{ active.delete("__none__"); active.has(k)?active.delete(k):active.add(k); syncChips(); apply(); };
    c.appendChild(b);
  });
  const comp=mk(`<span class="sw" style="background:#2F2C28"></span>Components`); comp.dataset.key="components";
  comp.onclick=()=>{ active.delete("__none__"); active.has("components")?active.delete("components"):active.add("components"); syncChips(); apply(); };
  c.appendChild(comp);
  syncChips();
}
function syncChips(){
  const isAuto = active.size===DEFAULT_ACTIVE.length && DEFAULT_ACTIVE.every(k=>active.has(k));
  document.querySelectorAll(".chip").forEach(b=>{
    let on=false;
    if(b.dataset.key==="preset-auto") on=isAuto;
    else if(b.dataset.key==="preset-all") on=active.size===0;
    else if(b.dataset.key==="preset-none") on=active.has("__none__");
    else if(b.dataset.svc) on=active.has(b.dataset.svc);
    else if(b.dataset.key==="components") on=active.has("components");
    b.classList.toggle("on",on); b.classList.toggle("off",!on);
  });
}
function buildLegend(){
  const lg=document.getElementById("legend");
  let h='<span class="it" style="font-weight:700;color:#1C1C1E">LEGEND:</span>';
  ["data","lv16","water","power_light","power_heavy"].forEach(k=>{
    h+=`<span class="it"><svg width="34" height="10"><line x1="2" y1="5" x2="32" y2="5" stroke="${SVC[k].color}" stroke-width="4"/></svg>${SVC[k].label} <span style="opacity:.7">(${SVC[k].pvc})</span></span>`;
  });
  h+=`<span class="it"><svg width="16" height="16"><circle cx="8" cy="9" r="6" fill="#fff" stroke="${SVC.presence.color}" stroke-width="1.4"/><circle cx="8" cy="10" r="1.8" fill="${SVC.presence.color}"/></svg>mmWave presence (wired 5V)</span>`;
  h+=`<span class="it"><svg width="20" height="14"><rect x="1" y="2" width="18" height="11" rx="3" fill="#2F2C28"/><circle cx="6" cy="7.5" r="2.6" fill="#fff"/></svg>Dark box = component (tap for install guide)</span>`;
  h+=`<span class="it"><svg width="34" height="10"><line x1="2" y1="5" x2="32" y2="5" stroke="#1C1C1E" stroke-width="4"/></svg>Solid = pull cable now</span>`;
  h+=`<span class="it"><svg width="34" height="10"><line x1="2" y1="5" x2="32" y2="5" stroke="#1C1C1E" stroke-width="4" stroke-dasharray="6,4"/></svg>Dashed = pull string only</span>`;
  h+=`<span class="it"><svg width="14" height="14"><rect x="1" y="1" width="12" height="12" rx="2" fill="#FFE650" stroke="#1C1C1E"/></svg>Server</span>`;
  h+=`<span class="it"><svg width="14" height="14"><rect x="1" y="1" width="12" height="12" rx="2" fill="#C8F0DC" stroke="#1C1C1E"/></svg>DB cupboard</span>`;
  lg.innerHTML=h;
}

function apply(){
  const conds=document.querySelectorAll(`#view-${floor} .cond`);
  conds.forEach(g=>{
    const ref=g.dataset.ref; const c=CONDUITS.find(x=>x.ref===ref); if(!c)return;
    const passSvc = active.size===0 || active.has(c.service);
    const passQ = !query || c.ref.toLowerCase().includes(query) || c.to.toLowerCase().includes(query)
                  || c.from.toLowerCase().includes(query) || c.contents.toLowerCase().includes(query);
    const visible = passSvc && passQ;
    g.classList.toggle("dim", !visible);
    const emph = visible && (ref===selRef || (query&&passQ) || (active.size>0&&active.size<=2));
    g.classList.toggle("emph", emph);
  });
  // mmWave markers follow the presence chip + search
  document.querySelectorAll(`#view-${floor} .mw`).forEach(g=>{
    const ref=g.dataset.ref; const m=MMWAVE.find(x=>x.ref===ref);
    const passSvc = active.size===0 || active.has("presence");
    const passQ = !query || ref.toLowerCase().includes(query) || (m&&m.room.toLowerCase().includes(query));
    g.classList.toggle("dim", !(passSvc&&passQ));
  });
  // component tags follow the service filter + search; dimmed ones are non-clickable
  document.querySelectorAll(`#view-${floor} .dev`).forEach(g=>{
    const id=g.dataset.id; const d=DEVICES.find(x=>x.id===id);
    const passSvc = active.size===0 || active.has("components"); // components are their own layer
    const passQ=!query || id.toLowerCase().includes(query) || (d&&d.label.toLowerCase().includes(query));
    g.classList.toggle("dim", !(passSvc&&passQ));
  });
}

function setFloor(f){
  floor=f; selRef=null; closePanel(); closeGuide();
  document.querySelectorAll(".tab").forEach(t=>t.classList.toggle("on",t.dataset.floor===f));
  document.querySelectorAll(".view").forEach(v=>v.classList.add("hide"));
  document.getElementById("view-"+f).classList.remove("hide");
  document.getElementById("compass").style.display = f==="RISER"?"none":"block";
  document.getElementById("doorhint").style.display = (f==="GF"||f==="FF")?"block":"none";
  resetVB();
  apply();
}

/* conduit detail panel */
function select(ref){
  const c=CONDUITS.find(x=>x.ref===ref); if(!c)return;
  selRef=ref;
  const col=SVC[c.service].color;
  document.getElementById("p-ref").textContent=c.ref;
  document.getElementById("p-ref").style.background=col;
  document.getElementById("p-size").textContent=`${SVC[c.service].label} · ${c.size} · ${SVC[c.service].pvc}`;
  const badge=document.getElementById("p-badge");
  badge.textContent=c.status==="provision"?"Pull string only":"Pull cable now";
  badge.className="badge "+(c.status==="provision"?"prov":"live");
  document.getElementById("p-route").innerHTML=
    `<span>${c.from}</span><span class="arr">→</span><span>${c.to}</span>`;
  document.getElementById("p-contents").textContent=c.contents;
  const ef=document.getElementById("p-explainfld");
  if(c.explain){document.getElementById("p-explain").textContent=c.explain; ef.style.display="";}
  else ef.style.display="none";
  const nf=document.getElementById("p-notefld");
  if(c.note){document.getElementById("p-note").textContent=c.note; nf.style.display="";}
  else nf.style.display="none";
  // offer an install guide if this conduit feeds a device that has one
  const gid=guideForConduit(ref);
  const gb=document.getElementById("p-guide");
  if(gid){gb.style.display=""; gb.textContent="Open install guide → "+(GUIDES[gid].title);
    gb.onclick=()=>openGuide(gid);}
  else gb.style.display="none";
  document.getElementById("panel").classList.add("open");
  document.getElementById("scrim").classList.add("on");
  apply();
}
function guideForConduit(ref){
  for(const id in GUIDES){if((GUIDES[id].related||[]).includes(ref))return id;}
  return null;
}
function syncScrim(){
  const open=document.getElementById("panel").classList.contains("open")
          || document.getElementById("guide").classList.contains("open");
  document.getElementById("scrim").classList.toggle("on",open);
}
function closePanel(){
  document.getElementById("panel").classList.remove("open");
  selRef=null; syncScrim(); apply();
}

/* install-guide panel */
function renderGuide(G){
  document.getElementById("panel").classList.remove("open");
  document.getElementById("g-title").textContent=G.title;
  document.getElementById("g-sub").textContent=G.sub||"";
  const ic=document.getElementById("g-icon");
  ic.style.background=SVC[G.svc]?SVC[G.svc].color:(G.color||"#1C1C1E");
  ic.textContent=G.glyph||"i";
  document.getElementById("g-body").innerHTML=buildGuideBody(G);
  document.querySelectorAll("#g-body .grel button").forEach(b=>b.onclick=()=>flashConduit(b.dataset.rel));
  document.getElementById("guide").classList.add("open");
  document.getElementById("scrim").classList.add("on");
}
function openGuide(id){const G=GUIDES[id]; if(G)renderGuide(G);}
/* if components overlap at the tapped spot, show a chooser first; otherwise open directly */
function devCluster(id){const d=DEVICES.find(x=>x.id===id); if(!d)return [];
  return DEVICES.filter(x=>x.floor===d.floor && Math.hypot(x.xy[0]-d.xy[0],x.xy[1]-d.xy[1])<30);}
function openDeviceAt(id){const cl=devCluster(id); if(cl.length>1) renderChooser(cl); else openGuide(id);}
function renderChooser(list){
  document.getElementById("panel").classList.remove("open");
  document.getElementById("g-title").textContent="Components here";
  document.getElementById("g-sub").textContent="A few components overlap — pick one";
  const ic=document.getElementById("g-icon"); ic.style.background="#2F2C28"; ic.textContent="▤";
  document.getElementById("g-body").innerHTML=`<div class="gsec"><div class="grel" style="flex-direction:column;align-items:stretch;gap:8px">`+
    list.map(d=>`<button data-pick="${d.id}" style="text-align:left;padding:11px 13px;font-size:13px">${GUIDES[d.id]?GUIDES[d.id].title:d.label}</button>`).join("")+`</div></div>`;
  document.querySelectorAll("#g-body [data-pick]").forEach(b=>b.onclick=()=>openGuide(b.dataset.pick));
  document.getElementById("guide").classList.add("open");
  document.getElementById("scrim").classList.add("on");
}
function openMmwave(ref){
  const m=MMWAVE.find(x=>x.ref===ref); if(!m)return;
  renderGuide({
    title:`mmWave presence — ${m.room}`, sub:`${m.mount} · ${m.powerShort}`,
    color:SVC.presence.color, glyph:"))",
    badge:"sensor — location only",
    inside:["mmWave presence sensor (model TBD: Aqara FP2 (Zigbee) or ESP32 + LD2410C)","Reports presence to Home Assistant"],
    power:m.power,
    mount:m.mountNote,
    note:"No dedicated conduit is being chased for these — power is by wire off the normal line (already discussed with the electrician). They talk to Home Assistant over Wi-Fi via the GF/FF ceiling APs; HA then drives the existing Sonoff lighting relays.",
    steps:[`Provide 5V at the point: ${m.powerShort}.`,"Mount the sensor with a clear view of the room.","Pair to Home Assistant (Zigbee for FP2, or Wi-Fi / ESPHome for LD2410).","In HA, map presence → the room's existing Sonoff lighting relay."]
  });
}
/* resolve an asset path: hosted = relative path; offline = inline data URI from window.__ASSETS */
function assetUrl(p){return (window.__ASSETS&&window.__ASSETS[p])||p;}
function buildGuideBody(G){
  let h="";
  if(G.badge){const cls=G.live===false?"prov":(G.glyph==="))"?"sensor":"live");
    h+=`<div class="gsec"><span class="badge ${cls}">${G.badge}</span></div>`;}
  if(G.inside&&G.inside.length) h+=`<div class="gsec"><h4>What's inside</h4><ul>${G.inside.map(x=>`<li>${x}</li>`).join("")}</ul></div>`;
  if(G.power) h+=`<div class="gsec"><h4>Power</h4><p>${G.power}</p></div>`;
  if(G.mount) h+=`<div class="gsec"><h4>Mounting</h4><p>${G.mount}</p></div>`;
  if(G.sensor) h+=`<div class="gsec"><h4>Sensor</h4><p>${G.sensor}</p></div>`;
  if(G.note) h+=`<div class="gsec"><div class="gnote">${G.note}</div></div>`;
  if(G.steps&&G.steps.length) h+=`<div class="gsec"><h4>Step by step</h4><ol class="gsteps">${G.steps.map(x=>`<li>${x}</li>`).join("")}</ol></div>`;
  if(G.imgs&&G.imgs.length) h+=`<div class="gsec gimgs"><h4>Reference images</h4>${G.imgs.map(s=>`<img loading="lazy" src="${assetUrl('assets/img/'+s)}" alt="">`).join("")}</div>`;
  if(G.related&&G.related.length) h+=`<div class="gsec"><h4>Conduits feeding this (tap to find on plan)</h4><div class="grel">${G.related.map(r=>`<button data-rel="${r}">${r}</button>`).join("")}</div></div>`;
  if(G.pdf && !window.__OFFLINE) h+=`<div class="gsec"><a class="gpdf" href="${assetUrl('assets/pdf/'+G.pdf)}" target="_blank" rel="noopener">Open the full PDF</a></div>`;
  return h;
}
function closeGuide(){document.getElementById("guide").classList.remove("open"); syncScrim();}

/* flash a conduit on the plan (switching floor if needed) */
function flashConduit(ref){
  const c=CONDUITS.find(x=>x.ref===ref); if(!c)return;
  closeGuide(); closePanel();
  if(c.floor!==floor) setFloor(c.floor);
  setTimeout(()=>{
    const g=document.querySelector(`#view-${c.floor} .cond[data-ref="${ref}"]`);
    if(g){g.classList.add("flash"); setTimeout(()=>g.classList.remove("flash"),1300);}
  },200);
}
/* flash the selected conduit from the detail panel */
function locate(){
  if(!selRef)return;
  const g=document.querySelector(`#view-${floor} .cond[data-ref="${selRef}"]`);
  if(!g)return;
  closePanel();
  setTimeout(()=>{g.classList.add("flash"); setTimeout(()=>g.classList.remove("flash"),1100);},150);
}

/* print cheat sheet */
function buildSheet(){
  const s=document.getElementById("sheet");
  let h="<h2>Conduit cheat sheet — automation focus</h2><table><thead><tr><th>Ref</th><th>Floor</th><th>Service</th><th>Size</th><th>Status</th><th>From &rarr; To</th><th>Contents / note</th></tr></thead><tbody>";
  ["data","lv16","water","power_light","power_heavy"].forEach(k=>{
    h+=`<tr class="sgrp"><td colspan="7">${SVC[k].label} &mdash; ${SVC[k].pvc}</td></tr>`;
    CONDUITS.filter(c=>c.service===k).forEach(c=>{
      h+=`<tr><td><b>${c.ref}</b></td><td>${c.floor}</td><td>${SVC[c.service].label}</td><td>${c.size}</td>`+
         `<td>${c.status==="provision"?"STRING":"CABLE"}</td><td>${c.from} &rarr; ${c.to}</td>`+
         `<td>${c.contents}${c.note?" &mdash; "+c.note:""}</td></tr>`;
    });
  });
  h+=`<tr class="sgrp"><td colspan="7">Presence (mmWave) — wired 5V, no conduit</td></tr>`;
  MMWAVE.forEach(m=>{
    h+=`<tr><td><b>${m.ref}</b></td><td>${m.floor}</td><td>mmWave</td><td>—</td><td>${m.mount}</td><td>${m.room}</td><td>${m.power}</td></tr>`;
  });
  h+="</tbody></table>";
  s.innerHTML=h;
}

/* ============================================================
   ZOOM / PAN
   ============================================================ */
const BASE={x:0,y:0,w:1000,h:1085};
let vb={x:0,y:0,w:1000,h:1085};
const planEl=document.getElementById("plan");
function applyVB(){planEl.setAttribute("viewBox",`${vb.x} ${vb.y} ${vb.w} ${vb.h}`);}
function clampVB(){
  const minW=BASE.w*0.16, maxW=BASE.w;
  vb.w=Math.max(minW,Math.min(maxW,vb.w));
  vb.h=vb.w*(BASE.h/BASE.w);
  const ox=BASE.w*0.12, oy=BASE.h*0.12;
  vb.x=Math.max(BASE.x-ox, Math.min(BASE.x+BASE.w-vb.w+ox, vb.x));
  vb.y=Math.max(BASE.y-oy, Math.min(BASE.y+BASE.h-vb.h+oy, vb.y));
}
function resetVB(){vb={x:BASE.x,y:BASE.y,w:BASE.w,h:BASE.h};applyVB();}
function metrics(){
  const r=planEl.getBoundingClientRect();
  const scale=Math.min(r.width/vb.w, r.height/vb.h);
  return {r,scale,offX:(r.width-vb.w*scale)/2, offY:(r.height-vb.h*scale)/2};
}
function toVB(cx,cy){const m=metrics();return {x:vb.x+(cx-m.r.left-m.offX)/m.scale, y:vb.y+(cy-m.r.top-m.offY)/m.scale};}
function zoomAt(vx,vy,f){const nw=Math.max(BASE.w*0.16,Math.min(BASE.w,vb.w*f));
  vb.x=vx-(vx-vb.x)*(nw/vb.w); vb.y=vy-(vy-vb.y)*(nw/vb.w); vb.w=nw; clampVB(); applyVB();}
function zoomCenter(f){const m=metrics();const c=toVB(m.r.left+m.r.width/2,m.r.top+m.r.height/2);zoomAt(c.x,c.y,f);}
function toggleFull(){
  const el=document.documentElement;
  const fs=document.fullscreenElement||document.webkitFullscreenElement;
  if(!fs){ const rq=el.requestFullscreen||el.webkitRequestFullscreen; if(rq)try{rq.call(el);}catch(e){} document.body.classList.add("maxed"); }
  else { const ex=document.exitFullscreen||document.webkitExitFullscreen; if(ex)try{ex.call(document);}catch(e){} document.body.classList.remove("maxed"); }
  setTimeout(resetVB,180);
}

let dragging=false,moved=false,sx=0,sy=0,sox=0,soy=0,suppress=false,pinchD=0;
function tdist(t){return Math.hypot(t[0].clientX-t[1].clientX,t[0].clientY-t[1].clientY);}
function tmid(t){return {x:(t[0].clientX+t[1].clientX)/2,y:(t[0].clientY+t[1].clientY)/2};}
planEl.addEventListener("touchstart",e=>{ if(e.touches.length===2){pinchD=tdist(e.touches);dragging=false;} },{passive:true});
planEl.addEventListener("touchmove",e=>{
  if(e.touches.length===2){ e.preventDefault();
    const nd=tdist(e.touches);
    if(pinchD){ const mid=tmid(e.touches), c=toVB(mid.x,mid.y); zoomAt(c.x,c.y,pinchD/nd); pinchD=nd; moved=true; suppress=true; }
  }
},{passive:false});
planEl.addEventListener("pointerdown",e=>{dragging=true;moved=false;sx=e.clientX;sy=e.clientY;sox=vb.x;soy=vb.y;});
window.addEventListener("pointermove",e=>{
  if(!dragging)return;
  if(Math.hypot(e.clientX-sx,e.clientY-sy)>6) moved=true;
  if(moved){ const m=metrics(); vb.x=sox-(e.clientX-sx)/m.scale; vb.y=soy-(e.clientY-sy)/m.scale; clampVB(); applyVB(); }
});
window.addEventListener("pointerup",()=>{ if(moved)suppress=true; dragging=false; });
planEl.addEventListener("click",e=>{ if(suppress){e.stopImmediatePropagation();e.preventDefault();suppress=false;} },true);
planEl.addEventListener("wheel",e=>{e.preventDefault();const c=toVB(e.clientX,e.clientY);zoomAt(c.x,c.y,e.deltaY>0?1.12:0.89);},{passive:false});

/* ============================================================
   INIT
   ============================================================ */
function init(){
  ["GF","FF"].forEach(f=>{
    const v=document.getElementById("view-"+f);
    drawPlan(f,v); drawConduits(f,v); drawHubs(f,v); drawMmwave(f,v); drawDevices(f,v);
  });
  drawRiser(document.getElementById("view-RISER"));
  const vt=document.getElementById("view-TERRACE");
  drawTerrace(vt); drawDevices("TERRACE",vt);
  buildChips(); buildLegend(); buildSheet();

  document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>setFloor(t.dataset.floor));
  document.getElementById("p-close").onclick=closePanel;
  document.getElementById("p-locate").onclick=locate;
  document.getElementById("g-close").onclick=closeGuide;
  document.getElementById("scrim").onclick=()=>{closePanel();closeGuide();};
  document.getElementById("search").addEventListener("input",e=>{query=e.target.value.trim().toLowerCase();apply();});
  document.getElementById("plan").addEventListener("click",()=>{closePanel();closeGuide();});
  document.addEventListener("keydown",e=>{if(e.key==="Escape"){closePanel();closeGuide();}});

  document.getElementById("zin").onclick=()=>zoomCenter(0.7);
  document.getElementById("zout").onclick=()=>zoomCenter(1.43);
  document.getElementById("zreset").onclick=resetVB;
  document.getElementById("zfull").onclick=toggleFull;
  document.getElementById("rotdismiss").onclick=()=>{document.getElementById("rotate").style.display="none";};

  setFloor("GF");
}
init();
