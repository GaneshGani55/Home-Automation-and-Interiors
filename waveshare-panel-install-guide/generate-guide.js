const fs = require("fs");
const path = require("path");

const OUT = __dirname;
const W = 1600;
const H = 1000;

const C = {
  ink: "#171717",
  muted: "#5e5b55",
  wall: "#eadfce",
  wallDark: "#d9c9b5",
  plaster: "#f4ecdf",
  shadow: "#00000018",
  wood: "#8a5633",
  wood2: "#a66c42",
  ply: "#c79b63",
  brass: "#bf8a2c",
  steel: "#9aa1a7",
  conduit: "#b9bdc1",
  cable: "#6f7478",
  cable2: "#8d949a",
  screen: "#1f2933",
  glass: "#263442",
  display: "#e8f3f5",
  blue: "#6f94aa",
  green: "#73946f",
  red: "#b96f60",
};

function esc(s) {
  return String(s).replace(/[&<>"]/g, (ch) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
  })[ch]);
}

function rect(x, y, w, h, fill = "none", stroke = C.ink, extra = "") {
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" stroke="${stroke}" ${extra}/>`;
}

function line(x1, y1, x2, y2, stroke = C.ink, extra = "") {
  return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" ${extra}/>`;
}

function pathD(d, fill = "none", stroke = C.ink, extra = "") {
  return `<path d="${d}" fill="${fill}" stroke="${stroke}" ${extra}/>`;
}

function text(x, y, s, size = 28, weight = 500, fill = C.ink, extra = "") {
  return `<text x="${x}" y="${y}" font-size="${size}" font-weight="${weight}" fill="${fill}" ${extra}>${esc(s)}</text>`;
}

function multiText(x, y, lines, size = 28, weight = 500, fill = C.ink, gap = 1.18) {
  return lines.map((s, i) => text(x, y + i * size * gap, s, size, weight, fill)).join("");
}

function label(x, y, lines, size = 26) {
  const arr = Array.isArray(lines) ? lines : [lines];
  const h = arr.length * size * 1.16 + 18;
  const w = Math.max(...arr.map((s) => s.length)) * size * 0.55 + 36;
  return [
    rect(x, y, w, h, "#fffdf8", C.ink, `stroke-width="2" rx="8"`),
    multiText(x + 18, y + 33, arr, size, 600, C.ink, 1.14),
  ].join("");
}

function callout(x1, y1, x2, y2, lines, side = "right") {
  const tx = side === "left" ? x2 - 290 : x2 + 16;
  const ty = y2 - 28;
  return [
    line(x1, y1, x2, y2, C.ink, `stroke-width="2" marker-end="url(#dot)"`),
    label(tx, ty, lines, 22),
  ].join("");
}

function dimH(x1, x2, y, labelText, above = true) {
  const tick = 15;
  const ty = above ? y - 16 : y + 36;
  return [
    line(x1, y, x2, y, C.ink, `stroke-width="2" marker-start="url(#arrow)" marker-end="url(#arrow)"`),
    line(x1, y - tick, x1, y + tick, C.ink, `stroke-width="2"`),
    line(x2, y - tick, x2, y + tick, C.ink, `stroke-width="2"`),
    text((x1 + x2) / 2, ty, labelText, 24, 700, C.ink, `text-anchor="middle"`),
  ].join("");
}

function dimV(x, y1, y2, labelText, side = "right") {
  const tick = 15;
  const tx = side === "left" ? x - 26 : x + 26;
  const anchor = side === "left" ? "end" : "start";
  return [
    line(x, y1, x, y2, C.ink, `stroke-width="2" marker-start="url(#arrow)" marker-end="url(#arrow)"`),
    line(x - tick, y1, x + tick, y1, C.ink, `stroke-width="2"`),
    line(x - tick, y2, x + tick, y2, C.ink, `stroke-width="2"`),
    `<text x="${tx}" y="${(y1 + y2) / 2}" font-size="24" font-weight="700" fill="${C.ink}" text-anchor="${anchor}" transform="rotate(-90 ${tx} ${(y1 + y2) / 2})">${esc(labelText)}</text>`,
  ].join("");
}

