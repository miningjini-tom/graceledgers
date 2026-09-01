// States where food is exempt from state sales tax but local taxes still apply.
// This is the column the dataset flags as not yet cross-verified.
const URL =
  "https://raw.githubusercontent.com/miningjini-tom/graceledgers/v2026.08.20/data/sales-tax-2026.json";

const res = await fetch(URL);           // CORS is open, this works in a browser
const data = await res.json();

const catch22 = data.jurisdictions.filter(
  (s) => s.grocery === "exempt" && s.grocery_local_taxable,
);

console.log(`${catch22.length} jurisdictions exempt food at state level`);
console.log("but still let local tax apply:");
for (const s of catch22) console.log(` ${s.name} (${s.abbr})`);
