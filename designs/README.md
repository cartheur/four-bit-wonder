## The design of breadboard

* Top: Two 4-bit switchers (address), one led-indicator-switches (data-input)
* Bottom: One led-indicator-2pb-switch (data-output|LOAD|RESET|R/P), one led-indicator-three (CORRECT|HIGH|LOW), one led-indicator-four (counter guess tracking)

Print these black holder modules for the Machine Autonomous Version panel:

| Qty | STL / FreeCAD module | Role |
| ---: | --- | --- |
| 2 | `4-bit-switcher` | Two four-switch address groups |
| 1 | `switches-indicator-four` | Four-switch data-input group with indicators |
| 1 | `led-indicator-2pb-switch` | Data-output indicators with two pushbuttons and switch |
| 1 | `led-indicator-four` | Four-indicator group for counter/guess tracking |
| 1 | `led-indicator-three` | Three comparison indicators: `LOW`, `MATCH`, `HIGH` |

**Total: 6 printed modules.**

### Nibble-RAM feature

[RAM7400](https://github.com/cartheur-dot/RAM7400)

### Communication

From the state of power-off to power-on, 2114 should be empty, but it is not.

![paradigm](/images/comm-paradigms.jpg)