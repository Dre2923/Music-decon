# Master Product Manifesto — Voice-First Music Intelligence Ecosystem

**Status:** MASTER / GOVERNING BUILD REFERENCE — LOCKED FOR CLAUDE CODE BUILD

This document is the authoritative product and engineering manifesto for the Voice-First Music Intelligence Ecosystem. It contains the confirmed product vision, architecture, licensing decisions, compliance requirements, monetization model, privacy architecture, development standards, security requirements, accessibility requirements, and release rules that govern the project.

An earlier 32-section version was drafted during a voice session and was not preserved as a file. If that document is ever recovered, it must be compared against this master to identify anything that may have been omitted. The recovered document does not automatically replace this master. Any genuinely missing requirement must be reconciled into this document deliberately so that the current verified technical, legal, security, and compliance protections are not lost.

This document is a living build authority. Changes to laws, platform rules, third-party terms, licenses, SDK requirements, security standards, or technical dependencies must be incorporated here when discovered.

---

## INSTRUCTIONS FOR CLAUDE CODE — MANDATORY BUILD DISCIPLINE

Before writing a single line of code from this manifesto, and again at every major milestone, the following applies without exception:

1. **Multi-pass verification requirement.** Every section touching security, privacy, child safety, billing, or licensing (Sections 4, 6, 6a, 6b, 7, 8, 8a, 10.3, 10.4, 10.10, 10.11) must be independently re-checked a minimum of **five times** before that portion of the build is considered complete — once during design, once immediately after implementation, once during integration testing, once during a dedicated security/compliance review pass, and once immediately before any release candidate is cut. Each pass must be logged (what was checked, what was found, what was changed) rather than silently repeated.
2. **No silent scope reduction.** If executing this manifesto in full appears to take longer or require more scripts than expected, that is not authorization to simplify, skip, or merge steps. Flag the tradeoff explicitly and wait for explicit approval before deviating.
3. **No assumption-filling on open items.** Anywhere this document says a value is a placeholder, an open issue, or "may change during implementation," Claude Code must stop and ask rather than inventing a plausible-sounding answer, especially for consent states, retention periods, and vendor-facing legal language.
4. **Security and compliance gates are blocking, not advisory.** A feature that fails a licensing, privacy, child-safety, or security check does not ship in a "we'll fix it later" state. It is blocked until it passes.

---

## 0. Non-Negotiable Master Rule

This project is a voice-first music intelligence, education, and diagnostic ecosystem — not a chatbot wrapper, not a generic MVP, not a template app with a music skin.

Any AI or developer working on this project in the future — including future instances of Claude, ChatGPT, Gemini, Claude Code, coding agents, contractors, or software engineers — must not simplify, water down, or "helpfully" reduce this vision to something smaller or more generic in the name of speed or convenience.

Every feature must be built to the full standard described here.

If a shortcut is proposed:
- it must be identified explicitly as a shortcut;
- its disadvantages and risks must be explained;
- the full-standard alternative must also be presented;
- it may not replace the approved design without explicit authorization.

Every major feature must answer one test: **"Why would someone use this instead of just asking ChatGPT, Gemini, or Claude directly?"**

Acceptable answers include capabilities such as: live audio diagnostics; direct microphone analysis; musical measurements derived from actual audio; saved structured progress; longitudinal improvement tracking; offline intelligence; hardware/DMX control; practice verification; personalized learning state; instrument/vocal diagnostics; real-time interaction with the user's working environment.

If a proposed feature cannot demonstrate meaningful value beyond a generic AI conversation, it must be reconsidered.

---

## 1. Core Concept

A voice-first app that listens to a musician working — DJing, singing, producing, playing an instrument, mixing live sound, or operating stage lighting — and provides real diagnostic feedback, explanation, guidance, and structured practice.

The experience should resemble a knowledgeable music mentor standing beside the user, observing what actually happens, rather than a search engine or generic chatbot answering hypothetical questions.

**Target users:** DJs, vocalists, songwriters, producers, beatmakers, recording engineers, live sound engineers, musicians, stage lighting operators.

**Core loop:** LISTEN → DIAGNOSE → EXPLAIN → SHOW → PRACTICE → VERIFY → SAVE

VERIFY is critical. The product should not simply tell the user what went wrong. When technically possible, it should listen again and determine whether the user actually corrected the issue.

