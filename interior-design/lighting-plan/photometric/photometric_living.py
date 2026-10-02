#!/usr/bin/env python3
"""
Photometric verification — double-height living room (GF) of the Chitradurga house.

Computes direct + indirect illuminance (lux) on the living-room floor grid, on key receiving
surfaces (coffee table, sofa seat, TV wall, curtain, stair treads, landing) for several lighting
scenes, using the fixture POSITIONS from ../lighting-data.js (single source of truth) and the
photometric parameters below, every one of which is tagged with its provenance:

   DOC-CAT  = TISVA Architectural Catalogue 2023 (Usha International; public PDF)
   DOC-PL   = TISVA Architectural Product list May-25 (the price list used for the design)
   DOC-OTH  = another manufacturer's published figure (smart bulbs)
   EST      = estimate (no TISVA photometric data exists; basis stated)
   CALC     = calculated here from the above
   FIT      = intensity-distribution shape fitted to TISVA's published polar curve / table

Model: each fixture = point source with an axially-symmetric intensity distribution
I(a) = sum of Gaussians (50 %-angle = nominal beam / 2 for the core, plus a wide skirt where the
catalogue data shows one), normalised to the fixture lumens. Illuminance on a surface point:
E = I(a) * cos(incidence) / d^2  (inverse-square + cosine law).  LED strips = Lambertian line
sources discretised into 50 mm segments.  Indirect light = room-cavity (flux-balance)
approximation with stated reflectances and an enclosure factor for the openings.
Outputs: results.json, tables.md, heatmap PNGs, section SVG (all in this folder).
Run:  python3 photometric_living.py
"""
import json, math, os, subprocess, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
FT = 0.3048

# ----------------------------------------------------------------------------- geometry from lighting-data.js
geo = json.loads(subprocess.run(["node", "-e", r"""
const L=require(process.argv[1]);const F=L.floors.GF;
console.log(JSON.stringify({fixtures:F.fixtures,strips:F.strips,services:F.services,rooms:F.rooms,voidRect:F.voidRect,
 pelmet:L.floors.FF.strips.find(s=>s.id==='S20')}));
""", str(HERE.parent / "lighting-data.js")], capture_output=True, text=True, check=True).stdout)
FX = {f["id"]: f for f in geo["fixtures"]}

# Heights (m above GF finished floor)                                            provenance: design doc §3/§4.6
H_STRIP_CEIL = 9 * FT          # 2.743 m  Rega Plus in the south-strip false ceiling
H_BEAM       = 11 * FT         # 3.353 m  soffit of the FF-slab edge beams (profile + track)
H_AXIOS      = H_BEAM - 0.20   # Axios 20W body is 25.5 cm tall (DOC-CAT); optical centre ~0.20 m below the track
H_LID        = 20.5 * FT       # 6.25 m   void-lid false ceiling (proposed)
H_PELMET     = 6.10            # strip inside the recessed pelmet
H_LANDING    = 6 * FT          # 1.83 m   half-landing floor (11 risers of ~166 mm)
H_FF         = 11.5 * FT       # 3.51 m   FF finished floor (slab 11 ft + finish)
PENDANT_XY   = (18.7, 31.4)
PENDANT_Z    = [2.6, 2.9, 3.2, 3.5, 3.8, 4.1, 4.4, 4.7, 5.0, 5.3]   # 10 globes, bottom 2.6 m, vertical cluster
PENDANT_OFF  = [(0,0),(0.3,0.1),(-0.25,0.2),(0.1,-0.3),(-0.3,-0.15),(0.35,-0.2),(-0.1,0.35),(0.2,0.3),(-0.35,0),(0.05,-0.1)]  # m

# ----------------------------------------------------------------------------- photometric parameters
# Each source type: lumens, distribution = list of (weight_fraction_of_peak, half_angle_deg); peak_factor applied to
# the analytic Gaussian peak to reproduce the measured "spill" seen in TISVA's own tables (Fugl: documented
# Enadir 1812 lx vs Gaussian 1995 lx -> 0.91).
P = {
 # --- documented ---
 "AXSP20": dict(lm=1600, cri=">80", cct="3000K", dist=None, peak_factor=0.91,
                src="DOC-CAT p.59: Axios Pro 20W black 3000K = 1600 lm, beam 15/24/38/60 selectable, CRI>80. No polar curve published -> single Gaussian at the chosen optic, 0.91 peak factor (CALC/EST)."),
 # --- estimated (not in any TISVA photometric document) ---
 "REGA12": dict(lm=900, cri=">90 (DOC-PL)", cct="3000K", dist="orrin13", peak_factor=1.0,
                src="EST: lumens 850-950 (TISVA COB downlights run 79-81 lm/W: Orrin 13W 1050 lm, Galaxy Pro 12W 960 lm, GVO 12W 950 lm; CRI>90 chips give ~10% less). Beam 38 deg inferred from code pattern ...338... Shape = FIT to Orrin 13W (DOC-CAT p.39) as the deep-recessed analogue; soft-shape case uses the Orrin 7.5W fit."),
 "REGA7":  dict(lm=520, cri=">90 (DOC-PL)", cct="3000K", dist="orrin75", peak_factor=1.0,
                src="EST: 500-560 lm (Orrin 7.5W = 600 lm at CRI80). Shape = FIT to Orrin 7.5W polar (peak ~1227 cd/klm) + table (p.37)."),
 "BOLT12": dict(lm=900, cri=">80", cct="3000K", dist=None, beam=36, peak_factor=0.91,
                src="EST: Rio SF 12W surface cylinder (TISVA, same family) is quoted >75 lm/W -> ~900 lm; beam 36 deg assumed (typical surface COB cylinder)."),
 "BOLT6":  dict(lm=450, cri=">80", cct="3000K", dist=None, beam=36, peak_factor=0.91, src="EST: half of Bolt 12W."),
 "SPOTLIT":dict(lm=140, cri="n/a", cct="3000K", dist=None, beam=120, peak_factor=1.0,
                src="EST: 2W PC downlighter, 120 deg (DOC-PL); ~70 lm/W -> 140 lm (+/-30)."),
 "LS3K":   dict(lm_per_m=900, eff=0.70, cri="NOT PUBLISHED", cct="3000K",
                src="EST: Lumelace 10 W/m 120 LED/m 3000K (DOC-CAT p.75 gives W/m only). Typical 2835 strips 80-110 lm/W -> 800-1100 lm/m; 0.70 transmission for the opal profile diffuser."),
 "BULB":   dict(lm=806, eff=0.75, cri="80", cct="3000K (tunable)",
                src="DOC-OTH: Philips Hue White Ambiance / IKEA Tradfri E27 = 806 lm (ACCEPTED design value 2026-10-02; the earlier 470 lm E14 assumption is kept as a sensitivity case); 0.75 transmission for an opal glass globe (EST)."),
 "LAMP":   dict(lm=800, eff=0.6, src="EST: decor floor lamp with an 800 lm bulb, fabric shade (60% out, mostly up/down)."),
}
# Intensity shapes fitted to the TISVA Orrin data (cd per klm vs angle). Two-Gaussian: core + skirt.
#  orrin75 : peak 1227 cd/klm (polar, DOC-CAT p.38), table: 30% of flux inside the 41.6 deg cone at 1 m.
#  orrin13 : peak ~3000 cd/klm (polar p.40, ring max 3181), table: 27% of flux inside the 32 deg cone at 1 m.
SHAPES = {
 "orrin75": [(0.79, 19.0), (0.21, 45.0)],   # weights of peak, half-angles (deg); normalised to lumens below
 "orrin13": [(0.80, 11.5), (0.20, 40.0)],
}

def gauss_int(hdeg):
    """integral_0^90 exp(-ln2 (a/h)^2) sin a da  (numerical)"""
    a = np.linspace(0, math.pi/2, 2000); h = math.radians(hdeg)
    return np.trapezoid(np.exp(-math.log(2)*(a/h)**2)*np.sin(a), a)

