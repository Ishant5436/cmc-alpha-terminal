# Software Quality Risk Register (FMEA Matrix): CMC-Alpha-Terminal
## Conforming to ISO/DIS 9001:2026 Clause 6 (Risk-Based Thinking)

This document tracks identified operational risks, mathematical failure modes, and automated mitigations for the `cmc-alpha-terminal` system.

---

## 1. Risk Evaluation Scale
- **Severity (S):** 1 (Negligible) to 5 (Catastrophic calculation error / memory corruption)
- **Likelihood (L):** 1 (Extremely Rare) to 5 (Frequent without controls)
- **Risk Priority Number (RPN):** $S \times L$ (Scale 1 to 25). RPN $\ge 12$ mandates automated gating.

---

## 2. Failure Modes and Effects Analysis (FMEA)

| Risk ID | Potential Failure Mode | Impact / Effect | Severity (S) | Likelihood (L) | Initial RPN | Automated Mitigation & Quality Control | Residual RPN |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RSK-CMC-01** | Zero-price or inverted candle ($high < low$) in Parkinson Volatility | Mathematical domain error, negative variance or NaN | 5 | 3 | **15** | Pre-condition assertions (`assert(high >= low)`, `assert(low > 0.0)`); verified in `test_parkinson_volatility_math` & `test_engine.cpp` | **2** (S=2, L=1) |
| **RSK-CMC-02** | Heap fragmentation or allocation latency on hot calculation path | Calculation stalls, degraded throughput, non-deterministic latency | 4 | 4 | **16** | Rule 3 Invariant: Zero `malloc`/`new` on hot path; fixed-capacity stack arrays; verified via `scripts/audit_safety_invariants.py` | **2** (S=2, L=1) |
| **RSK-CMC-03** | Upstream CoinMarketCap API rate limit (HTTP 429) or network disconnect | FastMCP tool failure, agent workflow interruption | 4 | 4 | **16** | Resilient offline mock fallback dataset (`cmc_terminal.sample_data`); verified in `test_client_offline_listings` & `test_client_offline_global_metrics` | **2** (S=2, L=1) |
| **RSK-CMC-04** | Empty asset array or single asset in cross-sectional ranker | Division-by-zero during percentile normalization | 4 | 3 | **12** | Explicit count guards (`if (count_ == 0) return; if (count_ == 1) items_[0].percentile = 0.5;`); verified in `test_engine.cpp` | **1** (S=1, L=1) |
| **RSK-CMC-05** | Monotonic extrema deque sliding window index wrap / boundary fault | Memory out-of-bounds access, corrupted price channel bounds | 5 | 3 | **15** | Compile-time capacity limits, static asserts, assertion density $\ge 2$; verified in `test_engine.cpp` | **2** (S=2, L=1) |
| **RSK-CMC-06** | Upstream API returning `None` or null values in market metrics | Python FastMCP server unhandled `TypeError` crash | 4 | 3 | **12** | Defensive type coercion, fallback defaults (`val or 0.0`), schema validation; verified in `test_mcp_none_value_resilience` | **2** (S=2, L=1) |
| **RSK-CMC-07** | Floating-point cancellation in running variance calculation | Negative variance or catastrophic precision loss | 4 | 3 | **12** | Welford single-pass recurrence algorithm with numerical stability bounds; verified in `test_engine.cpp` | **2** (S=2, L=1) |

---

## 3. Review & Verification Frequency
Audited continuously by the automated quality pipeline (`make audit-iso9001`) and static AST analyzers.
