# Machine Autonomous Version

## Identity

This is the independent progressive build of the Four-Bit Wonder concept. It
uses a new Vector `8016-1` Circbord and combines the base machine, Phase 1
autonomous hill climber, and Phase 2 autonomous address scan in one wire-wrap
system. It is not an incremental modification of the photographed original
board.

## Included Scope

| Stage | Capability |
| --- | --- |
| Base | Manual four-bit SRAM machine with visible panel controls and timing. |
| Phase 1 | Captures a target, changes one SRAM word toward it, and halts at equality. |
| Phase 2 | Scans the exposed addresses automatically after each address reaches its target. |

Phase 2B per-address target memory remains optional and is not part of the
core Machine Autonomous Version.

## Build References

- [Socket plan and board layout](README.md#machine-autonomous-version)
- [Phase 1 BOM](phase-one-bom.md)
- [Phase 2 BOM](phase-two-bom.md)
- [Legacy incremental addition](four-bit-wonder-autonomous-addition.md)

## Boundary

The photographed [existing Four-Bit Wonder](images/four-bit-wonder.jpg) remains
intact as a reference and incremental-build platform for the smaller
[Machine Memory and Game Version](machine-memory-and-game-version.md).
Do not use its layout, existing wiring, or spare physical area as a constraint
on this autonomous version.
