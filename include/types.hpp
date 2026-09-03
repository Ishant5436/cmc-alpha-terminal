#ifndef CMC_ALPHA_TYPES_HPP
#define CMC_ALPHA_TYPES_HPP

#include <cstdint>
#include <cstddef>
#include <cassert>
#include <cstring>
#include <algorithm>

namespace cmc {

// Fixed-capacity string to prevent heap allocations
template <std::size_t Capacity>
struct FixedString {
    char data[Capacity] = {0};
    std::size_t len = 0;

    FixedString() = default;

    explicit FixedString(const char* str) {
        assert(str != nullptr);
        std::size_t input_len = std::strlen(str);
        assert(input_len < Capacity);
        len = std::min(input_len, Capacity - 1);
        std::memcpy(data, str, len);
        data[len] = '\0';
    }

    [[nodiscard]] const char* c_str() const noexcept {
        assert(len < Capacity);
        return data;
    }

    [[nodiscard]] bool empty() const noexcept {
        return len == 0;
    }

    bool operator==(const FixedString& other) const noexcept {
        return (len == other.len) && (std::strncmp(data, other.data, len) == 0);
    }
};

enum class MarketRegime : uint8_t {
    COMPRESSION = 0,
    TRENDING = 1,
    EXPANSION_VOLATILE = 2
};

struct CMCTick {
    FixedString<16> symbol;
    double price{0.0};
    double volume_24h{0.0};
    double percent_change_24h{0.0};
    double market_cap{0.0};
    uint64_t timestamp{0};

    [[nodiscard]] bool is_valid() const noexcept {
        assert(!symbol.empty());
        assert(price >= 0.0);
        return (!symbol.empty() && price >= 0.0);
    }
};

} // namespace cmc

#endif // CMC_ALPHA_TYPES_HPP
