#!/usr/bin/env python3
"""Render the Four-Bit Wonder blank-board socket and wire-wrap plan as SVG."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "images" / "socket-layout.svg"


@dataclass(frozen=True)
class Socket:
    ref: str
    label: str
    pins: int
    x: int
    y: int


SOCKETS = (
    Socket("B1", "555", 8, 130, 235), Socket("B2", "74LS93", 14, 245, 225),
    Socket("B3", "74LS93", 14, 360, 225), Socket("B4", "74LS04", 14, 125, 590),
    Socket("B5", "74LS367", 16, 245, 570), Socket("B6", "uPB8226", 16, 375, 570),
    Socket("B7", "MM2114", 18, 495, 555), Socket("P0", "panel R/C", 24, 125, 940),
    Socket("P1", "panel R/C", 24, 285, 940), Socket("U1", "NE555", 8, 630, 230),
    Socket("U2", "74LS161", 16, 730, 220), Socket("U3", "74LS138", 16, 850, 220),
    Socket("U4", "74LS74", 14, 630, 420), Socket("U5", "74LS08", 14, 730, 420),
    Socket("U6", "74LS00", 14, 845, 420), Socket("P2", "P1 passives", 24, 960, 350),
    Socket("P3", "P1 passives", 24, 1100, 350), Socket("P4", "P1 passives", 24, 1240, 350),
    Socket("U7", "74LS173", 16, 700, 680), Socket("U8", "74LS85", 16, 825, 680),
    Socket("U9", "74LS193", 16, 950, 680), Socket("U10", "74LS125", 14, 1075, 690),
    Socket("U11", "74LS157", 16, 1190, 680), Socket("V1", "74LS393", 16, 1430, 205),
    Socket("V2", "74LS14", 14, 1550, 220), Socket("V3", "74LS157", 16, 1430, 470),
    Socket("V4", "74LS157", 16, 1550, 470), Socket("P5", "P2 passives", 24, 1435, 715),
)

ZONES = (
    ("BASE TIMING", 95, 165, 455, 350, "#f5e5c8"),
    ("PHASE 1 CLOCK / CONTROL", 610, 165, 735, 455, "#dbece5"),
    ("PHASE 2 ADDRESS", 1380, 165, 300, 820, "#dbe5f4"),
    ("BASE BUS / SRAM", 95, 530, 500, 290, "#f1dfd6"),
    ("PHASE 1 FOUR-BIT DATA PATH", 650, 640, 695, 240, "#f2e8cf"),
    ("PANEL INTERFACE / RESISTOR STRIPS", 95, 900, 1240, 305, "#e6e1f1"),
    ("PHASE 2B RESERVE", 1380, 1000, 300, 205, "#eeeeee"),
)

PANEL_HEADERS = (
    ("J1", "ADDR A0-A5", 430, 950, 150),
    ("J2", "DATA D0-D3", 595, 950, 150),
    ("J3", "LED0-LED9", 760, 950, 150),
    ("J4", "MODE / WRITE", 925, 950, 170),
    ("J5", "+5V / GND", 1110, 950, 170),
)

TEST_POINTS = (
    ("TP1", "CLK", 590, 245),
    ("TP2", "RST", 1090, 245),
    ("TP3", "D0-D3", 680, 630),
    ("TP4", "/CS", 840, 630),
    ("TP5", "/WE", 1000, 630),
    ("TP6", "ADDR", 1362, 720),
)

PHASE2B_GHOSTS = (
    ("189", 1410, 1035), ("189", 1455, 1035), ("189", 1500, 1035), ("189", 1545, 1035),
    ("139", 1410, 1120), ("153", 1455, 1120), ("153", 1500, 1120), ("04", 1545, 1120),
)

def socket_height(pins: int) -> int:
    return 38 + (pins // 2) * 18


def verify_no_socket_overlaps() -> None:
    for index, left in enumerate(SOCKETS):
        left_right = left.x + 82
        left_bottom = left.y + socket_height(left.pins)
        for right in SOCKETS[index + 1:]:
            right_right = right.x + 82
            right_bottom = right.y + socket_height(right.pins)
            overlaps = (
                left.x < right_right
                and left_right > right.x
                and left.y < right_bottom
                and left_bottom > right.y
            )
            if overlaps:
                raise ValueError(f"Socket overlap: {left.ref} and {right.ref}")


def svg_socket(socket: Socket) -> str:
    width = 82
    height = socket_height(socket.pins)
    dots = []
    for index in range(socket.pins // 2):
        pin_y = socket.y + 28 + index * 18
        dots.append(f'<circle cx="{socket.x + 8}" cy="{pin_y}" r="3.4"/>')
        dots.append(f'<circle cx="{socket.x + width - 8}" cy="{pin_y}" r="3.4"/>')
    label_y = socket.y + height // 2 - 4
    return f'''<g class="socket">
  <rect x="{socket.x}" y="{socket.y}" width="{width}" height="{height}" rx="5"/>
  <path d="M {socket.x + 29} {socket.y} q 12 15 24 0" class="notch"/>
  <text x="{socket.x + 14}" y="{socket.y + 20}" class="pin-one">1</text>
  <text x="{socket.x + width / 2}" y="{label_y}" class="ref">{escape(socket.ref)}</text>
  <text x="{socket.x + width / 2}" y="{label_y + 17}" class="label">{escape(socket.label)}</text>
  {''.join(dots)}
</g>'''


def svg_grid() -> str:
    vertical = "".join(f'<path d="M {x} 145 V 1205"/>' for x in range(85, 1720, 20))
    horizontal = "".join(f'<path d="M 85 {y} H 1715"/>' for y in range(145, 1210, 20))
    return f'<g class="grid">{vertical}{horizontal}</g>'


def svg_panel_header(ref: str, label: str, x: int, y: int, width: int) -> str:
    return f'''<g class="panel-header">
  <rect x="{x}" y="{y}" width="{width}" height="38" rx="4"/>
  <text x="{x + 10}" y="{y + 16}" class="panel-ref">{ref}</text>
  <text x="{x + 10}" y="{y + 31}" class="panel-label">{label}</text>
</g>'''


def svg_test_point(ref: str, label: str, x: int, y: int) -> str:
    return f'''<g class="test-point">
  <circle cx="{x}" cy="{y}" r="9"/>
  <text x="{x + 13}" y="{y - 3}">{ref}</text>
  <text x="{x + 13}" y="{y + 10}">{label}</text>
</g>'''


def svg_phase2b_ghost(label: str, x: int, y: int) -> str:
    return f'''<g class="ghost-socket">
  <rect x="{x}" y="{y}" width="34" height="68" rx="3"/>
  <text x="{x + 17}" y="{y + 38}">{label}</text>
</g>'''


def render() -> str:
    zones = []
    for label, x, y, width, height, color in ZONES:
        zones.append(
            f'<g><rect x="{x}" y="{y}" width="{width}" height="{height}" '
            f'fill="{color}" class="zone"/><text x="{x + 14}" y="{y + 24}" '
            f'class="zone-label">{label}</text></g>'
        )
    socket_svg = "\n".join(svg_socket(socket) for socket in SOCKETS)
    panel_headers = "\n".join(svg_panel_header(*header) for header in PANEL_HEADERS)
    test_points = "\n".join(svg_test_point(*point) for point in TEST_POINTS)
    ghosts = "\n".join(svg_phase2b_ghost(*ghost) for ghost in PHASE2B_GHOSTS)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1320" viewBox="0 0 1800 1320" role="img" aria-labelledby="title desc">
<title id="title">Four-Bit Wonder blank-board socket layout</title>
<desc id="desc">Approximate scaled DIP socket plan for the base machine and Phase 1 and 2 additions.</desc>
<style>
  .board {{ fill: #fbf5dd; stroke: #4d493f; stroke-width: 4; }}
  .zone {{ stroke: #6f6758; stroke-width: 1.4; stroke-dasharray: 7 5; }}
  .zone-label {{ font: 700 15px Georgia, serif; letter-spacing: 1.3px; fill: #403b31; }}
  .socket rect {{ fill: #20211e; stroke: #0d0e0d; stroke-width: 2; }}
  .socket circle {{ fill: #d9ccb0; }}
  .notch {{ stroke: #f7f1df; stroke-width: 2.3; fill: none; }}
  .ref {{ font: 700 12px monospace; fill: #ffffff; text-anchor: middle; }}
  .label {{ font: 10px monospace; fill: #ddd5c6; text-anchor: middle; }}
  .heading {{ font: 700 34px Georgia, serif; fill: #25231e; }}
  .subheading {{ font: 16px Georgia, serif; fill: #514c42; }}
  .legend {{ font: 13px monospace; fill: #36322b; }}
</style>
<rect width="1800" height="1320" fill="#f6f1e6"/>
<text x="70" y="55" class="heading">Four-Bit Wonder: Blank-Board Socket Plan</text>
<text x="70" y="82" class="subheading">Core build: 28 sockets. Placement plan only; circuit wiring follows in a separate schematic.</text>
<rect x="65" y="120" width="1670" height="1110" rx="14" class="board"/>
{''.join(zones)}
{socket_svg}
<g transform="translate(80 1260)"><rect width="1640" height="32" rx="5" fill="#e7dfca"/>
<text x="14" y="21" class="legend">Footprints scale by DIP pin pairs. Keep 100nF decouplers at IC sockets; use P0-P5 for resistor, timing, bulk, and control passives.</text></g>
</svg>'''


def main() -> None:
    if len(SOCKETS) != 28:
        raise ValueError(f"Expected 28 core sockets, found {len(SOCKETS)}")
    verify_no_socket_overlaps()
    OUTPUT.write_text(render(), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
