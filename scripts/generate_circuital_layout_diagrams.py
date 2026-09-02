#!/usr/bin/env python3
"""Render the Four-Bit Wonder Machine Autonomous Version socket plan as SVG."""

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
    width: int = 82


SOCKETS = (
    Socket("B1", "555", 8, 130, 235), Socket("B2", "74LS93", 14, 245, 225),
    Socket("B3", "74LS93", 14, 360, 225), Socket("B4", "74LS04", 14, 125, 590),
    Socket("B5", "74LS367", 16, 245, 570), Socket("B6", "uPB8226", 16, 375, 570),
    Socket("B7", "MM2114", 18, 495, 555), Socket("P0", "panel R/C", 24, 125, 940),
    Socket("P1", "panel R/C", 24, 285, 940), Socket("U1", "NE555", 8, 630, 230),
    Socket("U2", "74LS161", 16, 730, 220), Socket("U3", "74LS138", 16, 850, 220),
    Socket("U4", "74LS74", 14, 630, 420), Socket("U5", "74LS08", 14, 730, 420),
    Socket("U6", "74LS00", 14, 845, 420), Socket("P2", "555 R/C", 8, 555, 230, 50),
    Socket("P3", "LED drive", 16, 760, 1010, 70), Socket("P4", "mode/button", 16, 1010, 1010, 70),
    Socket("U7", "74LS173", 16, 700, 680), Socket("U8", "74LS85", 16, 825, 680),
    Socket("U9", "74LS193", 16, 950, 680), Socket("U10", "74LS125", 14, 1075, 690),
    Socket("U11", "74LS157", 16, 1190, 680), Socket("V1", "74LS393", 16, 1430, 205),
    Socket("V2", "74LS14", 14, 1550, 220), Socket("P5", "reset/button", 14, 1490, 400, 64),
    Socket("V3", "74LS157", 16, 1430, 590), Socket("V4", "74LS157", 16, 1550, 590),
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
    ("TP1", "CLK", 590, 365),
    ("TP2", "RST", 1090, 390),
    ("TP3", "D0-D3", 680, 630),
    ("TP4", "/CS", 840, 630),
    ("TP5", "/WE", 1000, 630),
    ("TP6", "ADDR", 1362, 720),
)

PHASE2B_GHOSTS = (
    ("189", 1410, 1035), ("189", 1455, 1035), ("189", 1500, 1035), ("189", 1545, 1035),
    ("139", 1410, 1120), ("153", 1455, 1120), ("153", 1500, 1120), ("04", 1545, 1120),
)

P2_ZONE = ("555 R/C", 550, 205, 60, 150)
P1_CONTROL_RESERVE = ("P1 CONTROL RESERVE", 960, 205, 360, 160)
P1_CONTROL_GHOSTS = (("08", 980, 270), ("123", 1030, 270), ("SPARE", 1080, 270))
POWER_PARTS = (
    ("J0", "2x T46-3-9/C", 110, 135, 105, "input"),
    ("C23", "47-100uF", 230, 135, 105, "bulk"),
    ("C24", "10-47uF P1", 1110, 575, 105, "bulk"),
    ("C25", "10-47uF P2", 1550, 855, 105, "bulk"),
)
TRANSISTORS = (("Q1", 850, 1040), ("Q2", 900, 1040), ("Q3", 950, 1040))

