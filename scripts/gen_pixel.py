#!/usr/bin/env python3
"""Generate the pixel-art assets for the profile README: header scene,
project cards, toolbox, divider and footer. Run from anywhere; writes
into ../assets relative to this file."""
import html
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

# palette
CREAM = "#fdf6e3"
BROWN = "#4a3b2a"
MIDBROWN = "#8a5a2b"
TAN = "#6b5b45"
ORANGE = "#e76f51"
AMBER = "#f4a261"
YELLOW = "#ffd95e"
SKY1 = "#aee9f7"
SKY2 = "#bfeefa"
GREEN_L = "#a5d977"
GREEN_M = "#6fbf59"
GREEN_D = "#4e9e3f"
WHITE = "#ffffff"
CLOUD_SHADOW = "#ddf2fa"
BLACK = "#2b2b2b"
RED = "#e05252"
FACE = "#f6c99f"
WOOD = "#c9955c"

FONT = "Menlo,Consolas,'DejaVu Sans Mono',monospace"

# 5x7 pixel font (rows of 5 bits per glyph)
GLYPHS = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "11110", "10001", "10001", "10001", "11110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "11110", "10000", "10000", "10000", "11111"],
    "F": ["11111", "10000", "11110", "10000", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10000", "10011", "10001", "10001", "01111"],
    "H": ["10001", "10001", "11111", "10001", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
}


def esc(s):
    return html.escape(s, quote=True)


def px(x, y, w, h, color, opacity=None):
    o = f' fill-opacity="{opacity}"' if opacity is not None else ""
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{color}"{o}/>'


def pixel_text(s, x, y, scale, color, opacity=None):
    """Render s in the 5x7 pixel font, top-left at (x, y)."""
    out = []
    cx = x
    for ch in s.upper():
        g = GLYPHS.get(ch, GLYPHS[" "])
        for row, bits in enumerate(g):
            # merge horizontal runs to keep the file small
            col = 0
            while col < 5:
                if bits[col] == "1":
                    run = col
                    while run < 5 and bits[run] == "1":
                        run += 1
                    out.append(px(cx + col * scale, y + row * scale,
                                  (run - col) * scale, scale, color, opacity))
                    col = run
                else:
                    col += 1
        cx += 6 * scale
    return "".join(out)


def pixel_text_width(s, scale):
    return (len(s) * 6 - 1) * scale


def pixel_frame(w, h, t, color):
    """Chunky border with stepped (notched) pixel corners; outside stays transparent."""
    s = 2 * t
    return "".join([
        px(s, 0, w - 2 * s, t, color),            # top
        px(s, h - t, w - 2 * s, t, color),        # bottom
        px(0, s, t, h - 2 * s, color),            # left
        px(w - t, s, t, h - 2 * s, color),        # right
        px(t, t, t, t, color), px(w - s, t, t, t, color),
        px(t, h - s, t, t, color), px(w - s, h - s, t, t, color),
    ])


def card_bg(w, h, t=4):
    s = 2 * t
    return (
        px(t, s, w - 2 * t, h - 2 * s, CREAM)
        + px(s, t, w - 2 * s, h - 2 * t, CREAM)
        + pixel_frame(w, h, t, BROWN)
    )


def sprite(grid, palette, x, y, scale):
    out = []
    for r, row in enumerate(grid):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch in palette:
                run = c
                while run < len(row) and row[run] == ch:
                    run += 1
                out.append(px(x + c * scale, y + r * scale,
                              (run - c) * scale, scale, palette[ch]))
                c = run
            else:
                c += 1
    return "".join(out)


# ----- little scene pieces -------------------------------------------------

def cloud(x, y, scale, drift=8, dur=26):
    body = "".join([
        px(0, 2 * scale, 14 * scale, 3 * scale, WHITE),
        px(2 * scale, 0, 5 * scale, 2 * scale, WHITE),
        px(8 * scale, 1 * scale, 4 * scale, 1 * scale, WHITE),
        px(1 * scale, 5 * scale, 12 * scale, 1 * scale, CLOUD_SHADOW),
    ])
    return (f'<g transform="translate({x},{y})">'
            f'<animateTransform attributeName="transform" type="translate" additive="sum" '
            f'values="0 0;{drift} 0;0 0" dur="{dur}s" repeatCount="indefinite"/>{body}</g>')


def sun(x, y, u=6):
    rows = [(4, 0, 4), (2, 1, 8), (1, 2, 10), (0, 3, 12), (0, 4, 12), (0, 5, 12),
            (0, 6, 12), (1, 7, 10), (2, 8, 8), (4, 9, 4)]
    body = "".join(px(x + dx * u, y + ry * u, w * u, u, YELLOW) for dx, ry, w in rows)
    core = px(x + 3 * u, y + 3 * u, 6 * u, 4 * u, "#ffe89a")
    rays = "".join([
        px(x + 5 * u, y - 3 * u, 2 * u, 2 * u, YELLOW),
        px(x + 5 * u, y + 11 * u, 2 * u, 2 * u, YELLOW),
        px(x - 4 * u, y + 4 * u, 2 * u, 2 * u, YELLOW),
        px(x + 14 * u, y + 4 * u, 2 * u, 2 * u, YELLOW),
    ])
    return body + core + rays


BEE_BODY = [
    "..ww....",
    "bYbYbY..",
    "bYbYbYb.",
    "bYbYbY..",
]
BEE_PAL = {"b": BLACK, "Y": YELLOW, "w": "#eaf7fd"}


def bee(x, y, scale=4, flap=0.22, path=None, dur=7):
    wings_up = px(2 * scale, -2 * scale, 3 * scale, 2 * scale, "#eaf7fd")
    wings_dn = px(2 * scale, -1 * scale, 3 * scale, 1 * scale, "#eaf7fd")
    body = sprite(BEE_BODY, BEE_PAL, 0, 0, scale)
    fly = ""
    if path:
        fly = (f'<animateTransform attributeName="transform" type="translate" additive="sum" '
               f'values="{path}" dur="{dur}s" repeatCount="indefinite"/>')
    return (f'<g transform="translate({x},{y})">{fly}{body}'
            f'<g>{wings_up}<animate attributeName="opacity" values="1;0;1" dur="{flap}s" repeatCount="indefinite"/></g>'
            f'<g>{wings_dn}<animate attributeName="opacity" values="0;1;0" dur="{flap}s" repeatCount="indefinite"/></g>'
            f'</g>')


def flower(x, y, u, petal):
    return "".join([
        px(x + u, y + 2 * u, u, 2 * u, GREEN_D),
        px(x, y, u, u, petal), px(x + 2 * u, y, u, u, petal),
        px(x + u, y - u, u, u, petal), px(x + u, y + u, u, u, petal),
        px(x + u, y, u, u, YELLOW),
    ])


PIXIE = [
    "..hhhhhh..",
    ".hhhhhhhh.",
    ".hffffffh.",
    ".hfeffefh.",
    ".hffffffh.",
    "..ffmmff..",
    "...ffff...",
    "..ssssss..",
    ".fssssssf.",
    ".fssssssf.",
    "..ssssss..",
    "..dd..dd..",
    "..dd..dd..",
]
PIXIE_PAL = {"h": MIDBROWN, "f": FACE, "e": BLACK, "m": "#d97b6c", "s": ORANGE, "d": BROWN}


def pixie(x, y, scale):
    body = sprite(PIXIE, PIXIE_PAL, x, y, scale)
    # two-frame waving arm, to the right of the body
    ax = x + 9 * scale
    arm_up = px(ax, y + 6 * scale, scale, 2 * scale, FACE) + px(ax, y + 5 * scale, scale, scale, FACE)
    arm_mid = px(ax, y + 7 * scale, scale, 2 * scale, FACE)
    return (body
            + f'<g>{arm_up}<animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite"/></g>'
            + f'<g>{arm_mid}<animate attributeName="opacity" values="0;1;0" dur="0.9s" repeatCount="indefinite"/></g>')


# ----- header --------------------------------------------------------------

def header(w=900, h=320):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
         f'shape-rendering="crispEdges" role="img" '
         f'aria-label="Pixel-art scene: Bishesh Shrestha — security tools, web apps and AI experiments">']
    p.append(px(0, 0, w, 150, SKY1))
    p.append(px(0, 150, w, h - 150, SKY2))
    p.append(sun(770, 34))
    p.append(cloud(60, 40, 5, drift=10, dur=30))
    p.append(cloud(340, 24, 4, drift=-8, dur=24))
    p.append(cloud(640, 64, 3, drift=7, dur=20))

    # hills (stepped silhouettes)
    steps_back = [232, 226, 220, 216, 214, 216, 220, 226, 232, 238, 242, 244, 242, 238, 234]
    seg = w / len(steps_back)
    for i, top in enumerate(steps_back):
        p.append(px(round(i * seg), top, round(seg) + 1, h - top, GREEN_L))
    steps_front = [274, 270, 266, 264, 264, 266, 270, 274, 276, 278, 278, 276, 274, 272, 270]
    for i, top in enumerate(steps_front):
        p.append(px(round(i * seg), top, round(seg) + 1, h - top, GREEN_M))

    # grass tufts + flowers
    for gx in (90, 210, 330, 470, 610, 750, 850):
        p.append(px(gx, 262, 4, 8, GREEN_D))
        p.append(px(gx + 8, 266, 4, 6, GREEN_D))
    p.append(flower(140, 282, 5, RED))
    p.append(flower(260, 290, 5, WHITE))
    p.append(flower(560, 286, 5, ORANGE))
    p.append(flower(690, 292, 5, RED))

    # wooden sign: BEE AUTOMATED
    sign_text = "BEE AUTOMATED"
    ts = 2
    tw = pixel_text_width(sign_text, ts)
    bw, bh = tw + 36, 7 * ts + 20
    bx, by = 44, 236
    p.append(px(bx + bw // 2 - 5, by + bh, 10, 26, MIDBROWN))
    p.append(px(bx - 4, by - 4, bw + 8, bh + 8, MIDBROWN))
    p.append(px(bx, by, bw, bh, WOOD))
    p.append(pixel_text(sign_text, bx + 18, by + 10, ts, BROWN))

    # name
    name = "BISHESH SHRESTHA"
    ns = 5
    nw = pixel_text_width(name, ns)
    nx, ny = (w - nw) // 2, 74
    p.append(pixel_text(name, nx + ns, ny + ns, ns, BROWN, opacity=0.18))
    p.append(pixel_text(name, nx, ny, ns, BROWN))
    p.append(f'<text x="{w / 2}" y="152" text-anchor="middle" font-family="{FONT}" '
             f'font-size="15" fill="{TAN}">security tools · web apps · ai experiments</text>')

    # inhabitants
    p.append(pixie(788, 210, 4))
    p.append(bee(320, 252, 4, path="0 0;30 -14;62 -6;30 8;0 0", dur=9))
    p.append(bee(590, 240, 3, path="0 0;-26 10;-50 -4;-20 -12;0 0", dur=11))

    p.append("</svg>\n")
    return "".join(p)


# ----- icons for cards -----------------------------------------------------

ICONS = {
    "pixie": (PIXIE, PIXIE_PAL),
    "magnifier": ([
        "...gggg...",
        "..g....g..",
        ".g......g.",
        ".g......g.",
        ".g......g.",
        ".g......g.",
        "..g....g..",
        "...gggg.m.",
        ".......mm.",
        "......mm..",
    ], {"g": "#4a7fa5", "m": MIDBROWN}),
    "shield": ([
        "tttttttttt",
        "t........t",
        "t........t",
        "t......c.t",
        "t.c...c..t",
        "t..c.c...t",
        ".t..c...t.",
        ".t......t.",
        "..t....t..",
        "...tttt...",
    ], {"t": "#3d8f83", "c": GREEN_D}),
    "radar": ([
        "...rrrr...",
        "..r....r..",
        ".r......r.",
        "r....s...r",
        "r...s....r",
        "r..ss....r",
        ".r.s....r.",
        "..r....r..",
        "...rrrr...",
        "..........",
    ], {"r": ORANGE, "s": RED}),
    "boat": ([
        ".....w....",
        "....ww....",
        "...www....",
        "..wwww....",
        ".wwwww....",
        "....m.....",
        "hhhhhhhhh.",
        ".hhhhhhh..",
        "bbbbbbbbbb",
        ".b.b.b.b..",
    ], {"w": AMBER, "m": MIDBROWN, "h": MIDBROWN, "b": "#4a7fa5"}),
    "plant": ([
        "....g.....",
        ".g..g..g..",
        "..g.g.g...",
        "...ggg....",
        "....g.....",
        ".pppppppp.",
        "..pppppp..",
        "..pppppp..",
        "..pppppp..",
        "..........",
    ], {"g": GREEN_D, "p": "#c96f4a"}),
    "flame": ([
        ".....o....",
        "....oo....",
        "...ooo....",
        "..ooooo...",
        ".ooyyoo...",
        ".oyyyyo...",
        ".oyyyyoo..",
        ".ooyyoo...",
        "..oooo....",
        "..........",
    ], {"o": ORANGE, "y": YELLOW}),
}

LANG_COLORS = {
    "TypeScript": "#3178c6",
    "Python": "#3572A5",
    "Shell": "#89e051",
    "HTML": "#e34c26",
    "JavaScript": "#d4b830",
    "Rust": "#dea584",
}

CARDS = [
    {
        "file": "beezpcap.svg", "name": "BeezPCAP", "icon": "magnifier", "lang": "HTML",
        "desc": ["PCAP threat hunting with Suricata and", "Zeek, enriched with IOC intelligence."],
        "tags": "suricata · zeek · threat-hunting",
    },
    {
        "file": "beezscan.svg", "name": "BeezScan", "icon": "shield", "lang": "HTML",
        "desc": ["Vulnerability scanner that checks your", "installed software against the NVD."],
        "tags": "nvd · cve · scanning",
    },
    {
        "file": "automated-cti.svg", "name": "Automated-CTI", "icon": "radar", "lang": "Python",
        "desc": ["Takes the busywork out of threat intel —", "sorts, dedupes and enriches IOC feeds."],
        "tags": "cti · iocs · feeds",
    },
    {
        "file": "fshipy.svg", "name": "Fshipy", "icon": "boat", "lang": "Python",
        "desc": ["Ships Wazuh logs into OpenSearch, with", "master-node detection and bulk ingest."],
        "tags": "wazuh · opensearch · logs",
    },
    {
        "file": "plantshelf.svg", "name": "PlantShelf", "icon": "plant", "lang": "JavaScript",
        "desc": ["A calm little web app for home plant", "keepers — visual shelf, watering tracker."],
        "tags": "web · plants · cozy",
    },
    {
        "file": "stressor.svg", "name": "Stressor", "icon": "flame", "lang": "Python",
        "desc": ["Floods your log pipeline with syslog", "traffic so production doesn't have to."],
        "tags": "syslog · load-testing",
    },
]


def card(c, w=430, h=140):
    grid, pal = ICONS[c["icon"]]
    lang_color = LANG_COLORS[c["lang"]]
    desc = "".join(
        f'<text x="96" y="{72 + i * 19}" font-family="{FONT}" font-size="12.5" fill="{TAN}">{esc(l)}</text>'
        for i, l in enumerate(c["desc"])
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges" role="img" aria-label="{esc(c['name'])}: {esc(' '.join(c['desc']))}">
{card_bg(w, h)}
<g>{sprite(grid, pal, 26, 34, 5 if c['icon'] != 'pixie' else 4)}</g>
<text x="96" y="46" font-family="{FONT}" font-size="18" font-weight="bold" fill="{BROWN}">{esc(c['name'])}</text>
{desc}
<text x="96" y="116" font-family="{FONT}" font-size="11.5" fill="{ORANGE}">{esc(c['tags'])}</text>
{px(w - 26 - len(c['lang']) * 7.2 - 14, 30, 8, 8, lang_color)}
<text x="{w - 26}" y="38" text-anchor="end" font-family="{FONT}" font-size="12" fill="{TAN}">{esc(c['lang'])}</text>
</svg>
'''


def flagship(w=880, h=180):
    grid, pal = ICONS["pixie"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges" role="img" aria-label="opersona — an AI persona that learns how you think">
{card_bg(w, h)}
<g>{sprite(grid, pal, 32, 34, 8)}</g>
<text x="152" y="56" font-family="{FONT}" font-size="26" font-weight="bold" fill="{BROWN}">opersona</text>
<text x="152" y="82" font-family="{FONT}" font-size="14" font-style="italic" fill="{MIDBROWN}">How you think, not what you know.</text>
<text x="152" y="110" font-family="{FONT}" font-size="13" fill="{TAN}">A persistent Claude persona with your reasoning fingerprint — your own Claude interviews</text>
<text x="152" y="129" font-family="{FONT}" font-size="13" fill="{TAN}">you, blind prediction tests keep it honest, and it all runs self-hosted on your machine.</text>
<text x="152" y="158" font-family="{FONT}" font-size="12.5" fill="{ORANGE}">live at opersona.me · MCP connector for claude.ai · TypeScript</text>
</svg>
'''


# ----- toolbox -------------------------------------------------------------

TOOL_ROWS = [
    ("SECURITY", ["Wazuh", "Suricata", "Zeek", "OpenSearch", "MISP", "Elastic"]),
    ("CLOUD & OPS", ["AWS", "Docker", "Kubernetes", "Ansible", "Vagrant", "Proxmox", "Linux"]),
    ("CODE", ["Python", "TypeScript", "Rust", "Next.js", "Django", "Bash"]),
    ("DATA & VIZ", ["Grafana", "Kibana", "MySQL", "MongoDB"]),
]
DOTS = [ORANGE, "#4a7fa5", GREEN_D, AMBER, "#3d8f83", RED, MIDBROWN]


def toolbox(w=880):
    rows = len(TOOL_ROWS)
    h = rows * 44 + 36
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
         f'shape-rendering="crispEdges" role="img" aria-label="Toolbox: security, cloud, code and data tools">',
         card_bg(w, h)]
    y = 30
    for ri, (label, tools) in enumerate(TOOL_ROWS):
        p.append(f'<text x="28" y="{y + 17}" font-family="{FONT}" font-size="11" '
                 f'font-weight="bold" fill="{MIDBROWN}">{esc(label)}</text>')
        x = 140
        for ti, t in enumerate(tools):
            cw = round(len(t) * 7.3) + 34
            p.append(px(x, y, cw, 26, "#f6ecd4"))
            p.append(f'<g transform="translate({x},{y})">{pixel_frame(cw, 26, 2, "#d9c9a3")}</g>')
            p.append(px(x + 10, y + 9, 8, 8, DOTS[(ri + ti) % len(DOTS)]))
            p.append(f'<text x="{x + 26}" y="{y + 18}" font-family="{FONT}" font-size="12" '
                     f'fill="{BROWN}">{esc(t)}</text>')
            x += cw + 10
        y += 44
    p.append("</svg>\n")
    return "".join(p)


# ----- divider & footer ----------------------------------------------------

def divider(w=880, h=30):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
         f'shape-rendering="crispEdges" role="img" aria-label="">']
    p.append(px(0, h - 8, w, 8, GREEN_M))
    for gx in range(20, w - 20, 60):
        p.append(px(gx, h - 14, 4, 6, GREEN_D))
        p.append(px(gx + 30, h - 12, 3, 4, GREEN_D))
    p.append(flower(w // 4, h - 20, 3, RED))
    p.append(flower(w // 2, h - 20, 3, WHITE))
    p.append(flower(3 * w // 4, h - 20, 3, ORANGE))
    p.append(bee(w - 120, 4, 2, path="0 0;-40 4;-80 -2;-40 6;0 0", dur=13))
    p.append("</svg>\n")
    return "".join(p)


def footer(w=880, h=90):
    msg = "THANKS FOR STOPPING BY"
    s = 3
    tw = pixel_text_width(msg, s)
    tx = (w - tw) // 2
    heart = [
        ".rr.rr.",
        "rrrrrrr",
        "rrrrrrr",
        ".rrrrr.",
        "..rrr..",
        "...r...",
    ]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
         f'shape-rendering="crispEdges" role="img" aria-label="Thanks for stopping by">']
    p.append(pixel_text(msg, tx, 16, s, BROWN))
    p.append(sprite(heart, {"r": RED}, tx + tw + 18, 16, 3))
    p.append(px(0, h - 10, w, 10, GREEN_M))
    for gx in range(30, w - 20, 80):
        p.append(px(gx, h - 16, 4, 6, GREEN_D))
    p.append(flower(w // 2 - 60, h - 22, 3, WHITE))
    p.append(flower(w // 2 + 60, h - 22, 3, RED))
    p.append(bee(w // 2 - 160, 50, 3, path="0 0;60 -6;120 2;60 8;0 0", dur=12))
    p.append(bee(w // 2 + 120, 46, 3, path="0 0;-50 8;-100 -4;-40 -8;0 0", dur=10))
    p.append("</svg>\n")
    return "".join(p)


# ----- write everything ----------------------------------------------------

os.makedirs(os.path.join(OUT, "cards"), exist_ok=True)
with open(os.path.join(OUT, "header.svg"), "w") as f:
    f.write(header())
print("wrote header.svg")
with open(os.path.join(OUT, "cards", "opersona.svg"), "w") as f:
    f.write(flagship())
print("wrote cards/opersona.svg")
for c in CARDS:
    with open(os.path.join(OUT, "cards", c["file"]), "w") as f:
        f.write(card(c))
    print("wrote cards/" + c["file"])
with open(os.path.join(OUT, "toolbox.svg"), "w") as f:
    f.write(toolbox())
print("wrote toolbox.svg")
with open(os.path.join(OUT, "divider.svg"), "w") as f:
    f.write(divider())
print("wrote divider.svg")
with open(os.path.join(OUT, "footer.svg"), "w") as f:
    f.write(footer())
print("wrote footer.svg")
