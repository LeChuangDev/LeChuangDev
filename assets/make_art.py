"""Generate the animated hero banner and the animated stack terminal (light + dark)."""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

THEMES = {
    "dark": {
        "bg1": "#0A0C11",
        "bg2": "#101319",
        "accent": "#8B5CF6",
        "pulse": "#C4B5FD",
        "cyan": "#22D3EE",
        "cyan_pulse": "#67E8F9",
        "title": "#F4F5F8",
        "muted": "#7C8698",
        "mono": "#B7BECF",
        "chip": "#121722",
        "chip_inner": "#8B5CF6",
        "scan_op": "0.22",
        "inner_op": "0.16",
        "chip_op": "0.5",
        "border": "#252C3A",
        "grid": "#FFFFFF",
        "grid_op": "0.065",
        "glow": "0.34",
        "fade": "#0A0C11",
        "panel": "#0C0F15",
        "panel_head": "#11151D",
        "panel_border": "#232A37",
        "dim": "#5C6678",
        "key": "#A78BFA",
        "val": "#CBD5E1",
        "cmd": "#E9E5FF",
    },
    "light": {
        "bg1": "#FCFBFF",
        "bg2": "#F3F0FC",
        "accent": "#6D28D9",
        "pulse": "#7C3AED",
        "cyan": "#0891B2",
        "cyan_pulse": "#0E7490",
        "title": "#14161C",
        "muted": "#6F7686",
        "mono": "#4B5563",
        "chip": "#F9F6FF",
        "chip_inner": "#6D28D9",
        "scan_op": "0.1",
        "inner_op": "0.34",
        "chip_op": "0.6",
        "border": "#E2DEF2",
        "grid": "#0B0D12",
        "grid_op": "0.05",
        "glow": "0.2",
        "fade": "#FFFFFF",
        "panel": "#FFFFFF",
        "panel_head": "#F7F5FE",
        "panel_border": "#E2DEF2",
        "dim": "#9AA1AF",
        "key": "#6D28D9",
        "val": "#374151",
        "cmd": "#1F2430",
    },
}

TRACES_LEFT = [
    "M938 116H876V84H804",
    "M938 144H852V172H768",
    "M938 172H844V212H700",
]
TRACES_RIGHT = [
    "M1114 144H1172V112H1240",
    "M1114 200H1192V236H1252",
]
VIAS_LEFT = [(804, 84), (768, 172), (700, 212)]
VIAS_RIGHT = [(1240, 112), (1252, 236)]