function stepBadge(n, title, audience) {
  return [
    `<circle cx="92" cy="86" r="42" fill="${C.brass}" stroke="${C.ink}" stroke-width="3"/>`,
    text(92, 99, String(n), 42, 800, "#fffdf8", `text-anchor="middle"`),
    text(158, 75, title, 42, 800),
    text(160, 112, audience, 23, 600, C.muted),
  ].join("");
}

function svg(n, title, audience, body) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<defs>
  <marker id="arrow" markerWidth="12" markerHeight="12" refX="6" refY="6" orient="auto-start-reverse">
    <path d="M 0 0 L 12 6 L 0 12 z" fill="${C.ink}"/>
  </marker>
  <marker id="dot" markerWidth="8" markerHeight="8" refX="4" refY="4">
    <circle cx="4" cy="4" r="3" fill="${C.ink}"/>
  </marker>
  <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="10" stdDeviation="7" flood-color="#000" flood-opacity="0.14"/>
  </filter>
  <pattern id="woodGrain" width="90" height="26" patternUnits="userSpaceOnUse">
    <rect width="90" height="26" fill="${C.wood}"/>
    <path d="M4 8 C25 2, 48 14, 88 7 M0 21 C25 15, 53 27, 92 19" fill="none" stroke="${C.wood2}" stroke-width="3" opacity="0.6"/>
  </pattern>
  <style>
    svg { background: #fffdf8; font-family: Inter, Avenir, Helvetica, Arial, sans-serif; }
    rect, path, line, circle, ellipse, polyline, polygon { vector-effect: non-scaling-stroke; }
  </style>
</defs>
<rect x="0" y="0" width="${W}" height="${H}" fill="#fffdf8" stroke="none"/>
${stepBadge(n, title, audience)}
${body}
<text x="1500" y="950" text-anchor="end" font-size="22" font-weight="600" fill="${C.muted}">Waveshare 10.1 in staircase panel install</text>
</svg>`;
}

function save(name, content) {
  fs.writeFileSync(path.join(OUT, name), content);
}

function wallSetout() {
  const wall = rect(210, 175, 1040, 650, C.wall, C.ink, `stroke-width="3" rx="2" filter="url(#softShadow)"`);
  const floor = line(150, 825, 1320, 825, C.ink, `stroke-width="3"`);
  const cavity = rect(610, 278, 280, 195, C.plaster, C.ink, `stroke-width="3"`);
  const center = [
    line(750, 245, 750, 505, C.ink, `stroke-width="2" stroke-dasharray="9 9"`),
    line(565, 376, 935, 376, C.ink, `stroke-width="2" stroke-dasharray="9 9"`),
    `<circle cx="750" cy="376" r="7" fill="${C.brass}" stroke="${C.ink}" stroke-width="2"/>`,
  ].join("");
  const screenGhost = rect(621, 291, 258, 170, "#00000008", C.screen, `stroke-width="2" stroke-dasharray="8 7"`);
  const switchPlate = rect(716, 640, 67, 75, "#f7f3ea", C.ink, `stroke-width="3" rx="5"`);
  const switches = [
    rect(728, 654, 17, 47, "#ffffff", C.ink, `stroke-width="2" rx="3"`),
    rect(754, 654, 17, 47, "#ffffff", C.ink, `stroke-width="2" rx="3"`),
  ].join("");
  const conduit = [
    pathD("M300 625 C405 585, 465 502, 610 392", "none", C.conduit, `stroke-width="26" stroke-linecap="round"`),
    pathD("M300 625 C405 585, 465 502, 610 392", "none", C.ink, `stroke-width="2" stroke-linecap="round"`),
    rect(245, 590, 110, 85, "#d8d8d6", C.ink, `stroke-width="3" rx="8"`),
    multiText(260, 625, ["server", "niche"], 21, 700, C.ink),
  ].join("");
  const dimensions = [
    dimH(610, 890, 250, "280 mm cavity width"),
    dimV(925, 278, 473, "195 mm cavity height", "right"),
    dimV(1330, 376, 825, "1500 mm FFL center", "right"),
    dimV(570, 473, 640, "~200 mm clear gap", "left"),
  ].join("");
  const labels = [
    callout(750, 376, 1038, 350, ["Screen center", "1500 mm FFL"], "right"),
    callout(750, 695, 1034, 690, ["Existing 2M", "stair light switch"], "right"),
    callout(414, 538, 118, 540, ["25 mm grey PVC", "C-Niche-Waveshare"], "right"),
    label(1008, 504, ["Align cavity center", "with switch centerline"], 22),
  ].join("");
  return svg(1, "Wall Set-Out", "For mason + electrician + homeowner", wall + floor + conduit + cavity + screenGhost + center + switchPlate + switches + dimensions + labels);
}

function masonryPocket() {
  const block = [
    `<polygon points="330,250 1020,250 1210,360 520,360" fill="${C.wall}" stroke="${C.ink}" stroke-width="3"/>`,
    `<polygon points="330,250 520,360 520,735 330,625" fill="${C.wallDark}" stroke="${C.ink}" stroke-width="3"/>`,
    `<polygon points="520,360 1210,360 1210,735 520,735" fill="${C.wall}" stroke="${C.ink}" stroke-width="3"/>`,
  ].join("");
  const pocket = [
    `<polygon points="670,418 952,418 952,614 670,614" fill="${C.plaster}" stroke="${C.ink}" stroke-width="3"/>`,
    `<polygon points="952,418 1018,456 1018,652 952,614" fill="#ddd0bd" stroke="${C.ink}" stroke-width="3"/>`,
    `<polygon points="670,418 736,456 1018,456 952,418" fill="#efe5d7" stroke="${C.ink}" stroke-width="3"/>`,
    rect(697, 446, 232, 140, "#fff7ec", C.ink, `stroke-width="2" stroke-dasharray="8 8"`),
  ].join("");
  const behind = [
    `<polygon points="1018,456 1126,520 1126,716 1018,652" fill="#cdb9a0" stroke="${C.ink}" stroke-width="2" opacity="0.86"/>`,
    dimH(952, 1018, 392, "80 mm cut depth"),
    dimH(1018, 1126, 750, "150 mm masonry remains", false),
    dimH(952, 1126, 815, "230 mm wall thickness", false),
  ].join("");
  const finish = [
    pathD("M706 458 L920 458 L920 574 L706 574 Z", "none", C.ink, `stroke-width="2"`),
    line(706, 478, 920, 478, C.steel, `stroke-width="1.5"`),
    line(706, 498, 920, 498, C.steel, `stroke-width="1.5"`),
    line(706, 518, 920, 518, C.steel, `stroke-width="1.5"`),
    line(706, 538, 920, 538, C.steel, `stroke-width="1.5"`),
    line(706, 558, 920, 558, C.steel, `stroke-width="1.5"`),
  ].join("");
  const labels = [
    callout(672, 418, 420, 390, ["Pocket opening", "280 x 195 mm"], "left"),
    callout(802, 520, 420, 610, ["Smooth plaster inside", "or 6 mm black ply liner"], "left"),
    callout(1058, 594, 1170, 500, ["Do not cut deeper", "150 mm wall stays solid"], "right"),
    label(122, 760, ["Critical for mason:", "square corners, flat back,", "no loose plaster dust"], 22),
  ].join("");
  return svg(2, "Masonry Pocket", "For mason", block + behind + pocket + finish + labels);
}

function cablesAndTest() {
  const wall = rect(330, 220, 880, 570, C.wall, C.ink, `stroke-width="3" rx="2" filter="url(#softShadow)"`);
  const server = [
    rect(120, 420, 230, 200, "#e7e7e1", C.ink, `stroke-width="3" rx="10"`),
    text(235, 462, "SERVER NICHE", 24, 800, C.ink, `text-anchor="middle"`),
    rect(172, 493, 128, 62, "#30363d", C.ink, `stroke-width="3" rx="8"`),
    text(236, 533, "Beelink", 24, 800, "#fffdf8", `text-anchor="middle"`),
    text(144, 590, "HDMI 2", 21, 700),
    text(245, 590, "USB-A", 21, 700),
  ].join("");
  const cavity = rect(760, 330, 280, 195, C.plaster, C.ink, `stroke-width="3"`);
  const conduit = [
    pathD("M350 520 C470 500, 594 405, 760 432", "none", C.conduit, `stroke-width="34" stroke-linecap="round"`),
    pathD("M350 520 C470 500, 594 405, 760 432", "none", C.ink, `stroke-width="2" stroke-linecap="round"`),
  ].join("");
  const cables = [
    pathD("M300 512 C444 500, 584 408, 766 420 C838 430, 838 490, 784 498 C742 504, 744 452, 818 448", "none", C.cable, `stroke-width="8" stroke-linecap="round"`),
    pathD("M300 532 C456 518, 590 428, 774 442 C870 452, 882 522, 800 522 C744 522, 746 472, 826 474", "none", C.cable2, `stroke-width="8" stroke-linecap="round"`),
    pathD("M300 548 C450 536, 588 458, 770 466 C858 470, 860 545, 790 548", "none", "#7d837d", `stroke-width="6" stroke-linecap="round" stroke-dasharray="14 10"`),
  ].join("");
  const screen = [
    rect(1005, 356, 258, 170, C.screen, C.ink, `stroke-width="3" rx="12"`),
    rect(1024, 374, 219, 138, C.display, C.ink, `stroke-width="2"`),
    text(1134, 435, "TEST", 42, 900, C.green, `text-anchor="middle"`),
    pathD("M1088 461 L1124 495 L1184 421", "none", C.green, `stroke-width="12" stroke-linecap="round" stroke-linejoin="round"`),
  ].join("");
  const labels = [
    callout(810, 515, 1088, 600, ["200 mm cable loop", "inside pocket"], "right"),
    callout(500, 420, 596, 306, ["1 x HDMI", "1 x USB", "1 x spare Cat6"], "right"),
    callout(1132, 526, 1258, 698, ["Test display + touch", "before closing cavity"], "right"),
    label(100, 700, ["Electrician note:", "no power socket at screen;", "USB powers screen"], 22),
  ].join("");
  const legend = [
    rect(1010, 220, 310, 86, "#fffdf8", C.ink, `stroke-width="2" rx="8"`),
    line(1032, 250, 1090, 250, C.cable, `stroke-width="8"`),
    text(1106, 258, "HDMI", 22, 700),
    line(1032, 280, 1090, 280, C.cable2, `stroke-width="8"`),
    text(1106, 288, "USB touch + 5V", 22, 700),
  ].join("");
  return svg(3, "Cable Route + Test", "For electrician", wall + conduit + server + cavity + cables + screen + legend + labels);
}

function bezelBuild() {
  const wall = rect(145, 280, 405, 320, C.wall, C.ink, `stroke-width="3" rx="2"`);
  const cavity = rect(207, 330, 280, 195, C.plaster, C.ink, `stroke-width="3"`);
  const sub = [
    rect(625, 305, 300, 220, C.ply, C.ink, `stroke-width="3" rx="8" filter="url(#softShadow)"`),
    rect(646, 330, 258, 170, "#eee1cb", C.ink, `stroke-width="2" rx="5"`),
    `<circle cx="662" cy="346" r="10" fill="${C.brass}" stroke="${C.ink}" stroke-width="2"/>`,
    `<circle cx="888" cy="346" r="10" fill="${C.brass}" stroke="${C.ink}" stroke-width="2"/>`,
    `<circle cx="662" cy="484" r="10" fill="${C.brass}" stroke="${C.ink}" stroke-width="2"/>`,
    `<circle cx="888" cy="484" r="10" fill="${C.brass}" stroke="${C.ink}" stroke-width="2"/>`,
    text(775, 561, "plywood sub-frame", 24, 800, C.ink, `text-anchor="middle"`),
  ].join("");
  const screen = [
    rect(957, 324, 258, 170, C.screen, C.ink, `stroke-width="3" rx="12" filter="url(#softShadow)"`),
    rect(977, 340, 219, 138, C.display, C.ink, `stroke-width="2"`),
    text(1086, 411, "Home", 31, 800, C.blue, `text-anchor="middle"`),
    text(1086, 448, "Assistant", 31, 800, C.blue, `text-anchor="middle"`),
  ].join("");
  const bezel = [
    rect(1175, 286, 320, 235, "url(#woodGrain)", C.ink, `stroke-width="3" rx="10" filter="url(#softShadow)"`),
    rect(1225, 333, 220, 140, "#fffdf8", C.ink, `stroke-width="3" rx="3"`),
    line(1215, 308, 1455, 308, "#e3b076", `stroke-width="4" stroke-linecap="round" stroke-dasharray="28 14"`),
    line(1215, 499, 1455, 499, "#e3b076", `stroke-width="4" stroke-linecap="round" stroke-dasharray="28 14"`),
    `<circle cx="1460" cy="493" r="9" fill="${C.brass}" stroke="${C.ink}" stroke-width="2"/>`,
  ].join("");
  const arrows = [
    line(528, 430, 606, 430, C.ink, `stroke-width="3" marker-end="url(#arrow)"`),
    line(925, 430, 950, 430, C.ink, `stroke-width="3" marker-end="url(#arrow)"`),
    line(1215, 430, 1168, 430, C.ink, `stroke-width="3" marker-end="url(#arrow)"`),
  ].join("");
  const dims = [
    dimH(1175, 1495, 250, "320 mm bezel external"),
    dimV(1518, 286, 521, "235 mm", "right"),
    dimH(1225, 1445, 560, "220 mm window", false),
    dimV(1150, 333, 473, "140 mm", "left"),
  ].join("");
  const labels = [
    line(347, 330, 276, 300, C.ink, `stroke-width="2" marker-end="url(#dot)"`),
    label(70, 238, ["Cavity hidden by", "20-25 mm overhang"], 22),
    callout(665, 347, 520, 190, ["4 x M3 brass", "standoffs"], "left"),
    callout(1085, 326, 970, 210, ["Screen case", "257.6 x 169.7 x 22 mm"], "left"),
    callout(1340, 308, 1330, 654, ["Slim vent slots", "top + bottom"], "right"),
  ].join("");
  return svg(4, "Bezel + Sub-Frame", "For carpenter", wall + cavity + sub + screen + bezel + arrows + dims + labels);
}

function magnetsNfc() {
  const cavity = [
    rect(205, 270, 520, 410, C.wall, C.ink, `stroke-width="3" rx="2" filter="url(#softShadow)"`),
    rect(314, 346, 280, 195, C.plaster, C.ink, `stroke-width="3"`),
  ].join("");
  const plates = [
    rect(333, 365, 48, 30, C.steel, C.ink, `stroke-width="2" rx="3"`),
    rect(527, 365, 48, 30, C.steel, C.ink, `stroke-width="2" rx="3"`),
    rect(333, 492, 48, 30, C.steel, C.ink, `stroke-width="2" rx="3"`),
    rect(527, 492, 48, 30, C.steel, C.ink, `stroke-width="2" rx="3"`),
  ].join("");
  const frame = [
    rect(900, 246, 390, 300, C.ply, C.ink, `stroke-width="3" rx="10" filter="url(#softShadow)"`),
    rect(958, 305, 258, 170, "#ead8bc", C.ink, `stroke-width="2" rx="5"`),
    rect(918, 265, 44, 44, "#343434", C.ink, `stroke-width="2" rx="5"`),
    rect(1228, 265, 44, 44, "#343434", C.ink, `stroke-width="2" rx="5"`),
    rect(918, 484, 44, 44, "#343434", C.ink, `stroke-width="2" rx="5"`),
    rect(1228, 484, 44, 44, "#343434", C.ink, `stroke-width="2" rx="5"`),
    text(940, 294, "N", 21, 900, "#fffdf8", `text-anchor="middle"`),
    text(1250, 294, "N", 21, 900, "#fffdf8", `text-anchor="middle"`),
    text(940, 513, "N", 21, 900, "#fffdf8", `text-anchor="middle"`),
    text(1250, 513, "N", 21, 900, "#fffdf8", `text-anchor="middle"`),
    rect(1130, 430, 108, 74, "#171717", C.ink, `stroke-width="3" rx="8"`),
    text(1184, 474, "ACR122U", 20, 800, "#fffdf8", `text-anchor="middle"`),
    `<circle cx="1249" cy="496" r="11" fill="${C.brass}" stroke="${C.ink}" stroke-width="2"/>`,
  ].join("");
  const align = [
    line(381, 380, 918, 287, C.ink, `stroke-width="2" stroke-dasharray="9 10"`),
    line(575, 380, 1228, 287, C.ink, `stroke-width="2" stroke-dasharray="9 10"`),
    line(381, 507, 918, 506, C.ink, `stroke-width="2" stroke-dasharray="9 10"`),
    line(575, 507, 1228, 506, C.ink, `stroke-width="2" stroke-dasharray="9 10"`),
  ].join("");
  const bezelFace = [
    rect(900, 642, 390, 175, "url(#woodGrain)", C.ink, `stroke-width="3" rx="10"`),
    rect(984, 674, 220, 96, "#fffdf8", C.ink, `stroke-width="3" rx="3"`),
    `<circle cx="1249" cy="779" r="11" fill="${C.brass}" stroke="${C.ink}" stroke-width="2"/>`,
    text(1095, 845, "front face", 23, 800, C.muted, `text-anchor="middle"`),
  ].join("");
  const labels = [
    line(355, 380, 274, 330, C.ink, `stroke-width="2" marker-end="url(#dot)"`),
    label(78, 286, ["Steel strike plates", "inside cavity"], 22),
    callout(940, 287, 745, 175, ["4 hidden magnets", "10 x 10 x 3 mm"], "left"),
    callout(1185, 468, 1322, 392, ["USB NFC reader", "behind lower-right"], "right"),
    callout(1249, 779, 1322, 755, ["Brass dot marks", "NFC tap point"], "right"),
    label(135, 735, ["Alignment step:", "push frame in place,", "mark plate centers,", "then screw plates"], 22),
  ].join("");
  return svg(5, "Magnets + NFC", "For carpenter + electrician", cavity + plates + frame + align + bezelFace + labels);
}

function serviceFinal() {
  const front = [
    rect(115, 240, 560, 555, C.wall, C.ink, `stroke-width="3" rx="2" filter="url(#softShadow)"`),
    rect(250, 335, 320, 235, "url(#woodGrain)", C.ink, `stroke-width="3" rx="10"`),
    rect(300, 382, 220, 140, C.display, C.ink, `stroke-width="3" rx="3"`),
    text(410, 445, "Dashboard", 30, 800, C.blue, `text-anchor="middle"`),
    `<circle cx="535" cy="543" r="9" fill="${C.brass}" stroke="${C.ink}" stroke-width="2"/>`,
    rect(379, 675, 67, 75, "#f7f3ea", C.ink, `stroke-width="3" rx="5"`),
    rect(391, 689, 17, 47, "#ffffff", C.ink, `stroke-width="2" rx="3"`),
    rect(417, 689, 17, 47, "#ffffff", C.ink, `stroke-width="2" rx="3"`),
    text(410, 820, "finished wall", 24, 800, C.muted, `text-anchor="middle"`),
  ].join("");
  const service = [
    rect(855, 235, 400, 560, C.wall, C.ink, `stroke-width="3" rx="2" filter="url(#softShadow)"`),
    rect(920, 355, 280, 195, C.plaster, C.ink, `stroke-width="3"`),
    rect(660, 344, 320, 235, "url(#woodGrain)", C.ink, `stroke-width="3" rx="10" filter="url(#softShadow)"`),
    rect(710, 391, 220, 140, C.display, C.ink, `stroke-width="3" rx="3"`),
    pathD("M920 465 C855 428, 803 538, 950 535 C1010 532, 1030 484, 980 450", "none", C.cable, `stroke-width="8" stroke-linecap="round"`),
    pathD("M918 496 C850 486, 830 595, 965 584 C1018 580, 1034 530, 985 502", "none", C.cable2, `stroke-width="8" stroke-linecap="round"`),
    line(980, 462, 830, 462, C.ink, `stroke-width="3" marker-end="url(#arrow)"`),
    dimH(660, 855, 315, "pull forward about 150 mm"),
    text(816, 676, "service position", 24, 800, C.muted, `text-anchor="middle"`),
  ].join("");
  const hand = [
    pathD("M620 608 C640 585, 668 594, 670 620 L672 664 C673 686, 649 694, 636 677 L602 632 C592 619, 606 605, 620 608 Z", "#fff4e6", C.ink, `stroke-width="3"`),
    pathD("M661 615 L715 578", "none", C.ink, `stroke-width="12" stroke-linecap="round"`),
    pathD("M645 612 L702 565", "none", C.ink, `stroke-width="10" stroke-linecap="round"`),
    pathD("M634 626 L684 590", "none", C.ink, `stroke-width="9" stroke-linecap="round"`),
  ].join("");
  const labels = [
    callout(535, 543, 640, 225, ["Small brass NFC", "tap marker"], "right"),
    line(410, 675, 280, 662, C.ink, `stroke-width="2" marker-end="url(#dot)"`),
    label(78, 616, ["Existing switch", "stays below"], 22),
    callout(946, 535, 1280, 600, ["Slack loop stays", "plugged in"], "right"),
    label(1244, 310, ["Service:", "pull straight out,", "swap part,", "push back in"], 24),
    text(930, 825, "Magnets re-engage when pushed flush", 26, 800, C.ink, `text-anchor="middle"`),
  ].join("");
  return svg(6, "Final + Service", "For homeowner + all trades", front + service + hand + labels);
}

const sheets = [
  ["step-01-wall-setout.svg", wallSetout()],
  ["step-02-masonry-pocket.svg", masonryPocket()],
  ["step-03-cable-route-test.svg", cablesAndTest()],
  ["step-04-bezel-subframe.svg", bezelBuild()],
  ["step-05-magnets-nfc.svg", magnetsNfc()],
  ["step-06-final-service.svg", serviceFinal()],
];

for (const [name, content] of sheets) save(name, content);

const index = `<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>Waveshare Panel Install Guide</title>
<style>
  body { margin: 0; background: #fffdf8; font-family: system-ui, sans-serif; color: #171717; }
  main { max-width: 1120px; margin: 32px auto; padding: 0 24px 48px; }
  h1 { font-size: 32px; margin: 0 0 20px; }
  figure { margin: 0 0 34px; page-break-inside: avoid; }
  img { width: 100%; border: 1px solid #d9c9b5; background: white; }
  figcaption { margin-top: 8px; font-size: 16px; color: #5e5b55; }
  @media print { body { background: white; } main { max-width: none; margin: 0; } figure { break-after: page; } }
</style>
<main>
<h1>Waveshare 10.1 in Staircase Panel Install Guide</h1>
${sheets.map(([name], i) => `<figure><img src="${name}" alt="Step ${i + 1}"><figcaption>Step ${i + 1}</figcaption></figure>`).join("\n")}
</main>`;
save("index.html", index);

console.log(`Wrote ${sheets.length} SVG sheets to ${OUT}`);
