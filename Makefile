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

.PHONY: all test test-cpp test-py build-cpp demo clean help

all: build-cpp

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

build-cpp: $(BIN_DIR)
	$(CXX) $(CXXFLAGS) $(SRC_DIR)/main.cpp -o $(BIN_DIR)/cmc_engine

test-cpp: $(BIN_DIR)
	$(CXX) $(CXXFLAGS) $(TEST_CPP_DIR)/test_engine.cpp -o $(BIN_DIR)/test_engine
	./$(BIN_DIR)/test_engine

test-py:
	PYTHONPATH=python python3 -m pytest -v tests/

test: test-cpp test-py

demo: build-cpp
	PYTHONPATH=python python3 -m cmc_terminal.tui --demo

clean:
	rm -rf $(BIN_DIR) .pytest_cache build dist *.egg-info

help:
	@echo "cmc-alpha-terminal build targets:"
	@echo "  make build-cpp  - Compile C++20 quantitative engine binary"
	@echo "  make test-cpp   - Run C++ deterministic test suite"
	@echo "  make test-py    - Run Python FastMCP & client test suite"
	@echo "  make test       - Run all tests (C++ and Python)"
	@echo "  make demo       - Launch interactive ASCII terminal demo"
	@echo "  make clean      - Remove build artifacts"
