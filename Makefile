build: .venv
	pip install pyyaml
	chmod u+x main.py

install:
	rm -f ~/bin/local.ci
	mkdir -p ~/bin/
	ln -s $(CURDIR)/main.py ~/bin/local.ci

.PHONY: install
