# Monte Carlo trade analyzer

The MC Analyze panel sits below the candidates table on the Single
Ticker tab and below the spreads table on Spreads / Directional /
Neutral. Pick any candidate (single-leg or multi-leg), and the
panel simulates 10,000 random underlying-price paths and reports
the resulting P&L distribution.

The intent is **diagnostic**: see what the distribution of
outcomes actually looks like for this trade, under today's IV,
before you place it.

This doc explains what the panel shows, how to read each metric,
and where the simulation's assumptions are likely to mislead you.

## The 8 metrics

The metrics are split into two rows: **headline** (row 1) and
**quant-grade** (row 2).

### Headline (row 1)

**P(profit)** — fraction of simulated paths with positive terminal
P&L. A `60%` reading means 6 in 10 simulated outcomes finished in
the green. Read this *with* Expected P&L — a 70%-POP trade with
small wins and one catastrophic loss is worse than a 55%-POP trade
with symmetric payoffs.

**Expected P&L** — mean P&L across all simulated paths. Positive
expected value is necessary but not sufficient: a high-variance
positive-EV trade still ruins you if you size it wrong.

**CVaR (worst 5%)** — average P&L of the worst 5% of simulated
paths. This is what you'd lose *on average* in the bad tail, not
the threshold you cross. If CVaR is −$2,400 on a $3,000 max-loss
spread, the bad-tail outcomes consume most of the budget.

**Breakeven move** — the signed % move in the underlying needed to
land at zero P&L at horizon. `+8.5%` means the stock needs to rise
8.5% from spot. `—` means breakeven isn't crossed inside the
sampled spot range (either all paths win or all lose).

### Quant-grade (row 2)

**VaR (5%)** — the threshold loss exceeded in 5% of paths. By
construction, `VaR ≤ CVaR` — CVaR is the *average* in the tail,
VaR is the *entry* to the tail. Showing both lets you compare
"how common are losses worse than X?" against "how bad are they
on average?"

**Sortino** — expected P&L divided by downside-only standard
deviation. Sharpe-analog that punishes downside without penalizing
upside, which is the right ratio for options because option
payoffs are deliberately asymmetric. `∞` means no simulated path
lost money; `—` means the ratio is too extreme to display
meaningfully.

**MC fair value** — discounted mean of terminal payoffs (excluding
the position's open cost). This is *the simulation's* fair price
for the contract under today's IV. The shown ± stderr is the 1-σ
confidence interval on the estimate; at 10k paths with antithetic
variates it's typically tight enough to ignore.

**Premium vs model** — MC fair value minus your open cost. Positive
= the market priced this below the model's fair value (the trade
looks rich relative to the simulation). Negative = the market
priced above. **Diagnostic, not actionable** — the simulation is
one calibrated view, not market truth, and the same caveats from
[INTERPRETING_IV.md](INTERPRETING_IV.md) apply (vol smile, skew,
event risk, etc.).

## The two charts

**Sampled paths** — 200 randomly-drawn simulated price paths
overlaid, with reference lines for spot (at t=0), every leg's
strike, and the breakeven spot at horizon. Visual sanity check
for whether the GBM cone looks reasonable for this name — too
narrow on a recent-mover, too wide on a tight range-bound stock,
etc.

**P&L histogram** — terminal P&L across all 10k paths, with mean
and median rules and color sign (green positive, red negative).
The shape tells you the trade's character at a glance: a tall
narrow positive spike with a long thin negative tail is the
classic credit position; a wide flatter green-leaning hump with a
clipped tail is a debit spread.

## Tweak assumptions

The expander above the metrics holds four knobs. Defaults are
sensible — only touch them when you have a reason.

**Vol source** — `chain_iv` (default) uses each leg's
market-implied volatility, weighted by absolute leg quantity
across legs. `custom` lets you override with a hand-typed vol.
Switch to `custom` when you want to ask "what if realized vol is
higher/lower than the chain implies?"

**Custom vol** — annualized decimal (e.g. `0.45` = 45% vol/yr).
Disabled when vol source is `chain_iv`.

**Paths** — `1k / 5k / 10k / 25k`. 10k is the default sweet spot:
sub-second runtime and ~1% stderr on `P(profit)`. Bump to 25k for
tighter confidence intervals when the position has a wide tail.

**Earnings jumps** — checkbox. When on, the simulation applies a
log-normal jump on any earnings date inside the position's
window. The jump σ is calibrated from the position's IV (or a
market straddle-implied move when one is supplied — this UI
doesn't currently expose that input). Useful for any position
straddling an earnings event. Turn it off if you're comparing
structures across the event-free part of the year and want
apples-to-apples.

**Drift premium above risk-free** — slider, default 0%. The
risk-neutral default (drift = risk-free rate) is the right choice
for pricing. Bias it positive if you want to model your own
directional thesis (e.g. +8%/yr expected return above the
risk-free); bias it negative for the inverse. Affects Expected
P&L and Breakeven move heavily — use with caution.

## Market View card (Single Ticker tab)