---

## 2. Platform & Infrastructure

- **Backend baseline:** Raspberry Pi 5.
- **Additional storage:** external/thumb-drive storage should be used for appropriate project assets, datasets, models, backups, and other storage-heavy components rather than unnecessarily consuming the Pi's primary system disk.
- **Primary clients:** iOS and Android. **Additional client:** Windows where appropriate.
- **Architecture principle:** offline-first. Local processing capable of running locally should remain available without Internet connectivity. Cloud services used opportunistically when they materially improve functionality. Offline actions queue locally and synchronize when connectivity returns.
- **Voice-first architecture:** voice must be part of the architecture from the beginning rather than being bolted on later.

**Offline-first source-of-truth rule:** The local data layer must remain capable of supporting core product operation when the network disappears. Any synchronization architecture must account for temporary connectivity failure, interrupted uploads, repeated requests, duplicate operations, conflict resolution, partial synchronization, transaction rollback, and corrupted or stale sync state. Offline-first does not mean security protections disappear while offline — sensitive local data remains subject to secure-storage requirements. OWASP MASVS treats secure local storage, cryptography, authentication, networking, platform interactions, application code, resilience, and privacy as major mobile-security control groups.

---

## 3. Audio Diagnostic Engine — BPM / Key / Pitch

**Rejected:** aubio (copyleft licensing concern), Essentia (AGPL commercial licensing conflict).

**Chosen:** librosa (ISC License, permissive) + bpm-detector (MIT, uses librosa internally).

**Pipeline design:** Record short audio chunks with a lightweight capture layer, then analyze completed buffers/chunks. librosa should not be architected as an always-open streaming engine — audio acquisition and analysis remain separate responsibilities. Analysis may include BPM, key, pitch, rhythm, spectral information, confidence measurements, and additional validated musical characteristics.

**Accuracy rule:** No musical diagnostic should be represented as certainty when the underlying analyzer only has a confidence estimate. The internal data model should support: result, confidence, source algorithm/version, time analyzed, relevant input characteristics — so later algorithm upgrades don't pretend all historical results came from the same engine.

---

## 4. Speech Recognition — Voice Command & Conversation

**Baseline engine:** OpenAI Whisper — code and model weights currently MIT licensed. Local path provides offline operation, privacy-preserving voice commands, no per-minute cloud charge, resilience without internet.

**Upgrade path:** Deepgram, used for connected-mode transcription where accuracy/latency/streaming justify cloud processing. Its current terms (checked as of the Aug 6, 2026 revision) permit integration into an app that adds independent functionality, and customer Input/Output remain "Your Content."

**Critical Deepgram privacy rule:** Deepgram's current terms grant a broad license to use customer content to improve its services, including model training/testing, *unless the API request uses its available training opt-out mechanism.* Production audio sent to Deepgram must use that opt-out on every applicable request unless a later, deliberately approved data policy states otherwise. This must be implemented at the integration layer, not left as a dashboard setting someone might forget.

**Deepgram age restriction:** Deepgram's terms require the agreeing party to be at least 18 (or higher local age of consent). The company operates the account, but end-user handling remains the app's responsibility — reinforcing that under-13 users must never reach Deepgram merely by being on a family subscription.

**Language support:** English, French, Spanish at launch. Domain-specific testing must use real DJ, production, mixing, and vocal terminology, equipment names, and accents — general speech benchmarks are not sufficient evidence the product understands specialized music vocabulary.

**Cost architecture:** Cloud speech costs are variable costs. The credits layer (Section 7) exists partly to prevent heavy connected-mode usage from becoming an uncontrolled expense.

---

## 4a. Deep Vocal / Pitch Analysis

**Rejected:** Parselmouth/Praat path — GPL copyleft conflicts with the proprietary commercial architecture.

**Chosen:** loqa-voice-dsp (MIT licensed) — provides YIN/pYIN pitch detection, LPC formant extraction, FFT/spectral measurement, HNR, H1-H2, iOS FFI, Android JNI.

**Supported diagnostic foundation:** pitch detection, pitch contour, formants, HNR, H1-H2, spectral analysis, vibrato derivation (from the pitch contour, not a separate module).

