# US Sales Tax Data, 2026

State and average local sales tax rates for all 50 US states and the District of
Columbia, with the parts most rate tables leave out: how each state treats
groceries, whether delivery charges are taxable, and the economic nexus
thresholds a remote seller has to watch.

JSON and CSV. No API key, no rate limit, no sign-up. **CC BY 4.0** — commercial
use is fine, credit is the only condition.

| File | Rows | Size |
|---|---|---|
| [`data/sales-tax-2026.json`](data/sales-tax-2026.json) | 51 | ~31 KB |
| [`data/sales-tax-2026.csv`](data/sales-tax-2026.csv) | 51 | ~9 KB |

## Read one column with suspicion

Most of this has been cross-verified. One field has not, and it is named here
rather than buried:

> **`grocery_local_taxable` has not been through independent cross-verification.**
> Every other column has.

It marks the minority of states that exempt food from the *state* rate while
still allowing *local* taxes on it — Georgia, North Carolina, Louisiana,
Arizona, Colorado, and South Carolina in the current data. The risk is
omission: if a state belongs in that set and is missing, its row understates the
tax on groceries.

If you verify it and find an error, open an issue. Corrections are the most
useful contribution this repo can receive, and every one of them is recorded
in the [changelog](CHANGELOG.md) with what the wrong value was.

## Columns

| Column | Meaning |
|---|---|
| `name`, `abbr`, `slug` | Jurisdiction identifiers |
| `has_state_sales_tax` | `false` for AK, DE, MT, NH, OR |
| `state_rate` | State rate on general merchandise |
| `avg_local_rate` | Population-weighted average of local rates |
| `combined_rate` | The two added together |
| `grocery` | `exempt` / `reduced` / `full`, **state rate only** |
| `grocery_rate` | State rate on unprepared food; empty where not published |
| `grocery_flat` | Grocery rate is the whole tax, no local addition (UT, VA) |
| `grocery_local_taxable` | Local tax applies to state-exempt food — *unverified* |
| `shipping` | `always` / `separate` / `varies` |
| `nexus_amount` | Economic nexus sales threshold, USD |
| `nexus_transactions` | Transaction-count threshold; empty where repealed |
| `nexus_logic` | `or` — either test triggers nexus |
| `agency_url` | The state's own tax authority |
| `page_url` | Human-readable write-up for that jurisdiction |

`shipping: varies` means *not established*, not *varies by transaction*. 41
jurisdictions are still `varies`, because settling it properly means reading 41
state administrative codes rather than trusting an aggregator. Two of them
disagreed with each other during compilation, and one had the Texas rule
backwards, which is why the remaining rows are marked unknown instead of filled
in.

## Caveats that actually matter

**These are averages.** No figure here is valid for a specific street address.
Local rates vary by city, county, and special district, and
[ZIP codes do not align with tax jurisdictions](https://graceledgers.com/tools/sales-tax-by-zip-code/)
— they are USPS delivery routes, not areas, and the Census Bureau says so
directly.

**Do not file a return with this.** Use it to compare states, prototype, teach,
populate a dropdown, or sanity-check a number someone handed you. For a real
sale, use the `agency_url` for that jurisdiction.

**Rates move.** Revised twice yearly, in January and July, plus corrections. The
`_meta.version` field carries the date. If you need a stable snapshot, vendor
your own copy rather than fetching at runtime.

## Using it

### Pick a URL deliberately

| | URL |
|---|---|
| **Pinned** — never changes | `https://raw.githubusercontent.com/miningjini-tom/graceledgers/v2026.08.20/data/sales-tax-2026.json` |
| **Latest** — tracks corrections | `https://raw.githubusercontent.com/miningjini-tom/graceledgers/main/data/sales-tax-2026.json` |

`main` moves. When a rate is corrected, anything reading `main` silently starts
returning different numbers — which is fine for a dashboard and not fine for
something that produced an invoice last quarter. **If the output matters, pin to
a tag** and bump it when you have read the [changelog](CHANGELOG.md).

```python
import json, urllib.request

URL = ("https://raw.githubusercontent.com/miningjini-tom/graceledgers/"
       "v2026.08.20/data/sales-tax-2026.json")          # pinned
data = json.load(urllib.request.urlopen(URL))

top = sorted(data["jurisdictions"], key=lambda s: -s["combined_rate"])[:5]
for s in top:
    print(s["name"], s["combined_rate"])
```

```python
import pandas as pd

CSV = ("https://raw.githubusercontent.com/miningjini-tom/graceledgers/"
       "v2026.08.20/data/sales-tax-2026.csv")
df = pd.read_csv(CSV)
print(df[df.grocery_local_taxable][["name", "combined_rate"]])
```

```js
const URL =
  "https://raw.githubusercontent.com/miningjini-tom/graceledgers/v2026.08.20/data/sales-tax-2026.json";
const data = await (await fetch(URL)).json();
console.log(data.jurisdictions.filter((s) => !s.has_state_sales_tax));
```

More in [`examples/`](examples/).

> **Use these raw URLs rather than graceledgers.com.** The website sits behind
> bot protection whose behaviour depends on the client and the network. Plain
> `curl` usually passes; `requests`, `urllib`, and `pandas.read_csv(url)`
> reliably do not — which is precisely the stack most people would reach for
> here. The protection is site-wide and unrelated to these files. GitHub serves
> the same bytes with no such check.

## Where the numbers come from

Rates: Tax Foundation, *State and Local Sales Tax Rates, Midyear 2026*.
Everything else: individual state revenue departments, one per row, in
`agency_url`.

The data was compiled for the calculators at
[graceledgers.com/tools](https://graceledgers.com/tools/), then cross-verified
independently. That pass found seven errors in the first version, including one
state whose shipping rule had been recorded backwards from a secondary source.
The [full log of what was wrong and why](CHANGELOG.md) is published rather than quietly fixed.

## Licence

[CC BY 4.0](LICENSE). Attribution:

```html
Sales tax data from <a href="https://graceledgers.com/data/">Grace Ledgers</a>,
licensed CC BY 4.0.
```

Plain text is fine where a link is not possible:
*Sales tax data from Grace Ledgers (graceledgers.com), CC BY 4.0.*

## Contributing

Corrections welcome, especially on `grocery_local_taxable` and the 41
`shipping: varies` rows. Please cite the state's own guidance rather than an
aggregator — this dataset has already been bitten once by two aggregators
disagreeing.