BANNER = """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="340" viewBox="0 0 1280 340" role="img" aria-label="LeChuangDev - From silicon to cloud">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="{bg1}"/>
      <stop offset="1" stop-color="{bg2}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.78" cy="0.12" r="0.72">
      <stop offset="0" stop-color="{accent}" stop-opacity="{glow}"/>
      <stop offset="0.5" stop-color="{accent}" stop-opacity="0.08"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="fadeDown" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0.55" stop-color="{fade}" stop-opacity="0"/>
      <stop offset="1" stop-color="{fade}" stop-opacity="0.85"/>
    </linearGradient>
    <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{accent}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{accent}" stop-opacity="{scan_op}"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="{grid}" stroke-opacity="{grid_op}" stroke-width="1"/>
    </pattern>
    <clipPath id="chipInner">
      <rect x="968" y="108" width="116" height="124" rx="8"/>
    </clipPath>
  </defs>

  <rect width="1280" height="340" rx="18" fill="url(#bg)"/>
  <rect width="1280" height="340" rx="18" fill="url(#grid)"/>
  <rect width="1280" height="340" rx="18" fill="url(#glow)"/>
  <rect width="1280" height="340" rx="18" fill="url(#fadeDown)"/>

  <!-- 电路走线：左侧来自硅片，右侧通向云端 -->
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <g stroke="{accent}" stroke-opacity="0.55" stroke-width="1.6">
{left_paths}
    </g>
    <g stroke="{accent}" stroke-opacity="0.55" stroke-width="1.6">
{right_paths}
    </g>
  </g>

  <!-- 走线上流动的信号 -->
  <g>
{pulses}
  </g>

  <!-- 过孔 -->
  <g>
{vias}
  </g>

  <!-- 芯片：引脚 -->
  <g stroke="{accent}" stroke-opacity="0.55" stroke-width="1.6" stroke-linecap="round">
    <path d="M938 116h14M938 144h14M938 172h14M938 200h14M938 228h14"/>
    <path d="M1100 116h14M1100 144h14M1100 172h14M1100 200h14M1100 228h14"/>
  </g>
  <!-- 芯片：本体 -->
  <rect x="952" y="92" width="148" height="156" rx="12" fill="{chip}" stroke="{accent}" stroke-opacity="{chip_op}" stroke-width="1.6"/>
  <rect x="968" y="108" width="116" height="124" rx="8" fill="none" stroke="{chip_inner}" stroke-opacity="{inner_op}" stroke-width="1.2"/>
  <!-- 芯片：逐行扫描的光带 -->
  <g clip-path="url(#chipInner)">
    <rect x="968" y="96" width="116" height="34" fill="url(#scan)">
      <animate attributeName="y" values="94;216;94" dur="6.5s" repeatCount="indefinite"/>
    </rect>
  </g>
  <!-- 芯片：核心与呼吸环 -->
  <circle cx="1026" cy="152" r="13" fill="none" stroke="{accent}" stroke-opacity="0.45" stroke-width="1.4"/>
  <circle cx="1026" cy="152" r="13" fill="none" stroke="{accent}" stroke-width="1.2">
    <animate attributeName="r" values="13;24;13" dur="3.6s" repeatCount="indefinite"/>
    <animate attributeName="stroke-opacity" values="0.5;0;0.5" dur="3.6s" repeatCount="indefinite"/>
  </circle>
  <circle cx="1026" cy="152" r="4" fill="{accent}" fill-opacity="0.9">
    <animate attributeName="r" values="4;5.4;4" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  <path d="M1013 152h-18M1039 152h18M1026 139v-18M1026 165v18" stroke="{accent}" stroke-opacity="0.25" stroke-width="1.2" stroke-linecap="round"/>

  <!-- 左侧文字 -->
  <g font-family="'Segoe UI','Helvetica Neue',Helvetica,Arial,system-ui,sans-serif">
    <text x="72" y="110" font-size="12" letter-spacing="4.4" fill="{muted}">FULL-STACK ENGINEER</text>
    <text x="70" y="184" font-size="58" font-weight="700" letter-spacing="-1.4" fill="{title}">LeChuangDev</text>
    <rect x="72" y="206" width="56" height="3" rx="1.5" fill="{accent}"/>
  </g>

  <!-- 终端提示符下轮播的三句自述 -->
  <g font-family="'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace">
    <rect x="72" y="239" width="8" height="12" rx="1.5" fill="{accent}" opacity="0.9">
      <animate attributeName="opacity" values="0.9;0.9;0;0" keyTimes="0;0.48;0.5;1" dur="1.05s" repeatCount="indefinite"/>
    </rect>
    <text x="92" y="249" font-size="13.5" letter-spacing="3.2" fill="{mono}">FROM SILICON TO CLOUD
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.3;0.33;1" dur="15s" begin="0s" repeatCount="indefinite"/>
    </text>
    <text x="92" y="249" font-size="13.5" letter-spacing="3.2" fill="{mono}" opacity="0">POWER · FIRMWARE · WEB · CLOUD
      <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.02;0.3;0.33;1" dur="15s" begin="5s" repeatCount="indefinite"/>
    </text>
    <text x="92" y="249" font-size="13.5" letter-spacing="3.2" fill="{mono}" opacity="0">先测量 · 后假设 · 单变量迭代
      <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.02;0.3;0.33;1" dur="15s" begin="10s" repeatCount="indefinite"/>
    </text>
    <text x="72" y="278" font-size="12" letter-spacing="2.2" fill="{muted}">zhangwenle.com　·　github.com/LeChuangDev</text>
  </g>

  <rect x="0.5" y="0.5" width="1279" height="339" rx="17.5" fill="none" stroke="{border}" stroke-width="1"/>
</svg>
"""

