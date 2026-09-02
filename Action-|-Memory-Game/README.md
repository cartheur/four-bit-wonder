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