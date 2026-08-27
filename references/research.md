# Desk Research Protocol

Loaded by any thinking skill before recording an unknown as a risk, an assumption, or an open question. It defines what to look up with WebSearch per dimension, how to judge a source, and how to record a finding auditably.

## Operating Rule

**Search before flagging ignorance as a risk.** A fact WebSearch can settle in two minutes must never be recorded as an open question, an assumption, or a key risk. "The user doesn't know" is a prompt to look it up.

| Situation | Wrong move | Required move |
|---|---|---|
| User doesn't know the regulatory landscape | Record "regulatory uncertainty" as a key risk | Search the regulator, then record what the regime requires. If it forbids the business at GTM's implied scale, that is `killer`, not `proceed-with-caution` |
| User can't estimate CAC for a channel | Record "CAC unknown", let `evidence_strength` fall to weak | Search published benchmarks for that channel and industry, present the range, ask where they sit in it |
| User names a competitor but not its pricing | Record "pricing unclear" | Fetch the pricing page |
| User claims a market is large | Record it as an assumption and move on | Search a registry, association, or government statistic that counts the actual population of buyers |

Only two things introduce new facts into an idea: what the user learned from talking to real people, and desk research. Reasoning over existing material is inference — never record it under a research heading.

## Per-Dimension Search Targets

### Alternatives and competitors (validate, gtm)

Look up: pricing pages, dated review-site listings, changelogs, shutdown notices, funding and acquisition news, post-mortems of dead products in the category.

Queries: `<product> pricing`; `<category> software reviews <year>`; `<product> shutting down`; `<product> acquired by`; `<category> startup post-mortem why we failed`.

Good source: the vendor's own pricing or changelog page; a review site whose reviews carry dates; a founder's own shutdown write-up.

Establishes that an alternative exists, what it charges, whom it targets, whether it is maintained, and what killed comparable attempts. Does **not** establish that its customers are unhappy, that it is beatable, or that list price is what buyers pay.

### Market size and segment counts (validate)

Look up: industry-association membership counts, government statistical agencies, business registries, occupation tables, licensing-body registers (they publish licensee counts).

Queries: `number of <business type> in <country> statistics`; `<industry> association annual report members`; `<country> business register <sector> count`.

Good source: a statistical agency table or an association's annual report, with a stated collection year.

Establishes a countable population of candidate buyers — the only market number worth writing down. Top-down analyst TAM figures ("the $X billion market growing at Y% CAGR") are near-worthless here: paywalled, restated third-hand, scoped so the category swallows adjacent spend, and silent on how many entities could plausibly buy this. If only a TAM headline exists, record it as an assumption and name the missing count.

### Distribution and CAC benchmarks (gtm)

Look up: benchmark reports segmented by channel and industry, ad-platform rate cards, agency and industry surveys, keyword difficulty and volume, community size and posting rules.

Queries: `<channel> advertising benchmarks <industry> <year>`; `average CPC <industry> <platform>`; `<platform> ads minimum budget`; `r/<subreddit> rules self promotion`.

Good source: an ad platform's own documentation; a benchmark report naming its sample and period; a community's rules page.

Establishes an order-of-magnitude cost band per channel, whether the channel is open at all (many communities ban promotion outright), and how contested the keywords are. Does **not** establish this idea's CAC — medians hide enormous variance. Present each finding as a band to test against, then ask which end of it the user expects and why.

### Regulatory and licensing (feasibility) — highest yield

The most searchable dimension in the product and the most decision-changing: a regime that forbids the business, or requires a license the user cannot obtain, converts a vague caution into a `killer` verdict.

Look up: the regulator's site, the licensing body's register and application requirements, the applicable data-protection regime, sector regimes (financial services, insurance, health and medical devices, food handling, employment and worker classification, alcohol, education, childcare, transport), and the terms of service of any platform the idea depends on.

Queries — search the **regulator**, not the topic: `<country> <sector> regulator licensing requirements`; `do I need a license to <activity> <jurisdiction>`; `<activity> regulated activity <jurisdiction> guidance`; `<platform> API terms scraping`.

Good source: the regulator's or licensing body's own guidance, the statute or official register, the platform's live terms page. Law-firm alerts are usable orientation and often name the regime, but confirm against the primary text.

Establishes whether the activity is regulated, who regulates it, what the license is called, and whether platform terms permit the mechanic the idea relies on. Does **not** establish that the user's structure complies — record "this regime applies; scope of compliance unconfirmed" and, where exposure is material, name a qualified professional as the next step rather than more searching.

### Vendor, API and infrastructure pricing (feasibility, mvp)

