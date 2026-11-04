# Designing Expectation and Price Scenarios

## Expectations first, without pretending they are observable facts

Define the metric, period, accounting basis, currency, units, and information
date before comparing estimates. A fiscal-year consensus EPS, next-quarter
whisper EPS, and long-term growth implied by price answer different questions.
Identify the pivotal driver rather than treating EPS as the whole investment.

Use reverse valuation where the business and evidence support it. Multiple
growth/margin/reinvestment/discount-rate/duration combinations can explain one
price. Show an implied range or sensitivity frontier, what was held fixed, and
which assumptions have independent evidence. Do not call one fitted solution
the market's uniquely revealed belief. If a reverse DCF is unsuitable, use a
business-appropriate expectations test and state the unidentified dimensions.

Build an independent operating forecast from causal drivers, with ranges, and
then compare it with external expectations. Missing consensus is a coverage gap,
not a reason to replace forward estimates with trailing multiples or abandon
the inquiry. Missing fundamental evidence still constrains confidence.

## What does the derivative refer to?

For comparable operating observations X, state the frequency and definition:

- Change in level: X(t) - X(t-1).
- Growth: X(t) / X(t-1) - 1, only with a meaningful denominator.
- Growth acceleration: growth(t) - growth(t-1), in percentage points.
- Forecast revision: E(as-of b, target period) / E(as-of a, same target period)
  - 1. Track revision breadth and dispersion where coverage permits.
- Revision acceleration: change in revision pace over comparable as-of windows
  for the same target period, with a stable contributor cohort where possible.
- Surprise: reported result minus the pre-event expectation; specify consensus
  and whisper comparisons separately, and use a percentage only if meaningful.

A zero/negative denominator, changing contributors, acquisition, FX move,
seasonality, base effect, accounting change, interpolation, or rolling NTM
composition can distort these comparisons. Use absolute/percentage-point
changes or a stable bridge instead. Do not infer acceleration from only two
points or from comparing different target years. Do not differentiate smoothed
estimates as though they were independently observed daily fundamentals.

The important question is whether the path exceeds or falls short of the path
that investors already require, and whether subsequent revisions can continue.
For example, growth falling from 30% to 20% can be favorable relative to a 10%
expectation. Absolute deterioration and positive surprise can coexist.

## Causal map and remaining surprise

For consequential links, identify mechanism, observable evidence, expected lag,
alternative explanation, and a falsifier. A chain can stop or reverse at any
link. Ask where the binding constraint is now: technology, demand, supply,
distribution, regulation, power, financing, or investment capacity.

An event matters through unresolved information. For each major catalyst note:
what is already known, what is disputed, the result needed to move estimates,
who would revise their view, and why the effect can persist. Distinguish higher
profits from a longer profitable growth period and from a lower discount rate.
Do not count an earnings beat, an estimate revision, and rerating as three
independent catalysts when they describe one transmission chain.

For the supplied AI case, compare at least the relevant opposing mechanisms:
lower inference costs can compress revenue per task and hardware spend per task,
or expand adoption/usage enough to increase total demand. Test paid enterprise
usage, monetization, workload mix, unit economics, funding, orders and capacity
before propagating a consumer-service estimate into total-company ARR and then
sector-wide CAPEX. Memory mix gains can coexist with weaker total spending;
cash-rich hyperscalers and leveraged customers can respond differently.
Treat this as a reusable example, not a standing bearish AI thesis.

## Capacity, allocation, and recognition

Separate the company's funding capacity from investor demand for its shares.
For company funding, inspect cash generation, liquidity, maturities, collateral,
credit spreads, funding terms, and the return on incremental investment. For
investor demand, ask which plausible cohort can and would increase exposure,
what alternative they would forgo, and what selling/issuance must be absorbed.
Evidence may include investor-category flows, fund creations/redemptions,
ownership/benchmark constraints, free float, turnover, concentration, breadth,
buybacks and new issuance. Treat reported cohorts as coarse aggregates.

There is no universal amount of cash needed for a 30% share-price rise. Prices
are set at the margin; cash changes hands between buyers and sellers. Market
capitalization is not a cumulative inflow account. Deposits, money supply, fund
AUM changes, short interest, and trading volume each measure something else.
Use them as qualified inputs, never as a cash-budget identity or proof of
investor intent. A credible shortage of incremental demand can nevertheless
make a good-business/cheap-share scenario unattractive over the chosen horizon.

## A small conditional tree

