# DoraHacks BUIDL Submission Package

**Hackathon:** CoinMarketCap: Build with CMC: API Hackathon (Prize: CMC Pro-API 1-Year Grant + Ecosystem Support for Top 3 Projects)  
**Project Name:** CMC-Alpha-Terminal  
**Track:** Developer Tooling / Trading Intelligence / AI Agent Infrastructure  
**Author / Hacker:** Ishant Panchal (`@Ishant5436` / `ishant.p@somaiya.edu`)  
**Repository:** https://github.com/Ishant5436/cmc-alpha-terminal  

---

## 1. Project Tagline
An institutional-grade, zero-heap quantitative screening engine and FastMCP agent gateway powered by the CoinMarketCap Pro API.

---

## 2. Problem Statement
Autonomous AI agents and quantitative execution bots need sub-millisecond market regime classification, liquidity depth auditing, and cross-sectional factor ranking across the global cryptocurrency universe. Existing tools are either slow Python notebooks with GC latency pauses or black-box visual charts with zero programmable API interfaces for autonomous LLM agents (Claude / Gemini).

---

## 3. The Solution
`CMC-Alpha-Terminal` combines:
1. **Deterministic C++20 Core:** Zero-heap Welford variance tracking, monotonic lookback extrema deques, and Parkinson realized volatility kernels adhering strictly to Deterministic Safety Invariants (Power of 10).
2. **CoinMarketCap Pro API Ingestion:** Real-time `/cryptocurrency/listings/latest`, `/quotes/latest`, and `/global-metrics/quotes/latest` ingestion with offline snapshot replay for reproducible evaluation.
3. **FastMCP Server for AI Agents:** 5 production MCP tools enabling LLMs to screen momentum, detect volatility regimes, audit liquidity depth, and generate execution directives (`LONG`, `HOLD`, `AVOID`).
4. **Interactive ANSI Terminal Dashboard:** Real-time ASCII terminal monitor launchable via `make demo`.

---

## 4. Technical Metrics
- **Tests Passing:** 19/19 (4 C++20 + 15 Python FastMCP tests)
- **Compiler Invariants:** `-std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror` (Zero warnings on Apple Silicon ARM64 & Linux)
- **Latency:** Sub-microsecond C++ inference; $< 50$ ms MCP tool dispatch.
- **Offline Mode:** 100% reproducible for judges without live API keys.
