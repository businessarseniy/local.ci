build: .venv
	python3 -m venv .venv
	./.venv/bin/pip3 install pyyaml
	chmod u+x ./main.py

install:
	rm -f ~/bin/local.ci
	ln -s $(CURDIR)/main.py ~/bin/local.ci

.PHONY: install
