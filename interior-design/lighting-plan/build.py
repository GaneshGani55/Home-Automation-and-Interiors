#!/usr/bin/env python3
"""Build the single-file lighting map (lighting-plan.html) by inlining lighting-data.js into
lighting-plan.src.html, and print the bill of materials as Markdown (paste into the design doc).

Usage:  python3 build.py            # writes lighting-plan.html + prints BOM
"""
import json, math, re, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
src = (HERE / "lighting-plan.src.html").read_text(encoding="utf-8")
data = (HERE / "lighting-data.js").read_text(encoding="utf-8")
out = src.replace('<script src="lighting-data.js"></script>', "<script>\n" + data + "\n</script>")
import base64
for ph, fn in (("__HEATMAP_FULL__", "photometric/living-lux-heatmap-full.png"), ("__HEATMAP_EVENING__", "photometric/living-lux-heatmap-evening.png")):
    f = HERE / fn
    if f.exists():
        out = out.replace(ph, "data:image/png;base64," + base64.b64encode(f.read_bytes()).decode())
# living lux-check table from the photometric results
rj = HERE / "photometric" / "results.json"
if rj.exists():
    R = json.loads(rj.read_text(encoding="utf-8"))
    def kv(sc, name):
        return next(k["total"] for k in R[sc]["keys"] if k["name"] == name)
    rows = [("Coffee-table top (0.45 m)", "Coffee-table top"), ("N sofa, book in hand (0.75 m)", "N sofa, book held (reading plane)"),
            ("Accent-chair seat under the 2 Rega (0.45 m)", "Accent chairs (south strip), seat"), ("Floor at TV viewing side", "TV viewing area, floor (W side)"),
            ("North corners, floor", "NW corner floor"), ("Stair base, tread 1", "Stair base (tread 1)"), ("Half landing (Avia 7 W, accepted)", "Half landing centre"),
            ("Stair wall — soffit accent C1 crown (vertical, proposed)", "Stair wall — soffit accent C1 crown (x 20.2 ft, 2.5 m)"), ("Stair wall — soffit accent C2 crown (vertical)", "Stair wall — soffit accent C2 crown (x 22.5 ft, 3.0 m)"), ("Landing back wall — F37 pool (vertical)", "Landing back wall (x 25.5 ft, 2.5 m) — F37 pool"),
            ("TV feature panel at 2.5 m (vertical)", "TV feature panel, 2.5 m"), ("Curtain at 1.5 m (vertical)", "Curtain, 1.5 m (eye level, seated view)"), ("Curtain at 3.2 m (vertical)", "Curtain, 3.2 m")]
    h = '<table><thead><tr><th>Point</th><th class="num">FULL</th><th class="num">EVENING</th><th class="num">MOVIE</th><th class="num">NIGHT walk</th></tr></thead><tbody>'
    for lab, key in rows:
        h += "<tr><td>%s</td>%s</tr>" % (lab, "".join('<td class="num">%.0f</td>' % kv(sc, key) for sc in ("FULL", "EVENING", "MOVIE", "NIGHT")))
    st = {sc: R[sc]["stats"] for sc in ("FULL", "EVENING", "MOVIE", "NIGHT")}
    h += "<tr><td><b>Living floor average · min · max · Uo</b></td>%s</tr>" % "".join('<td class="num">%.0f · %.0f · %.0f · %.2f</td>' % (st[sc]["avg"], st[sc]["min"], st[sc]["max"], st[sc]["u_min_avg"]) for sc in ("FULL", "EVENING", "MOVIE", "NIGHT"))
    h += "</tbody></table>"
    out = out.replace("__LUX_TABLE__", h)
(HERE / "lighting-plan.html").write_text(out, encoding="utf-8")
print("wrote lighting-plan.html (%d KB)" % (len(out) // 1024))

# --- BOM via node (the data file is plain JS) ---
js = r"""
const L=require(process.argv[1]);
const q={},len={},rooms={};const add=(k,n)=>{q[k]=(q[k]||0)+n;};
for(const [fl,F] of Object.entries(L.floors)){
  F.fixtures.forEach(f=>{add(f.p,1);(rooms[f.p]=rooms[f.p]||new Set()).add(F.rooms.find(r=>r.id===f.room).name.split(' ')[0]+(fl==='FF'?'(FF)':''));});
  F.strips.forEach(s=>{if(L.products[s.kind])len[s.kind]=(len[s.kind]||0)+s.len_m;s.drivers.forEach(d=>add(d,1));});
}
for(const [k,m] of Object.entries(len))add(k,Math.ceil(m*1.1/5));
let tot=0;const rows=[];
for(const k of Object.keys(L.products)){if(!q[k])continue;const P=L.products[k];const t=q[k]*P.mrp;tot+=t;
  rows.push(`| ${P.fam} | ${P.name}${len[k]?` (${len[k].toFixed(1)} m needed)`:''} | \`${P.code}\` | p.${P.page} | ${q[k]} | ${P.mrp.toLocaleString('en-IN')} | ${t.toLocaleString('en-IN')} |`);}
console.log('| Family | Item | Order code | Cat. page | Qty | MRP ₹ | Total ₹ |');
console.log('|---|---|---|---|---:|---:|---:|');
rows.forEach(r=>console.log(r));
console.log(`| **TISVA total at MRP** | | | | | | **${tot.toLocaleString('en-IN')}** |`);
console.log('\nSTRIP metres:',JSON.stringify(len));
console.log('30% discount ≈',Math.round(tot*0.7).toLocaleString('en-IN'));
// per-room fixture counts
const perRoom={};for(const [fl,F] of Object.entries(L.floors)){F.fixtures.forEach(f=>{const r=F.rooms.find(r=>r.id===f.room).name;const key=(fl==='FF'?'FF · ':'GF · ')+r;perRoom[key]=perRoom[key]||{};perRoom[key][f.p]=(perRoom[key][f.p]||0)+1;});}
console.log('\nPER ROOM:');for(const [r,c] of Object.entries(perRoom))console.log(' -',r,':',Object.entries(c).map(([k,n])=>`${n}× ${k}`).join(', '));
"""
res = subprocess.run(["node", "-e", js, str(HERE / "lighting-data.js")], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print(res.stderr)
