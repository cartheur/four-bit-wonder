# Machine Memory and Game Version

## Identity

This is the small incremental improvement to the photographed Four-Bit Wonder.
It is a manual memory-match exploration stage: one `74LS85` compares the SRAM
word selected by the address switches with a value selected by the four data
switches. Red, yellow, and green indicators make the relation visible.

## Intended Focus

It is a read-and-match game, not an autonomous learner. The player chooses an
address and a proposed four-bit value; the indicators show whether the stored
word is lower, equal, or higher. The original manual write mechanism remains
unchanged.

## Included Hardware

| Qty | Part | Role |
| ---: | --- | --- |
| 1 | `74LS85` with 16-pin socket | Compares the SRAM read word with the four data switches. |
| 1 | `100nF` ceramic capacitor | Local comparator decoupling. |
| 3 | Red, yellow, and green panel indicators | Show `MATCH`, `HIGH / DECREASE`, and `LOW / INCREASE`. |
| 3 | NPN low-side driver stages | Drive the indicators without overloading LS-TTL outputs. |

Use existing unused panel LEDs where available; otherwise fit one red, one
yellow, and one green LED. The complete connection and driver guidance is in
[the comparator-stage document](comparator-version.md).

For the Polysance podcast or educational framing, use the
[Machine Memory and Game action brief](action-brief/GAME.md).

## Exploration Boundary

Do not add target latches, counters, sequencers, autonomous write control, or
automatic address scanning in this version. Those changes belong only to the
separate Machine Autonomous Version after this comparator experiment has made
the memory relationship visible and testable.

## Separation From Other Tracks

- [Existing Four-Bit Wonder](images/four-bit-wonder.jpg): retained original reference board.
- Machine Memory and Game Version: this small original-board comparator and memory-match game.
- [Machine Autonomous Version](machine-autonomous-version.md): separate new-board Base + Phase 1 + Phase 2 autonomous build.
