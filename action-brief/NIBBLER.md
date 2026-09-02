# RAM7400 Nibble Target: Action Brief

## Purpose

This is an optional follow-on mini-project for the Machine Memory and Game
Version. Four `74LS00` chips form four independent volatile D-latches: one
nibble of visible target memory. A person sets a target on the four data
switches, presses a dedicated latch button, and the stored target remains at
the comparator while the switches can be changed.

It is deliberately separate from the small `74LS85` comparator modification.
Build and validate that modification first.

## Why It Is Interesting

The existing game compares the SRAM word with the live data-switch setting.
This mini-project gives the target its own physical, volatile memory. It makes
the distinction between a proposed value, a latched value, and the value read
from the `MM2114A` visible without making the board autonomous.

Power removal clears no defined state: the NAND latches are volatile and their
power-on contents must be treated as unknown.

## Minimum Hardware

| Qty | Part | Role |
| ---: | --- | --- |
| 4 | `74LS00` with 14-pin sockets | One self-contained NAND D-latch per bit. |
| 4 | 4.7k ohm resistors | RAM7400 per-bit feedback/data interface. |
| 4 | `1N4148` diodes | Isolate each latch output from its data input path. |
| 2 | 100nF ceramic capacitors | Local decoupling, placed across the latch sockets. |
| 1 | Normally-closed, open-on-press pushbutton | Shared latch/write pulse. |
| 1 | Small separate perfboard or breadboard section | Keeps this experimental module reversible. |

Use the proven per-bit circuit in the [RAM7400 project](https://github.com/cartheur-dot/RAM7400).
Verify the actual resistor value and `74LS00` pin wiring against that circuit
before assembly; do not infer it from a generic NAND-latch diagram.

## Interface Boundary

For one nibble, provide these labelled terminals:

| Signals | Connection |
| --- | --- |
| `D0`-`D3` | Four data-switch signals, used while loading the target. |
| `LATCH` | One shared pulse from the dedicated pushbutton. |
| `Q0`-`Q3` | Four latch outputs to the `B0`-`B3` inputs of the `74LS85`. |
| `+5V`, `GND` | Common supply with local decoupling. |

This is not a two-wire module. Its four data lines, latch control, and supply
connections are all required. Bring `Q0`-`Q3` out as dedicated taps before the
RAM7400 diode/resistor feedback path.

Do **not** connect the RAM7400 data/output path directly to the bidirectional
`MM2114A` data bus. The latch output is active through its feedback network;
connecting it to the SRAM bus risks contention. The only planned connection to
the current modification is the dedicated `Q0`-`Q3` target input at the
comparator.

## Demonstration Sequence

1. Build and prove the comparator-only memory game first.
2. Set a four-bit target using the existing data switches.
3. Press `LATCH` to store that target in the RAM7400 nibble.
4. Change the data switches and show that the comparator target remains held.
5. Select SRAM addresses and observe lower, equal, or higher against the held target.

## Communication Boundary

Describe this as a hand-loaded volatile target register or a NAND-latch memory
exercise. It does not learn, select its own target, write the SRAM
automatically, or survive power removal. Those behaviours remain outside this
mini-project and outside the original-board modification.
