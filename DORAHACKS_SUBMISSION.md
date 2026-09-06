# DoraHacks BUIDL Submission Package

**Hackathon:** CoinMarketCap: Build with CMC: API Hackathon (Prize: CMC Pro-API 1-Year Grant + Ecosystem Support for Top 3 Projects)  
**Project Name:** CMC-Alpha-Terminal  
**DoraHacks BUIDL:** https://dorahacks.io/buidl/48301  
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
- **Tests Passing:** 21/21 (4 C++20 + 17 Python FastMCP tests)
- **Compiler Invariants:** `-std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror` (Zero warnings on Apple Silicon ARM64 & Linux)
- **Dual-Mode FastMCP Server:** Returns programmatic typed dictionaries for autonomous agent tool-chaining alongside formatted markdown for LLM chat display.
- **Latency:** Sub-microsecond C++ inference; $< 50$ ms MCP tool dispatch.
- **Offline Mode:** 100% reproducible for judges without live API keys.

---

## 5. Visual Walkthrough & Demo Commands

- **Visual Terminal Demo:** [`assets/cmc_terminal_demo.gif`](https://raw.githubusercontent.com/Ishant5436/cmc-alpha-terminal/main/assets/cmc_terminal_demo.gif)
- **Video Walkthrough:** [`assets/cmc_terminal_demo.mp4`](https://github.com/Ishant5436/cmc-alpha-terminal/raw/main/assets/cmc_terminal_demo.mp4)

```bash
# 1. Clone & Run Complete Test Suite (21/21 Passing)
git clone https://github.com/Ishant5436/cmc-alpha-terminal.git
cd cmc-alpha-terminal
make test

# 2. Launch Interactive Terminal Demo (Offline Mock Engine)
make demo
```

### Claude Desktop / Claude Code Integration
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "cmc-alpha-terminal": {
      "command": "python3",
      "args": ["-m", "cmc_terminal.server"],
      "cwd": "/path/to/cmc-alpha-terminal",
      "env": {
        "CMC_PRO_API_KEY": "<OPTIONAL_LIVE_KEY>"
      }
    }
  }
}
```

