# Monetization

Credit ledger, 14-day reverse trial, and Apple/Google/Microsoft billing integrations. See manifesto Section 7.

**Status:** not yet implemented.

Key rules from the manifesto this module must honor:
- Every credit-ledger operation is transactional: transaction ID, profile/account, credit delta, reason, purchase source, purchase transaction reference, timestamp, balance, reversal/refund status. No silent balance edits.
- Purchased Apple IAP credits never expire; promotional/free credits are tracked separately so their rules cannot accidentally violate purchased-credit treatment.
- Free tier must provide real diagnostic utility, not function only as an ad screen for Premium.
