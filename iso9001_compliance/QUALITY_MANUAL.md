# Software Quality Management System (QMS) Manual: CMC-Alpha-Terminal
## Conforming to ISO/DIS 9001:2026 (Draft International Standard)

---

### 1. Scope & Application
This Quality Manual establishes the Software Quality Management System (QMS) policies, procedures, and deterministic controls implemented across the `cmc-alpha-terminal` repository. It formalizes quality engineering practices for high-assurance market data ingestion, Parkinson volatility estimation, Welford statistical accumulation, cross-sectional ranking, and FastMCP agent tool interfaces under **ISO/DIS 9001:2026**.

---

### 2. Clause 4: Context of the Organization & Digital Infrastructure
- **4.1 Organizational Context & Computing Architecture:** The quantitative engine operates natively on Apple Silicon ARM64 architecture (Darwin macOS), compiled using C++20 (`-std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror`) with zero dynamic heap allocations on quantitative calculation paths.
- **4.2 Stakeholder Expectations:** Market participants, algorithmic agents, and hackathon evaluators require zero unhandled exceptions, sub-microsecond algorithmic throughput, resilient API fallback on rate-limits, and mathematical numerical stability.
- **4.3 Scope of the QMS:** Encompasses all C++20 core execution kernels (`ParkinsonEstimator`, `WelfordAccumulator`, `CrossSectionalRanker`, `MonotonicExtremaDeque`, `FixedString`), Python client and FastMCP server tools (`cmc_terminal.server`, `cmc_terminal.client`), and the interactive terminal dashboard (`cmc_terminal.tui`).
- **4.4 QMS and Automated Verification:** Quality gates are codified in [`Makefile`](file:///Users/ishantpanchal/cmc-alpha-terminal/Makefile), orchestrating C++ unit tests, Python FastMCP integration tests, LLVM AddressSanitizer/UBSan runtime memory validation, static AST safety invariant analysis, and automated QMS clause audits.

---

### 3. Clause 5: Leadership & Quality Culture
- **5.1 Leadership & Commitment:** Engineering governance strictly enforces a **Zero Completion Claims Without Verification** policy. No software release or submission milestone is recognized without fresh, reproducible terminal verification proving 100% green test passes.
- **5.2 Quality Policy:** The project commits to zero dynamic heap allocations on the hot path, compile-time static asserts, strict input validation against NaN/Inf values, and deterministic $O(1)$ algorithmic complexities.
- **5.3 Organizational Roles & Responsibilities:** Automated static AST analyzers, compiler memory sanitizers, and regression test suites serve as non-discretionary gating mechanisms.

---

### 4. Clause 6: Planning & Risk-Based Thinking
- **6.1 Actions to Address Risks & Opportunities:** The QMS maintains an active [`RISK_REGISTER.md`](file:///Users/ishantpanchal/cmc-alpha-terminal/iso9001_compliance/RISK_REGISTER.md) evaluating failure modes including API rate-limit throttling (HTTP 429), floating-point zero division, circular queue boundary underflows, and NaN propagation.
- **6.2 Quality Objectives:**
  - *Numerical Stability:* Zero NaN or Inf propagation across Parkinson volatility calculations and Welford running variance accumulators.
  - *Memory Safety:* 0 memory leaks, 0 buffer overruns, and 0 undefined behavior verified under AddressSanitizer and UndefinedBehaviorSanitizer.
  - *Algorithmic Complexity:* Strict $O(1)$ amortized sliding-window extrema tracking via monotonic deques and $O(N \log N)$ bounded in-place cross-sectional ranking.
  - *Power of 10 Invariants:* 100% compliance with Gerard J. Holzmann's safety-critical coding standards (functions $\le 60$ lines, assertion density $\ge 2$).

---

### 5. Clause 7: Support & Tool Qualification
- **7.1 Resources & Qualified Compilers:**
  - C++ Compiler: Clang++ with C++20 support (`-std=c++20`).
  - Runtime Sanitizers: LLVM AddressSanitizer (`-fsanitize=address`) & UndefinedBehaviorSanitizer (`-fsanitize=undefined`).
  - Python Environment: Python 3.12+ with pytest, anyio, and FastMCP.
  - Static AST Analyzers: Automated Python AST inspection script validating Power of 10 safety invariants.
- **7.2 Competence & Training:** Comprehensive technical documentation, architecture specifications, and API usage guides maintained in [`README.md`](file:///Users/ishantpanchal/cmc-alpha-terminal/README.md) and [`DORAHACKS_SUBMISSION.md`](file:///Users/ishantpanchal/cmc-alpha-terminal/DORAHACKS_SUBMISSION.md).
- **7.5 Documented Information:** Test run logs, sanitizer traces, and machine-readable audit artifacts are retained in `target/iso9001_audit_report.json`.

---

### 6. Clause 8: Operational Planning and Control (Software V&V)
- **8.1 Verification and Validation Protocol:**
  - *Verification (Unit & Whitebox):* Mathematical verification of Parkinson variance scale factor ($1 / (4 \ln 2)$), Welford recurrence relations, and cross-sectional percentile distributions in `tests/cpp/test_engine.cpp`.
  - *Validation (Sanitizers):* ASan/UBSan execution (`make asan`) verifying clean heap and pointer integrity.
  - *Integration (FastMCP & TUI):* Automated testing of MCP tool dispatch, parameter validation, offline mock fallback, and terminal rendering in `tests/test_server.py`, `tests/test_client.py`, and `tests/test_tui.py`.
- **8.7 Control of Non-conforming Outputs:** Any assertion panic, sanitizer alert, or invariant violation halts compilation and blocks pull requests immediately.

---

### 7. Clause 9: Performance Evaluation
- **9.1 Monitoring & Measurement:** Continuous benchmarking of C++ calculation latency and Python FastMCP request round-trip times.
- **9.2 Internal Audit:** Automated static and structural compliance verification executed via [`scripts/audit_iso9001_compliance.py`](file:///Users/ishantpanchal/cmc-alpha-terminal/scripts/audit_iso9001_compliance.py).
- **9.3 Safety Auditing:** AST invariant checker [`scripts/audit_safety_invariants.py`](file:///Users/ishantpanchal/cmc-alpha-terminal/scripts/audit_safety_invariants.py) auditing all C++ source files.

---

### 8. Clause 10: Continual Improvement
- **10.1 Non-conformity and Corrective Action:** Defect identification triggers root cause analysis and immediate test case codification in `tests/`.
- **10.2 Continual Improvement Cycle:** Regular profiling, offline mock dataset expansion, and deterministic code refinement to maintain mission-critical reliability.
