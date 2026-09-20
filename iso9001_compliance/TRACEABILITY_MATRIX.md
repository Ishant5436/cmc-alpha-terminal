# ISO/DIS 9001:2026 Bidirectional Traceability Matrix: CMC-Alpha-Terminal

This matrix establishes forward and backward traceability between quantitative analysis requirements, source implementation, test targets, and verified quality evidence.

---

## 1. Traceability Mapping

| Requirement ID | Requirement Specification | Test Case ID | Test Implementation | Target Source Component | Verifiable Evidence Artifact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-CMC-001** | High-precision Parkinson extreme value volatility estimator | `TC-VOL-01` | [`test_engine.cpp`](file:///Users/ishantpanchal/cmc-alpha-terminal/tests/cpp/test_engine.cpp) | [`parkinson_vol.hpp`](file:///Users/ishantpanchal/cmc-alpha-terminal/include/parkinson_vol.hpp) | `bin/test_engine` console log |
| **REQ-CMC-002** | Numerically stable Welford online mean and variance accumulator | `TC-WF-01` | [`test_engine.cpp`](file:///Users/ishantpanchal/cmc-alpha-terminal/tests/cpp/test_engine.cpp) | [`welford.hpp`](file:///Users/ishantpanchal/cmc-alpha-terminal/include/welford.hpp) | `bin/test_engine` console log |
| **REQ-CMC-003** | In-place cross-sectional ranker with percentile transformation | `TC-RNK-01` | [`test_engine.cpp`](file:///Users/ishantpanchal/cmc-alpha-terminal/tests/cpp/test_engine.cpp) | [`ranker.hpp`](file:///Users/ishantpanchal/cmc-alpha-terminal/include/ranker.hpp) | `bin/test_engine` console log |
| **REQ-CMC-004** | Amortized $O(1)$ sliding-window monotonic extrema deque | `TC-DEQ-01` | [`test_engine.cpp`](file:///Users/ishantpanchal/cmc-alpha-terminal/tests/cpp/test_engine.cpp) | [`monotonic_deque.hpp`](file:///Users/ishantpanchal/cmc-alpha-terminal/include/monotonic_deque.hpp) | `bin/test_engine` console log |
| **REQ-CMC-005** | Zero-heap stack-allocated fixed-capacity string container | `TC-STR-01` | [`test_engine.cpp`](file:///Users/ishantpanchal/cmc-alpha-terminal/tests/cpp/test_engine.cpp) | [`types.hpp`](file:///Users/ishantpanchal/cmc-alpha-terminal/include/types.hpp) | `bin/test_engine` console log |
| **REQ-CMC-006** | AddressSanitizer and UndefinedBehaviorSanitizer zero leak guarantee | `TC-SAN-01` | `make asan` | All compiled binaries | ASan terminal report (0 leaks) |
| **REQ-CMC-007** | Strict Power of 10 safety invariant adherence (AST analyzer) | `TC-AST-01` | [`audit_safety_invariants.py`](file:///Users/ishantpanchal/cmc-alpha-terminal/scripts/audit_safety_invariants.py) | All C++ headers & sources | AST Invariant Analyzer log |
| **REQ-CMC-008** | Offline mock fallback resilience on CMC API disconnects | `TC-CLI-01` | [`test_client.py`](file:///Users/ishantpanchal/cmc-alpha-terminal/tests/test_client.py) | [`client.py`](file:///Users/ishantpanchal/cmc-alpha-terminal/python/cmc_terminal/client.py) | Pytest execution report |
| **REQ-CMC-009** | FastMCP multi-tool agent interface and parameter validation | `TC-MCP-01` | [`test_server.py`](file:///Users/ishantpanchal/cmc-alpha-terminal/tests/test_server.py) | [`server.py`](file:///Users/ishantpanchal/cmc-alpha-terminal/python/cmc_terminal/server.py) | Pytest execution report |
| **REQ-CMC-010** | Resilience against null or missing upstream API response fields | `TC-MCP-02` | [`test_server.py`](file:///Users/ishantpanchal/cmc-alpha-terminal/tests/test_server.py) | [`server.py`](file:///Users/ishantpanchal/cmc-alpha-terminal/python/cmc_terminal/server.py) | Pytest execution report |
| **REQ-CMC-011** | Interactive ANSI color and terminal dashboard rendering | `TC-TUI-01` | [`test_tui.py`](file:///Users/ishantpanchal/cmc-alpha-terminal/tests/test_tui.py) | [`tui.py`](file:///Users/ishantpanchal/cmc-alpha-terminal/python/cmc_terminal/tui.py) | Pytest execution report |

---

## 2. Verification Coverage
- **Total Tracked Requirements:** 11
- **Verification Coverage:** 100% (11/11 verified with automated tests)
- **Sanitizer & Safety Verification:** AddressSanitizer (0 leaks), UBSan (0 errors), AST Invariants (0 violations).