TERMINAL = """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="286" viewBox="0 0 1280 286" role="img" aria-label="技术栈：power / firmware / web / cloud / tooling">
  <defs>
    <linearGradient id="panel" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0" stop-color="{panel_head}"/>
      <stop offset="0.18" stop-color="{panel}"/>
      <stop offset="1" stop-color="{panel}"/>
    </linearGradient>
    <radialGradient id="tglow" cx="0.1" cy="0" r="0.9">
      <stop offset="0" stop-color="{accent}" stop-opacity="{glow}"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="tgrid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="{grid}" stroke-opacity="{grid_op}" stroke-width="1"/>
    </pattern>
  </defs>

  <rect width="1280" height="286" rx="16" fill="url(#panel)"/>
  <rect width="1280" height="286" rx="16" fill="url(#tgrid)"/>
  <rect width="1280" height="286" rx="16" fill="url(#tglow)"/>

  <!-- 窗口标题栏 -->
  <path d="M0 16a16 16 0 0 1 16-16h1248a16 16 0 0 1 16 16v30H0z" fill="{panel_head}"/>
  <circle cx="34" cy="26" r="5" fill="#F87171"/>
  <circle cx="52" cy="26" r="5" fill="#FBBF24"/>
  <circle cx="70" cy="26" r="5" fill="#34D399"/>
  <text x="94" y="30" font-family="'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace" font-size="11.5" letter-spacing="1.2" fill="{dim}">stack — zsh — 1280×286</text>
  <line x1="0" y1="46" x2="1280" y2="46" stroke="{panel_border}" stroke-width="1"/>

  <g font-family="'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace" font-size="15">
    <text x="48" y="84" fill="{cmd}">$ stack --list
      <animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.02;0.07;1" dur="3s" repeatCount="1"/>
    </text>
    <g>
      <animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.07;0.12;1" dur="3s" repeatCount="1"/>
      <text x="48" y="126" fill="{key}">power</text>
      <text x="176" y="126" fill="{val}">DC-DC 拓扑 · 纹波抑制 · 热设计 · 多层板 Layout</text>
    </g>
    <g>
      <animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.10;0.15;1" dur="3s" repeatCount="1"/>
      <text x="48" y="158" fill="{key}">firmware</text>
      <text x="176" y="158" fill="{val}">STM32 · ESP32 · 裸机 C · FreeRTOS · CMSIS · USB-PD</text>
    </g>
    <g>
      <animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.13;0.18;1" dur="3s" repeatCount="1"/>
      <text x="48" y="190" fill="{key}">web</text>
      <text x="176" y="190" fill="{val}">Astro · Vue · TypeScript · Tailwind · Vite</text>
    </g>
    <g>
      <animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.16;0.21;1" dur="3s" repeatCount="1"/>
      <text x="48" y="222" fill="{key}">cloud</text>
      <text x="176" y="222" fill="{val}">Docker · Kubernetes · Nginx · GitHub Actions</text>
    </g>
    <g>
      <animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.19;0.24;1" dur="3s" repeatCount="1"/>
      <text x="48" y="254" fill="{key}">tooling</text>
      <text x="176" y="254" fill="{val}">KiCad · 立创 EDA · PyQt6 · Playwright</text>
    </g>
    <rect x="48" y="266" width="9" height="15" fill="{accent}" opacity="0">
      <animate attributeName="opacity" values="0;0.9;0.9;0;0" keyTimes="0;0.01;0.5;0.52;1" dur="3.4s" begin="3.2s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- 右侧：示波器式的实时信号，作为留白的视觉配重 -->
  <line x1="742" y1="70" x2="742" y2="262" stroke="{panel_border}" stroke-width="1"/>
  <g font-family="'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace">
    <text x="778" y="84" font-size="11" letter-spacing="2.4" fill="{dim}">LIVE SIGNAL</text>
    <text x="1226" y="84" font-size="11" letter-spacing="1.6" fill="{dim}" text-anchor="end">CH1 · 1 kHz</text>
    <g stroke="{grid}" stroke-opacity="0.06" stroke-width="1">
      <path d="M778 120H1226M778 160H1226M778 200H1226M778 240H1226"/>
      <path d="M838 96V252M930 96V252M1022 96V252M1114 96V252M1206 96V252"/>
    </g>
    <path d="M778 180H1226" stroke="{accent}" stroke-opacity="0.18" stroke-width="1" stroke-dasharray="3 5"/>
    <path d="{wave}" fill="none" stroke="{accent}" stroke-opacity="0.22" stroke-width="1.6" stroke-linejoin="round"/>
    <path d="{wave}" fill="none" stroke="{pulse}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"
          pathLength="1000" stroke-dasharray="86 914">
      <animate attributeName="stroke-dashoffset" values="0;-1000" dur="7s" repeatCount="indefinite"/>
    </path>
    <circle cx="778" cy="180" r="3" fill="{cyan}">
      <animate attributeName="opacity" values="0.35;1;0.35" dur="2.8s" repeatCount="indefinite"/>
    </circle>
  </g>

  <rect x="0.5" y="0.5" width="1279" height="285" rx="15.5" fill="none" stroke="{panel_border}" stroke-width="1"/>
</svg>
"""


