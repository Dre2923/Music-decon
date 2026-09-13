# Content Protection / Source Separation

Source-separation and copyright data-minimization layer. See manifesto Section 6.

**Status:** not yet implemented. All three separation-library candidates (Spleeter, Open-Unmix, Demucs) have unresolved model-weight licensing items — see `docs/OPEN_ISSUES.md` #4 and #5 and `docs/DEPENDENCY_REGISTER.md`. No pretrained weights may be vendored into this module until their row in the dependency register is unblocked.

Key rules from the manifesto this module must honor:
- Source separation is not a copyright exemption and must never be marketed as eliminating copyright liability.
- Analyze in memory where practical; retain only diagnostic features/results.
- Delete temporary mixed audio and separated stems once no longer required; no default permanent archiving of copyrighted background stems.
- `umxl` (Open-Unmix) pretrained weights are CC BY-NC-SA 4.0 and must never ship in the commercial product.
