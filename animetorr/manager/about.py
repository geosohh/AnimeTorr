# -*- coding: utf-8 -*-
"""
About window.
"""
__author__ = 'Sohhla'


from PyQt4 import QtGui, QtCore
from qt.about import Ui_Dialog as Ui_About


class WindowAbout():
    """
    Creates About window.
    """
    def __init__(self, parent_window):
        self.dialog_about = QtGui.QDialog(parent_window, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.Window)
        self.ui_about = Ui_About()
        self.ui_about.setupUi(self.dialog_about)

    def show(self):
        """
        Shows About window.
        """
        self.dialog_about.exec_()