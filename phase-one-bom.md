# Bill of Materials

This is the Phase 1 bill for the [Machine Autonomous Version](machine-autonomous-version.md),
a progressive build on a new board. Together with the base machine and Phase 2,
it does not modify or repurpose the photographed Four-Bit Wonder. The
incremental design in `four-bit-wonder-autonomous-addition.md` is retained as a
separate legacy track.

## Logic ICs

| Qty needed | Part | Status | Basket quantity | Role |
| ---: | --- | --- | ---: | --- |
| 1 | `SN74LS85N` | In stock | 0 | Four-bit comparator |
| 1 | `SN74LS173AN` | In basket | 10 | Latched four-bit target register |
| 1 | `SN74LS193N` | In basket | 10 | Candidate up/down register |
| 1 | `SN74LS161AN` | In basket | 10 | Autonomous phase counter |
| 1 | `SN74LS138N` | In stock | 0 | Phase decoder |
| 1 | `SN74LS74AN` | In basket | 10 | `HALT` flip-flop |
| 1 | `SN74LS08N` | In basket | 10 | Clock and enable gates |
| 1 | `SN74LS00N` | In stock | 0 | Active-low control gates |
| 1 | `SN74LS125AN` | In basket | 10 | Dedicated tri-state driver from the candidate register to the SRAM write bus |
| 1 | `SN74LS157N` | In basket | 10 | Selects manual or automatic SRAM control sources |
| 1 | `NE555P` | In basket | 10 | Dedicated autonomous clock |

The basket also contains `10 x SN74LS175N`. They are not required for this
version: the `74LS173` is the selected target register because its tri-state
outputs leave room for later bus expansion.

## Panel Hardware

| Qty needed | Part | Status | Basket quantity | Role |
| ---: | --- | --- | ---: | --- |
| 1 | E-Switch `100SP1T1B1M3QEH` | In basket | 2 | Replaces the CS switch with `MANUAL / DISABLED / AUTO` selection |

This switch is SPDT `ON-NONE-ON`. Its existing-panel hole must be enlarged from
`5.2 mm` to `6.35 mm`; orient its anti-rotation key against the holder edge.
One purchased switch remains as a spare.

No new switch or pushbutton is needed. The existing write button is mode-gated:
it writes manually in `MANUAL` and performs `LOAD TARGET / START` in `AUTO`.

For the replacement board, use the same normally-closed, open-on-press
connection as `NEXT ADDRESS`: the button input is grounded while released, and
a `10k` pull-up makes it high when pressed. Debounce it with `100nF` to ground
and use the `74LS14` to produce an active-low press event. The existing write
button is the same stocked part and has this confirmed contact polarity.

## Still Needed Outside the Basket

| Qty | Part | Suggested value or specification | Purpose |
| ---: | --- | --- | --- |
| 1 | Vector `8016-1` Circbord | `155 x 155 mm` | Selected replacement-board substrate for the base machine and Phase 1/2 wiring. |
| 1 | NE555 timing resistor `RA` | `10k` | Autonomous-clock timing network |
| 1 | NE555 timing resistor `RB` | `4.7k` in series with an in-stock `100k` linear trimmer | Adjustable autonomous-clock timing network |
| 1 | Alternative fixed `RB` resistor | `68k`, in basket | Produces approximately one phase per second with a `10uF` timing capacitor |
| 1 | Timing capacitor | `10uF`, verify from passive stock | NE555 astable timing network |
| 1 | `100nF` capacitor per added IC | Ceramic, X7R or C0G | Local decoupling; 11 for the ten TTL ICs plus NE555 |
| 1 | Bulk capacitor | `10uF` or greater, at least 10 V | Added-module 5 V rail support |
| 3 | NPN transistor | `2N3904`, `BC547`, or similar | Low-side drivers for the existing bezel LEDs, if they are not already driven |
| 3 | Base resistor | `10k` | NPN base current limit |
| 3 | LED resistor | `330 ohm`, stock has 90 | LED current limit for 5 V NPN low-side drivers |
| 3 | Base-emitter pull-down resistor | `100k`, optional but recommended | Keeps LED drivers off during reset/power-up |
| 2 | Mode-input pull-down resistor | `10k`, in basket | Defines `MANUAL=0` and `AUTO=0` in the selector's centre position |
| 1 | Write-button debounce network | `10k` pull-up plus `100nF` to ground | For a normally-closed, open-on-press button; produces one clean auto-mode target/start event. |
| as needed | DIP sockets | Appropriate 14-, 16-, and 20-pin sockets | Recommended for all new ICs |
| as needed | Wire-wrap wire / hook-up wire | 30 AWG wire-wrap or insulated solid wire | Expansion-module wiring |

## Existing Board Items Used Without Repurposing

| Existing item | Use |
| --- | --- |
| `MM2114A` SRAM | Receives the selected address's revised value through the new controlled interface |
| Four top data switches | Target source, observed at high impedance and captured by the added `74LS173` |
| Six address switches | Continue to select the state being trained |
| Read/Write switch | Continues to control manual operation |
| Existing write button | Mode-gated manual write or automatic target/start action |
| Lower green bezel LED | `INCREASE`: candidate is below target |
| Lower yellow bezel LED | `DECREASE`: candidate is above target |
| Upper red bezel LED | `MATCH / HALT`: candidate equals target |

The existing 555, `74LS93` counters, `uPB8226C`, `SN74LS367A`, and
`DM74LS04N` remain untouched by this addition.

## Basket Check

The updated `basket/basket.xls` supplies every required purchased TTL part for
the finalized design: `74LS74`, `74LS157`, `74LS173`, `74LS08`, `74LS161`,
`74LS193`, `74LS125`, and `NE555P`, plus two replacement mode switches. The
required `74LS85`, `74LS138`, and `74LS00` are covered by existing stock.

The basket does not cover passive components, sockets, wire, or LED-driver
parts listed above. Verify existing bezel LED resistor arrangements before
buying or fitting duplicate current-limit resistors.
