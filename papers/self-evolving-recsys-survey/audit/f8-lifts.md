# F8: broad-metric online lifts, loop by loop

The F8 range in the paper (17 loops report an online lift on a broad metric, not summed over launches, from +0.052% to +4.86%; earlier drafts stated this as "all below 5%", kept as the last column) was
made by hand from the `headline_gain` field of `design.csv`. This list gives the lift counted for each loop so the count
can be checked. Of the 19 core loops with an online experiment, GEARS is left out: it reports per-surface online lifts (Table 3, Metric 1 from +0.011% to +0.14% over seven surfaces), but its metrics are anonymised as "Metric 1-3", so whether any is broad cannot be told. Counted, it would lower the range's floor to +0.011% and leave every lift below 5%.
Broad metrics are watch time, engagement, sessions, orders, revenue, GMV and similar whole-product measures. Where a
paper reports a fresh confirmation, that figure is counted; otherwise the paper's reported figure, which for A/B Agent is a selecting round (F9). For Sortify
the confirmed second-market figure is counted, not the first market's selecting-round +9.2%. Coded by one author.

| Loop | Lift counted | Below 5% |
|---|---|---|
| RecHarness | ADVV +2.084% (7-day A/B) | yes |
| Google/YouTube | +0.06% YouTube-level (Gated Path; largest +1.10% surface-level, Wide&Deep) | yes |
| EvoRec | revenue +1.85% | yes |
| NOVA | GMV +1.25% / +1.70% / +2.02% | yes |
| AgentX | app time +0.561% | yes |
| AgentX-Model | watch time +0.3–0.8% (10–15% acquisition efficiency is a narrower metric) | yes |
| AutoLR | only lifts summed over nine launches (+5.75% penetration, +10.83% consumption time, +5.55% VV) | no single lift |
| CORAL | sessions +0.16%, watch time +0.15% | yes |
| AgenticRecTune | engagement +0.75% / +0.90% | yes |
| Sortify | GMV/UU +4.15% (confirmed, Country B; not the selecting round's +9.2%) | yes |
| RecEvolve | user satisfaction +3.77% | yes |
| Astar | GMV +4.86% | yes |
| SR-Agent | orders +0.71% | yes |
| Trajectories-to-Evidence | page duration +0.75% (user-growth net utility +6.34% is a narrower metric) | yes |
| EvoPilot | GSRR +0.66% | yes |
| PILOT | up to +1.60% Core IPV, +1.50% transaction amount (a non-randomised before/after comparison of the best of five buckets, F9) | yes |
| A/B Agent | GMV +4.829% (the selecting round) | yes |
| DMRL | LTV +0.052% | yes |

All 17 loops that report a single broad-metric lift report one below 5%, from +0.052% (DMRL) to +4.86% (Astar); AutoLR reports no single lift. Six loops list several values or an "up to" figure (Google/YouTube, NOVA, AgentX-Model, CORAL, AgenticRecTune, PILOT); every value listed for them lies inside +0.052% to +4.86%. DMRL's +0.052% is its main-table value (Tables 2 and 5); the same full configuration appears in four other tables, run in non-overlapping time windows, at +0.042%, +0.021%, +0.064% and +0.050%, so taking DMRL's lowest value would move the lower end to +0.021% (the upper end, Astar's single value, is unaffected). PILOT's figure is not from a randomised experiment; without it the count is 16 and the range is unchanged. Whether a metric is broad is a judgement; the metric counted for each loop is named above.
