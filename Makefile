SUDO := sudo

PIP := pip
PYTHON := python3.11

CURRENT_USER := $(shell whoami)
USER_DIR := /home/$(CURRENT_USER)
ROOT_DIR := /root

REQUIERMENTS_DIR := requirements
SRC_DIR := src

.DEFAULT_GOAL = help

.PHONY: setup-venv
setup-venv:
	$(PYTHON) -m venv .

.PHONY: setup
setup:
	$(SUDO) apt-get update
	$(PIP) install -r $(REQUIERMENTS_DIR)/requirements.txt
	$(PYTHON) setup.py build
	$(PYTHON) setup.py install

.PHONY: clean
clean:
	rm -rf bin \
		build \
		include \
		lib \
		lib64 \
		dist \
		NBA_Awards_Predictor.egg-info

.PHONY: data-work
data-work:
	data_prepare
	data_team_prepare
	data_format
	data_link

.PHONY: model-all-nba
model-all-nba:
	model_params_search
	model_train

.PHONY: model-rookie
model-rookie:
	model_params_search_rookie
	model_train_rookie

.PHONY: help
help:
	@echo "-------------------- USAGE --------------------"
	@echo ""
	@echo "setup"
	@echo "		setup project, install requirements"
	@echo ""
	@echo "clean"
	@echo "		clean project"
