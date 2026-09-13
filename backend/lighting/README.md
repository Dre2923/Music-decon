# Stage Lighting / DMX

DMX512 output abstraction and Open Fixture Library-based fixture loading, for use with Enttec/DMXKing USB-DMX hardware. See manifesto Section 5.

**Status:** not yet implemented. The underlying library choice (DmxPy vs. PyDMX) is an open item — see `docs/OPEN_ISSUES.md` #6 — pending reconfirmation of license and hardware support at integration time.

Key rules from the manifesto this module must honor:
- Lighting commands pass through an abstraction layer; no application logic embeds a specific adapter implementation directly.
- The UI must never imply that a phone or Pi can output DMX512 without compatible external hardware.