**Important product-language rule:** Acoustic measurements (HNR, formants, H1-H2) must not become medical diagnoses. Acceptable phrasing: "increased breathiness measurement," "unstable pitch," "detected vibrato width," "stronger/weaker harmonic relationship." Unacceptable: diagnosing vocal disease.

**Raspberry Pi path:** either (a) compile and access the Rust implementation via FFI/PyO3, or (b) implement verified equivalents with permissively licensed numerical libraries. Whichever is chosen must be benchmarked on actual Pi hardware — loqa's published benchmarks were run on Apple M-series hardware and cannot be treated as Pi performance guarantees.

---

## 5. Stage Lighting / DMX Control

**Rejected:** previously identified GPL/copyleft options (OLA, udmx-pyusb, PyDMXControl).

**Candidate clean path:** PyDMX (license/hardware support reconfirmed at integration time) or DmxPy (supports Enttec USB DMX Pro-compatible hardware, including DMXKing ultraDMX devices, via PySerial), paired with Open Fixture Library (MIT) for fixture definitions.

**Hardware requirement:** USB-DMX hardware is a real product dependency. The app must clearly tell users when a feature requires external hardware — no interface should imply a phone or Pi can output DMX512 without compatible hardware.

**Hardware-abstraction rule:** Lighting commands must pass through an abstraction layer rather than embedding a particular adapter implementation throughout application logic, protecting the product against vendor/driver changes.

---

## 6. Copyright, Audio Handling & Content-Protection Layer

The original intent remains: reduce unnecessary handling or retention of copyrighted background material. **Legal clarification:** source separation is not a copyright exemption and cannot be marketed as automatically eliminating copyright liability. A technical filter can minimize incidental copyrighted material processed by the product — it does not transform unauthorized copyrighted material into authorized material. Apple requires developers to ensure content accessed/displayed/downloaded/streamed from third-party services is authorized under applicable rights and terms.

**Candidates:** Spleeter, Open-Unmix, Demucs.

- **Spleeter:** source code MIT licensed. However, pretrained-weight licensing questions were still being raised in the upstream repository as of 2026. **Master rule: do not ship Spleeter pretrained weights in the commercial product until the exact model artifact and its commercial redistribution/use rights are documented in the dependency register.** This is a release gate, not optional paperwork.
- **Open-Unmix:** code is MIT. The `umxl` pretrained weights are explicitly CC BY-NC-SA 4.0 (non-commercial) and must not ship in the commercial product. Other Open-Unmix models require individual artifact-level license verification before packaging.
- **Demucs:** code is MIT, but Meta archived the original repository in January 2025 — no longer automatically preferable merely for separation quality. Maintenance status, dependency health, model licensing, and Pi performance all matter now.

**Data-minimization design:** analyze in memory where practical; retain only diagnostic features/results; delete temporary mixed audio and separated stems once no longer required; do not permanently archive copyrighted background stems by default; give users explicit control where saving recordings is a feature.

---

## 6a. Platform Compliance — Apple, Google, Windows

**Apple App Store**
- **Recording indicator:** Guideline 2.5.14 requires explicit user consent plus a clear visual/audible indication when recording microphone, camera, screen, or activity. Every listening/diagnostic session must begin through informed user action, show a clear recording/listening state, and make stopping obvious.
- **In-App Purchase:** credits/currency bought through IAP may not expire and requires appropriate restoration mechanisms for restorable purchases. Purchased credits must be permanently ledgered unless spent, refunded, charged back, or legitimately adjusted.
- **Third-party AI disclosure:** clear disclosure required where personal data is shared with third parties, including third-party AI, with explicit permission where applicable — the Deepgram handoff must be visible and consent-based.
- **Privacy labels:** must disclose both first-party and relevant third-party partner data practices, kept accurate as practices change; privacy manifests/signatures required for certain third-party SDKs.
- **Account deletion:** apps supporting account creation must let users initiate deletion inside the app — built into account settings from the beginning, not added later.

**Google Play**
- **Data Safety:** must declare collection/sharing/security practices including data handled by third-party SDKs, not just first-party code. The dependency inventory and Data Safety answers must stay linked — changing an SDK may require changing the store declaration.
- **Families/children:** mixed-audience apps must put non-child-approved SDK/API behavior behind a neutral age screen or otherwise prevent collection from children. A proper neutral age screen does not encourage users to falsify their age (e.g., no preselected "acceptable" age).
- **AI:** specific AI-generated-content requirements and safety obligations apply. The product must accurately characterize deterministic DSP measurements vs. algorithmic diagnostics vs. AI-generated explanations/content — do not mislabel ordinary DSP as "AI," and do not hide genuinely generated AI output where disclosure is required.
- **Account deletion:** Android apps allowing account creation require a discoverable in-app deletion path plus an external web deletion path per policy.
- **Subscription cancellation:** must respect current Google Play cancellation mechanisms and access requirements.

