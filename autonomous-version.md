# Autonomous Version: Four-Bit SRAM Hill Climber

## Goal

This extension turns one manually selected SRAM location into a small
closed-loop machine. It captures a four-bit target from the existing top data
switches, reads the word stored at the selected address, changes it by one
toward that target, writes it back, and stops when the values match.

For a target in the range `0`-`15`, the loop reaches equality in at most 15
write cycles. The learned value remains in the `MM2114A` while power is
applied.

This is deliberately a **single-address** version. The original six address
switches remain in control, so the operator can choose which memory state the
machine is allowed to revise.

## Added Parts

| Quantity | Part | Role |
| --- | --- | --- |
| 1 | `74LS85` | Compares current candidate with target |
| 1 | `74LS175` | Captures the target word from the existing four data switches |
| 1 | `74LS193` | Loads, increments, or decrements the current SRAM word |
| 1 | `74LS161` | Four-state sequence counter |
| 1 | `74LS138` | Decodes the controller phases |
| 1 | `74LS08` | Gates clock pulses and enables |
| 1 | `74LS00` | Inverts/gates active-low SRAM and stop signals as required |
| 0 or 1 | `74LS125` or `74LS244` | Drives the counter word onto the SRAM bus if the existing `uPD8226C` cannot do so |
| 1 | Momentary `TARGET LOAD` button | Captures the top-switch target into the `74LS175` |
| 1 | Momentary `RUN/RESET` button or toggle | Starts/restarts the controller |
| 3 | NPN LED drivers and resistors | Drives `LOW`, `MATCH`, and `HIGH` LEDs if no existing driver stage is available |
| 1 per IC | `100 nF` ceramic capacitor | Local supply decoupling |

The board already contains a 555 and two `74LS93` counters. Use a sufficiently
slow divided output from that timing section as the controller clock. A visible
rate, around one operation per second, is preferable while debugging.

## Data Paths

```text
top data switches -----> 74LS175 target register -----> 74LS85 B inputs

2114 read bus ---------> 74LS193 parallel inputs
74LS193 Q outputs -----> 74LS85 A inputs
74LS193 Q outputs -----> tri-state bus driver --------> 2114 data bus (write only)
```

The target register is the essential new separation. Pressing `TARGET LOAD`
copies the current four data switches into the `74LS175`; after that, changing
the top switches no longer changes the target used by the machine.

Use the same bit ordering everywhere: bit 0 to bit 0 through bit 3 to bit 3.
On the `74LS85`, tie its cascade inputs to standalone values:

```text
A<B cascade input = GND
A=B cascade input = +5V
A>B cascade input = GND
```

## Controller Phases

Use the `74LS161` and `74LS138` as a repeating four-phase controller. The
exact gates depend on the existing `/CS`, `/WE`, and bus-driver wiring, but the
electrical states must follow this order.

| Phase | SRAM state | Other action |
| --- | --- | --- |
| `0: READ/LOAD` | `/CS` low, `/WE` high | Enable SRAM output; assert the `74LS193` parallel-load input to copy the current word |
| `1: COMPARE` | Read remains active or outputs are held stable | `74LS85` compares counter word with latched target |
| `2: STEP` | SRAM write disabled | If `A<B`, clock the `74LS193` up once; if `A>B`, clock it down once; if equal, set `HALT` |
| `3: WRITE` | `/CS` low, `/WE` low | Enable counter-to-SRAM bus driver and write the revised counter value |

The `74LS193` has separate up and down clock inputs. Gate the phase-2 pulse so
only one is pulsed:

```text
UP clock pulse   = STEP_PULSE AND (A < B)
DOWN clock pulse = STEP_PULSE AND (A > B)
```

Keep the non-selected clock input high. Never drive both count clocks with a
pulse at the same time.

`A=B` sets a flip-flop or latch named `HALT`. `HALT` disables the sequence
clock, prevents phase 3 from asserting `/WE`, and lights the top `MATCH` LED.
The two other comparator outputs drive the lower `LOW` and `HIGH` LEDs.

## Bus Safety

This design needs explicit ownership of the SRAM data bus.

- In phases 0 and 1, the 2114 is the only bus driver. The counter-to-bus driver
  must be disabled.
- In phase 3, disable the SRAM output by asserting write, then enable only the
  counter-to-bus driver.
- The top data switches must remain separated from the SRAM bus by their
  existing series resistors or a properly controlled buffer.
- Do not connect the `74LS193` outputs directly to the bidirectional SRAM bus.
  Use the existing `uPD8226C` only if its direction and enable controls give a
  genuine high-impedance state; otherwise add a `74LS125` or `74LS244`.

Before connecting the automatic controller, arrange a manual/automatic control
selection point for `/CS`, `/WE`, and bus enable. Do not let the manual switch
and controller drive the same TTL control node against each other.

## Start Sequence

1. Leave the autonomous controller stopped.
2. Choose the address to be trained using the existing six address switches.
3. Set the desired four-bit target using the top data switches.
4. Press `TARGET LOAD` to capture that target in the `74LS175`.
5. Press `RUN/RESET` to clear `HALT` and reset the four-phase sequencer to
   `READ/LOAD`.
6. Watch the lower LEDs alternate as necessary. The top LED lights when the
   selected SRAM word equals the captured target.

## Optional Next Step: Address Scanning

To let the machine train all 64 exposed locations, add two `74LS157` 2:1
multiplexers. They select either the existing six manual address-switch lines
or six automatic counter bits. Advance the address counter after each matched
state. Keep this as a later addition: it requires a clear definition of when a
location is considered learned and whether its target comes from a fixed rule,
a second memory region, or a new external source.