def socket_height(pins: int) -> int:
    return 38 + (pins // 2) * 18


def verify_no_socket_overlaps() -> None:
    for index, left in enumerate(SOCKETS):
        left_right = left.x + left.width
        left_bottom = left.y + socket_height(left.pins)
        for right in SOCKETS[index + 1:]:
            right_right = right.x + right.width
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
    width = socket.width
    height = socket_height(socket.pins)
    dots = []
    for index in range(socket.pins // 2):
        pin_y = socket.y + 28 + index * 18
        dots.append(f'<circle cx="{socket.x + 8}" cy="{pin_y}" r="3.4"/>')
        dots.append(f'<circle cx="{socket.x + width - 8}" cy="{pin_y}" r="3.4"/>')
    label_y = socket.y + height // 2 - 4
    return f'''<g class="socket">
  <rect x="{socket.x}" y="{socket.y}" width="{width}" height="{height}" rx="5"/>
  <path d="M {socket.x + width / 2 - 12} {socket.y} q 12 15 24 0" class="notch"/>
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


def svg_power_part(ref: str, label: str, x: int, y: int, width: int, kind: str) -> str:
    return f'''<g class="power-part {kind}">
  <rect x="{x}" y="{y}" width="{width}" height="24" rx="4"/>
  <text x="{x + 8}" y="{y + 11}" class="power-ref">{ref}</text>
  <text x="{x + 8}" y="{y + 21}" class="power-label">{label}</text>
</g>'''


def svg_transistor(ref: str, x: int, y: int) -> str:
    pins = "".join(f'<circle cx="{x + 9 + index * 9}" cy="{y + 40}" r="2.5"/>' for index in range(3))
    return f'''<g class="transistor">
  <rect x="{x}" y="{y}" width="36" height="30" rx="12"/>
  <text x="{x + 18}" y="{y + 19}">{ref}</text>{pins}
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
    p1_ghosts = "\n".join(svg_phase2b_ghost(*ghost) for ghost in P1_CONTROL_GHOSTS)
    power_parts = "\n".join(svg_power_part(*part) for part in POWER_PARTS)
    transistors = "\n".join(svg_transistor(*transistor) for transistor in TRANSISTORS)
    p2_label, p2_x, p2_y, p2_width, p2_height = P2_ZONE
    p2_zone = f'''<g><rect x="{p2_x}" y="{p2_y}" width="{p2_width}" height="{p2_height}" class="local-zone"/>
<text x="{p2_x + p2_width / 2}" y="{p2_y + 16}" class="local-zone-label">{p2_label}</text></g>'''
    reserve_label, reserve_x, reserve_y, reserve_width, reserve_height = P1_CONTROL_RESERVE
    p1_reserve = f'''<g><rect x="{reserve_x}" y="{reserve_y}" width="{reserve_width}" height="{reserve_height}" class="control-reserve"/>
<text x="{reserve_x + 14}" y="{reserve_y + 22}" class="control-reserve-label">{reserve_label}</text>
<text x="{reserve_x + 14}" y="{reserve_y + 43}" class="control-reserve-note">optional control logic</text>
{p1_ghosts}</g>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1320" viewBox="0 0 1800 1320" role="img" aria-labelledby="title desc">
<title id="title">Four-Bit Wonder Machine Autonomous Version socket layout</title>
<desc id="desc">Approximate scaled DIP socket plan for the independent Four-Bit Wonder new-board base machine and Phase 1 and 2 additions.</desc>
<style>
  .board {{ fill: #fbf5dd; stroke: #4d493f; stroke-width: 4; }}
  .grid {{ stroke: #a89d81; stroke-width: .45; opacity: .20; }}
  .zone {{ stroke: #6f6758; stroke-width: 1.4; stroke-dasharray: 7 5; }}
  .zone-label {{ font: 700 15px Georgia, serif; letter-spacing: 1.3px; fill: #403b31; }}
  .local-zone {{ fill: #f3e3b8; stroke: #8b7854; stroke-width: 1.2; stroke-dasharray: 4 3; }}
  .local-zone-label {{ font: 700 9px monospace; fill: #5b4d36; text-anchor: middle; }}
  .control-reserve {{ fill: #ffffff; fill-opacity: .24; stroke: #5b8f77; stroke-width: 1.2; stroke-dasharray: 6 4; }}
  .control-reserve-label {{ font: 700 12px Georgia, serif; letter-spacing: 1px; fill: #3f6653; }}
  .control-reserve-note {{ font: 10px monospace; fill: #4d7460; }}
  .socket rect {{ fill: #20211e; stroke: #0d0e0d; stroke-width: 2; }}
  .socket circle {{ fill: #d9ccb0; }}
  .notch {{ stroke: #f7f1df; stroke-width: 2.3; fill: none; }}
  .pin-one {{ font: 700 10px monospace; fill: #f1bf59; }}
  .ref {{ font: 700 12px monospace; fill: #ffffff; text-anchor: middle; }}
  .label {{ font: 10px monospace; fill: #ddd5c6; text-anchor: middle; }}
  .heading {{ font: 700 34px Georgia, serif; fill: #25231e; }}
  .subheading {{ font: 16px Georgia, serif; fill: #514c42; }}
  .legend {{ font: 13px monospace; fill: #36322b; }}
  .rail-plus {{ stroke: #ad4c40; stroke-width: 8; }}
  .rail-ground {{ stroke: #3d6c9f; stroke-width: 8; }}
  .rail-label {{ font: 700 12px monospace; }}
  .panel-header rect {{ fill: #f7f1df; stroke: #635b4e; stroke-width: 1.2; }}
  .panel-ref {{ font: 700 11px monospace; fill: #473f34; }}
  .panel-label {{ font: 10px monospace; fill: #473f34; }}
  .test-point circle {{ fill: #f7f1df; stroke: #7b4c35; stroke-width: 2; }}
  .test-point text {{ font: 10px monospace; fill: #704330; }}
  .ghost-socket rect {{ fill: #ffffff; fill-opacity: .28; stroke: #6c6c6c; stroke-width: 1.2; stroke-dasharray: 4 3; }}
  .ghost-socket text {{ font: 10px monospace; fill: #646464; text-anchor: middle; }}
  .power-part rect {{ stroke: #5c5548; stroke-width: 1.2; }}
  .power-part.input rect {{ fill: #e9e2d5; }}
  .power-part.fuse rect {{ fill: #f5d783; }}
  .power-part.bulk rect {{ fill: #d8e7df; }}
  .power-ref {{ font: 700 9px monospace; fill: #423a2e; }}
  .power-label {{ font: 8px monospace; fill: #423a2e; }}
  .transistor rect {{ fill: #53544d; stroke: #20211e; stroke-width: 1.4; }}
  .transistor circle {{ fill: #d9ccb0; }}
  .transistor text {{ font: 700 10px monospace; fill: #ffffff; text-anchor: middle; }}
</style>
<rect width="1800" height="1320" fill="#f6f1e6"/>
<text x="70" y="55" class="heading">Four-Bit Wonder: Machine Autonomous Version</text>
<text x="70" y="82" class="subheading">Independent new-board core: 28 sockets. Conceptual 0.1-inch grid; confirm final board dimensions before fabrication.</text>
<rect x="65" y="120" width="1670" height="1110" rx="14" class="board"/>
{svg_grid()}
<g aria-label="power rail locations">
  <path d="M 82 150 V 1200" class="rail-plus"/><text x="88" y="160" class="rail-label" fill="#ad4c40">+5V</text>
  <path d="M 1718 150 V 1200" class="rail-ground"/><text x="1685" y="160" class="rail-label" fill="#3d6c9f">GND</text>
</g>
{''.join(zones)}
{p2_zone}
{p1_reserve}
<g aria-label="power entry and bulk capacitors">{power_parts}
  <text x="350" y="151" class="control-reserve-note">USB-A: red +5V / black GND -> J0</text>
</g>
{socket_svg}
<g aria-label="LED driver transistor positions">{transistors}
  <text x="850" y="1100" class="control-reserve-note">Q1-Q3 LED drivers</text>
</g>
{panel_headers}
{test_points}
<g aria-label="optional Phase 2B ghost footprints">{ghosts}
  <text x="1410" y="1198" class="panel-label">P6-P8: 3 x 24-pin passives</text>
</g>
<g transform="translate(80 1260)"><rect width="1640" height="32" rx="5" fill="#e7dfca"/>
<text x="14" y="21" class="legend">Grid is a drafting reference only; pin 1 is amber. Keep bulk capacitors at rails and 100nF decouplers at IC sockets.</text></g>
</svg>'''


def main() -> None:
    if len(SOCKETS) != 28:
        raise ValueError(f"Expected 28 core sockets, found {len(SOCKETS)}")
    verify_no_socket_overlaps()
    OUTPUT.write_text(render(), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