**Windows / Microsoft Store**
- Must maintain accurate privacy information; a privacy policy is required whenever the app accesses, collects, or transmits personal information.
- Store certification is not instantaneous — can take up to several business days depending on package type, including technical/security/content checks. Release planning must budget this in.

---

## 6b. Privacy & Data Lifecycle Architecture

First-class system requirement. For each category of user data, the architecture must identify: **COLLECT → PROCESS → STORE → SYNC → SHARE → RETAIN → DELETE**

**Data inventory (minimum):** account identifiers, profile information, birthdate/age-screen state, parental-consent state, raw microphone audio, temporary audio chunks, transcriptions, diagnostic measurements, practice history, saved lessons, cloud sync records, billing/credit entitlements, device/telemetry information, crash/analytics information.

**Data minimization:** collect only what's needed. Audio processable locally should not automatically become a permanent cloud asset.

**Raw-audio default:** unless the user explicitly chooses a feature requiring saved recording, diagnostic audio should be transient by default. Derived musical measurements may be retained without retaining the entire source recording.

**Deletion propagation:** account/profile deletion must address local database, backend database, object/audio storage, cloud sync queue, analytics identifiers where required, third-party processors, and backups per documented retention policy. Apple requires privacy policies to address collection, usage, retention/deletion, and withdrawal of consent.

---

## 7. Monetization

**Model:** Freemium + subscription + carefully bounded credits.

**Free tier:** must provide real utility — demonstrate the system can actually listen, analyze, diagnose, teach. Not merely an advertising screen for Premium.

**Premium:** may unlock deeper diagnostics, extended lessons, advanced practice modes, richer saved progress, longer conversational assistance, more advanced analysis.

**Reverse trial:** new users get 14 days of premium functionality before reverting to the genuine free tier unless they subscribe.

**Credits:** apply specifically to variable-cost operations — extended cloud speech processing, especially compute-intensive cloud analysis, specifically identified premium diagnostic workloads. Core learning should not feel like a taxicab meter.

**Credit ledger rules:** must be transactional. Each operation records transaction ID, profile/account, credit delta, reason, purchase source, purchase transaction reference, timestamp, balance (or safely derived balance), and reversal/refund status where relevant. No silent balance edits.

**Apple rule:** purchased IAP credits cannot expire. Promotional (free) credits must be accounted for separately so their business rules can't accidentally violate purchased-credit treatment.

---

## 8. Multi-User Access

**Family billing:** launch feature. One paying account may support multiple distinct profiles, each with separate progress, history, practice state, recommendations, age/consent state, and saved diagnostics.

**Teacher/coach dashboard:** deferred. A different privacy relationship from family billing — requires deliberate permission, revocation, role-based access, audit behavior, and student/parent visibility. Must not be quietly introduced by reusing family-profile permissions.

---

## 8a. Family-Plan Parental Consent Flow — COPPA / Google Play Families

**Correct legal trigger:** Family billing by itself does not automatically make the service legally "mixed audience." COPPA applies to online services directed to children under 13, and services with actual knowledge they are collecting personal information from a child under 13. Google separately requires declaring target audiences and complying with Families Policy when children are included. **If this product intentionally permits under-13 profiles, it must implement the child-data architecture below.**

**Step 1 — Neutral age screen:** Profile creation collects birthdate without preselecting an adult age, explaining how to bypass restrictions, or encouraging a false response.

**Step 2 — Under-13 local-safe mode (before compliant parental authorization):** no Deepgram; no unnecessary third-party analytics; no advertising profiling; no third-party data sharing; no unrestricted cloud sync; only approved local functionality. On-device Whisper and local DSP are strategically valuable here, not just for offline performance.

**Step 3 — Parental consent (CORRECTED):** Email-plus consent is appropriate *only* when children's information is used internally and not disclosed to third parties. **Email-plus may NOT be treated as sufficient authorization for sending an under-13 user's voice/audio to Deepgram.**