def ecg_path(x0: float = 778, x1: float = 1226, y: float = 180) -> str:
    import math

    period = (x1 - x0) / 2.0
    pts: list[str] = []
    for k in range(2):
        base = x0 + k * period
        seq = [
            (0.00, 0), (0.26, 0), (0.33, 6), (0.40, -6), (0.47, 0),
            (0.56, 0), (0.60, 24), (0.64, -46), (0.68, 14), (0.72, 0),
            (0.84, 0), (0.90, -14), (0.96, 0), (1.00, 0),
        ]
        for frac, dy in seq:
            x = base + frac * period
            pts.append(f"{x:.1f} {y + dy}")
    return "M" + " L".join(pts)


def build(theme: str) -> None:
    c = THEMES[theme]

    left_paths = "\n".join(f'      <path d="{p}"/>' for p in TRACES_LEFT)
    right_paths = "\n".join(f'      <path d="{p}"/>' for p in TRACES_RIGHT)

    pulses = []
    durations = (3.4, 4.1, 4.8)
    for i, path in enumerate(TRACES_LEFT):
        dur = durations[i]
        pulses.append(
            f'    <circle r="3.2" fill="{c["pulse"]}" opacity="0">\n'
            f'      <animateMotion dur="{dur}s" begin="{0.2 + i * 0.9:.1f}s" repeatCount="indefinite" path="{path}"/>\n'
            f'      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.12;0.72;1" '
            f'dur="{dur}s" begin="{0.2 + i * 0.9:.1f}s" repeatCount="indefinite"/>\n'
            f"    </circle>"
        )
    for i, path in enumerate(TRACES_RIGHT):
        dur = 3.0 + i * 0.8
        pulses.append(
            f'    <circle r="2.8" fill="{c["pulse"]}" opacity="0">\n'
            f'      <animateMotion dur="{dur}s" begin="{1.4 + i * 1.1:.1f}s" repeatCount="indefinite" path="{path}"/>\n'
            f'      <animate attributeName="opacity" values="0;0.8;0.8;0" keyTimes="0;0.12;0.72;1" '
            f'dur="{dur}s" begin="{1.4 + i * 1.1:.1f}s" repeatCount="indefinite"/>\n'
            f"    </circle>"
        )

    vias = []
    for x, y in VIAS_LEFT:
        vias.append(f'    <circle cx="{x}" cy="{y}" r="3.4" fill="{c["accent"]}" fill-opacity="0.9"/>')
        vias.append(
            f'    <circle cx="{x}" cy="{y}" r="7.6" fill="none" stroke="{c["accent"]}" stroke-opacity="0.3" stroke-width="1.2"/>'
        )
    for x, y in VIAS_RIGHT:
        vias.append(f'    <circle cx="{x}" cy="{y}" r="3" fill="{c["accent"]}" fill-opacity="0.75"/>')

    svg = BANNER.format(left_paths=left_paths, right_paths=right_paths, pulses="\n".join(pulses), vias="\n".join(vias), **c)
    (ASSETS / f"banner-{theme}.svg").write_text(svg, encoding="utf-8")

    term = TERMINAL.format(wave=ecg_path(), **c)
    (ASSETS / f"stack-{theme}.svg").write_text(term, encoding="utf-8")

    print(f"{theme}: banner {len(svg)}B, stack {len(term)}B")


if __name__ == "__main__":
    for t in ("dark", "light"):
        build(t)
