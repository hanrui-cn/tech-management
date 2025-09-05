# Makefile for Tech Management LaTeX document
.PHONY: build clean html

# Variables
SRC_DIR := src
BUILD_DIR := build
MAIN_TEX := tech-management.tex
OUTPUT_PDF := tech-management.pdf
OUTPUT_HTML := tech-management.html

build:
	@mkdir -p $(BUILD_DIR)
	@cp $(SRC_DIR)/$(MAIN_TEX) $(BUILD_DIR)/
	@cd $(BUILD_DIR) && xelatex -interaction=nonstopmode $(MAIN_TEX)
	@cd $(BUILD_DIR) && xelatex -interaction=nonstopmode $(MAIN_TEX)
	@echo "Build complete! PDF: $(BUILD_DIR)/$(OUTPUT_PDF)"

html:
	@mkdir -p $(BUILD_DIR)
	@echo "Generating HTML..."
	@cp $(SRC_DIR)/$(MAIN_TEX) $(BUILD_DIR)/
	@cp style.css $(BUILD_DIR)/
	@cd $(BUILD_DIR) && pandoc $(MAIN_TEX) -o $(OUTPUT_HTML) --standalone --metadata title="tech-management" --css=style.css}]}}}
	@echo "HTML build complete! Open $(BUILD_DIR)/$(OUTPUT_HTML) in browser"

clean:
	@rm -rf $(BUILD_DIR)
	@rm -f $(SRC_DIR)/*.aux $(SRC_DIR)/*.log $(SRC_DIR)/*.toc $(SRC_DIR)/*.out
	@rm -f $(SRC_DIR)/*.fdb_latexmk $(SRC_DIR)/*.fls $(SRC_DIR)/*.synctex.gz $(SRC_DIR)/*.xdv
	@rm -f $(SRC_DIR)/*.bbl $(SRC_DIR)/*.blg $(SRC_DIR)/*.idx $(SRC_DIR)/*.ind $(SRC_DIR)/*.ilg
	@echo "Clean complete!"