Look up: price pages, free-tier and rate-limit docs, tier thresholds where price steps up, deprecation and pricing-change history.

Queries: `<vendor> pricing per <unit>`; `<API> rate limits`; `<API> deprecated <year>`; `<vendor> price increase announcement`.

Good source: the vendor's own pricing, docs, and changelog pages.

Establishes unit cost, the volume at which the bill jumps, and the vendor's record of changing terms on dependents. Compute run cost at GTM's implied volume, not at one user. Does **not** establish negotiated pricing.

### Labor and build cost (feasibility, mvp)

Look up: salary surveys and government wage data by role and region, contractor and agency rate benchmarks.

Queries: `<role> salary <region> <year> survey`; `<role> contractor day rate <region>`; `<country> wage statistics <occupation>`.

Establishes a defensible cost band per role-month. Does **not** establish how many role-months the build takes — that stays the user's estimate, and pushing back on it is a red-flag matter, not a research one.

## Query Craft

| Instead of searching | Search |
|---|---|
| `<product name>` | `<product> pricing` — one page carries tiers, segment, and positioning |
| `<category> market size` | `number of <buyer type> in <region>` — a countable population beats a TAM headline |
| `<competitor> launch` | `<competitor> shut down` / `why we shut down <product>` — post-mortems state the real constraint; launch coverage is a press release |
| `is <activity> legal` | `<jurisdiction> <sector> regulator`, then read its guidance — the regulator names the regime, blogs paraphrase it |
| `<API> cost` | `<API> pricing` plus `<API> rate limits` — the limit, not the price, usually breaks the plan |

Add the year wherever currency matters (pricing, benchmarks, regulation), and add `site:<gov or association domain>` to pin a search to a primary publisher.

## Source Quality Tiers

| Tier | What it is | How to spot it |
|---|---|---|
| **Primary — usable as evidence** | The party's own publication: vendor pricing, regulator guidance, statutes and registers, government statistics, filings, platform terms, founder post-mortems, dated first-hand reviews | Published by the entity the claim is about; dated or versioned; states its own scope |
| **Secondary — usable with attribution** | Benchmark reports with named methodology, association reports, established trade press, law-firm alerts | Named author and date; states sample or sources; links to primary material |
| **Unusable — never record as research** | Vendor content marketing framed as research, undated pages, aggregator listicles restating one another, AI-generated roundups, competitor-hosted "X vs Y" pages | No date or author; identical sentences and numbers across sites with no shared original; "best 10 tools" ending in a signup CTA; statistics with no attributable origin |

When several sites repeat one number, trace it to the original publisher. If the trail dead-ends, the number is not evidence — record the claim as an assumption and say the trail dead-ended.

## Recording a Finding

At the point the claim is used in the artifact:

```markdown
**Researched:** <claim, stated plainly> — <publisher>, <date of source>. <URL>. Retrieved <YYYY-MM-DD>.
```

All five elements are required: claim, publisher, date of the source, URL, date retrieved. A source with no visible publication date is recorded as `date unknown` and drops a tier.

**A finding with no retrievable source is not research.** Write it as `**Assumption:** <claim>`, exactly as if no search had happened — recollection, plausible inference, and a result whose link cannot be produced all fall under this rule. Such assumptions count against `evidence_strength`, which gates whether a `go` verdict is available at all.

Where research contradicts an earlier artifact, do not rewrite it — Protocol D applies: add the finding to that artifact's `## Notes from <current-phase> phase` footer, or log a `gaps` entry if non-trivial.

## Keep the User in the Loop

Present findings; never silently overwrite what the user believes.

> "I found <finding> — <publisher>, <date>. Does that match what you know? If it's wrong or out of date, tell me what you've seen."

The answer is itself signal: a founder who says "that price is list, everyone here gets 40% off" has contributed a fact worth more than the page. Record the correction as user-stated, keep the source finding alongside it, and label any reasoning over both as inference. Never soften a finding to be encouraging — report what was found, including when it is bad for the idea.

## When Search Returns Nothing

Say so explicitly. Do not skip the dimension quietly or fill the hole with plausible-sounding numbers.

> "I searched for <what> and found nothing usable — <what came back and why it was rejected: undated, content marketing, no primary source>. Do you have a source, or do we record this as an assumption?"

Then record it as `**Assumption:** <claim>`, note in `## Open Questions` what would resolve it and where such a fact would live (a named regulator, registry, or vendor page), and let it weigh on `evidence_strength`. If the item is regulatory or licensing, add it to `key_risks` too — an unanswered legality question is a live risk, not a missing number.
