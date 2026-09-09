#pragma once

#include <cstddef>
#include <cmath>
#include <cassert>
#include <array>

namespace cmc {

template <std::size_t MaxBars>
class ParkinsonEstimator {
    static_assert(MaxBars > 0, "MaxBars must be greater than zero");

private:
    std::array<double, MaxBars> log_ratios_squared_{};
    std::size_t count_{0};
    static constexpr double CONST_FACTOR = 0.36067376022224085; // 1.0 / (4.0 * ln(2))

public:
    constexpr ParkinsonEstimator() noexcept = default;

    void update(double high, double low) noexcept {
        assert(high >= low);
        assert(low > 0.0 || (high == 0.0 && low == 0.0));

        if (count_ >= MaxBars) {
            return;
        }

        double val = 0.0;
        if (high > 0.0 && low > 0.0) {
            double ratio = high / low;
            assert(ratio >= 1.0);
            double log_ratio = std::log(ratio);
            val = log_ratio * log_ratio;
        }

        log_ratios_squared_[count_] = val;
        count_++;
        assert(count_ <= MaxBars);
    }

    [[nodiscard]] std::size_t count() const noexcept {
        return count_;
    }

    [[nodiscard]] double realized_volatility() const noexcept {
        assert(count_ <= MaxBars);
        if (count_ == 0) {
            return 0.0;
        }

        double sum_sq = 0.0;
        for (std::size_t i = 0; i < count_; ++i) {
            sum_sq += log_ratios_squared_[i];
        }

        double variance = (CONST_FACTOR * sum_sq) / static_cast<double>(count_);
        assert(variance >= 0.0);
        return std::sqrt(variance);
    }

    void reset() noexcept {
        count_ = 0;
        assert(count_ == 0);
    }
};

} // namespace cmc
