#! /bin/bash

#
# Description:
# ================================================================
# Time-stamp: "2022-05-13 00:14:41 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

# Different versions are required for my ECCE plots
python3.8 -mpip uninstall PyQt5
python3.8 -mpip uninstall PyQt5-sip
python3.8 -mpip uninstall PyQtWebEngine
python3.8 -m pip install pyqt5==5.14.0
echo
python3.8 setgui.py 
