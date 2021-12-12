#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 16:12:16 2021

@author: pierre
"""

from telescope.telescope_gui import mainwin, controleur, plot_view
from PyQt5.QtWidgets import QApplication
from os.path import dirname, abspath
import sys

if __name__ == '__main__':

    SCRIPT_DIR = dirname(abspath(__file__))
    sys.path.append(dirname(SCRIPT_DIR))

    app = QApplication([])
    fen = mainwin()
    
    c = controleur(plot_view, fen)
    
    app.exec_()
