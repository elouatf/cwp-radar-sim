# Project metadata
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
APP_NAME = radar
SRC_FILE = ihm/main.py
ADD_DATA = ihm/RadarView.qml:ihm
DIST_DIR = dist

.PHONY: all venv install build run clean

# Default target: build the app
all: build

# Create virtual environment (if it doesn't exist)
venv:
	@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)

# Install dev dependencies (in venv)
install: venv
	$(PIP) install -r requirements-dev.txt

# Build the standalone app with PyInstaller, including QML file
build: install
	$(PYTHON) -m PyInstaller --onefile --name $(APP_NAME) \
		--add-data "$(ADD_DATA)" $(SRC_FILE)

# Run the app from the dist folder
run: build
	./$(DIST_DIR)/$(APP_NAME)

# Clean up build artifacts
clean:
	rm -rf build/ $(DIST_DIR)/ *.spec