Above the candidates table, a small accented card translates your
(Direction × Option Type) selection into a one-line stance and a
list of representative strategies:

| Direction | Option Type | Stance |
|---|---|---|
| Sell | Calls | Bearish / neutral-down |
| Sell | Puts  | Bullish / neutral-up |
| Sell | Both  | Range-bound (short volatility) |
| Buy  | Calls | Bullish |
| Buy  | Puts  | Bearish |
| Buy  | Both  | Volatility expansion (long vol) |

Color codes the tone — green for premium income, red for
directional, amber for range-bound, purple for vol expansion.
Helps confirm you're scanning the right corner of the chain for
your view.

## Recommended Action card (Portfolio tab)

For each position in your uploaded CSV, the Portfolio tab renders
an action card *above* the candidates table. It picks the same
rank-1 IV-rich call the table picks, then translates it into
explicit instructions:

- **ROLL existing covered call** — when there's an open short
  call. Shows the buy-to-close + sell-to-open net credit (or
  debit), and the new stock breakeven below which the roll cost
  you net.
- **SELL TO OPEN covered call** — when you hold ≥100 shares with
  no open call. Auto-sizes contracts to `shares // 100`, shows
  total premium collected, max profit if called away, the
  delta-based assignment probability, and the stock breakeven.
- **Stock position too small for covered call** — when you hold
  <100 shares. Renders in amber and explicitly says "not
  actionable" rather than misleading you with a partial figure.

The IV+pp magnitude of the underlying pick appears in the card's
small label ("top IV+pp signal (+5.3 pp)") so you can sanity-check
whether the recommendation is leaning on real signal or noise —
apply the magnitude heuristics from
[INTERPRETING_IV.md](INTERPRETING_IV.md).

## Engine assumptions

The model is **Geometric Brownian Motion** (the same family
Black-Scholes uses):

```
S(t+dt) = S(t) · exp((μ − ½σ²) dt + σ √dt · Z)
```

with **Merton-style log-normal jumps** added on each earnings date
inside the position's window. Variance reduction via **antithetic
variates** — for every shock `Z`, the simulation also uses `−Z`,
halving the effective sample variance for free.

**Why GBM and not Heston / local vol** — at retail timescales
(days to a few months) the marginal accuracy gain of stochastic-
vol models is on the order of 1% of the metrics, at ~10× compute
cost. Calibration is also fragile. GBM keeps the engine cheap,
easy to reason about, and consistent with the Black-Scholes
assumption the scanner's IV surface already uses.

**Why no American exercise** — retail option holders typically
roll or close before deep-ITM early exercise becomes optimal, so
European exercise is the right default for the panel's
"if held to horizon" framing.

**Multi-leg handling** — all legs share one simulation. The
position's terminal payoff is the sum of per-leg intrinsic values
at horizon, netted against each leg's open cost. No special case
for verticals vs. condors vs. PMCC vs. anything else — the engine
treats them uniformly.

## What this is not

- **Not a fair-value claim.** The MC fair value is what the
  simulation says under today's IV. The market's price is also "a
  fair value" — under different assumptions about jumps, skew,
  and realized vol. Don't read a positive "Premium vs model" as
  tradeable edge.
- **Not a probabilistic forecast.** P(profit) is the fraction of
  *simulated* paths that profit, under GBM plus earnings jumps.
  Real return distributions have fatter tails than log-normal.
  Read it as "if reality looked like the model, this is the
  fraction…" not "this is the chance the trade works".
- **Not predictive of realized vol.** The simulation uses today's
  IV as a proxy for future realized vol. If realized vol exceeds
  implied, long positions outperform the simulation; if realized
  falls short, short positions outperform. The panel isn't
  trying to forecast that gap.
- **Not a recommendation.** Like the IV+pp ranking, treat the MC
  output as one data point in your own analysis, not a trade
  signal.

## When the simulation lies most

- **Around binary events** (FDA decisions, takeover votes,
  earnings with thin straddle data). GBM plus a log-normal jump
  can't represent a true bimodal outcome.
- **On thin or stale chains.** If a leg's IV came from a stale
  quote, the simulation inherits that staleness, usually as an
  over- or under-stated cone width.
- **At long horizons (>180 DTE).** GBM's log-normal assumption
  drifts further from reality as the horizon grows; the cone
  widens faster than realized distributions typically do.
- **For deep-ITM short legs.** American-style early exercise risk
  isn't modeled. The simulation under-estimates dealer-hedging-
  driven roll pressure on those positions.

If any of these apply to a candidate you're looking at, treat the
panel's numbers as suggestive rather than precise.

## Reproducibility

Each run uses a fresh RNG seed unless one is passed into
`SimulationConfig.seed` (UI doesn't expose this; CLI / notebook
use can pin it). Results across runs vary within the stderr
window shown on MC fair value.

The cache key is the tuple `(position, config)`. Re-expanding the
same selection re-renders instantly — no re-simulation. Changing
any tweak knob (or selecting a different row) invalidates the
cache and triggers a fresh run.