class Src:
    """Point source with intensity I(alpha) [cd]; alpha = angle from the aim axis."""
    def __init__(self, pos, lm, shape=None, beam=None, aim=None, peak_factor=1.0, label=""):
        self.pos = np.array(pos, float); self.label = label
        self.aim = np.array(aim if aim is not None else (0,0,-1), float); self.aim /= np.linalg.norm(self.aim)
        if shape is None:
            shape = [(1.0, beam/2)]
        ws = np.array([w for w,_ in shape]); hs = [h for _,h in shape]
        # I(a) = I0 * sum w_i exp(-ln2 (a/h_i)^2); flux = 2*pi*I0*sum w_i*G(h_i)  => I0
        G = np.array([gauss_int(h) for h in hs])
        self.I0 = lm / (2*math.pi*float((ws*G).sum())) * peak_factor
        self.shape = list(zip(ws, hs)); self.lm = lm
    def I(self, alpha):
        return self.I0 * sum(w*np.exp(-math.log(2)*(alpha/math.radians(h))**2) for w,h in self.shape)
    def E(self, pts, normal):
        """illuminance at points (N,3) on a plane with unit normal (3,)"""
        v = pts - self.pos                      # source -> point
        d = np.linalg.norm(v, axis=1); u = v/d[:,None]
        cosa = np.clip(u @ self.aim, -1, 1); alpha = np.arccos(cosa)
        cosi = np.clip(-(u @ normal), 0, None)  # light must arrive from the front of the surface
        I = self.I(alpha); I = np.where(alpha > math.pi/2, 0, I)
        return I*cosi/d**2

def strip_sources(p0, p1, z, lm_per_m, face=(0,0,-1), step=0.05, label=""):
    """Lambertian line source along p0->p1 (ft, plan) at height z (m) -> list of Lambertian point sources"""
    a = np.array([p0[0]*FT, p0[1]*FT, z]); b = np.array([p1[0]*FT, p1[1]*FT, z])
    L = np.linalg.norm(b-a); n = max(1, int(L/step)); out=[]
    for i in range(n):
        c = a + (b-a)*(i+0.5)/n
        out.append(Src(c, lm_per_m*L/n, shape=[(1.0, 60.0)], aim=face, peak_factor=1.0, label=label))  # 60 deg half-angle Gaussian ~ Lambertian
    return out

def ft3(x, y, z):  return np.array([x*FT, y*FT, z])

# ----------------------------------------------------------------------------- build the sources per scene
def axios(fid, beam, target):
    f = FX[fid]; pos = ft3(f["x"], f["y"], H_AXIOS); tgt = np.array(target)
    return Src(pos, P["AXSP20"]["lm"], beam=beam, aim=tgt-pos, peak_factor=P["AXSP20"]["peak_factor"], label=f"{fid} Axios 20W {beam}°")

TARGETS = {
 "stair":   ft3(20.5, 23.15, 2.5),          # upper flight, mid tread
 "tv":      ft3(27.0, 31.0, 2.5),           # feature panel, 2.5 m up
 "curtain": ft3(18.3, 36.8, 3.2),           # curtain, upper half (above eye line)
 "coffee":  ft3(18.7, 31.4, 0.45),          # coffee-table top (recommended 4th head)
}
OPTICS = {"F40": 38, "F41": 24, "F42": 60, "F43x": 24}

def build(scene, rega_shape="orrin13", fourth_head=False, bulb_lm=None, landing_fix="AVIA7", pelmet_mode="down"):
    S = []
    dim = scene
    def add(src, lvl):
        if lvl > 0:
            src.I0 *= lvl; src.lm *= lvl; S.append(src)
    # Rega Plus 12W x2 (south strip, 9 ft)
    for fid in ("F38","F39"):
        f = FX[fid]; add(Src(ft3(f["x"],f["y"],H_STRIP_CEIL), P["REGA12"]["lm"], shape=SHAPES[rega_shape], label=f"{fid} Rega Plus 12W"), dim["down"])
    # Rega Plus 7W: passage x2, hall, MBR passage (9 ft) — they spill into the living's edges
    for fid in ("F6","F7","F8","F9"):
        f = FX[fid]; add(Src(ft3(f["x"],f["y"],H_STRIP_CEIL), P["REGA7"]["lm"], shape=SHAPES["orrin75"], label=f"{fid} Rega Plus 7W"), dim["walk"])
    # Axios heads (E beam, 11 ft)
    add(axios("F40", OPTICS["F40"], TARGETS["stair"]), dim["track"])
    add(axios("F41", OPTICS["F41"], TARGETS["tv"]), dim["track"])
    add(axios("F42", OPTICS["F42"], TARGETS["curtain"]), dim["track"])
    if fourth_head:
        f = FX["F41"]; pos = ft3(f["x"], 28.4, H_AXIOS)
        add(Src(pos, P["AXSP20"]["lm"], beam=24, aim=TARGETS["coffee"]-pos, peak_factor=0.91, label="F43x Axios 20W 24° (proposed)"), dim["track"])
    # Beam-edge profile (S + E beams) facing down
    s10 = next(s for s in geo["strips"] if s["id"]=="S10"); lpm = P["LS3K"]["lm_per_m"]*P["LS3K"]["eff"]
    for seg in strip_sources(s10["pts"][0], s10["pts"][1], H_BEAM, lpm, label="S10 beam edge"): add(seg, dim["cove"])
    for seg in strip_sources(s10["pts2"][0], s10["pts2"][1], H_BEAM, lpm, label="S10 beam edge E"): add(seg, dim["cove"])
    # Curtain pelmet strip (void lid), facing down, 0.1 m off the curtain
    pel = geo["pelmet"]
    if pelmet_mode == "down":      # as drawn: profile facing straight down, 76 mm off the fabric
        for seg in strip_sources((pel["pts"][0][0], 36.55), (pel["pts"][1][0], 36.55), H_PELMET, lpm, label="S20 pelmet"): add(seg, dim["pelmet"])
    else:                          # recommended: asymmetric/angled profile tilted 45 deg toward the fabric, 150 mm off it
        for seg in strip_sources((pel["pts"][0][0], 36.3), (pel["pts"][1][0], 36.3), H_PELMET, lpm, face=(0, 0.7071, -0.7071), label="S20 pelmet"): add(seg, dim["pelmet"])
    # TV unit strips: vertical reveals facing the wall -> modelled as 50% of flux emitted sideways into the room at 1.6 m
    for seg in strip_sources((26.6, 28.5), (26.6, 34.5), 1.6, 0.5*lpm, face=(-1,0,0), label="S11 TV unit"): add(seg, dim["tv"])
    # Pendant cluster: smart bulbs, isotropic (opal globes)
    blm = (bulb_lm or P["BULB"]["lm"]) * P["BULB"]["eff"]
    for z,(ox,oy) in zip(PENDANT_Z, PENDANT_OFF):
        pos = ft3(*PENDANT_XY, z) + np.array([ox,oy,0])
        add(Src(pos, blm, shape=[(1.0, 1000.0)], aim=(0,0,-1), label="pendant globe"), dim["pendant"])   # h=1000 deg -> isotropic
    # Floor lamp beside the accent chairs (decor), shade at 1.5 m: 60% of 800 lm, half down half up
    lampxy = (16.0, 25.9)
    add(Src(ft3(*lampxy, 1.5), P["LAMP"]["lm"]*P["LAMP"]["eff"]*0.5, shape=[(1.0,60.0)], aim=(0,0,-1), label="floor lamp (down)"), dim["lamp"])
    add(Src(ft3(*lampxy, 1.5), P["LAMP"]["lm"]*P["LAMP"]["eff"]*0.5, shape=[(1.0,60.0)], aim=(0,0,1), label="floor lamp (up)"), dim["lamp"])
    # Stair: Bolt over the half landing (11 ft soffit), Spotlit foot-lights (wall y=17.5 facing N, 0.3 m above tread)
    f = FX["F37"]
    if landing_fix == "AVIA7":     # ACCEPTED 2026-10-02: Avia 7W surface spot on the landing soffit, aimed at the stair feature wall above flight 1
        pos = ft3(f["x"], f["y"], H_BEAM-0.10); tgt = ft3(23.0, 17.55, 2.6)
        add(Src(pos, 520, beam=36, aim=tgt-pos, peak_factor=0.91, label="F37 AVIA7 -> stair wall"), dim["stair"])
    else:
        add(Src(ft3(f["x"],f["y"],H_BEAM-0.10), P[landing_fix]["lm"], beam=P[landing_fix]["beam"], peak_factor=0.91, label=f"F37 {landing_fix}"), dim["stair"])
    for fid in ("F31","F32","F33","F34","F35"):
        f = FX[fid]; z_tread = tread_z(f["x"], flight=1) + 0.3
        add(Src(ft3(f["x"], 17.55, z_tread), P["SPOTLIT"]["lm"], beam=120, aim=(0,1,0), label=f"{fid} Spotlit"), dim["stair"])
    f = FX["F36"]; add(Src(ft3(26.95, f["y"], H_LANDING+0.3), P["SPOTLIT"]["lm"], beam=120, aim=(-1,0,0), label="F36 Spotlit"), dim["stair"])
    return S

