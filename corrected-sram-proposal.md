# Corrected 2114 SRAM Front Panel Proposal

This is a buildable version of the four-bit SRAM front-panel idea. It uses a
2114 SRAM as a manually programmed 256 x 4-bit memory and removes the clock
from the memory-access path.

## Design Goal

Set an eight-bit address and a four-bit value with switches. Press `WRITE` to
store the value. At all other times, LEDs show the value already stored at the
selected address.

The 2114 is asynchronous SRAM: it does not need a clock. A clean, debounced
active-low write signal is all that is required.

## Wiring Overview

```text
Address switches (8) ----------------> 2114 A0-A7
A8, A9 ------------------------------> GND
/CS ----------------------------------> GND

Data switches (4)
  each: switch node -- 10k series ---> 2114 I/O0-I/O3
        switch node -- 10k ----------> GND
        SPST switch connects node ----> +5V

Write pushbutton
  button + RC debounce + two 74HCT14 gates --> 2114 /WE

2114 I/O0-I/O3 ----------------------> 74HCT244 inputs
74HCT244 outputs -- 2.2k resistors --> four data LEDs
```

## Address Inputs

Use eight SPST switches for `A0` through `A7`. Each address input needs a
10k pulldown resistor to ground, and its switch connects the input to `+5V`.
This makes an open switch a logic `0` and a closed switch a logic `1`.

Tie `A8` and `A9` directly to ground. The 2114 still contains 1,024 nibbles,
but this front panel deliberately exposes only addresses `0x00` through
`0xFF`.

Tie the active-low chip-select input, `/CS`, to ground so the RAM is selected
continuously.

## Data Inputs and Bus Safety

The 2114 I/O pins are bidirectional. During a read, the SRAM drives them; in a
write, the switches must drive them instead. Do not connect the switches
directly to the SRAM I/O pins because conflicting values would create bus
contention.

For each data bit:

- Use an SPST switch to connect a switch node to `+5V`.
- Connect that switch node to ground through a 10k pulldown resistor.
- Connect the switch node to the corresponding SRAM I/O pin through a second
  10k series resistor.

During a write, the resistor supplies the selected logic level to the SRAM.
During a read, it limits any current caused by a switch value that differs
from the RAM's output. The RAM can therefore safely drive the bus.

## Write Button and Debounce

Use a `74HCT14` Schmitt-trigger inverter to debounce the write button:

```text
+5V --- 100k ---+--- input of HCT14 gate 1
                |
              100nF
                |
               GND

Pushbutton: input node to GND

HCT14 gate 1 output --> HCT14 gate 2 input
HCT14 gate 2 output --> 2114 /WE
```

The first inverter goes high while the debounced button is pressed; the second
inverter makes the final `/WE` output low while pressed. Holding the button
low simply rewrites the same selected value, which is harmless.

Tie unused `74HCT14` inputs to a defined logic level, either ground or `+5V`.

## Read Display

Connect the four 2114 I/O pins to inputs on a `74HCT244`. Tie the buffer's
active-low output-enable pins to ground. Connect each buffer output through a
2.2k resistor to an LED, with the LED cathode connected to ground.

Use `74HCT244` rather than `74HC244`. HCT-family inputs accept TTL-level
logic highs reliably, which is useful with older 2114 variants whose output
high voltage may not meet a 74HC input threshold.

## Operating Table

| State | `/CS` | `/WE` | Result |
| --- | ---: | ---: | --- |
| Normal/read | 0 | 1 | LEDs show the nibble stored at the selected address. |
| `WRITE` pressed | 0 | 0 | The switch-selected nibble is stored at the selected address. |
| `WRITE` released | 0 | 1 | The circuit returns to read/display mode. |

## Parts List

- 1 x 2114-compatible 1K x 4 SRAM
- 1 x 74HCT14 Schmitt-trigger hex inverter
- 1 x 74HCT244 octal buffer
- 8 x SPST address switches
- 4 x SPST data switches
- 1 x momentary pushbutton for `WRITE`
- 12 x 10k resistors for address and data switch pulldowns
- 4 x 10k resistors in series with the data switch outputs
- 4 x LEDs and 4 x 2.2k LED resistors
- 1 x 100k resistor and 1 x 100nF capacitor for button debounce
- 1 x 100nF ceramic decoupling capacitor per IC
- 1 x 10uF bulk capacitor on the regulated 5V supply

## What To Leave Out

The 555 timer, 1 kHz clock, 74LS74, and 74LS00 are not needed for this manual
memory front panel. A clock can be added later for a counter, sequencer, or a
separate status LED, but it should not be presented as a requirement for SRAM
reads or writes.
