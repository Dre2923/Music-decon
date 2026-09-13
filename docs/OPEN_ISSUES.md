# Open Issues Register

Per `MANIFESTO.md` Section 14, every unresolved item in the manifesto must be tracked here as an **OPEN ISSUE** rather than silently resolved by assumption. Nothing in this file may be converted to a completed design decision without explicit sign-off from the product owner, logged with a date and decision below.

Do not delete a row when work starts on it — move it to "Resolved" with the decision and date once sign-off is recorded.

## Blocking — must be resolved before related code ships

| # | Issue | Manifesto ref | Why it's open | Blocks |
|---|---|---|---|---|
| 1 | Exact retention period (in days) for child-profile personal data | 8a | Manifesto explicitly forbids inventing a number without sign-off | Any code that expires/purges under-13 profile data |
| 2 | Verifiable-parental-consent method for a future Deepgram child-data disclosure | 8a | Six preconditions listed, none yet satisfied | Enabling Deepgram for any under-13 profile (must stay disabled otherwise) |
| 3 | Final exact `ConsentState` enum values/transitions | 8a | "May change during implementation" but must be decided deliberately, not improvised mid-build | Data-access-layer consent enforcement |
| 4 | Spleeter pretrained-weight commercial redistribution/use rights | 6 | Licensing questions were still open upstream as of 2026; release gate | Shipping any Spleeter model weights |
| 5 | Open-Unmix non-`umxl` model artifact licenses | 6 | Requires individual artifact-level verification; `umxl` itself is confirmed CC BY-NC-SA 4.0 and is already excluded | Packaging any Open-Unmix pretrained model besides an already-cleared one |
| 6 | PyDMX vs. DmxPy final selection | 5 | Manifesto says license/hardware support must be reconfirmed "at integration time" | Building the DMX output abstraction against a concrete library |
| 7 | Windows/Microsoft Store certification lead time for this app's package type | 6a | Not quantified in the manifesto; affects release scheduling | Windows release-date planning |

## Deferred by design (not blocking, but not in scope without a deliberate decision to un-defer)

| # | Item | Manifesto ref | Note |
|---|---|---|---|
| D1 | Teacher/coach dashboard | 8 | Explicitly deferred; must not be built by quietly reusing family-profile permissions |

## Standing mechanism (not a single item — ongoing)

| # | Item | Manifesto ref | Cadence |
|---|---|---|---|
| M1 | Re-verify Apple/Google/Microsoft/FTC/OWASP/NIST/WCAG sources and all dependency licenses | 10.2, 13, 16 | Before every major milestone, beta, and production submission — see `DEPENDENCY_REGISTER.md` and `COMPLIANCE_LOG.md` |

## Resolved

_(none yet)_

---

If the earlier 32-section voice-session draft mentioned in the manifesto's preamble is ever recovered, diff it against `MANIFESTO.md` and add any genuinely missing requirement as a new row here first — do not merge it directly into the manifesto without deliberate reconciliation.
