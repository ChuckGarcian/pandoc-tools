#
# Author: Jake Zimmerman <jake@zimmerman.io>
#
# ===== Usage ================================================================
#
# make                  Prepare docs/ folder (all markdown & assets)
# make docs/index.html  Recompile just docs/index.html
#
# make watch            Start a local HTTP server and rebuild on changes
# PORT=4242 make watch  Like above, but use port 4242
#
# make clean            Delete all generated files
#
# ============================================================================


# Local Directory of markdown files
TOP_DIR_NAME := ut-website
SRC_DIRS := ../../$(TOP_DIR_NAME)
IMG_SRC := $(SRC_DIRS)/img-src

# SRC_DIRS := src

SOURCES := $(shell find $(SRC_DIRS) -type f -name '*.md')
TARGETS := $(patsubst $(SRC_DIRS)/%.md,docs/%.html,$(SOURCES))

# Private Folder 
ENCRYPT_DIR := docs/Writings/Private
PSWD_FILE := ../../$(TOP_DIR_NAME)/pswd_file
PSWD := $(shell cat $(PSWD_FILE))

.PHONY: all
all: docs/.nojekyll $(TARGETS)
	staticrypt $(ENCRYPT_DIR)/dir.html --short \
  					 -p $(PSWD) \
						 -d $(ENCRYPT_DIR) \
						 -o $(ENCRYPT_DIR)/dir.html

.PHONY: clean
clean:
	rm -rf docs

.PHONY: watch
watch:
	./tools/serve.sh --watch

docs/.nojekyll: $(wildcard public/*) public/.nojekyll
	rm -vrf docs && mkdir -p docs && cp -vr $(IMG_SRC) public/.nojekyll public/* docs

.PHONY: docs
docs: docs/.nojekyll

# UTCS User 
USER:= chuckg

# Remote Machine 
REMOTE := $(USER)@linux.cs.utexas.edu

# Remote Directory
RDIR := /u/$(USER)/public_html

# Toggle Tufte Theme
TUFTE := true

deploy: all remote-clean push_remote
	
push_remote: 
	scp -r docs/* $(REMOTE):$(RDIR) \
	&& ssh $(REMOTE) 'chmod -R o+r+x $(RDIR)' \
  && ssh $(REMOTE) 'ls -l $(RDIR)' 

remote-clean: 
	ssh $(REMOTE) 'rm -r $(RDIR)/*'

# Generalized rule: how to build a .html file from each .md
# Note: you will need pandoc 2 or greater for this to work
docs/%.html: $(SRC_DIRS)/%.md template.html5 Makefile tools/build.sh
	tools/build.sh "$<" "$@" $(TUFTE)


