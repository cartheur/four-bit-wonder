# Machine Memory and Game: Polysance Action Brief

## Purpose

Use the Machine Memory and Game Version as a small, legible educational action:
one `74LS85` compares a value held in SRAM with a value selected by a person.
Red, yellow, and green indicators make the relation visible as lower, equal,
or higher. The point is not to claim an autonomous learner, but to show how a
simple memory relation can become observable and playable.

## Podcast Or Educational Talking Points

1. Start with the existing Four-Bit Wonder: six switches select a memory address and four switches propose a four-bit value.
2. Explain that the `74LS85` answers one concrete question: is the stored value lower than, equal to, or higher than the proposed value?
3. Demonstrate the three outcomes: green for stored value lower, red for match, and yellow for stored value higher.
4. Frame the interaction as a small memory-match game: select an address, propose a value, observe the relation, then use the existing manual write controls to change the stored state if desired.
5. Emphasize legibility: the address, proposed value, stored value, and comparison result remain physically inspectable.
6. Draw the boundary clearly: this version does not choose values, write automatically, sequence phases, or scan addresses.
7. Connect it to the later Machine Autonomous Version only as an exploration path: the comparator result is made visible here before a separate new-board machine acts on it.

## Demonstration Sequence

1. Select an address and put the existing board in read mode.
2. Set a target value on the four data switches.
3. Show the active comparison indicator and explain its meaning.
4. Change the target or address to show a different outcome.
5. Optionally make a manual write, return to read mode, and show that the comparison changed because memory changed.

## Communication Guardrails

- Call this a comparator-based memory game or exploration, not an autonomous machine.
- Do not imply that the board learns, chooses, or retains state after power removal.
- Keep the contrast explicit: this is a small modification to the original board; the autonomous version is a separate new-board project.

## Technical Reference

The circuit design, parts list, and wire-wrap instructions remain in
[the comparator-stage document](../comparator-version.md). Consult the local
[`SN74LS85` datasheet](../datasheets/74ls85.pdf) before fitting the IC.