**Under-13 Deepgram launch rule:** For launch, Deepgram remains disabled for under-13 profiles, period. A future release may reconsider this only after all of the following are completed: (1) current Deepgram contract/terms reviewed for the proposed child-data use; (2) the required verifiable-parental-consent method for that specific disclosure is established; (3) applicable FTC and Google requirements are satisfied; (4) the privacy notice names the relevant disclosure; (5) the data-processing architecture can technically enforce the consent state; (6) explicit approval is recorded. Until then, under-13 profiles remain local-processing only.

**COPPA 2025 amendments:** strengthened protections include separate parental opt-in for certain third-party disclosures, tighter data-retention limits, and stronger controls on monetization/sharing of child data. Children's personal information cannot be kept indefinitely and should be retained only as reasonably necessary for the purpose collected — child-profile data needs an explicit retention schedule (placeholder — see Instructions for Claude Code above; do not invent a specific number of days without explicit sign-off).

**Consent state (enforced at backend/data-access layer, not just hidden buttons):** NOT_APPLICABLE, AGE_SCREEN_PENDING, UNDER_13_RESTRICTED, PARENT_NOTICE_SENT, PARENT_INTERNAL_USE_CONSENT_VERIFIED, CLOUD_DISCLOSURE_NOT_AUTHORIZED, REVOKED. The exact enum may change during implementation, but the enforcement principle may not.

---

## 9. Design & Visual Standards

Interface must feel premium, modern, professional, current — not left as a vague "make it beautiful" instruction.

**Accessibility baseline:** target WCAG 2.2 AA — normal text contrast at least 4.5:1, large text at least 3:1, text resizable to 200% without loss of content/functionality. Android touch targets at least 48dp × 48dp. Apple VoiceOver requires meaningful accessibility labels for important interface elements.

**Voice-first does not mean voice-only:** every critical operation (Start/Stop Listening, Repeat explanation, Save/Delete result, Cancel recording, Manage subscription, Delete account) needs a usable visual/touch equivalent — protecting accessibility, noisy-environment usability, privacy, and platform compliance.

**Recording state:** must be distinctive and unmistakable. The user should never wonder "Is this app recording me right now?"

---

## 10. Development & Operations Standards

**10.1 Licensing discipline:** every third-party component needs a dependency record — name, version, source repo, code license, model/weight license where applicable, dataset license where applicable, commercial-use status, redistribution status, attribution requirement, date checked, source link. Code license and model-weight license must never be assumed identical (see Open-Unmix umxl example, Section 6).

**10.2 Continuous compliance rule:** platform policies are not frozen because this manifesto was correct when written. Before major milestones, beta distribution, TestFlight/internal testing, Google Play testing, Windows certification, every production submission, and every major SDK/vendor replacement — re-check current official requirements (Apple guidelines/privacy/SDK/StoreKit rules; Google Developer Policies/Families/Data Safety/billing/AI policy; Microsoft Store policy; FTC COPPA; OWASP MASVS; NIST SSDF; applicable WCAG/platform accessibility guidance). If a rule changes, documentation and implementation update before release, not after rejection.

**10.3 Security baseline:** OWASP MASVS as principal mobile security verification baseline — secure storage, cryptography, authentication, secure networking, platform security, code security, resilience, privacy. Use platform-secure storage mechanisms, not home-built cryptography. Encrypt sensitive information at rest/in transit, use HTTPS, avoid sensitive-data leakage through logs/caches, maintain third-party libraries.

**10.4 Secure software lifecycle:** NIST SSDF informs the development process — reduce vulnerabilities, reduce impact of undiscovered flaws, address root causes so vulnerabilities don't recur. Build process must include dependency review, code review, automated tests, vulnerability checking, secret scanning, release validation, and incident/root-cause correction.

**10.5 Secrets:** never hard-code production Deepgram API keys, signing credentials, database passwords, store secrets, or cloud tokens. Isolate secrets from source control; production clients must not contain backend master credentials.

**10.6 Database writes:** every mutation needs validation, error handling, transaction safety where appropriate, rollback/atomicity where appropriate, and idempotency for repeatable network operations. Payment, credit, consent, and synchronization mutations require particular care.

**10.7 Backup & restore:** a backup is not valid merely because a file exists — restoration must be tested. A backup system is only proven when data can be restored successfully.