def tread_z(x, flight):
    """height (m) of the stair surface at plan x (ft). flight 1: x 16.9 -> 24 rises 0 -> 1.83; flight 2: 24 -> 16.9 rises 1.83 -> 3.51"""
    if flight == 1: return float(np.clip((x-16.9)/(24-16.9), 0, 1))*H_LANDING
    return H_LANDING + float(np.clip((24-x)/(24-16.9), 0, 1))*(H_FF-H_LANDING)

SCENES = {
 "FULL":    dict(down=1, walk=1, track=1, cove=1, pelmet=1, tv=1, pendant=1, lamp=1, stair=1),
 "EVENING": dict(down=0, walk=0, track=0, cove=0.4, pelmet=0.4, tv=0.4, pendant=0.3, lamp=1, stair=0),
 "MOVIE":   dict(down=0, walk=0, track=0, cove=0.2, pelmet=0, tv=0.15, pendant=0, lamp=0, stair=0),
 "NIGHT":   dict(down=0, walk=1, track=0, cove=0.1, pelmet=0, tv=0, pendant=0, lamp=0, stair=1),
}

# ----------------------------------------------------------------------------- indirect (room-cavity) approximation
SURF = [  # (name, area m2, reflectance)  — living void + south strip, night (curtains drawn)
 ("floor polished blond-ivory tile", 5.24*4.75, 0.50),
 ("N wall warm ivory + curtains", 5.06*6.4 - 2*(2.44*1.83), 0.60), ("N wall curtains (greige dim-out)", 2*(2.44*1.83), 0.45),
 ("W wall: greige stone/microcement TV panel + teak flutes", 3.63*6.4, 0.42),
 ("E side: FF-living balustrade + passage openings (part open)", 4.7*6.4, 0.30),
 ("S side: beam face + strip ceiling + stair void", 5.24*1.0 + 2.5*1.2 + 2.6, 0.65),
 ("void lid ceiling soft snow", 5.06*3.35, 0.80),
]
ENCLOSURE = 0.65   # fraction of first-bounce flux kept in the living volume (rest escapes to passage, FF living, stair well)

def indirect_lux(sources):
    phi = sum(s.lm for s in sources if "pendant" in s.label or "lamp" in s.label or "Axios" in s.label or "Rega Plus 12W" in s.label or "S10" in s.label or "S20" in s.label or "S11" in s.label)
    A = sum(a for _,a,_ in SURF); rho = sum(a*r for _,a,r in SURF)/A
    return phi*rho*ENCLOSURE/(A*(1-rho)), phi, A, rho

# ----------------------------------------------------------------------------- receiving surfaces
def grid_points():
    xs = np.arange(5.9, 27.01, 0.5); ys = np.arange(17.5, 36.91, 0.5)
    X, Y = np.meshgrid(xs, ys); Z = np.zeros_like(X); mask = np.zeros_like(X, bool)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            x, y = X[i,j], Y[i,j]
            inside = False
            if 9.8 <= x <= 27 and 21.3 <= y <= 36.9: inside = True            # living incl. S strip
            if 12.2 <= x <= 16.8 and 18 <= y <= 21.3: inside = True            # stair-base hall
            if 5.9 <= x <= 9.8 and 20 <= y <= 26.05: inside = True             # passage
            if 16.9 <= x <= 24 and 17.5 <= y <= 21.1: inside = True; Z[i,j] = tread_z(x,1)   # flight 1
            if 16.9 <= x <= 24 and 21.3 <= y <= 25.0: inside = True; Z[i,j] = tread_z(x,2)   # flight 2
            if 24 <= x <= 27 and 17.5 <= y <= 25.0: inside = True; Z[i,j] = H_LANDING        # landing
            mask[i,j] = inside
    return X, Y, Z, mask

KEYPTS = [  # name, x ft, y ft, z m, normal
 ("Living centre (void), floor",            18.7, 31.4, 0.00, (0,0,1)),
 ("Coffee-table top",                       18.7, 31.4, 0.45, (0,0,1)),
 ("N sofa, seat",                           18.0, 35.3, 0.45, (0,0,1)),
 ("N sofa, book held (reading plane)",      18.0, 35.0, 0.75, (0,0,1)),
 ("E return sofa, seat",                    11.6, 31.5, 0.45, (0,0,1)),
 ("Accent chairs (south strip), seat",      13.5, 23.3, 0.45, (0,0,1)),
 ("TV viewing area, floor (W side)",        24.0, 31.0, 0.00, (0,0,1)),
 ("Passage threshold, floor",               9.9, 24.0, 0.00, (0,0,1)),
 ("Stair base (tread 1)",                   17.3, 19.3, 0.00, (0,0,1)),
 ("Flight 1 mid tread",                     20.5, 19.3, None, (0,0,1)),
 ("Half landing centre",                    25.5, 21.25, H_LANDING, (0,0,1)),
 ("Flight 2 mid tread (seen from living)",  20.5, 23.15, None, (0,0,1)),
 ("NE corner floor (window corner)",        10.8, 36.3, 0.00, (0,0,1)),
 ("NW corner floor",                        26.4, 36.3, 0.00, (0,0,1)),
 ("W edge, under TV, floor",                26.0, 31.0, 0.00, (0,0,1)),
 ("E edge, balustrade line, floor",         10.5, 28.0, 0.00, (0,0,1)),
 # vertical surfaces
 ("TV screen centre (wall x=27, 1.1 m)",    27.0, 31.0, 1.10, (-1,0,0)),
 ("TV feature panel, 2.5 m",                27.0, 31.0, 2.50, (-1,0,0)),
 ("TV feature panel, 4.5 m",                27.0, 31.0, 4.50, (-1,0,0)),
 ("Curtain, 1.5 m (eye level, seated view)",18.3, 36.8, 1.50, (0,-1,0)),
 ("Curtain, 3.2 m",                         18.3, 36.8, 3.20, (0,-1,0)),
 ("Curtain, 5.5 m (top, under pelmet)",     18.3, 36.8, 5.50, (0,-1,0)),
 ("Stair feature wall (y=17.5), 1.2 m above tread 6", 20.9, 17.55, None, (0,1,0)),
 ("Stair feature wall above flight 1 (x 23 ft, 2.6 m) — Avia pool", 23.0, 17.55, 2.60, (0,1,0)),
 ("Flight 2 riser face, mid (seen from living)", 20.5, 25.0, None, (0,1,0)),
]

