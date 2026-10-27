PYTHON ?= python3

.PHONY: verify sources test cost-model
verify:
	$(PYTHON) -B scripts/verify.py
	$(PYTHON) -B -m unittest discover -s tests -v

sources:
	$(PYTHON) -B scripts/sources.py

test:
	$(PYTHON) -B -m unittest discover -s tests -v

cost-model:
	$(PYTHON) -B -m satbounds.cost certificates/models/general.json
	$(PYTHON) -B -m satbounds.cost certificates/models/fixed-density.json
