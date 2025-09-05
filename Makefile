# Makefile for Tech Management LaTeX document


# Variables
OUTPUT_PDF = build/tech-management.pdf
OUTPUT_HTML = public/index.html
SOURCE_TEX = src/tech-management.tex
HTML_TEMPLATE = templates/index-template.html
CSS_FILE = templates/style.css
SRC_DIR := src
BUILD_DIR := build
MAIN_TEX := tech-management.tex

# Default target
.PHONY: build html clean

build: $(OUTPUT_PDF)

html: $(OUTPUT_HTML)

$(OUTPUT_PDF): $(SOURCE_TEX)
	@mkdir -p $(BUILD_DIR)
	@cp $(SRC_DIR)/$(MAIN_TEX) $(BUILD_DIR)/
	@cd $(BUILD_DIR) && xelatex -interaction=nonstopmode $(MAIN_TEX)
	@cd $(BUILD_DIR) && xelatex -interaction=nonstopmode $(MAIN_TEX)
	@echo "Build complete! PDF: $(OUTPUT_PDF)"

$(OUTPUT_HTML): $(SOURCE_TEX) $(HTML_TEMPLATE) $(CSS_FILE)
	@mkdir -p public
	@cp $(CSS_FILE) public/
	@pandoc $(SOURCE_TEX) -f latex -t html5 --template=$(HTML_TEMPLATE) --css=style.css -o $(OUTPUT_HTML)
	@if [ -f $(OUTPUT_PDF) ]; then cp $(OUTPUT_PDF) public/; fi
	@echo "HTML build complete! File: $(OUTPUT_HTML)"



clean:
	@rm -rf $(BUILD_DIR)
	@rm -f $(SRC_DIR)/*.aux $(SRC_DIR)/*.log $(SRC_DIR)/*.toc $(SRC_DIR)/*.out
	@rm -f $(SRC_DIR)/*.fdb_latexmk $(SRC_DIR)/*.fls $(SRC_DIR)/*.synctex.gz $(SRC_DIR)/*.xdv
	@rm -f $(SRC_DIR)/*.bbl $(SRC_DIR)/*.blg $(SRC_DIR)/*.idx $(SRC_DIR)/*.ind $(SRC_DIR)/*.ilg
	@echo "Clean complete!"
