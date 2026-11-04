---
name: tcx-expectations
description: Analyze companies and investment scenarios through Expectations Investing, comparing own forecasts, consensus, whispers, and price-implied expectations with revisions, remaining catalysts, marginal demand, and market reactions. Use for company analysis, investment timing, and conditional buy/sell price ranges; exclude simple quotes or factual lookups.
---

# TCX Expectations

For company investment analysis, understand what can change in the
business, what investors already expect, and what could change their willingness
to own the shares. Build competing paths before drawing an investment conclusion.
This also applies when the user simply asks to analyze a company.

## Decision standard

A low multiple or discount to intrinsic value does not establish a buying
opportunity. A high multiple or premium to central intrinsic value does not
automatically rule one out. Assess prospective returns, loss exposure, remaining
expectation revisions, the relevant horizon, and competing uses of capital.
Retain valuation as an expectations and downside anchor; do not require market
price to converge to it within the investment horizon.

The canonical [equity valuation method](../../../.tradingcodex/subagents/skills/valuation-analyst/tcx-valuation/references/equity-valuation.md) governs
financial evidence, forward estimates, comparable periods, and value-date
discipline. This method adds conditional market-price and action scenarios.
If those scenarios disagree with the valuation conclusion, explain the conflict
and its effect on the proposed action instead of forcing agreement.

## Frame the company

- Establish the information cutoff, sourced current price, investment horizon,
  next decision-relevant events, and forecast periods. Separate an event trade
  from the default twelve-month valuation horizon.
- Compare four distinct objects on matched metrics and dates: own estimates,
  published consensus, attributable whispers, and model-implied expectations in
  price. Guidance and reported actuals provide separate context. Unavailable
  whispers remain unobserved; a proxy is not a discovered whisper number.
- Trace the relevant chain from customer needs and willingness to pay through
  substitution, competition, unit economics, investment, funding, and cash flow.
  Identify the current bottleneck and who benefits when it moves. Investigate
  the links that can change the conclusion, rather than every possible input.
- Distinguish levels, growth, growth acceleration, fixed-period estimate
  revisions, and revision acceleration. Evaluate each relative to what was
  expected before the information arrived. Decelerating growth can still be an
  upside surprise; accelerating growth can still disappoint.
- Ask what remains to be demonstrated: magnitude, duration, profitability,
  financing resilience, or a new demand source. Map the unpriced uncertainty,
  evidence that would resolve it, likely timing, and the investors it could move.
  Do not turn the number of positive headlines into a numerical surprise score.

Use [scenario design](references/scenario-design.md) for the scenario tree,
market recognition, probability updates, and conditional entry/exit ranges.
Use [evidence collection](references/evidence-collection.md) when selecting
sources, reconstructing expectations, or evaluating flow and reaction data.

## Connect expectations to investment demand

Assess both capacity to take risk and willingness to allocate it here. Specify
the plausible marginal buyer, why they would buy now rather than an alternative,
and the holders or new supply they must absorb. Financing, credit, participation,
positioning, relative performance, and event reactions can support or weaken that
case. Their relevance varies by business and horizon.

Treat this as an evidence-based hypothesis. A market-capitalization increase is
not the amount of cash required to achieve that price increase. Narrow leadership
alone does not establish exhausted demand, and the same price fall cannot serve
as several independent pieces of bearish evidence.

## Deliver the decision

Explain the dominant causal path, strongest competing path, and expectation gap.
When numerical inputs support it, show upside/base/downside outcomes with
current-evidence-based probabilities, same-date market-price ranges or
representative targets, expected return, and material downside. Use explicit
judgment assumptions and sensitivity where calibration is unavailable. If a
numeric bridge cannot be supported, retain useful conditional paths and state
the missing input. Separate market-price estimates from intrinsic value.
Conditional reaction branches must aggregate without counting an outcome twice.

Give conditional buy/add, hold, reduce/sell, and wait/avoid regions when the
evidence supports them. State their horizon, necessary observations, price or
return conditions, invalidation, and next update trigger. A conditional region
can be empty; never manufacture a buy price simply because the user requested one.
If precise prices are unsupported, give the missing input and an actionable
condition instead of invented precision. Estimates and provisional judgments are
permitted before official confirmation when their assumptions remain visible.

Write around the decision and its reasoning, not a checklist of research tasks.
Include the finding that would most change the action. Do not make a universal
rule that all entries must wait for a rally, a positive earnings print, or a flow
confirmation; account for the return forgone while waiting and false signals.

## Research subagent

For a material unresolved expectations/recognition question, use the reusable
[expectations analyst brief](agents/expectations-analyst.md). Pass its absolute
path, the bounded question, cutoff, horizon, source ownership, and reusable
evidence IDs. Load the brief explicitly in the child; do not rely on inherited
chat history. Use native delegation only when it improves the work.

This brief supplies a specialty to an available native child; it does not
register a new persistent role or create a separate service identity. In
TradingCodex research, preserve `tcx-workflow`, source-gate, calculation, and
parent-recording requirements. Reuse existing fundamental, valuation, macro,
technical, portfolio, and risk work; do not duplicate those responsibilities or
use this child as a substitute for a required independent reviewer. The skill
grants no order or approval authority.