**10.8 Sync testing must cover:** device offline, device reconnect, server temporarily unreachable, duplicate transmission, partially completed request, multiple devices editing, conflict, stale client, app termination mid-sync.

**10.9 Logging & observability:** production logs must help diagnose failure without leaking sensitive user audio, tokens, passwords, unnecessary transcripts, or child data. Monitor backend health, API errors, sync failures, billing failures, crash rates, audio pipeline failures, latency, resource exhaustion, storage capacity.

**10.10 Account deletion:** a launch architecture requirement, not a later settings-page feature. Apple requires in-app initiation; Google requires it plus an externally accessible deletion path. Must be supported by the data model from day one.

**10.11 AI-vendor isolation:** Deepgram or any future cloud AI/transcription vendor must sit behind an internal provider interface so core logic isn't structurally dependent on one vendor — enabling offline fallback, provider replacement, pricing-change resilience, outage handling, policy-change resilience, and region-specific restrictions.

**10.12 Dependency-change gate:** before upgrading/replacing a dependency, check license, model license, compatibility, supported CPU/OS architecture, security history, maintenance status, performance, privacy behavior, and terms of service if cloud-based. An update is not automatically an improvement.

**10.13 Front-end standards:** readable typography, accessible contrast, semantic accessibility labels, adequate touch targets, scalable text, logical focus order, screen-reader compatibility, no critical operation dependent solely on color.

**10.14 Release compliance gate:** no production build ships until the release checklist confirms LICENSE → SECURITY → PRIVACY → CHILD SAFETY → BILLING → ACCESSIBILITY → BACKUP/RESTORE → SYNC → STORE COMPLIANCE → PERFORMANCE → TESTING. A failed mandatory gate blocks release.

---

## 11. Build Sequence Scope & Script Count

Primary technical areas resolved sufficiently to begin systematic build planning: audio diagnostics, offline/connected speech, deep vocal analysis, lighting integration, source separation/content handling, family profiles, monetization, compliance architecture.

**Estimated implementation scope: approximately 32–37 primary scripts/modules at launch scope**, with supporting configuration, tests, platform projects, migrations, and documentation potentially increasing the physical file count. This is an architectural estimate, not a limit on how many files Claude Code is "allowed" to create.

- **Audio & diagnostics core (~6):** chunked audio capture; librosa BPM/key/pitch; vocal DSP integration; vibrato calculation; source-separation/content-minimization; diagnostic explanation generation.
- **Voice & language (~4):** local Whisper; Deepgram provider (with training opt-out built in); connectivity/provider switching; EN/FR/ES localization.
- **Lighting (~2):** DMX output abstraction; fixture-profile loader.
- **Data & sync (~4):** local schema (including per-profile consent-status field); safe database-write layer; offline operation queue; reconnect synchronization.
- **Monetization (~5):** credit ledger; reverse trial; Apple billing; Google billing; Microsoft billing.
- **Multi-user & compliance (~6-7):** family profile service; neutral-age screen; under-13 locked-down-mode enforcement at data-access layer; parental consent verification flow; third-party AI consent; privacy/data lifecycle enforcement; account deletion propagation.
- **Core loop & educational content (~4):** intent router; LISTEN→DIAGNOSE→EXPLAIN→SHOW→PRACTICE→VERIFY→SAVE orchestrator; lesson/practice engine; saved progress.
- **Client shells (~3):** iOS; Android; Windows.
- **Testing (not capped by the script estimate):** backup/restore verification; sync/conflict tests; French music-terminology tests; Spanish music-terminology tests; audio diagnostic accuracy tests; billing/credit tests; age-gate enforcement tests (proving an under-13 profile cannot reach Deepgram); account-deletion tests; accessibility tests; security tests; Deepgram-offline fallback tests.

---

## 12. Mandatory Pre-Release Evidence

Nothing is "done" merely because a feature works once. For important product areas, release evidence should exist:

- **Audio diagnostics:** reference test clips, expected ranges, accuracy report.
- **Voice:** EN/FR/ES domain vocabulary tests, offline behavior, cloud fallback.
- **Family safety:** tests proving an under-13 restricted profile cannot reach Deepgram.
- **Billing:** purchase, restoration, cancellation, refund/revocation, credit ledger integrity.
- **Sync:** offline mutation, reconnect, duplicate request, conflict.
- **Backup:** successful restore onto a clean environment.
- **Privacy:** data inventory mapped to App Store privacy and Google Data Safety answers.
- **Security:** OWASP MASVS-based review.
- **Accessibility:** VoiceOver/TalkBack, text scaling, contrast, touch-target review.

