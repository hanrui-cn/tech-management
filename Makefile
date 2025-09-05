# Makefile for building the LaTeX document
.PHONY: build clean rebuild git-init view

# Variables
SRC_DIR := src
BUILD_DIR := build
MAIN_TEX := main.tex
OUTPUT_PDF := main.pdf
AUX_EXTENSIONS := aux fls fdb_latexmk log nav out snm toc xdv synctex.gz

build:
	@echo "Building the document..."
	@mkdir -p $(BUILD_DIR)
	@mkdir -p $(BUILD_DIR)/chapters
	cd $(SRC_DIR) && xelatex -interaction=nonstopmode -output-directory=../$(BUILD_DIR) $(MAIN_TEX)
	cd $(SRC_DIR) && xelatex -interaction=nonstopmode -output-directory=../$(BUILD_DIR) $(MAIN_TEX)
	@echo "Build complete! PDF is at $(BUILD_DIR)/$(OUTPUT_PDF)"

clean:
	@echo "Cleaning build directory and auxiliary files..."
	@rm -rf $(BUILD_DIR)/*
	@for ext in $(AUX_EXTENSIONS); do \
		rm -f $(SRC_DIR)/*.$$ext; \
		rm -f $(SRC_DIR)/chapters/*.$$ext 2>/dev/null || true; \
	done
	@echo "Clean complete!"

rebuild: clean build
	@echo "Rebuild complete!"

# Initialize git repository
git-init:
	@git init
	@git add .
	@git commit -m "Initial commit: Tech Management book project"
	@echo "Git repository initialized and initial commit created!"

# View the generated PDF (requires open command on macOS)
view:
	@open $(BUILD_DIR)/$(OUTPUT_PDF) 2>/dev/null || echo "Unable to open PDF viewer. PDF is located at $(BUILD_DIR)/$(OUTPUT_PDF)"
