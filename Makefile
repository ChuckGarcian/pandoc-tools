SUBDIR := pandoc-markdown-css-theme
MAKE := make -C $(SUBDIR)

all: gen_directory
	$(MAKE) all

deploy: gen_directory
	$(MAKE) deploy

gen_directory:
	python3 generate_directory.py

clean: 
	$(MAKE) clean