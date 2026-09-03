#!/usr/bin/env python3
"""Generate the animated terminal header SVG for the GitHub profile README."""
import html

W, H = 900, 318
BG = "#0d1117"
BAR = "#161b22"
GREEN = "#00FF41"
FG = "#e6edf3"
DIM = "#8b949e"
FONT = "'SF Mono','Cascadia Code','Fira Code',Menlo,Consolas,'DejaVu Sans Mono',monospace"
X = 34
CHAR_W = 10.0   # approx monospace advance at font-size 16
TYPE_SPEED = 0.045  # seconds per character


def esc(s):
    return html.escape(s, quote=True)


def typed_line(clip_id, y, t0, spans, total_len):
    """A command line revealed character-by-character via a discrete clip animation."""
    dur = max(total_len * TYPE_SPEED, 0.001)
    n = total_len
    values = ";".join(f"{i * CHAR_W:.0f}" for i in range(n + 1))
    key_times = ";".join(f"{i / n:.4f}" for i in range(n + 1))
    tspans = "".join(
        f'<tspan fill="{c}"{extra}>{esc(t)}</tspan>' for t, c, extra in spans
    )
    return f'''
  <clipPath id="{clip_id}"><rect x="{X}" y="{y - 20}" width="0" height="28">
    <animate attributeName="width" begin="{t0}s" dur="{dur:.3f}s" calcMode="discrete"
      values="{values}" keyTimes="{key_times}" fill="freeze"/>
  </rect></clipPath>
  <g clip-path="url(#{clip_id})">
    <text x="{X}" y="{y}" font-family="{FONT}" font-size="16">{tspans}</text>
  </g>'''


def fade_line(y, t0, spans, size=16, weight="normal", filt=""):
    tspans = "".join(
        f'<tspan fill="{c}"{extra}>{esc(t)}</tspan>' for t, c, extra in spans
    )
    return f'''
  <g opacity="0"{filt}>
    <animate attributeName="opacity" begin="{t0}s" dur="0.25s" values="0;1" fill="freeze"/>
    <text x="{X}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}">{tspans}</text>
  </g>'''


parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'role="img" aria-label="Terminal: whoami — Bishesh Shrestha, security engineer and automation addict">'
)
parts.append(f'''
  <defs>
    <filter id="glow" x="-20%" y="-40%" width="140%" height="180%">
      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="{GREEN}" flood-opacity="0.55"/>
    </filter>
    <clipPath id="win"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12"/></clipPath>
  </defs>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{BG}" stroke="{GREEN}" stroke-opacity="0.28"/>
  <g clip-path="url(#win)">
    <rect x="1" y="1" width="{W - 2}" height="46" fill="{BAR}"/>
  </g>
  <line x1="1" y1="47" x2="{W - 1}" y2="47" stroke="{GREEN}" stroke-opacity="0.15"/>
  <circle cx="28" cy="24" r="7" fill="#ff5f56"/>
  <circle cx="52" cy="24" r="7" fill="#ffbd2e"/>
  <circle cx="76" cy="24" r="7" fill="#27c93f"/>
  <text x="{W / 2}" y="29" text-anchor="middle" font-family="{FONT}" font-size="13" fill="{DIM}">bishesh@bee-automated: ~/github</text>''')

# --- terminal script -------------------------------------------------------
# 1) $ whoami
cmd1 = "$ whoami"
parts.append(typed_line("t1", 88, 0.4, [("$ ", GREEN, ""), ("whoami", FG, "")], len(cmd1)))
# 2) big name output
parts.append(fade_line(
    124, 1.1,
    [("Bishesh Shrestha", GREEN, ""), ("  ·  security engineer · automation addict", DIM, ' font-size="15" font-weight="normal"')],
    size=22, weight="bold", filt=' filter="url(#glow)"'))
# 3) $ cat motto.txt
cmd2 = "$ cat motto.txt"
parts.append(typed_line("t2", 164, 1.9, [("$ ", GREEN, ""), ("cat motto.txt", FG, "")], len(cmd2)))
# 4) motto output
parts.append(fade_line(
    194, 2.95,
    [('"Chaos is not the enemy. Unpreparedness is."', DIM, ' font-style="italic"')]))
# 5) $ ls ~/now
cmd3 = "$ ls ~/now"
parts.append(typed_line("t3", 234, 3.6, [("$ ", GREEN, ""), ("ls ~/now", FG, "")], len(cmd3)))
# 6) opersona output
parts.append(fade_line(
    264, 4.35,
    [("opersona/", GREEN, ' font-weight="bold"'), ("   # teaching an AI how I think", DIM, "")]))
# 7) idle prompt + blinking cursor
parts.append(f'''
  <g opacity="0">
    <animate attributeName="opacity" begin="4.9s" dur="0.15s" values="0;1" fill="freeze"/>
    <text x="{X}" y="298" font-family="{FONT}" font-size="16" fill="{GREEN}">$</text>
    <rect x="{X + 20}" y="284" width="10" height="18" fill="{GREEN}">
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/>
    </rect>
  </g>''')

parts.append("</svg>\n")

out = "".join(parts)
import os
path = os.path.join(os.path.dirname(__file__), "..", "assets", "header.svg")
import os
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w") as f:
    f.write(out)
print(f"wrote {path} ({len(out)} bytes)")
