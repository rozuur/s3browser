PYTHON3 := $(shell brew --prefix)/bin/python3
APP = s3browse
VENV_DIR = .$(APP)_venv

.PHONY = remove_venv


$(VENV_DIR)/bin/activate: $(PYTHON3)
	$(PYTHON3) -m venv $(VENV_DIR)
	brew install libmagic


$(PYTHON3):
	brew install python3


remove_venv:
	rm -r $(VENV_DIR)