---

## 13. Compliance & Dependency Revalidation Register

Every important external rule or dependency must carry a Last Verified value: Apple App Review Guidelines, Google Developer Policies, Microsoft Store policies, FTC COPPA, Deepgram Terms, Spleeter code license, Spleeter model license, Open-Unmix code/model license, loqa-voice-dsp license, librosa license, Whisper code/model license — each with a last-verified date. A coding agent may not remove this mechanism because it appears "administrative." It is part of product risk control.

---

## 14. Rule for Future AI/Developers

Distinguish among: **CONFIRMED** (a decision in this manifesto), **VERIFIED EXTERNAL FACT** (checked against a reliable current source), **IMPLEMENTATION CHOICE** (a technical detail decidable during coding without changing scope), **OPEN ISSUE** (a question requiring research before implementation), **PROPOSED CHANGE** (something that would alter this manifesto and requires deliberate approval).

An AI must never silently convert an OPEN ISSUE into a made-up assumption, or a PROPOSED CHANGE into a completed design decision merely because the alternate implementation is easier.

---

## 15. Final Product Standard

The standard is not "Does it run?" The standard is: Does it work accurately? Does it work offline where promised? Does it protect users? Does it protect children correctly? Does it protect the company? Does it respect licenses? Does it respect copyrighted material? Does it survive connectivity problems? Does it survive billing errors? Can it restore its data? Can a user delete their account? Is it accessible? Is it secure? Can its claims be defended? Does it provide something a generic chatbot cannot? And would a professional musician actually trust it?

If the answer to any required part is no, the product is not finished.

---

## 16. Master Maintenance Rule

This manifesto must not become stale. At every major release cycle, review official sources controlling the portions of the product being released: **CHECK → IDENTIFY CHANGE → ASSESS IMPACT → UPDATE MANIFESTO/REQUIREMENTS → UPDATE IMPLEMENTATION → TEST → RELEASE.** A policy change must never be silently ignored. A dependency-license change must never be silently accepted. A model-weight change must never be assumed to inherit the library's code license. A vendor-Terms change must never be treated as irrelevant simply because the API still works.

---

## 17. Current Research Baseline — September 12, 2026

This version was checked against: Apple App Review Guidelines, App Privacy documentation, third-party SDK/privacy-manifest requirements, StoreKit restoration documentation; Google Play Data Safety policy, Families Policy, target-audience/neutral-age-screen guidance, account-deletion policy, billing/subscription documentation, AI-content policy; Microsoft Store publishing/privacy/certification documentation; FTC COPPA Rule and guidance, 2025 amendments; NIST SSDF; OWASP MASVS; W3C WCAG 2.2; current Deepgram Terms; upstream Whisper, librosa, Spleeter, Open-Unmix, Demucs licensing/status; loqa-voice-dsp documentation; Open Fixture Library licensing; DmxPy documentation; bpm-detector documentation.

This establishes the current baseline — it does not authorize future developers to assume these sources will remain unchanged forever.

---

## Non-Negotiable Closing Rule

Build the product described here. Do not shrink it into a chatbot. Do not remove offline-first architecture because cloud implementation is easier. Do not replace local diagnostics with generic AI guesses. Do not sacrifice privacy for convenience. Do not route child audio into third-party services without required legal and technical authorization. Do not ship a model because its repository code happens to be MIT. Do not accept inaccessible UI because it looks fashionable. Do not call a backup successful until restoration is tested. Do not call synchronization reliable until failure cases are tested. Do not call an AI diagnostic accurate without measurement. Do not call the application production-ready until its licensing, security, privacy, billing, accessibility, child-safety, platform-compliance, and recovery gates pass.

And before every major release, reverify the rules against current official sources rather than relying solely on what was true when this manifesto was written.

---

*This is the Master Product Manifesto and governing build reference for the Voice-First Music Intelligence Ecosystem. Locked for Claude Code build per the Instructions above — the five-pass verification requirement on security/privacy/compliance sections is not optional.*
