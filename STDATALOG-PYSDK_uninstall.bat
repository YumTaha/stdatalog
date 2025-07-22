@ECHO OFF 
:: This batch file is used to install all Python packages needed to use the HSDPython_SDK and its examples
ECHO HSDPython_SDK Unistaller
:: Section 1: stdatalog_pnpl
ECHO ===========================================
ECHO uninstalling stdatalog_pnpl...
ECHO ===========================================
python -m pip uninstall stdatalog_pnpl -y
:: Section 2: stdatalog_core
ECHO ===========================================
ECHO uninstalling stdatalog_core
ECHO ===========================================
python -m pip uninstall stdatalog_core -y
:: Section 3: stdatalog_dtk
ECHO ===========================================
ECHO uninstalling stdatalog_dtk
ECHO ===========================================
python -m pip uninstall stdatalog_dtk -y
:: Section 4: stdatalog_gui
ECHO ===========================================
ECHO uninstalling stdatalog_gui...
ECHO ===========================================
python -m pip uninstall stdatalog_gui -y
PAUSE
