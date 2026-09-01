# Changelog

Every correction to the data is recorded here, including what was wrong, why,
and where the right answer came from. A dataset that admits one weak column is
making a claim; a dataset that shows its correction history is proving it.

Versions follow the `_meta.version` field and are tagged in this repository, so
`v2026.08.20` is a permanent snapshot you can pin to.

## v2026.08.20 — first public release

51 jurisdictions. Rates from Tax Foundation *State and Local Sales Tax Rates,
Midyear 2026*; everything else checked against individual state revenue
departments.

**Known weakness, stated rather than hidden**

- `grocery_local_taxable` has not been through independent cross-verification.
  It currently marks GA, NC, LA, AZ, CO, SC. The risk is omission: a state that
  belongs in the set but is missing will understate the tax on groceries.

**Deliberately incomplete**

- 41 of 51 `shipping` values are `varies`, meaning *not established*. Settling
  them means reading state administrative codes rather than trusting
  aggregators — see the corrections below for why that distinction was made the
  hard way.

### Corrections made before release

These were found by an independent cross-verification pass over the first
compilation. Seven values were wrong. All were in fields that had to be looked
up per state rather than copied from a single table — the columns taken wholesale
from one source had no errors at all.

| Field | Was | Now | Why it was wrong |
|---|---|---|---|
| `shipping` (AL) | `always` | `separate` | **Backwards.** Ala. Admin. Code r. 810-6-1-.178 exempts delivery by common carrier when separately stated. Two secondary aggregators listed Alabama as always taxable; the state rule says the opposite. |
| `grocery_rate` (AL) | 3.0 | 2.0 | Phased cut had two effective dates — 4%→3% in Sept 2023, 3%→2% in Sept 2025. Only the first was captured. |
| `grocery` (MS) | `full` | `reduced` 5.0 | Mississippi cut groceries from 7% to 5% on 1 July 2025. |
| `grocery_rate` (UT) | 3.0 + local | 3.0 flat | Utah's 3% is 1.75% state + 1.25% local combined, uniform statewide. Adding local tax on top produced 4.32%. |
| `grocery_rate` (VA) | omitted | 1.0 flat | Recorded as "sources conflict" when they did not. The state portion was removed in 2023, leaving a uniform 1% statewide. |
| `nexus_transactions` (IL) | 200 | none | Repealed effective 1 January 2026. |
| `nexus_transactions` (KY) | 200 | none | Repealed effective 1 August 2026. |

Rate table also moved from the January 2026 edition to the midyear (1 July)
edition, changing average local rates in AZ, AR, CA, GA, IL, KS, LA, NM, NC, VT,
WA, WV, WY.

### One thing worth knowing about official sources

Louisiana's Sales and Use Tax Commission for Remote Sellers still publishes the
200-transaction economic nexus threshold on its FAQ, along with 2020
registration deadlines. That threshold was repealed by **Act 375 of the 2023
Regular Session**, effective 1 August 2023.

The dataset follows the enrolled Act, not the FAQ. If your figures disagree with
this file for Louisiana, check which of the two you are reading.

---

## How corrections get made

Open an issue with the state, the field, and a citation. **Cite the state's own
guidance or the statute, not an aggregator** — this dataset has already been
bitten once by two aggregators contradicting each other, one of which had the
Texas shipping rule backwards.

Accepted corrections are recorded here with the same detail as the table above,
including what the wrong value was. Removing the evidence of an error is how a
dataset stops being trustworthy.