def point_E(sources, x, y, z, normal):
    pts = np.array([[x*FT, y*FT, z]]); n = np.array(normal, float)
    return float(sum(s.E(pts, n)[0] for s in sources))

def contributions(sources, x, y, z, normal):
    pts = np.array([[x*FT, y*FT, z]]); n = np.array(normal, float); c = {}
    for s in sources:
        k = s.label.split(" ")[0] if s.label.startswith(("F","S","pendant","floor")) else s.label
        if "pendant" in s.label: k = "pendant cluster"
        if "lamp" in s.label: k = "floor lamp"
        if "S10" in s.label: k = "S10 beam-edge profile"
        if "S20" in s.label: k = "S20 pelmet strip"
        if "S11" in s.label: k = "S11 TV-unit strips"
        c[k] = c.get(k, 0) + float(s.E(pts, n)[0])
    return c

# ----------------------------------------------------------------------------- run
def run_scene(name, **kw):
    S = build(SCENES[name], **kw)
    Eind, phi, A, rho = indirect_lux(S)
    X, Y, Z, M = grid_points()
    pts = np.stack([X[M]*FT, Y[M]*FT, Z[M]], axis=1)
    Ed = np.zeros(len(pts))
    for s in S: Ed += s.E(pts, np.array([0,0,1.0]))
    Et = Ed + Eind
    grid = np.full(X.shape, np.nan); grid[M] = Et
    liv = M & (X >= 9.8) & (Y >= 21.3) & ~((X >= 16.9) & (Y <= 25.0))   # living room floor only (incl. strip), stair excluded
    st  = M & (X >= 16.9) & (Y >= 17.5) & (Y <= 25.0)                     # both flights + landing
    gl = grid[liv]; gs = grid[st]
    stats = dict(avg=float(np.nanmean(gl)), min=float(np.nanmin(gl)), max=float(np.nanmax(gl)),
                 stair_avg=float(np.nanmean(gs)), stair_min=float(np.nanmin(gs)), stair_max=float(np.nanmax(gs)))
    stats["u_min_avg"] = stats["min"]/stats["avg"]; stats["u_min_max"] = stats["min"]/stats["max"]
    # brightest / darkest cells
    k = np.nanargmax(np.where(liv, grid, np.nan)); kmin = np.nanargmin(np.where(liv, grid, np.nan))
    stats["max_at"] = (float(X.flat[k]), float(Y.flat[k])); stats["min_at"] = (float(X.flat[kmin]), float(Y.flat[kmin]))
    e10 = sum(float(s.E(np.array([ft3(18.7,25.85,0)]), np.array([0,0,1.0]))[0]) for s in S if "S10" in s.label)
    keys = []
    for (nm, x, y, z, nrm) in KEYPTS:
        if z is None:
            z = tread_z(x, 1 if y < 21.2 else 2) + (1.2 if "wall" in nm else 0.0)
            if "riser" in nm: z = tread_z(x, 2) - 0.08
        Edir = point_E(S, x, y, z, nrm); vertical = nrm[2] == 0
        keys.append(dict(name=nm, x=x, y=y, z=round(z,2), direct=Edir, indirect=Eind*(0.8 if vertical else 1.0), total=Edir + Eind*(0.8 if vertical else 1.0),
                         contrib=contributions(S, x, y, z, nrm)))
    return dict(scene=name, kw={k:(v if not isinstance(v,float) else round(v,3)) for k,v in kw.items()}, indirect=Eind, phi_total=phi, area=A, rho=rho,
                stats=stats, keys=keys, grid=grid, X=X, Y=Y, M=M, e10=e10)

# ----------------------------------------------------------------------------- figures
def colormap(v, vmin=3, vmax=600):
    """log-scaled warm colormap: deep navy -> blue -> amber -> pale yellow"""
    t = np.clip((np.log10(np.maximum(v, 1e-3)) - math.log10(vmin))/(math.log10(vmax)-math.log10(vmin)), 0, 1)
    anchors = [(0.0,(20,24,52)),(0.25,(40,78,140)),(0.5,(120,140,120)),(0.7,(214,160,60)),(0.85,(245,205,110)),(1.0,(255,245,200))]
    out = np.zeros(t.shape+(3,), np.uint8)
    for i in range(len(anchors)-1):
        a_t, a_c = anchors[i]; b_t, b_c = anchors[i+1]
        m = (t >= a_t) & (t <= b_t); f = ((t-a_t)/(b_t-a_t))[m]
        for ch in range(3): out[...,ch][m] = (a_c[ch] + (b_c[ch]-a_c[ch])*f).astype(np.uint8)
    return out

