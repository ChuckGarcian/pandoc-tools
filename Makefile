SUBDIR := pandoc-markdown-css-theme
SRC_DIRS := ../ut-website-md
MAKE := make -C $(SUBDIR)

DEL_SOURCES := $(shell find $(SRC_DIRS) -type f -name 'dir.md')

all: gen_directory
	$(MAKE) all

deploy: gen_directory
	$(MAKE) deploy

gen_directory:
	python3 generate_directory.py

clean: 
	$(foreach file, $(DEL_SOURCES), rm -f $(file);) 
	$(MAKE) clean