## A Four-Bit Wonder

Repo for technical details on the four-bit wonder machine intelligence system.

_Background_

Invented between the years 2021 and 2024, a protobord called _Boagaphish_ to work-through the [details](http://www.paradoxtechnologies.org/engineering/modelc_new/modelc.html) of what machine intelligence _really_ looks like without all the fanfare and (over) hype - although there is good reason to be enthusiastic.

![boagaphish](/images/four-bit-wonder.jpg)

## Current Addition

The Four-Bit Wonder is a handmade, legible two-part experiment: a 555 plus two
`74LS93` timing-divider section, and a manually addressable `MM2114A` 1K x
4-bit SRAM environment. Six front-panel switches select an exposed address;
four top switches set a four-bit value. The board makes timing, bus transfer,
stored state, and power-on indeterminacy visible rather than hiding them in
software.

The planned addition is a small autonomous hill climber. In `AUTO` mode it
captures a four-bit target from the existing data switches, reads the selected
SRAM word, increments or decrements that word toward the target, writes the
revised value back, and halts on equality. The original timing and bus sections
remain untouched.

The existing CS switch is replaced by an E-Switch `100SP1T1B1M3QEH` SPDT
`ON-NONE-ON` selector with `MANUAL / DISABLED / AUTO` positions. The existing
write button remains a manual write control in `MANUAL`; in `AUTO` it becomes
`LOAD TARGET / START`. No new panel holes are required. The lower green LED
means `INCREASE`, the lower yellow LED means `DECREASE`, and the upper red LED
means `MATCH / HALT`.

### Wire-Wrap Sockets To Add

The full autonomous addition requires **11 new wire-wrap sockets**:

- `6 x 16-pin`: `74LS85`, `74LS173`, `74LS193`, `74LS161`, `74LS138`, and `74LS157`
- `4 x 14-pin`: `74LS74`, `74LS08`, `74LS00`, and `74LS125`
- `1 x 8-pin`: separate NE555 autonomous clock

See [the autonomous-addition write-up](four-bit-wonder-autonomous-addition.md)
for the operating design and [the bill of materials](bill-of-materials.md) for
part availability.

## Layout Advice

The broad empty centre of the perfboard is sufficient for the 11 new wire-wrap
sockets if the addition is kept in two compact clusters: control above and data
path beside the SRAM.

```text
TOP EDGE / EXISTING SWITCHES
+------------------------------------------------------------------+
| [existing 555 + 74LS93 timing section]       [CS -> M / D / A]   |
| [existing empty sockets]                                         |
|                                                                  |
|                     AUTONOMOUS CONTROL CLUSTER                   |
|                     +----------------------------------+         |
|                     | [NE555] [161] [138]              |         |
|                     | [ 74 ]  [ 08] [ 00]              |         |
|                     +----------------------------------+         |
|                                                                  |
|       existing LS367 / LS04       DATA / MEMORY CLUSTER          |
|       +--------------------+      +-------------------------+    |
|       |                    |      | [173] [85]  [193]       |    |
|       +--------------------+      | [157] [125] [space]     |    |
|                                   +-------------------------+    |
|                                           |              |       |
|                                     target/comparator   short    |
|                                     wiring              SRAM bus |
|                                                   [MM2114 SRAM]  |
|                                                                  |
|  existing resistor networks                         uPD8226C     |
+------------------------------------------------------------------+
BOTTOM LED / SWITCH PANEL
```

Orient every new DIP notch toward the top edge. Keep the `74LS125` nearest the
`MM2114`, and keep `74LS173`, `74LS85`, and `74LS193` adjacent. Leave at least
two clear perfboard rows between sockets and existing components for wire-wrap
clearance, with a free edge column for `+5V`, ground, and decoupling wiring.
