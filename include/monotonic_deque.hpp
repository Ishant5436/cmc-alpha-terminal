#ifndef CMC_ALPHA_MONOTONIC_DEQUE_HPP
#define CMC_ALPHA_MONOTONIC_DEQUE_HPP

#include <cstddef>
#include <cassert>
#include <cmath>
#include <array>

namespace cmc {

template <typename T, std::size_t WindowSize>
class MonotonicExtremaDeque {
    static_assert(WindowSize > 0, "WindowSize must be strictly positive");

private:
    std::array<T, WindowSize> buffer_{};
    std::size_t head_{0};
    std::size_t count_{0};

public:
    constexpr MonotonicExtremaDeque() noexcept = default;

    void push(T val) noexcept {
        assert(!std::isnan(val));
        assert(head_ < WindowSize);

        buffer_[head_] = val;
        head_ = (head_ + 1) % WindowSize;
        if (count_ < WindowSize) {
            count_++;
        }
        assert(count_ <= WindowSize);
    }

    [[nodiscard]] bool empty() const noexcept {
        return count_ == 0;
    }

    [[nodiscard]] std::size_t size() const noexcept {
        assert(count_ <= WindowSize);
        return count_;
    }

    [[nodiscard]] T min() const noexcept {
        assert(count_ > 0);
        T res = buffer_[0];
        for (std::size_t i = 1; i < count_; ++i) {
            if (buffer_[i] < res) {
                res = buffer_[i];
            }
        }
        assert(res <= buffer_[0]);
        return res;
    }

    [[nodiscard]] T max() const noexcept {
        assert(count_ > 0);
        T res = buffer_[0];
        for (std::size_t i = 1; i < count_; ++i) {
            if (buffer_[i] > res) {
                res = buffer_[i];
            }
        }
        assert(res >= buffer_[0]);
        return res;
    }

    void reset() noexcept {
        head_ = 0;
        count_ = 0;
        assert(empty());
    }
};

} // namespace cmc

#endif // CMC_ALPHA_MONOTONIC_DEQUE_HPP
