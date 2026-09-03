#ifndef CMC_ALPHA_RANKER_HPP
#define CMC_ALPHA_RANKER_HPP

#include <cstddef>
#include <cassert>
#include <array>
#include <algorithm>
#include <cstring>
#include "types.hpp"

namespace cmc {

template <std::size_t MaxAssets>
class CrossSectionalRanker {
    static_assert(MaxAssets > 0, "MaxAssets must be positive");

public:
    struct Item {
        FixedString<16> symbol;
        double raw_score{0.0};
        double percentile{0.0};
    };

private:
    std::array<Item, MaxAssets> items_{};
    std::size_t count_{0};

public:
    constexpr CrossSectionalRanker() noexcept = default;

    bool add_asset(const char* sym, double score) noexcept {
        assert(sym != nullptr);
        assert(!std::isnan(score));

        if (count_ >= MaxAssets) {
            return false;
        }

        items_[count_].symbol = FixedString<16>(sym);
        items_[count_].raw_score = score;
        items_[count_].percentile = 0.0;
        count_++;
        assert(count_ <= MaxAssets);
        return true;
    }

    [[nodiscard]] std::size_t count() const noexcept {
        return count_;
    }

    void compute_ranks() noexcept {
        assert(count_ <= MaxAssets);
        if (count_ == 0) {
            return;
        }

        // Rank indices in-place using a static index array
        std::array<std::size_t, MaxAssets> indices{};
        for (std::size_t i = 0; i < count_; ++i) {
            indices[i] = i;
        }

        // Stable sort indices by raw_score ascending
        std::sort(indices.begin(), indices.begin() + count_, [this](std::size_t a, std::size_t b) {
            return items_[a].raw_score < items_[b].raw_score;
        });

        // Compute uniform percentile [1/N, 1.0]
        double n_dbl = static_cast<double>(count_);
        for (std::size_t rank = 0; rank < count_; ++rank) {
            std::size_t item_idx = indices[rank];
            items_[item_idx].percentile = static_cast<double>(rank + 1) / n_dbl;
            assert(items_[item_idx].percentile > 0.0);
            assert(items_[item_idx].percentile <= 1.0);
        }
    }

    [[nodiscard]] double get_percentile(const char* sym) const noexcept {
        assert(sym != nullptr);
        assert(count_ <= MaxAssets);

        FixedString<16> target(sym);
        for (std::size_t i = 0; i < count_; ++i) {
            if (items_[i].symbol == target) {
                return items_[i].percentile;
            }
        }
        return 0.0;
    }

    [[nodiscard]] const Item* get_item(std::size_t idx) const noexcept {
        assert(idx < count_);
        return &items_[idx];
    }
};

} // namespace cmc

#endif // CMC_ALPHA_RANKER_HPP
