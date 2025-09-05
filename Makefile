# Makefile for Tech Management LaTeX document
.PHONY: build clean

# Variables
SRC_DIR := src
BUILD_DIR := build
MAIN_TEX := tech-management.tex
OUTPUT_PDF := tech-management.pdf

build:
	@mkdir -p $(BUILD_DIR)
	@cp $(SRC_DIR)/$(MAIN_TEX) $(BUILD_DIR)/
	@cd $(BUILD_DIR) && xelatex -interaction=nonstopmode $(MAIN_TEX)
	@cd $(BUILD_DIR) && xelatex -interaction=nonstopmode $(MAIN_TEX)
	@echo "Build complete! PDF: $(BUILD_DIR)/$(OUTPUT_PDF)"

clean:
	@rm -rf $(BUILD_DIR)
	@rm -f $(SRC_DIR)/*.aux $(SRC_DIR)/*.log $(SRC_DIR)/*.toc $(SRC_DIR)/*.out
	@echo "Clean complete!"