def font(sz, bold=False):
    for p in (["/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if bold else ["/System/Library/Fonts/Supplemental/Arial.ttf"]) + ["/System/Library/Fonts/Helvetica.ttc"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

def heatmap(res, fname, title, keypts=True):
    X, Y, grid, M = res["X"], res["Y"], res["grid"], res["M"]
    S = 28  # px per ft
    x0, y0 = 5.9, 17.5; W = int((27-x0)*S)+1; Hh = int((36.9-y0)*S)+1
    mL, mT, mR, mB = 60, 70, 170, 110
    img = Image.new("RGB", (W+mL+mR, Hh+mT+mB), (250,247,240)); d = ImageDraw.Draw(img)
    # cells
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if not M[i,j]: continue
            px = mL + (X[i,j]-x0-0.25)*S; py = mT + (Y[i,j]-y0-0.25)*S
            c = tuple(int(v) for v in colormap(np.array([grid[i,j]]))[0])
            d.rectangle([px, py, px+0.5*S, py+0.5*S], fill=c)
    def R(x1,y1,x2,y2, **kw): d.rectangle([mL+(x1-x0)*S, mT+(y1-y0)*S, mL+(x2-x0)*S, mT+(y2-y0)*S], **kw)
    R(9.8,21.3,27,36.9, outline=(40,34,28), width=3)                       # living
    R(10.4,25.9,27,36.9, outline=(90,120,200), width=2)                      # void
    R(9.8,25.2,27,25.9, fill=(150,140,120)); R(9.8,25.9,10.4,29.8, fill=(150,140,120))  # beams
    R(16.9,17.5,24,21.1, outline=(80,80,80), width=1); R(16.9,21.3,24,25, outline=(80,80,80), width=1); R(24,17.5,27,25, outline=(80,80,80), width=1)
    R(12.2,18,16.8,21.3, outline=(80,80,80), width=1); R(5.9,20,9.8,26.05, outline=(80,80,80), width=1)
    f9, f10, f11, f13 = font(9), font(10), font(11), font(13, True)
    lab = [(18.4,36.2,"N WALL · 8 ft window + curtain"), (26.2,31,"TV WALL"), (18.5,25.55,"FF-slab edge beam, soffit 11 ft"), (13.3,22.3,"9 ft strip ceiling"),
           (20.4,19.3,"flight 1 ↑W"), (20.4,23.2,"flight 2 ↑E"), (25.5,18.2,"landing +1.83 m"), (14.5,18.5,"hall"), (7.8,20.6,"passage"), (18.7,33.5,"VOID — 21 ft overhead")]
    for x,y,t in lab:
        d.text((mL+(x-x0)*S, mT+(y-y0)*S), t, fill=(40,34,28), font=f9, anchor="mm")
    # fixtures
    for f in geo["fixtures"]:
        if f["id"] in ("F38","F39","F6","F7","F8","F9","F40","F41","F42","F37","F31","F32","F33","F34","F35","F36"):
            px, py = mL+(f["x"]-x0)*S, mT+(f["y"]-y0)*S
            col = (200,60,30) if f["p"]=="AXSP20" else (30,60,160)
            d.ellipse([px-4,py-4,px+4,py+4], fill=(255,255,255), outline=col, width=2); d.text((px+6,py-5), f["id"], fill=col, font=f9)
    px, py = mL+(PENDANT_XY[0]-x0)*S, mT+(PENDANT_XY[1]-y0)*S
    d.polygon([(px,py-8),(px+3,py-3),(px+8,py-2),(px+4,py+2),(px+5,py+8),(px,py+5),(px-5,py+8),(px-4,py+2),(px-8,py-2),(px-3,py-3)], fill=(122,79,163)); d.text((px+9,py-6),"pendant",fill=(122,79,163),font=f9)
    if keypts:
        offs = {"Living centre (void), floor": (-6, -10, "rm"), "Coffee-table top": (6, 8, "lm"), "N sofa, seat": (-6, 4, "rm"), "N sofa, book held (reading plane)": (6, -2, "lm"),
                "TV viewing area, floor (W side)": (-6, 8, "rm"), "W edge, under TV, floor": (-6, -8, "rm"), "Flight 1 mid tread": (6, 10, "lm"), "Flight 2 mid tread (seen from living)": (6, 10, "lm"),
                "Half landing centre": (-6, 12, "rm"), "Stair base (tread 1)": (-6, 6, "rm")}
        for k in res["keys"]:
            if k["name"].startswith(("TV screen","TV feature","Curtain","Stair feature","Flight 2 riser")): continue
            px, py = mL+(k["x"]-x0)*S, mT+(k["y"]-y0)*S
            dx, dy, anc = offs.get(k["name"], (5, 2, "lm"))
            d.ellipse([px-3,py-3,px+3,py+3], fill=(0,0,0)); d.text((px+dx,py+dy), f"{k['total']:.0f}", fill=(0,0,0), font=f10, anchor=anc)
    # colour bar
    cx = mL+W+30
    for i in range(Hh):
        v = 10**(math.log10(3) + (1-i/Hh)*(math.log10(600)-math.log10(3)))
        c = tuple(int(q) for q in colormap(np.array([v]))[0]); d.line([cx, mT+i, cx+18, mT+i], fill=c)
    for v in (5,10,20,50,100,200,400):
        yy = mT + (1-(math.log10(v)-math.log10(3))/(math.log10(600)-math.log10(3)))*Hh
        d.line([cx+18, yy, cx+23, yy], fill=(0,0,0)); d.text((cx+26, yy), f"{v} lx", fill=(0,0,0), font=f10, anchor="lm")
    d.text((mL, 16), title, fill=(20,20,20), font=f13);
    d.text((mL, 36), f"Scene {res['scene']} · living avg {res['stats']['avg']:.0f} lx · min {res['stats']['min']:.0f} · max {res['stats']['max']:.0f} · Uo (min/avg) {res['stats']['u_min_avg']:.2f} · indirect term {res['indirect']:.0f} lx", fill=(70,60,50), font=f10)
    d.text((mL, 52), "Top = SOUTH, bottom = NORTH (main door side), left = EAST, right = WEST · black dots = total lux (direct + indirect) at that point · 0.5 ft grid on floor / treads / landing", fill=(70,60,50), font=f9)
    cap = ["Model: Axios 20W = 1600 lm (TISVA catalogue) with the chosen optics; Rega Plus 12W = ESTIMATED 900 lm, intensity shape fitted to TISVA's Orrin 13W data;",
           "strips ESTIMATED 630 lm/m effective; pendant = 10 × 806 lm smart bulbs in opal globes (×0.75). Indirect = room-cavity approximation (ρ avg 0.51, enclosure 0.65).",
           "This is a MODEL, not a measurement — provenance of every number is in the Photometric Verification section of the design doc."]
    for i,t in enumerate(cap): d.text((mL, mT+Hh+12+14*i), t, fill=(70,60,50), font=f9)
    d.text((mL, mT+Hh+62), "5 ft", fill=(0,0,0), font=f10); d.line([mL+30, mT+Hh+68, mL+30+5*S, mT+Hh+68], fill=(0,0,0), width=2)
    img.save(HERE/fname); return fname

def section_svg(resFULL, fname):
    """N–S section through x = 18.7 ft (void centre line), looking WEST. Heights in m, plan y in ft."""
    y0, y1 = 16.5, 38.0; z1 = 7.4; S = 26; H = 24                      # px per ft (horizontal), px per 0.1 m? use 1 m = 90 px
    PXM = 90; W = int((y1-y0)*S)+220; Hh = int(z1*PXM)+140
    def X(y): return 60 + (y1 - y)*S          # north on the LEFT? keep sheet convention: south left, north right
    def X(y): return 60 + (y - y0)*S
    def Y(z): return 40 + (z1 - z)*PXM
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" font-family="Helvetica, Arial, sans-serif" font-size="11">')
    o.append(f'<rect width="{W}" height="{Hh}" fill="#faf7f0"/>')
    # floor, slabs
    o.append(f'<line x1="{X(y0)}" y1="{Y(0)}" x2="{X(y1)}" y2="{Y(0)}" stroke="#2b241e" stroke-width="3"/>')
    o.append(f'<text x="{X(y0)+4}" y="{Y(0)+14}" fill="#2b241e">GF finished floor (0 m)</text>')
    # roof slab over everything
    o.append(f'<rect x="{X(y0)}" y="{Y(6.9)}" width="{X(y1)-X(y0)}" height="{0.2*PXM}" fill="#8c8278"/>')
    o.append(f'<text x="{X(y0)+4}" y="{Y(6.9)-4}" fill="#2b241e">roof slab ≈ 6.7 m (22 ft)</text>')
    # FF slab + corridor south of the beam (y < 25.2): slab 3.35–3.51 m
    o.append(f'<rect x="{X(y0)}" y="{Y(3.51)}" width="{X(25.2)-X(y0)}" height="{0.16*PXM}" fill="#8c8278"/>')
    o.append(f'<text x="{X(17)}" y="{Y(3.51)-4}" fill="#2b241e">FF corridor slab · GF ceiling 11 ft (3.35 m)</text>')
    # beam 25.2–25.9, 3.05–3.51 (bottom at 11 ft = 3.35? beam soffit 11 ft, depth 1 ft above: 3.35..3.66)
    o.append(f'<rect x="{X(25.2)}" y="{Y(3.66)}" width="{X(25.9)-X(25.2)}" height="{(3.66-3.35)*PXM}" fill="#6b5f4d"/>')
    o.append(f'<text x="{X(25.9)+3}" y="{Y(3.5)}" fill="#6b5f4d">edge beam, soffit 11 ft</text>')
    # strip false ceiling 9 ft from y 21.3 to 25.2
    o.append(f'<rect x="{X(21.3)}" y="{Y(2.743)}" width="{X(25.2)-X(21.3)}" height="{0.08*PXM}" fill="#d9a31a"/>')
    o.append(f'<text x="{X(21.5)}" y="{Y(2.743)+22}" fill="#8a6a10">9 ft false ceiling (2.74 m)</text>')
    # void lid at 6.25
    o.append(f'<rect x="{X(25.9)}" y="{Y(6.25)}" width="{X(36.9)-X(25.9)}" height="{0.08*PXM}" fill="#d9a31a" opacity=".8"/>')
    o.append(f'<text x="{X(27)}" y="{Y(6.25)-6}" fill="#8a6a10">void lid false ceiling ≈ 20.5 ft (6.25 m) — proposed</text>')
    # N wall with windows
    o.append(f'<rect x="{X(36.9)}" y="{Y(6.9)}" width="12" height="{(6.9)*PXM}" fill="#3a3129"/>')
    for (za,zb) in ((0.61,2.44),(4.27,6.1)):
        o.append(f'<rect x="{X(36.9)}" y="{Y(zb)}" width="12" height="{(zb-za)*PXM}" fill="#e6b422"/>')
    o.append(f'<text x="{X(36.9)-150}" y="{Y(6.9)+14}" fill="#2b241e">N wall · 8 ft windows (lower + upper)</text>')
    # curtain line
    o.append(f'<line x1="{X(36.75)}" y1="{Y(6.1)}" x2="{X(36.75)}" y2="{Y(0.02)}" stroke="#a89f8c" stroke-width="3" stroke-dasharray="6 3"/>')
    o.append(f'<text x="{X(36.75)+16}" y="{Y(2.2)}" fill="#6d6257">curtain</text>')
    # stair flights (schematic, south of the beam, drawn in section as sloped lines)
    o.append(f'<polyline points="{X(21.3)},{Y(0)} {X(21.3)},{Y(0)}" stroke="#555" fill="none"/>')
    o.append(f'<line x1="{X(17.5)}" y1="{Y(0.6)}" x2="{X(21.1)}" y2="{Y(0.6)}" stroke="#777" stroke-width="2" stroke-dasharray="3 3"/>')
    o.append(f'<text x="{X(17.6)}" y="{Y(0.6)-4}" fill="#777">flight 1 (behind, rises W)</text>')
    o.append(f'<line x1="{X(21.3)}" y1="{Y(2.6)}" x2="{X(25.0)}" y2="{Y(2.6)}" stroke="#777" stroke-width="2" stroke-dasharray="3 3"/>')
    o.append(f'<text x="{X(21.4)}" y="{Y(2.6)+14}" fill="#777">flight 2 mid ≈ 2.6 m (seen from living)</text>')
    # fixtures: Rega at y 23.3 (x 12,15 -> out of plane) draw cone
    def cone(yc, z, half, color, lbl, zt=0.0, dy=0):
        r = (z-zt)*math.tan(math.radians(half))/FT
        o.append(f'<polygon points="{X(yc)},{Y(z)} {X(yc-r)},{Y(zt)} {X(yc+r)},{Y(zt)}" fill="{color}" opacity=".18"/>')
        o.append(f'<circle cx="{X(yc)}" cy="{Y(z)}" r="5" fill="{color}"/>')
        o.append(f'<text x="{X(yc)-60}" y="{Y(z)-22}" fill="{color}" font-weight="bold">{lbl}</text>')
    cone(23.3, 2.743, 19, "#3b6ea5", "Rega Plus 12W ×2 (x 12 and 15 ft)")
    # Axios on E beam at y 26.6/27.8/29.0 -> draw at their y with aim to curtain (F42) in plane; others out of plane
    o.append(f'<circle cx="{X(29.0)}" cy="{Y(H_AXIOS)}" r="5" fill="#b3542a"/>')
    o.append(f'<line x1="{X(29.0)}" y1="{Y(H_AXIOS)}" x2="{X(36.75)}" y2="{Y(3.2)}" stroke="#b3542a" stroke-width="2" stroke-dasharray="5 3"/>')
    o.append(f'<text x="{X(26.3)}" y="{Y(H_AXIOS)+20}" fill="#b3542a" font-weight="bold">Axios 20W heads on E beam (x 10.1 ft, 3.15 m): F40→stair, F41→TV wall (both out of plane), F42→curtain 60°</text>')
    # beam edge profile
    o.append(f'<rect x="{X(25.85)-3}" y="{Y(3.35)}" width="6" height="6" fill="#d9a31a"/>')
    o.append(f'<text x="{X(25.85)-200}" y="{Y(3.2)}" fill="#8a6a10">S10 LED profile under beam edge (11 ft) → ≈ {resFULL["e10"]:.0f} lx on the floor directly below</text>')
    # pendant cluster
    for z in PENDANT_Z:
        o.append(f'<line x1="{X(31.4)}" y1="{Y(6.25)}" x2="{X(31.4)}" y2="{Y(z)}" stroke="#7a4fa3" stroke-width="1"/>')
        o.append(f'<circle cx="{X(31.4)+(hash(z)%7-3)*3}" cy="{Y(z)}" r="6" fill="#efe3f7" stroke="#7a4fa3" stroke-width="2"/>')
    o.append(f'<text x="{X(31.4)+14}" y="{Y(5.6)}" fill="#7a4fa3" font-weight="bold">pendant cluster: 10 globes, 2.6–5.3 m, anchored to roof slab</text>')
    # pelmet
    o.append(f'<rect x="{X(36.3)}" y="{Y(6.25)}" width="{X(36.9)-X(36.3)}" height="{0.3*PXM}" fill="#d9a31a"/>')
    o.append(f'<text x="{X(32.0)}" y="{Y(6.6)}" fill="#8a6a10">S20 pelmet strip (6.1 m) washes the curtain</text>')
    # coffee table / sofa
    o.append(f'<rect x="{X(30.7)}" y="{Y(0.45)}" width="{X(32.1)-X(30.7)}" height="{0.45*PXM}" fill="#d6c5a8" stroke="#8b6f4e"/>')
    o.append(f'<rect x="{X(33.9)}" y="{Y(0.85)}" width="{X(36.6)-X(33.9)}" height="{0.85*PXM}" fill="#d4c4b0" stroke="#8b6f4e"/>')
    o.append(f'<text x="{X(34.0)}" y="{Y(0.85)-6}" fill="#5c432b">N sofa (back 0.85 m)</text>')
    # heights scale
    for z in range(0, 8):
        o.append(f'<line x1="{X(y0)-8}" y1="{Y(z)}" x2="{X(y0)}" y2="{Y(z)}" stroke="#2b241e"/>')
        o.append(f'<text x="{X(y0)-40}" y="{Y(z)+4}" fill="#2b241e">{z} m</text>')
    for ft_ in (9, 11, 21):
        z = ft_*FT; o.append(f'<text x="{X(y1)+6}" y="{Y(z)+4}" fill="#8a6a10">{ft_} ft</text>')
    # key lux annotations from FULL scene
    kv = {k["name"]: k["total"] for k in resFULL["keys"]}
    ann = [(23.3, 0.0, f"accent-chair floor ≈ {kv.get('Accent chairs (south strip), seat',0):.0f} lx (seat)"),
           (31.4, 0.5, f"coffee table ≈ {kv['Coffee-table top']:.0f} lx"),
           (35.0, 0.8, f"sofa reading plane ≈ {kv['N sofa, book held (reading plane)']:.0f} lx"),
           (36.75, 1.5, f"curtain 1.5 m ≈ {kv['Curtain, 1.5 m (eye level, seated view)']:.0f} lx (vertical)"),
           (36.75, 5.5, f"curtain 5.5 m ≈ {kv['Curtain, 5.5 m (top, under pelmet)']:.0f} lx")]
    for y, z, t in ann:
        o.append(f'<text x="{X(y)-4}" y="{Y(z)-26 if z<1 else Y(z)+16}" fill="#1f1a14" font-size="11" text-anchor="{"end" if y>34 else "start"}">{t}</text>')
    o.append(f'<text x="{X(y0)}" y="{Hh-60}" fill="#1f1a14" font-size="13" font-weight="bold">N–S section through the void centre line (x = 18.7 ft), looking west · FULL scene values (direct + indirect, modelled)</text>')
    o.append(f'<text x="{X(y0)}" y="{Hh-42}" fill="#6d6257">Inverse-square at a glance: the same 900 lm downlight gives ≈ {resFULL["isq"][0]:.0f} lx on the floor from 9 ft, ≈ {resFULL["isq"][1]:.0f} lx from 11 ft and ≈ {resFULL["isq"][2]:.0f} lx from 21 ft (nadir, single fixture).</text>')
    o.append(f'<text x="{X(y0)}" y="{Hh-26}" fill="#6d6257">Only the pendant globes, the pelmet strip and the curtain-motor pelmet sit above 11 ft; every other living-room light is at 9 ft or 11 ft. Nothing is recessed at 21 ft.</text>')
    o.append('</svg>')
    (HERE/fname).write_text("\n".join(o), encoding="utf-8"); return fname

# ----------------------------------------------------------------------------- tables
def md_tables(results, extra):
    out = []
    F = results["FULL"]
    out.append("### Lux at the important points (direct + indirect)\n")
    out.append("| Receiving point (height) | FULL | EVENING | MOVIE | NIGHT walk | main contributors in FULL |")
    out.append("|---|---:|---:|---:|---:|---|")
    for i,k in enumerate(F["keys"]):
        row = [k["name"] + f" ({k['z']:.2f} m)"]
        for sc in ("FULL","EVENING","MOVIE","NIGHT"):
            row.append(f"{results[sc]['keys'][i]['total']:.0f}")
        top = sorted(k["contrib"].items(), key=lambda kv: -kv[1])[:3]
        row.append(", ".join(f"{n} {v:.0f}" for n,v in top if v >= 1) + f"; indirect {k['indirect']:.0f}")
        out.append("| " + " | ".join(row) + " |")
    out.append("\n### Floor-grid statistics (living room incl. the south strip; 0.5 ft grid)\n")
    out.append("| Scene | average lx | min lx | max lx | Uo = min/avg | min/max | indirect term | lumens in play | brightest cell (x, y ft) | darkest cell (x, y ft) | stairs avg / min / max |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|")
    for sc,r in results.items():
        s = r["stats"]
        out.append(f"| {sc} | {s['avg']:.0f} | {s['min']:.0f} | {s['max']:.0f} | {s['u_min_avg']:.2f} | {s['u_min_max']:.2f} | {r['indirect']:.0f} lx | {r['phi_total']:.0f} lm | {s['max_at'][0]:.1f}, {s['max_at'][1]:.1f} | {s['min_at'][0]:.1f}, {s['min_at'][1]:.1f} | {s['stair_avg']:.0f} / {s['stair_min']:.0f} / {s['stair_max']:.0f} |")
    out.append("\n### Sensitivity (FULL scene) — how much the unknowns move the answer\n")
    out.append("| Case | coffee table | sofa reading plane | accent-chair seat | half landing | curtain 1.5 m / 3.2 m (vertical) | living avg | min | Uo |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for name, r in extra.items():
        kv = {k["name"]: k["total"] for k in r["keys"]}
        out.append(f"| {name} | {kv['Coffee-table top']:.0f} | {kv['N sofa, book held (reading plane)']:.0f} | {kv['Accent chairs (south strip), seat']:.0f} | {kv['Half landing centre']:.0f} | {kv['Curtain, 1.5 m (eye level, seated view)']:.0f} / {kv['Curtain, 3.2 m']:.0f} | {r['stats']['avg']:.0f} | {r['stats']['min']:.0f} | {r['stats']['u_min_avg']:.2f} |")
    # robustness: halve the indirect term
    kvF = {k["name"]: k for k in results["FULL"]["keys"]}
    out.append(f"| Indirect term halved (ρ or enclosure 40 % lower) | {kvF['Coffee-table top']['direct']+results['FULL']['indirect']/2:.0f} | {kvF['N sofa, book held (reading plane)']['direct']+results['FULL']['indirect']/2:.0f} | {kvF['Accent chairs (south strip), seat']['direct']+results['FULL']['indirect']/2:.0f} | — | — | ≈{results['FULL']['stats']['avg']-results['FULL']['indirect']/2:.0f} | ≈{results['FULL']['stats']['min']-results['FULL']['indirect']/2:.0f} | — |")
    return "\n".join(out)

def beam_table():
    rows = ["| Beam angle (50 %) | footprint Ø at 1 m | at 2.7 m (9 ft ceiling → floor) | at 3.35 m (11 ft) | at 4.1 m (E-beam head → coffee table) | at 6.4 m (21 ft) | what it is for |", "|---|---:|---:|---:|---:|---:|---|"]
    use = {15:"idols, art, basin — a tight pool", 24:"TV panel, coffee table, long throws", 36:"general downlight (Rega/Orrin class, '38°')", 60:"wash a curtain or wall from mid distance", 120:"foot-lights, panels — soft spread, no pool"}
    for b in (15,24,36,60,120):
        D = lambda d: 2*d*math.tan(math.radians(b/2))
        rows.append(f"| {b}° | {D(1):.2f} m | {D(2.7):.1f} m | {D(3.35):.1f} m | {D(4.1):.1f} m | {D(6.4):.1f} m | {use[b]} |")
    return "\n".join(rows)

def isq_table():
    # one 900 lm fixture, Orrin-13 shape, nadir illuminance at 2.74 / 3.35 / 6.4 m
    s = Src((0,0,0), 900, shape=SHAPES["orrin13"]); I0 = s.I0
    rows = ["| Mounting height above floor | distance d | E at nadir = I₀/d² (900 lm, I₀ ≈ %d cd) | footprint Ø (38°) | relative |" % I0, "|---|---:|---:|---:|---:|"]
    vals = []
    for ft_ in (9, 11, 21):
        d = ft_*FT; E = I0/d**2; vals.append(E)
        rows.append(f"| {ft_} ft | {d:.2f} m | {E:.0f} lx | {2*d*math.tan(math.radians(19)):.1f} m | {E/vals[0]*100:.0f} % |")
    return "\n".join(rows), vals

def fixture_table(resFULL):
    S = build(SCENES["FULL"])
    rows = ["| Fixture (plan position) | height | electrical | luminous flux | peak intensity I₀ (model) | beam | main receiving surface | distance to it | incidence | direct lux there | data basis |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    def row(fid, s, surface, pt, nrm, basis):
        d = np.linalg.norm(np.array(pt)-s.pos); v = (np.array(pt)-s.pos)/d; alpha = math.degrees(math.acos(np.clip(v@s.aim,-1,1)))
        inc = math.degrees(math.acos(np.clip(-(v@np.array(nrm)),0,1)))
        E = float(s.E(np.array([pt]), np.array(nrm,float))[0])
        return f"| {fid} | {s.pos[2]:.2f} m | {basis[0]} | {s.lm:.0f} lm | {s.I0:.0f} cd | {basis[1]} | {surface} | {d:.1f} m | {inc:.0f}° off-normal, {alpha:.0f}° off-axis | {E:.0f} lx | {basis[2]} |"
    bysrc = {s.label: s for s in S}
    rows.append(row("F38 Rega Plus 12W (x12, y23.3)", bysrc["F38 Rega Plus 12W"], "floor under accent chairs", ft3(12,23.3,0), (0,0,1), ("12 W", "38° (inferred)", "lm EST, shape FIT Orrin 13W")))
    rows.append(row("F39 Rega Plus 12W (x15, y23.3)", bysrc["F39 Rega Plus 12W"], "accent-chair seat 0.45 m", ft3(13.5,23.3,0.45), (0,0,1), ("12 W", "38° (inferred)", "lm EST, shape FIT")))
    rows.append(row("F40 Axios 20W → stair", bysrc["F40 Axios 20W 38°"], "flight 2 mid tread", TARGETS["stair"], (0,0,1), ("20 W", "38° optic", "lm DOC-CAT; shape CALC")))
    rows.append(row("F41 Axios 20W → TV panel", bysrc["F41 Axios 20W 24°"], "TV feature panel 2.5 m (vertical)", TARGETS["tv"], (-1,0,0), ("20 W", "24° optic", "lm DOC-CAT; shape CALC")))
    rows.append(row("F42 Axios 20W → curtain", bysrc["F42 Axios 20W 60°"], "curtain 3.2 m (vertical)", TARGETS["curtain"], (0,-1,0), ("20 W", "60° optic", "lm DOC-CAT; shape CALC")))
    rows.append(row("F37 Avia 7W on landing soffit → stair wall", bysrc["F37 AVIA7 -> stair wall"], "stair feature wall at the aim point, 2.6 m (vertical)", ft3(23.0,17.55,2.6), (0,1,0), ("7 W", "36° (assumed)", "lm EST (520 lm); CRI>90 per price list")))
    # pendant: sum over globes
    pend = [s for s in S if "pendant" in s.label]; Ecoffee = sum(float(s.E(np.array([TARGETS["coffee"]]), np.array([0,0,1.0]))[0]) for s in pend)
    rows.append(f"| Pendant cluster (10 globes, x18.7 y31.4) | 2.6–5.3 m | 10 × ~5 W | {sum(s.lm for s in pend):.0f} lm (after globe) | {pend[0].I0:.0f} cd per globe (isotropic) | 360° | coffee-table top | 2.2–4.9 m | 0° | {Ecoffee:.0f} lx | bulb lm DOC-OTH; globe τ EST |")
    s10 = [s for s in S if "S10" in s.label]; E10 = sum(float(s.E(np.array([ft3(18.7,25.85,0)]), np.array([0,0,1.0]))[0]) for s in s10)
    rows.append(f"| S10 beam-edge profile (6.3 m) | 3.35 m | 63 W | {sum(s.lm for s in s10):.0f} lm eff. | Lambertian line | 120° | floor directly below the beam | 3.35 m | 0° | {E10:.0f} lx | lm/m EST |")
    s20 = [s for s in S if "S20" in s.label]
    for z in (5.5, 3.2, 1.5):
        E20 = sum(float(s.E(np.array([ft3(18.3,36.8,z)]), np.array([0,-1.0,0]))[0]) for s in s20)
        rows.append(f"| S20 pelmet strip (3.4 m) | 6.10 m | 34 W | {sum(s.lm for s in s20):.0f} lm eff. | Lambertian line | 120° | curtain at {z} m (vertical) | {6.1-z:.1f} m | grazing | {E20:.0f} lx | lm/m EST |")
    sp = bysrc["F33 Spotlit"]
    rows.append(row("F33 Spotlit Pro 2W (wall, tread 6)", sp, "tread 6, 0.3 m from wall", ft3(20.9, 18.5, tread_z(20.9,1)), (0,0,1), ("2 W", "120°", "lm EST")))
    return "\n".join(rows)

if __name__ == "__main__":
    results = {sc: run_scene(sc) for sc in SCENES}
    isq_md, isq_vals = isq_table(); results["FULL"]["isq"] = isq_vals
    extra = {
        "ACCEPTED design (Rega 900 lm, Orrin-13 shape, 806 lm bulbs, Avia 7W on the landing)": results["FULL"],
        "Rega soft shape (Orrin-7.5 fit, more spill)": run_scene("FULL", rega_shape="orrin75"),
        "Rega 800 lm (low estimate)": run_scene("FULL"),   # placeholder replaced below
        "Previous design: Bolt 12W over the landing + 470 lm bulbs": run_scene("FULL", landing_fix="BOLT12", bulb_lm=470),
        "Bulbs 470 lm instead of 806 lm": run_scene("FULL", bulb_lm=470),
        "Landing: Bolt 6W downlight instead of the Avia": run_scene("FULL", landing_fix="BOLT6"),
        "(rejected) + 4th Axios head 24° aimed at the coffee table": run_scene("FULL", fourth_head=True),
        "Pelmet: profile tilted 45° toward the fabric, 150 mm off it (tested — no gain below the top metre)": run_scene("FULL", pelmet_mode="angled"),
    }
    P["REGA12"]["lm"] = 800; extra["Rega 800 lm (low estimate)"] = run_scene("FULL"); P["REGA12"]["lm"] = 900
    # calibration check of the Orrin fits against the catalogue tables
    cal = {}
    for shape, lm, d, beamD, Eav_doc in (("orrin75", 600, 1.0, 0.76, 397.75), ("orrin75", 600, 3.0, 2.29, 44.19), ("orrin13", 1050, 1.0, 0.58, 1071.08), ("orrin13", 1050, 3.0, 1.73, 119.01)):
        s = Src((0,0,d), lm, shape=SHAPES[shape]); r = np.linspace(0, beamD/2, 200); pts = np.stack([r, np.zeros_like(r), np.zeros_like(r)],1)
        E = s.E(pts, np.array([0,0,1.0])); Eav = float(np.trapezoid(E*2*math.pi*r, r)/(math.pi*(beamD/2)**2))
        cal[f"{shape} {lm} lm at {d} m, beam Ø {beamD} m"] = dict(model_Eav=Eav, catalogue_Eav=Eav_doc, model_nadir=float(s.I0/d**2), peak_cd_per_klm=float(s.I0/lm*1000))
    tabs = []
    tabs.append("### Calibration of the intensity shapes against TISVA's published Orrin tables\n")
    tabs.append("| Case | model average lux in the catalogue beam Ø | catalogue Eav_B | model nadir lux | model peak cd/klm (catalogue polar max: 7.5 W ≈ 1227, 13 W ≈ 3181) |")
    tabs.append("|---|---:|---:|---:|---:|")
    for k,v in cal.items(): tabs.append(f"| {k} | {v['model_Eav']:.0f} | {v['catalogue_Eav']:.0f} | {v['model_nadir']:.0f} | {v['peak_cd_per_klm']:.0f} |")
    tabs.append("\n" + md_tables(results, extra))
    tabs.append("\n### Beam angle → footprint (Ø = 2·d·tan(θ/2))\n" + beam_table())
    tabs.append("\n### Inverse-square: one Rega-class 900 lm downlight, nadir illuminance vs mounting height\n" + isq_md)
    tabs.append("\n### Fixture → surface table (FULL scene, direct component only)\n" + fixture_table(results["FULL"]))
    # indirect budget
    r = results["FULL"]; tabs.append(f"\n### Indirect-light budget (room-cavity approximation)\n\nSurfaces: " + "; ".join(f"{n} {a:.0f} m² ρ {rho}" for n,a,rho in SURF) + f". Total area {r['area']:.0f} m², area-weighted ρ = {r['rho']:.2f}, enclosure factor {ENCLOSURE}. FULL-scene flux into the room {r['phi_total']:.0f} lm → indirect ≈ {r['indirect']:.0f} lx; EVENING {results['EVENING']['phi_total']:.0f} lm → {results['EVENING']['indirect']:.0f} lx; MOVIE → {results['MOVIE']['indirect']:.0f} lx.")
    (HERE/"tables.md").write_text("\n".join(tabs), encoding="utf-8")
    # figures
    heatmap(results["FULL"], "living-lux-heatmap-full.png", "Living room floor lux — FULL scene (everything on), accepted design 2026-10-02")
    heatmap(results["EVENING"], "living-lux-heatmap-evening.png", "Living room floor lux — EVENING scene (coves 40 %, pendant 30 %, lamp on)")
    heatmap(extra["Previous design: Bolt 12W over the landing + 470 lm bulbs"], "living-lux-heatmap-full-previous.png", "Living room floor lux — FULL scene, PREVIOUS design for comparison (Bolt 12 W over the landing, 470 lm bulbs)")
    section_svg(results["FULL"], "living-section.svg")
    # json (without grids)
    slim = {sc: {k:v for k,v in r.items() if k not in ("grid","X","Y","M")} for sc,r in results.items()}
    slim["sensitivity"] = {n: {k:v for k,v in r.items() if k not in ("grid","X","Y","M")} for n,r in extra.items()}
    slim["calibration"] = cal; slim["params"] = {k:{kk:vv for kk,vv in v.items()} for k,v in P.items()}; slim["shapes"] = SHAPES
    (HERE/"results.json").write_text(json.dumps(slim, indent=1, default=float), encoding="utf-8")
    print((HERE/"tables.md").read_text())
