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
LATEX_PROCESSOR := latex_processor.py
IDEAS_FILES := $(shell find src/ideas -name '*.tex' 2>/dev/null)

# Default target
.PHONY: build html clean

build: $(OUTPUT_PDF)

html: $(OUTPUT_HTML)

$(OUTPUT_PDF): $(SOURCE_TEX) $(LATEX_PROCESSOR) $(IDEAS_FILES)
	@mkdir -p $(BUILD_DIR)
	@python3 $(LATEX_PROCESSOR) $(SOURCE_TEX) build/temp-expanded.tex
	@cd $(SRC_DIR) && xelatex -interaction=nonstopmode -output-directory=../$(BUILD_DIR) $(MAIN_TEX)
	@cd $(SRC_DIR) && xelatex -interaction=nonstopmode -output-directory=../$(BUILD_DIR) $(MAIN_TEX)
	@echo "Build complete! PDF: $(OUTPUT_PDF)"

$(OUTPUT_HTML): $(SOURCE_TEX) $(HTML_TEMPLATE) $(CSS_FILE) $(LATEX_PROCESSOR) $(IDEAS_FILES)
	@mkdir -p public build
	@cp $(CSS_FILE) public/
	@python3 $(LATEX_PROCESSOR) $(SOURCE_TEX) build/expanded.tex
	@pandoc build/expanded.tex -f latex -t html5 --template=$(HTML_TEMPLATE) --css=style.css --variable=date:"$(shell date +'%Y年%m月%d日')" -o $(OUTPUT_HTML)
	@if [ -f $(OUTPUT_PDF) ]; then cp $(OUTPUT_PDF) public/; fi
	@echo "HTML build complete! File: $(OUTPUT_HTML)"



clean:
	@rm -rf $(BUILD_DIR)
	@rm -f $(SRC_DIR)/*.aux $(SRC_DIR)/*.log $(SRC_DIR)/*.toc $(SRC_DIR)/*.out
	@rm -f $(SRC_DIR)/*.fdb_latexmk $(SRC_DIR)/*.fls $(SRC_DIR)/*.synctex.gz $(SRC_DIR)/*.xdv
	@rm -f $(SRC_DIR)/*.bbl $(SRC_DIR)/*.blg $(SRC_DIR)/*.idx $(SRC_DIR)/*.ind $(SRC_DIR)/*.ilg
	@echo "Clean complete!"
