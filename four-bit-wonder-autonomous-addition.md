# The Four-Bit Wonder Autonomous Addition

## Purpose

This addition gives the Four-Bit Wonder a small, visible form of goal-seeking
behaviour. It does not turn the board into a general-purpose computer and does
not replace its existing timing divider or manual SRAM experiment. Instead, it
adds one constrained loop:

1. capture a four-bit target;
2. read the four-bit value at one selected SRAM address;
3. determine whether that value is too low, correct, or too high;
4. change the value by one in the required direction;
5. write it back; and
6. stop when the stored value equals the target.

The result is a physical, inspectable hill climber. Its target, current state,
direction of change, memory, and stopping condition are all visible on the
panel.

## What Remains Untouched

The original board remains itself.

- The upper-left 555 and two `74LS93` timing-divider section is not reused.
- The existing `uPD8226C`, `SN74LS367A`, `DM74LS04N`, and SRAM support wiring
  are not repurposed.
- The six address switches remain the operator's address selector.
- The four top data switches remain normal manual data-entry controls.
- The existing Read/Write switch remains a manual-mode control.
- The original write pushbutton remains a manual write control in manual mode.

The addition reads the data-switch state at high impedance, and provides a
separate slow clock, comparator, registers, sequencer, and write-bus driver.

## Panel Changes

No new panel holes are required.

### Chip-Select Switch Becomes Mode Selector

Replace the existing chip-select toggle with E-Switch
`100SP1T1B1M3QEH`, an SPDT `ON-NONE-ON` switch. The three lever positions are:

| Lever position | Mode | SRAM ownership |
| --- | --- | --- |
| Position 1 | `MANUAL` | Original controls retain ownership |
| Centre | `DISABLED` | SRAM deselected and all added bus drivers disabled |
| Position 3 | `AUTO` | Added controller owns `/CS`, `/WE`, and the write-bus enable |

The switch is not connected directly to the 2114 `/CS` pin. Its common contact
connects to `+5V`; each throw feeds a separate mode input with a pull-down
resistor. The centre position therefore produces `MANUAL=0` and `AUTO=0`.
Logic in the addition selects the proper control source and guarantees that
only one source can control the SRAM.

The exact replacement needs a `6.35 mm` mounting hole. The original hole is
`5.2 mm`; enlarge it to `6.35 mm`. On this panel, orient the anti-rotation key
against the existing holder edge, as the adjacent switches do. Do not drill the
auxiliary locking-ring hole.

### Existing Write Button Has Two Meanings

| Mode | Pushbutton action |
| --- | --- |
| `MANUAL` | Original manual write pulse |
| `AUTO` | `LOAD TARGET / START`: capture target, clear `HALT`, reset the sequencer, and begin the loop |
| `DISABLED` | No SRAM action |

The button signal must be mode-gated. In automatic mode it must not reach the
original manual write-enable path.

### Indicators

Use the two spare lower bezel LEDs and the free upper LED.

| LED | Comparator condition | Panel meaning |
| --- | --- | --- |
| Lower green | `candidate < target` | `INCREASE` |
| Lower yellow | `candidate > target` | `DECREASE` |
| Upper red | `candidate = target` | `MATCH / HALT` |

Only one indicator is lit at a time. The red LED is a stop-state indicator,
not a fault indication.

## Added Logic

```text
top data switches --> 74LS173 target latch --------> 74LS85 B inputs

2114 read bus -----> 74LS193 parallel-load inputs
74LS193 Q outputs --> 74LS85 A inputs
74LS193 Q outputs --> added tri-state driver ------> 2114 write bus

74LS85 outputs ----> direction LEDs and controller
```

The `74LS173` captures the target at the start of an automatic run. Its inputs
tap the **switch side** of the existing data-input series resistors. This is a
high-impedance observation point and does not load or change the existing
manual path.

The `74LS193` is the working candidate register. It parallel-loads the word
read from the SRAM, counts up once when the candidate is too low, counts down
once when it is too high, then presents that revised word to the SRAM only
during the automatic write phase.

The `74LS85` is a standalone comparator. Tie its cascade inputs as follows:

```text
A<B cascade input = GND
A=B cascade input = +5V
A>B cascade input = GND
```

## Autonomous Timing and Control

