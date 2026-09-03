#ifndef CMC_ALPHA_WELFORD_HPP
#define CMC_ALPHA_WELFORD_HPP

#include <cstddef>
#include <cmath>
#include <cassert>

namespace cmc {

class WelfordAccumulator {
private:
    std::size_t n_{0};
    double mean_{0.0};
    double m2_{0.0};

public:
    constexpr WelfordAccumulator() noexcept = default;

    void update(double x) noexcept {
        assert(!std::isnan(x));
        assert(!std::isinf(x));

        n_ += 1;
        double delta = x - mean_;
        mean_ += delta / static_cast<double>(n_);
        double delta2 = x - mean_;
        m2_ += delta * delta2;
    }

    [[nodiscard]] std::size_t count() const noexcept {
        return n_;
    }

    [[nodiscard]] double mean() const noexcept {
        assert(n_ >= 0);
        return mean_;
    }

    [[nodiscard]] double sample_variance() const noexcept {
        assert(n_ >= 0);
        if (n_ < 2) {
            return 0.0;
        }
        return m2_ / static_cast<double>(n_ - 1);
    }

    [[nodiscard]] double sample_stddev() const noexcept {
        double var = sample_variance();
        assert(var >= 0.0);
        return std::sqrt(var);
    }

    void reset() noexcept {
        assert(n_ >= 0);
        n_ = 0;
        mean_ = 0.0;
        m2_ = 0.0;
        assert(n_ == 0);
    }
};

} // namespace cmc

#endif // CMC_ALPHA_WELFORD_HPP
