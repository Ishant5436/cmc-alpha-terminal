#include <iostream>
#include <cassert>
#include <cmath>
#include <cstring>
#include "types.hpp"
#include "welford.hpp"
#include "monotonic_deque.hpp"
#include "parkinson_vol.hpp"
#include "ranker.hpp"

// Test 1: Welford streaming accumulator numerical stability
void test_welford_accumulator() {
    cmc::WelfordAccumulator acc;
    assert(acc.count() == 0);
    assert(std::isnan(acc.mean()) || acc.mean() == 0.0);

    // Feed values: 10, 20, 30
    acc.update(10.0);
    acc.update(20.0);
    acc.update(30.0);

    assert(acc.count() == 3);
    assert(std::abs(acc.mean() - 20.0) < 1e-9);
    assert(std::abs(acc.sample_variance() - 100.0) < 1e-9);
    assert(std::abs(acc.sample_stddev() - 10.0) < 1e-9);
    std::cout << "[PASS] Welford Accumulator numerical invariants verified.\n";
}

// Test 2: Monotonic Deque O(1) Sliding Window Extrema
void test_monotonic_deque() {
    cmc::MonotonicExtremaDeque<double, 4> deque;
    assert(deque.empty());

    // Window size 4
    deque.push(10.0);
    deque.push(25.0);
    deque.push(15.0);
    deque.push(5.0);

    assert(deque.size() == 4);
    assert(std::abs(deque.max() - 25.0) < 1e-9);
    assert(std::abs(deque.min() - 5.0) < 1e-9);

    // Evict oldest (10.0) and push new high (30.0)
    deque.push(30.0);
    assert(deque.size() == 4);
    assert(std::abs(deque.max() - 30.0) < 1e-9);
    assert(std::abs(deque.min() - 5.0) < 1e-9);

    std::cout << "[PASS] Monotonic Extrema Deque O(1) invariants verified.\n";
}

// Test 3: Parkinson Volatility Extreme-Value Kernel
void test_parkinson_volatility() {
    cmc::ParkinsonEstimator<5> parkinson;
    assert(parkinson.count() == 0);

    // Feed 5 high-low bars
    parkinson.update(105.0, 95.0);
    parkinson.update(110.0, 100.0);
    parkinson.update(102.0, 98.0);
    parkinson.update(115.0, 105.0);
    parkinson.update(108.0, 102.0);

    assert(parkinson.count() == 5);
    double vol = parkinson.realized_volatility();
    assert(vol > 0.0);
    assert(!std::isnan(vol));
    assert(!std::isinf(vol));

    // Zero-range bar must not panic or NaN
    cmc::ParkinsonEstimator<3> flat_vol;
    flat_vol.update(100.0, 100.0);
    flat_vol.update(100.0, 100.0);
    flat_vol.update(100.0, 100.0);
    assert(flat_vol.realized_volatility() == 0.0);

    std::cout << "[PASS] Parkinson Volatility Kernel numerical invariants verified.\n";
}

// Test 4: Zero-Heap Cross-Sectional Alpha Ranker
void test_cross_sectional_ranker() {
    cmc::CrossSectionalRanker<10> ranker;
    
    // Add 4 assets with raw momentum scores
    assert(ranker.add_asset("BTC", 5.2));
    assert(ranker.add_asset("ETH", 8.1));
    assert(ranker.add_asset("SOL", 14.5));
    assert(ranker.add_asset("DOGE", -2.3));

    assert(ranker.count() == 4);
    ranker.compute_ranks();

    // SOL should be highest rank (1.0), DOGE lowest (0.25)
    double sol_rank = ranker.get_percentile("SOL");
    double doge_rank = ranker.get_percentile("DOGE");

    assert(std::abs(sol_rank - 1.0) < 1e-6);
    assert(std::abs(doge_rank - 0.25) < 1e-6);
    assert(sol_rank > doge_rank);

    std::cout << "[PASS] Cross-Sectional Ranker percentile distribution verified.\n";
}

int main() {
    std::cout << "=== Running cmc-alpha-terminal C++20 Test Suite ===\n";
    test_welford_accumulator();
    test_monotonic_deque();
    test_parkinson_volatility();
    test_cross_sectional_ranker();
    std::cout << "=== ALL C++20 DETERMINISTIC INVARIANTS PASSED (4/4) ===\n";
    return 0;
}
