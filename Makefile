CXX := clang++
CXXFLAGS := -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror -Iinclude
ARCH := $(shell uname -m)

ifeq ($(ARCH), arm64)
	CXXFLAGS += -arch arm64
endif

BIN_DIR := bin
SRC_DIR := src
INCLUDE_DIR := include
TEST_CPP_DIR := tests/cpp

ASAN_FLAGS := -std=c++20 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -Iinclude
ifeq ($(ARCH), arm64)
	ASAN_FLAGS += -arch arm64
endif

.PHONY: all test test-cpp test-py build-cpp demo clean help asan lint

all: build-cpp

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

build-cpp: $(BIN_DIR)
	$(CXX) $(CXXFLAGS) $(SRC_DIR)/main.cpp -o $(BIN_DIR)/cmc_engine

test-cpp: $(BIN_DIR)
	$(CXX) $(CXXFLAGS) $(TEST_CPP_DIR)/test_engine.cpp -o $(BIN_DIR)/test_engine
	./$(BIN_DIR)/test_engine

asan: $(BIN_DIR)
	$(CXX) $(ASAN_FLAGS) $(TEST_CPP_DIR)/test_engine.cpp -o $(BIN_DIR)/test_engine_asan
	./$(BIN_DIR)/test_engine_asan

test-py:
	PYTHONPATH=python python3 -m pytest -v tests/

test: test-cpp test-py
	python3 scripts/audit_safety_invariants.py

lint:
	/Users/ishantpanchal/.local/bin/ruff check python/ tests/ scripts/
	python3 scripts/audit_safety_invariants.py

demo: build-cpp
	PYTHONPATH=python python3 -m cmc_terminal.tui --demo

clean:
	rm -rf $(BIN_DIR) .pytest_cache build dist *.egg-info

help:
	@echo "cmc-alpha-terminal build targets:"
	@echo "  make build-cpp  - Compile C++20 quantitative engine binary"
	@echo "  make test-cpp   - Run C++ deterministic test suite"
	@echo "  make asan       - Run C++ test suite under AddressSanitizer/UBSan"
	@echo "  make test-py    - Run Python FastMCP & client test suite"
	@echo "  make test       - Run all tests and safety invariant audits"
	@echo "  make lint       - Run ruff linter and AST safety invariant checks"
	@echo "  make demo       - Launch interactive ASCII terminal demo"
	@echo "  make clean      - Remove build artifacts"
