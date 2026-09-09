#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <chrono>
#include <array>
#include "types.hpp"
#include "welford.hpp"
#include "monotonic_deque.hpp"
#include "parkinson_vol.hpp"
#include "ranker.hpp"

// Curated top institutional benchmark assets
struct AssetFeed {
    const char* symbol;
    double price;
    double high_24h;
    double low_24h;
    double volume_24h;
    double change_24h;
};

static const AssetFeed BENCHMARK_UNIVERSE[] = {
    {"BTC",  64250.0, 65100.0, 63800.0, 28500000000.0,  1.85},
    {"ETH",   3480.0,  3550.0,  3420.0, 14200000000.0,  2.40},
    {"SOL",    148.5,   154.2,   144.1,  4800000000.0,  5.10},
    {"BNB",    585.0,   592.0,   578.0,  1100000000.0,  0.75},
    {"XRP",      0.58,    0.60,    0.57,  1350000000.0, -0.40},
    {"DOGE",     0.115,   0.122,   0.111,  850000000.0,  3.20},
    {"ADA",      0.36,    0.375,   0.352,  340000000.0,  1.10},
    {"AVAX",    26.4,    27.8,    25.9,   410000000.0,  4.30},
    {"LINK",    11.8,    12.4,    11.5,   290000000.0,  3.80},
    {"NEAR",     4.55,    4.82,    4.41,   380000000.0,  6.20}
};

static constexpr std::size_t UNIVERSE_SIZE = sizeof(BENCHMARK_UNIVERSE) / sizeof(BENCHMARK_UNIVERSE[0]);

static void print_header() noexcept {
    assert(UNIVERSE_SIZE > 0);
    assert(BENCHMARK_UNIVERSE != nullptr);
    std::cout << "\n========================================================================================\n";
    std::cout << "                 CMC-ALPHA-TERMINAL: C++20 QUANTITATIVE CORE ENGINE                     \n";
    std::cout << "        Zero-Heap High-Frequency Regime Classifier & Cross-Sectional Alpha Ranker        \n";
    std::cout << "========================================================================================\n";
    std::cout << std::left 
              << std::setw(8)  << "Symbol" 
              << std::setw(12) << "Price ($)" 
              << std::setw(12) << "24h Chg (%)" 
              << std::setw(14) << "Parkinson Vol" 
              << std::setw(14) << "Alpha Score" 
              << std::setw(16) << "Percentile Rank" 
              << std::setw(12) << "Regime" << "\n";
    std::cout << "----------------------------------------------------------------------------------------\n";
}

struct AssetAnalysis {
    double vol{0.0};
    double rank{0.0};
    const char* regime{""};
};

// Pure computation: ranking + volatility classification, with zero I/O, so
// the surrounding timer measures inference cost only, not terminal output.
static std::array<AssetAnalysis, UNIVERSE_SIZE> compute_analysis() noexcept {
    assert(UNIVERSE_SIZE > 0);
    assert(UNIVERSE_SIZE <= 64);

    cmc::WelfordAccumulator return_stats;
    cmc::CrossSectionalRanker<64> ranker;
    for (std::size_t i = 0; i < UNIVERSE_SIZE; ++i) {
        assert(BENCHMARK_UNIVERSE[i].price > 0.0);
        assert(BENCHMARK_UNIVERSE[i].symbol != nullptr);
        ranker.add_asset(BENCHMARK_UNIVERSE[i].symbol, BENCHMARK_UNIVERSE[i].change_24h);
        return_stats.update(BENCHMARK_UNIVERSE[i].change_24h);
    }
    ranker.compute_ranks();
    assert(return_stats.count() == UNIVERSE_SIZE);

    std::array<AssetAnalysis, UNIVERSE_SIZE> results{};
    for (std::size_t i = 0; i < UNIVERSE_SIZE; ++i) {
        const auto& item = BENCHMARK_UNIVERSE[i];
        assert(item.high_24h >= item.low_24h);

        // Track rolling high/low extrema via MonotonicExtremaDeque
        cmc::MonotonicExtremaDeque<double, 4> extrema;
        extrema.push(item.low_24h);
        extrema.push(item.price);
        extrema.push(item.high_24h);
        const double rolling_high = extrema.max();
        const double rolling_low = extrema.min();
        assert(rolling_high >= rolling_low);

        cmc::ParkinsonEstimator<4> p_vol;
        p_vol.update(rolling_high, rolling_low);
        double vol = p_vol.realized_volatility();
        double rank = ranker.get_percentile(item.symbol);
        const char* regime = (vol > 0.035) ? "VOLATILE" : (item.change_24h > 3.0 ? "TRENDING" : "COMPRESS");
        results[i] = {vol, rank, regime};
    }
    assert(results.size() == UNIVERSE_SIZE);
    return results;
}


static void print_analysis(const std::array<AssetAnalysis, UNIVERSE_SIZE>& results, double elapsed_us) noexcept {
    assert(elapsed_us >= 0.0);
    assert(results.size() == UNIVERSE_SIZE);

    for (std::size_t i = 0; i < UNIVERSE_SIZE; ++i) {
        const auto& item = BENCHMARK_UNIVERSE[i];
        const auto& r = results[i];
        assert(r.regime != nullptr);
        std::cout << std::left
                  << std::setw(8)  << item.symbol
                  << std::setw(12) << std::fixed << std::setprecision(2) << item.price
                  << std::setw(12) << std::showpos << item.change_24h << std::noshowpos
                  << std::setw(14) << std::setprecision(4) << r.vol
                  << std::setw(14) << std::setprecision(2) << item.change_24h
                  << std::setw(16) << std::setprecision(2) << r.rank
                  << std::setw(12) << r.regime << "\n";
    }
    std::cout << "========================================================================================\n";
    std::cout << "[EXECUTION ENGINE: ZERO HEAP ALLOCATIONS | MEASURED INFERENCE LATENCY: "
               << std::fixed << std::setprecision(2) << elapsed_us
               << " microseconds for " << UNIVERSE_SIZE << " assets]\n\n";
}

static void analyze_universe() noexcept {
    const auto start = std::chrono::steady_clock::now();
    const auto results = compute_analysis();
    const auto end = std::chrono::steady_clock::now();
    assert(end >= start);

    const double elapsed_us = std::chrono::duration<double, std::micro>(end - start).count();
    assert(elapsed_us >= 0.0);

    print_analysis(results, elapsed_us);
}

int main(int argc, char* argv[]) {
    assert(argc >= 1);
    assert(argv != nullptr);
    (void)argv;
    print_header();
    analyze_universe();
    return 0;
}
