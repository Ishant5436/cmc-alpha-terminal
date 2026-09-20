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

.PHONY: all test test-cpp test-py build-cpp demo clean help asan lint audit-iso9001

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

audit-iso9001:
	python3 scripts/audit_iso9001_compliance.py

test: test-cpp test-py
	python3 scripts/audit_safety_invariants.py
	python3 scripts/audit_iso9001_compliance.py

lint:
	/Users/ishantpanchal/.local/bin/ruff check python/ tests/ scripts/
	python3 scripts/audit_safety_invariants.py
	python3 scripts/audit_iso9001_compliance.py

demo: build-cpp
	PYTHONPATH=python python3 -m cmc_terminal.tui --demo

clean:
	rm -rf $(BIN_DIR) .pytest_cache build dist *.egg-info target

help:
	@echo "cmc-alpha-terminal build targets:"
	@echo "  make build-cpp      - Compile C++20 quantitative engine binary"
	@echo "  make test-cpp       - Run C++ deterministic test suite"
	@echo "  make asan           - Run C++ test suite under AddressSanitizer/UBSan"
	@echo "  make test-py        - Run Python FastMCP & client test suite"
	@echo "  make audit-iso9001  - Run automated ISO/DIS 9001:2026 QMS auditor"
	@echo "  make test           - Run all tests, safety invariants, and QMS audits"
	@echo "  make lint           - Run ruff linter and AST safety invariant checks"
	@echo "  make demo           - Launch interactive ASCII terminal demo"
	@echo "  make clean          - Remove build artifacts"
