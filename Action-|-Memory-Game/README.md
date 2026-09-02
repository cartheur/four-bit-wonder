**Machine Memory and Game Version: Next Steps**

1. Install one 16-pin wire-wrap socket for the `74LS85` on the existing Four-Bit Wonder. Add a `100nF` capacitor directly across its supply pins.

2. Trace and verify the existing signals before wrapping:
   - `S0-S3`: top data-switch side of the existing series resistors
   - `M0-M3`: SRAM read-data side of those resistors
   - `/CS`, `/WE`, `+5V`, and ground

3. Wire the comparator:
   - `A0-A3 <- M0-M3`
   - `B0-B3 <- S0-S3`
   - Cascade inputs: `A<B = GND`, `A=B = +5V`, `A>B = GND`

4. Add three indicator paths:
   - Green: `A<B`, stored word lower, `LOW / INCREASE`
   - Red: `A=B`, stored word equal, `MATCH`
   - Yellow: `A>B`, stored word higher, `HIGH / DECREASE`

5. Use transistor LED drivers rather than driving LEDs directly from the `74LS85`. First verify whether the existing panel LEDs already have resistors. Avoid assuming the planned `330 ohm` resistors work with a simple `10k` transistor base resistor; that combination can demand more LED/driver current than the LS output safely provides. Start at low current, such as the documented `3.3k` LED resistors, then test brightness and logic levels.

6. Test in read-only mode only: `/CS` asserted and `/WE` inactive. Check all 16 target values against known SRAM contents, then verify exactly one LED indicates lower, match, or higher.

7. Leave the existing write path, timing, and address controls unchanged. Do not add latches, counters, automatic write control, or address scanning in this version.

This gives a small, reversible game-like memory exploration on the original board and validates the comparator/indicator behavior that the separate autonomous build later expands upon.

**Machine Memory and Game Version Parts**

| Qty | Part | Notes |
| ---: | --- | --- |
| 1 | `SN74LS85N` | Four-bit comparator; listed as in stock. |
| 1 | 16-pin DIP wire-wrap socket | For the `74LS85`. |
| 1 | `100nF` ceramic capacitor | Directly across comparator power pins. |
| 3 | NPN transistor | `2N3904`, `BC547`, or equivalent low-side LED drivers. |
| 3 | `10k` resistor | Transistor base resistors. |
| 3 | `3.3k` resistor | Initial LED current-limit values. Do not start with `330 ohm` here. |
| 3 | `100k` resistor | Recommended base-emitter pull-downs. |
| 1 each | Red, yellow, green LED | Only if suitable unused panel LEDs are not already present. |
| 1 | 24-pin DIP wire-wrap passive strip | Recommended: the existing two strips have only four spare paired positions, while this stage needs at least six resistor positions. |
| As needed | AWG28 wire-wrap wire | Blue for the eight comparator data inputs, green for LED-drive nets, red/black only for power and ground. |

Also have a multimeter or logic probe available to verify the SRAM read bus before connecting the comparator.

No new memory IC, clock, counter, switch, or new board is needed for this version.