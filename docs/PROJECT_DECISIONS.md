# Project decisions and analytical judgement

This file records decisions that materially affect interpretation.

## 1. Use broad sectors rather than force detailed mappings

Only sectors with defensible coverage across production, output PPI and energy intensity are retained in the main panel. C23 is not forced into the two-outcome model.

**Reason:** classification consistency is more important than maximising the number of sectors.

## 2. Freeze exposure before the main energy crisis

Energy intensity is averaged over 2018–2020 and then held fixed.

**Reason:** the exposure measure should not mechanically incorporate later behavioural responses to the shock being studied.

## 3. Log-transform and standardise energy intensity

The cross-sector exposure distribution is strongly skewed because C13 textiles is extreme relative to the other matched sectors.

**Reason:** the log scale limits leverage without deleting the observation. Raw-z and winsorised-log versions remain in the robustness suite.

## 4. Use All Fuels as the primary common price shock

A fuel-share-weighted sector index was considered but the required historical sector/fuel weights were not safely recoverable from the source interface used in the project.

**Reason:** a simpler measured variable is preferable to an apparently sophisticated variable built from guessed inputs. Gas and electricity shocks remain separate robustness checks.

## 5. Use two-way fixed effects

Sector fixed effects absorb time-invariant sector characteristics; quarter fixed effects absorb shocks common to all sectors.

**Reason:** the coefficient is intended to represent a differential exposure-response relationship, not the aggregate effect of the national energy-price series.

## 6. Use Driscoll–Kraay as primary inference

The output specification shows strong heteroskedasticity and cross-sectional dependence.

**Reason:** a common covariance estimator robust to these panel-error features is more defensible than choosing the smallest p-value across alternatives.

## 7. Treat C13 sensitivity as a result, not a nuisance

Removing C13 reverses the producer-price coefficient.

**Reason:** with only seven sectors, influential observations must be visible. The full-sample coefficient is therefore described as fragile rather than presented as a stable pass-through finding.

## 8. Avoid causal language

The analysis is based on public sector-level panel data and does not have a strong quasi-experimental identification design.

**Reason:** conclusions use terms such as “associated with”, “differential response” and “exposure relationship”.