Construct distinct upside/base/downside business paths and relevant market
recognition states conditional on each. Recognition can include delayed uptake,
skepticism, fading crowding, expanding participation, or a risk-off discount.
Use only distinctions that could change the decision; a flat scenario table
is sufficient if it preserves the same conditional reasoning.

For business state F and recognition state R:

    joint probability(F,R) = probability(F) * probability(R | F)
    expected price(H) = sum over leaves [joint probability * price(H,F,R)]

Business probabilities sum to 100%; conditional recognition probabilities sum
to 100% within each business branch; all leaf probabilities also sum to 100%.
Do not multiply unconditional business and liquidity weights as if independent.
Use the same horizon, currency, share basis, and distribution assumptions at
the leaves. Include material funding, dilution, distress, and negative-surprise
outcomes, as well as a credible path that defeats the preferred thesis.

Assign provisional probabilities from base rates, current attributable evidence,
and explicit judgment. Separate the probability of an operating event from the
probability it is recognized by H. Correlated inputs do not create additional
independent confidence. Where observations support only ranges, show probability
and price sensitivity; do not label judgment weights empirically calibrated.

Each leaf should connect operating drivers to cash flow/value and explain its
market-price bridge. Forward multiples may be a cross-check or a market pricing
convention if period-aligned and supported by comparable states; they are not
an unexplained target-setting shortcut. Explain changing discount/duration or
recognition assumptions. Keep near-event pricing distinct from twelve-month
valuation and from long-term intrinsic value. Do not lower intrinsic cash-flow
value solely because near-term flows are weak, or attach an arbitrary optimism
premium to a desired price. If the price bridge is unidentified, return a
conditional range/readiness limit rather than a precise price.

If a compact three-row target table is used, explain how recognition leaves
were aggregated. Preserve the unfavorable recognition branch; a conditional
average target can conceal a material probability of losing money.

## Entry and exit regions depend on both price and state

Use a return hurdle appropriate to the stated horizon, sourced opportunity cost,
loss tolerance, and investor mandate where available. An assumed hurdle is a
research assumption, not personal suitability or a risk-approved limit.

For an unlevered cash equity evaluated at candidate entry P in observable state z:

    expected net return(P,z,H)
      = sum over leaves [q(leaf | z,P) * (price(H,leaf) + cash distributions(leaf))]
        / P - 1 - estimated round-trip cost as a fraction of P

State tax and FX treatment and avoid double-counting distributions. For other
instruments use their actual payoff mechanics. Compare both the expected
return and the distribution of losses, uncertainty, and funding/path constraints.
Fixed weights, costs, and distributions produce only a local illustrative entry
ceiling. If price or new information changes expectations, re-estimate the tree;
do not mechanically extend that ceiling across a changed market state.

- Buy/add: an entry region where remaining expectation upside and the return
  distribution are attractive given the required observations and loss exposure.
  It may be above central intrinsic value, but must explain the rerating/estimate
  path, possible reversal, and dependence on new buyers or financing.
- Wait/avoid: cheapness can coexist with negative revisions, financing stress,
  already exhausted catalysts, or an unfavorable allocation/recognition path.
  Distinguish evidence against an entry from simply missing evidence.
- Hold versus reduce/sell: evaluate prospective returns from today's price,
  remaining catalyst inventory, thesis change, alternatives, taxes/costs and
  available portfolio context. Do not anchor the decision to the purchase price
  or automatically sell at a historical valuation multiple. A sell/trim region
  for an existing holder is not authority or a recommendation to open a short.

Specify price condition, observable state, horizon/event window, falsifier,
review date/trigger, and the decisive missing input. An entry region can be
empty even at a large valuation discount. A strong expected return alone is
insufficient if the loss/uncertainty profile fails the stated constraints.
Avoid translating a required observation into an untested universal rule that
all buys must follow technical confirmation. Consider pre-event entry, waiting,
and abstaining where each is a realistic choice.

## Update without rewriting history

Freeze the pre-event expectation and scenario. Compare the actual operating
result, forward guidance/revisions, and relative price/volume reaction with it.
Unexpected weakness can reflect a higher whisper, discount-rate shock, supply,
or event contamination; it does not prove one explanation by itself. Update
the affected branch and say what else would discriminate among explanations.

Record what was observable at the original decision date versus learned later.
Later ARR charts, model comparisons, or holdings disclosures may improve the
next hypothesis but cannot validate an earlier information set retrospectively.
Evaluate scenario probability and process separately from a single realized
return. Over multiple resolved cases, assess calibration and price-range
coverage before claiming the method adds predictive skill.
