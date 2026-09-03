#!/usr/bin/env python3
"""Generate static terminal-themed project card SVGs for the profile README."""
import html
import os

BG = "#0d1117"
GREEN = "#00FF41"
FG = "#e6edf3"
DIM = "#8b949e"
FONT = "'SF Mono','Cascadia Code','Fira Code',Menlo,Consolas,'DejaVu Sans Mono',monospace"

LANG_COLORS = {
    "TypeScript": "#3178c6",
    "Python": "#3572A5",
    "Shell": "#89e051",
    "HTML": "#e34c26",
    "JavaScript": "#f1e05a",
}

CARDS = [
    {
        "file": "beezpcap.svg",
        "name": "BeezPCAP",
        "desc": ["Automated PCAP threat hunting — Suricata + Zeek", "detections, enriched with IOC intelligence."],
        "lang": "HTML",
        "tags": "# suricata  # zeek  # threat-hunting",
    },
    {
        "file": "beezscan.svg",
        "name": "BeezScan",
        "desc": ["Fast vulnerability scanner — checks your installed", "software against the NVD."],
        "lang": "HTML",
        "tags": "# nvd  # cve  # vuln-scanning",
    },
    {
        "file": "automated-cti.svg",
        "name": "Automated-CTI",
        "desc": ["Automates bulky cyber threat intelligence work —", "sorts, dedupes and enriches IOC feeds."],
        "lang": "Python",
        "tags": "# cti  # iocs  # automation",
    },
    {
        "file": "fshipy.svg",
        "name": "Fshipy",
        "desc": ["Streams Wazuh logs into OpenSearch — master-node", "detection and bulk ingest built in."],
        "lang": "Python",
        "tags": "# wazuh  # opensearch  # logging",
    },
    {
        "file": "stressor.svg",
        "name": "Stressor",
        "desc": ["Simulates high-volume syslog traffic to stress-test", "log pipelines before production does."],
        "lang": "Python",
        "tags": "# syslog  # chaos  # load-testing",
    },
    {
        "file": "aws-manager.svg",
        "name": "AWS-Manager",
        "desc": ["Interactive Bash menu for managing AWS EC2", "straight from the terminal."],
        "lang": "Shell",
        "tags": "# aws  # ec2  # bash",
    },
]


def esc(s):
    return html.escape(s, quote=True)


def card(c, w=430, h=140):
    lang_color = LANG_COLORS[c["lang"]]
    desc_lines = "".join(
        f'<text x="26" y="{72 + i * 20}" font-family="{FONT}" font-size="13" fill="{DIM}">{esc(l)}</text>'
        for i, l in enumerate(c["desc"])
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(c['name'])}: {esc(' '.join(c['desc']))}">
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="10" fill="{BG}" stroke="{GREEN}" stroke-opacity="0.28"/>
  <text x="26" y="38" font-family="{FONT}" font-size="16" font-weight="bold">
    <tspan fill="{GREEN}">&#10095; </tspan><tspan fill="{FG}">{esc(c['name'])}</tspan><tspan fill="{GREEN}">/</tspan>
  </text>
  {desc_lines}
  <text x="26" y="{h - 20}" font-family="{FONT}" font-size="12" fill="{GREEN}" fill-opacity="0.65">{esc(c['tags'])}</text>
  <circle cx="{w - 26 - len(c['lang']) * 7.4 - 12:.0f}" cy="33" r="5" fill="{lang_color}"/>
  <text x="{w - 26}" y="38" text-anchor="end" font-family="{FONT}" font-size="12" fill="{DIM}">{esc(c['lang'])}</text>
</svg>
'''


def flagship(w=880, h=170):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="opersona: an AI persona that learns how you think">
  <defs>
    <filter id="glow" x="-20%" y="-40%" width="140%" height="180%">
      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="{GREEN}" flood-opacity="0.5"/>
    </filter>
  </defs>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="{BG}" stroke="{GREEN}" stroke-opacity="0.45"/>
  <text x="30" y="46" font-family="{FONT}" font-size="22" font-weight="bold" filter="url(#glow)">
    <tspan fill="{GREEN}">&#10095; </tspan><tspan fill="{FG}">opersona</tspan><tspan fill="{GREEN}">/</tspan>
  </text>
  <circle cx="{w - 30 - 10 * 8.0 - 12:.0f}" cy="40" r="5" fill="{LANG_COLORS['TypeScript']}"/>
  <text x="{w - 30}" y="45" text-anchor="end" font-family="{FONT}" font-size="13" fill="{DIM}">TypeScript</text>
  <text x="30" y="82" font-family="{FONT}" font-size="14" fill="{FG}">How you think, not what you know.</text>
  <text x="30" y="106" font-family="{FONT}" font-size="13" fill="{DIM}">A persistent Claude persona that learns your reasoning fingerprint — interviewed by</text>
  <text x="30" y="126" font-family="{FONT}" font-size="13" fill="{DIM}">your own Claude, proven by blind prediction tests, self-hosted and private by construction.</text>
  <text x="30" y="{h - 18}" font-family="{FONT}" font-size="12" fill="{GREEN}" fill-opacity="0.65"># ai  # claude  # mcp  # nextjs  # self-hosted  &#8594;  live at opersona.me</text>
</svg>
'''


outdir = os.path.join(os.path.dirname(__file__), "..", "assets", "cards")
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, "opersona.svg"), "w") as f:
    f.write(flagship())
print("wrote opersona.svg")
for c in CARDS:
    with open(os.path.join(outdir, c["file"]), "w") as f:
        f.write(card(c))
    print("wrote", c["file"])
