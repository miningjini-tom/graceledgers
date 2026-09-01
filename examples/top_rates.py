"""Five highest combined sales tax rates in the US."""
import json
import urllib.request

URL = ("https://raw.githubusercontent.com/miningjini-tom/graceledgers/"
       "v2026.08.20/data/sales-tax-2026.json")

with urllib.request.urlopen(URL) as fh:
    data = json.load(fh)

print("version:", data["_meta"]["version"], "| rates as of",
      data["_meta"]["rates_as_of"])

top = sorted(data["jurisdictions"], key=lambda s: -s["combined_rate"])[:5]
for s in top:
    print(f"{s['name']:<15} {s['combined_rate']:>6.2f}%  "
          f"(state {s['state_rate']:.2f} + local {s['avg_local_rate']:.2f})")