The addition has its own slow clock. A separate NE555 astable, adjusted to
roughly one controller phase per second, keeps the original timing-divider
section entirely independent. The clock feeds a `74LS161` phase counter and a
`74LS138` phase decoder.

| Phase | SRAM condition | Added logic action |
| --- | --- | --- |
| `READ/LOAD` | `/CS` asserted; `/WE` inactive | SRAM drives its data bus; `74LS193` parallel-loads the current word |
| `COMPARE` | Read state retained | `74LS85` evaluates candidate against target |
| `STEP` | Writing disabled | Pulse `74LS193` up for `candidate < target`, down for `candidate > target`; set `HALT` on equality |
| `WRITE` | `/CS` asserted; `/WE` active | Enable only the new counter-to-SRAM bus driver and store the revised word |

A `74LS74` stores `HALT`. Equality disables the sequence clock before another
write can occur. Selecting `MANUAL`, or pressing the button in `AUTO`, clears
`HALT` and returns the controller to `READ/LOAD`.

`74LS08` and `74LS00` gates generate the gated count pulses and active-low
control signals. The non-selected `74LS193` count-clock input stays high;
never pulse both count inputs together.

## Safe SRAM Interface

The added circuitry must not be wired in parallel with the original SRAM
control lines. Insert a small control interface between the existing logic and
the 2114:

```text
MANUAL mode: original `/CS`, `/WE`, and manual data path --> 2114
AUTO mode:   controller `/CS`, `/WE`, and 74LS193 data path --> 2114
DISABLED:    `/CS` high; every added bus driver high impedance
```

Use the purchased `74LS125` as the added counter-to-SRAM tri-state driver. Its
outputs connect to the SRAM data bus only during the `WRITE` phase of `AUTO`
mode. This avoids relying on, or changing, the existing `uPD8226C` role.

The interface must make bus contention impossible:

- During read and compare, the new `74LS125` is disabled.
- During automatic write, the 2114 output is disabled by its write state before
  the `74LS125` is enabled.
- In manual mode, every automatic driver is disabled.
- In disabled mode, the SRAM is deselected.

## Added Parts

| Qty | Part | Role |
| ---: | --- | --- |
| 1 | `74LS85` | Four-bit comparator |
| 1 | `74LS173` | Captured target register |
| 1 | `74LS193` | Candidate up/down register |
| 1 | `74LS161` | Phase counter |
| 1 | `74LS138` | Phase decoder |
| 1 | `74LS74` | `HALT` flip-flop |
| 1 | `74LS08` | Clock/enable gates |
| 1 | `74LS00` | Active-low control gates |
| 1 | `74LS125` | Added, dedicated SRAM write-bus driver |
| 1 | NE555 | Independent autonomous clock |
| 1 | E-Switch `100SP1T1B1M3QEH` | Three-position `MANUAL / DISABLED / AUTO` selector |
| 3 | NPN transistor plus base resistor | LED low-side drivers, if the bezel LEDs are not already driven |
| 1 per IC | `100nF` ceramic capacitor | Local decoupling |

The stock `74LS85`, `74LS138`, and `74LS00` complete the earlier basket. The
remaining TTL parts for the addition are already in the basket.

## Operating Sequence

1. Select `MANUAL`.
2. Use the six address switches to choose the location to train.
3. Set a number from `0` to `15` on the four top data switches.
4. Move the selector to `AUTO`.
5. Press the existing write button once. It captures the target and starts the
   loop.
6. Observe green while the value rises, yellow while it falls, and red when it
   matches and stops.
7. Return to `MANUAL` to inspect or change the board with its original
   controls.

The stored result is volatile: it persists while the board has power, but is
not a reliable retained value after power is removed.

## Build Order

Build and test this in stages:

1. Fit the replacement mode switch and verify `MANUAL`, `DISABLED`, and `AUTO`
   logic levels with the SRAM disconnected from automatic control.
2. Add the `74LS85` and three LED drivers; confirm the comparison indicators in
   manual read mode.
3. Add the target latch and verify that the target stays fixed after the four
   top switches move.
4. Add the `74LS193` and verify one controlled up/down step without SRAM
   writing.
5. Add the SRAM control interface and test one automatic read-modify-write
   cycle at a slow clock rate.
6. Enable continuous cycling only after the single-cycle behaviour is correct.
