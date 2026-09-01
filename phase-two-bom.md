# Phase 2 Bill of Materials: Autonomous Address Scanning

Phase 2 extends the single-address autonomous hill climber into a machine that
can step through all 64 addresses exposed by the front panel. It preserves
manual address selection and the Phase 1 controller described in
`four-bit-wonder-autonomous-addition.md`.

This phase uses one captured four-bit target for every address. A separate
target for each address is an optional Phase 2B expansion, listed below.

## Required New Logic ICs

| Qty | Part | Basket status | Role |
| ---: | --- | --- | --- |
| 1 | `SN74LS393N` | Basket has 10; reserve 1 | Dual four-bit counter used as a six-bit automatic address counter. Use outputs `QA` through `QD` of the first section and `QA`, `QB` of the second section for address bits `A0` through `A5`. |
| 2 | `SN74LS157N` | Basket has 10; inventory has none: retain/order 2 | Six 2:1 address multiplexers. Together they select either the six front-panel address-switch signals or the six automatic-counter signals. |
| 1 | `SN74LS14N` | Inventory has 10: reserve 1 | Schmitt-trigger inverters for debouncing and shaping the `ADVANCE`, reset, and mode-transition signals. |

Cascade the two counter sections by connecting the first section's `QD` output
to the second section's clock input. Reset both sections together.

The existing Phase 1 `74LS08` and `74LS00` may have spare gates for the
`MATCH AND ADVANCE` logic. If a further `SN74LS08N` is needed, it is already
covered by the basket quantity of ten.

## Optional Control IC

| Qty | Part | Basket status | When to fit it | Role |
| ---: | --- | --- | --- | --- |
| 1 | `SN74LS123N` | Inventory has 10: reserve 1 | Recommended if the match/advance handoff produces an uncertain pulse or if a clean single-step control is desired. | Dual retriggerable monostable; creates one defined address-advance pulse. |

At the intended slow demonstration speed, the `74LS393` is suitable. Do not
clock it directly from a comparator output: derive a clean, phase-qualified
advance pulse after `MATCH / HALT` has been established.

## Optional Phase 2B: A Target for Each Address

The Phase 1 `74LS173` stores only one four-bit target. To give all 64 SRAM
locations independent four-bit targets, add the following target-memory bank:

| Qty | Part | Basket status | Role |
| ---: | --- | --- | --- |
| 4 | `SN74LS189AN` | Five on order; reserve 4, one spare | Four 16 x 4-bit RAMs provide 64 four-bit target words. |
| 1 | `SN74LS139N` | Stock has 24: reserve 1 | Decodes address bits `A4` and `A5` to select one `74LS189` target-RAM chip while programming. |
| 2 | `SN74LS153N` | Basket has 10; reserve 2 | Select the four-bit output of one target-RAM chip using address bits `A4` and `A5`. |
| 1 | `SN74LS04N` | Inventory has 60: reserve 1 | Restores the true target polarity after the `74LS189`'s inverted outputs. |

The `74LS189` output is inverted and not tri-state, so its four RAM outputs
must not be tied together. The two `74LS153` packages select one RAM's four
outputs before the `74LS04` restores the normal polarity for the comparator.
This expansion also needs 16 pull-up resistors, one on every `74LS189` output,
and a defined way to load target RAM: a temporary manual programming mode, a
second target source, or a fixed target-generation rule. Do not add this bank
until that behaviour has been chosen.

## New Passive and Mechanical Parts

| Qty | Part | Suggested value or specification | Purpose |
| ---: | --- | --- | --- |
| 4 | `100nF` ceramic capacitor | X7R or C0G, one per new required IC | Local decoupling for the `74LS393`, two `74LS157`s, and `74LS14`. |
| 1 | Bulk capacitor | `10uF` to `47uF`, at least 10 V | Supports the expanded 5 V TTL rail. |
| 1 | Pull-up resistor | `4.7k` to `10k`; inventory has both values | Holds the automatic-counter reset inactive. |
| 1 | Reset capacitor | `100nF` to `1uF`, selected with the pull-up | Optional power-on reset for the address counter. |
| 1 | Advance pushbutton | Momentary, normally open | Optional manual `NEXT ADDRESS` control for test and demonstration. |
| 1 | Debounce resistor | `10k`; inventory has 100 | Used with the `74LS14` for the optional advance pushbutton. |
| 1 | Debounce capacitor | `100nF` | Used with the `74LS14` for the optional advance pushbutton. |
| as needed | DIP sockets | 14-pin for `74LS14`; 16-pin for `74LS393` and `74LS157`; inventory has 30 and 36 respectively | Recommended for the added ICs. |
| as needed | Wire-wrap wire / hook-up wire | 30 AWG wire-wrap or insulated solid wire; inventory includes 28 AWG Kynar | Address-path and control wiring. |

Add one further `100nF` capacitor if the optional `74LS123` is fitted. The
Phase 2B target-memory bank requires eight more capacitors: one for each of
its eight added ICs.

## Address-Path Summary

```text
address switches A0-A5 --+--> two 74LS157s --+--> MM2114A address inputs
                          |                    |
74LS393 counter A0-A5 ----+                    +--> selected by AUTO mode
```

`AUTO=0` must leave the original manual address switches selected. `AUTO=1`
selects the counter. Reset the counter to address `0` whenever an automatic
scan begins, unless a later version deliberately supports resume-from-current
address behaviour.

## Basket Correlation and Purchase Summary

The basket contains ten each of `SN74LS157N`, `SN74LS08N`, `SN74LS393N`, and
`SN74LS153N`; retain the Phase 2 quantities in that order. These parts are not
recorded in `inventory/list.csv`. The inventory already provides
`10 x SN74LS14N`, `10 x SN74LS123N`, `60 x SN74LS04N`, ample 14- and 16-pin
sockets, wire, and both `4.7k` and `10k` resistors. Stock also includes
`24 x SN74LS139N`; five `SN74LS189AN` parts are on order, of which four are
needed for the target map. Neither list includes the capacitors required by
this phase.

Buy for base Phase 2:

| Qty | Part |
| ---: | --- |
| 4 | `100nF` ceramic capacitors |
| 1 | `10uF` to `47uF` bulk capacitor, at least 10 V |
| 1 | Reset capacitor, `100nF` to `1uF` |
| 1 | Debounce capacitor, `100nF`, only with the optional `NEXT ADDRESS` button |

Reserve from the basket: `1 x SN74LS393N` and `2 x SN74LS157N`. Reserve from
inventory: `1 x SN74LS14N`, and optionally `1 x SN74LS123N`. If the optional
target RAM is built, reserve `2 x SN74LS153N` from the basket and `1 x
SN74LS04N` plus 16 pull-up resistors from inventory. Reserve `1 x SN74LS139N`
from stock and four of the five ordered `SN74LS189AN` parts.
