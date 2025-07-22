#!/bin/bash 
#This batch file is used to install all Python packages needed to use the HSDPython_SDK and its examples
echo "HSDPython_SDK Uninstaller"

# Section 1: stdatalog_pnpl
echo "==========================================="
echo "uninstalling stdatalog_pnpl..."
echo "==========================================="
python3 -m pip uninstall stdatalog_pnpl -y
# Section 2: stdatalog_core
echo "==========================================="
echo "uninstalling stdatalog_core"
echo "==========================================="
python3 -m pip uninstall stdatalog_core -y
# Section 3: stdatalog_dtk
echo "==========================================="
echo "uninstalling stdatalog_dtk"
echo "==========================================="
python3 -m pip uninstall stdatalog_dtk -y
# Section 4: stdatalog_gui
echo "==========================================="
echo "uninstalling stdatalog_gui..."
echo "==========================================="
python3 -m pip uninstall stdatalog_gui -y