#!/bin/bash

# Activate the venv
source /home/faicelou/Workspace/cwp-radar-sim/.venv/bin/activate

# Add Qt libs to the LD_LIBRARY_PATH
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/home/faicelou/Workspace/cwp-radar-sim/.venv/lib/python3.12/site-packages/PySide6/Qt/lib"

# Launch the app
exec python3 -m ihm.main
