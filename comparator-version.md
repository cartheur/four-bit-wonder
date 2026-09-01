# Comparator Version: Four-Bit Memory Match Game

## Purpose

This is the smallest extension to the Four-Bit Wonder. It uses a `74LS85`
4-bit magnitude comparator and three existing unused panel LEDs to compare a
value manually selected on the four top data switches with the value currently
read from the `MM2114A` SRAM.

It is a read-and-match game, not an autonomous learner. The four data switches
remain both the normal data-entry controls and the comparison target.

## Existing Board Signals

The connections below use names rather than physical pin numbers because the
board wiring should be traced before soldering a new branch.

| Signal | Source | Use in this add-on |
| --- | --- | --- |
| `S0`-`S3` | Four top data switches, on the switch side of their series resistors | Target word |
| `M0`-`M3` | 2114 data bus, on the SRAM/bus-buffer side of the series resistors | Current stored word during a read |
| `/CS` | Existing chip-select control | Defines whether SRAM output is valid |
| `/WE` | Existing read/write control | Must be high for a read |
| `+5V`, `GND` | Board supply | Comparator and LED drivers |

`S0` is the least-significant bit and `S3` is the most-significant bit. Keep
the same bit order at every connection.

## 74LS85 Connections

The comparator must receive two independent words. Do not connect both sides
of the comparator to the bidirectional SRAM bus.

| 74LS85 input | Connect to |
| --- | --- |
| `A0`-`A3` | `M0`-`M3`, the read side of the SRAM data bus |
| `B0`-`B3` | `S0`-`S3`, directly at the data-switch side of the series resistors |
| cascade `A<B` input | `GND` |
| cascade `A=B` input | `+5V` |
| cascade `A>B` input | `GND` |
| `VCC` | `+5V` |
| `GND` | `GND` |

The cascade inputs make this a standalone four-bit comparison. Add a `100 nF`
ceramic capacitor directly between the `74LS85` supply pins.

The useful output meanings are:

| Comparator output | Meaning | Suggested panel LED |
| --- | --- | --- |
| `A < B` | Stored word is lower than switch word | Lower unused LED: `LOW` |
| `A = B` | Stored word matches switch word | Top unused LED: `MATCH` |
| `A > B` | Stored word is higher than switch word | Other lower unused LED: `HIGH` |

## LED Drivers

Do not rely on an LS-TTL output to source panel LED current directly. For each
of the three outputs, use an NPN low-side driver:

```text
74LS85 output -- 10k -- base of 2N3904 (or BC547)
                         emitter -- GND

+5V -- LED resistor -- LED anode
LED cathode ----------- collector
```

Start with `3.3k` LED resistors for ordinary indicator LEDs. A `100k`
base-to-emitter resistor is optional but keeps the transistor definitely off
when the logic is unpowered. The existing LEDs may already have current
limiting resistors; verify this before adding another resistor.

## Operating Procedure

1. Keep `/CS` asserted and select **READ** (`/WE` high).
2. Choose an SRAM address with the board's six address switches.
3. Set a target number from `0` to `15` on the four top data switches.
4. Read the three LEDs.
5. Change the selected address or target word and repeat.

The result is meaningful only while the SRAM is selected for read. During a
write, or when the chip is deselected, the `MM2114A` output bus is
high-impedance and the comparator result is not meaningful.

## What This Demonstrates

The selected address is a small state, the top switches are a proposed value,
and the LEDs expose a direct relation between them: lower, equal, or higher.
It makes the memory/bus operation inspectable without changing the original
manual write mechanism.

## Limitation

The data switches cannot simultaneously be a fixed target and a new value to
write. Moving them to enter a revised word also moves the comparison target.
The autonomous design in `autonomous-version.md` solves that by latching the
target word before it begins modifying SRAM.
