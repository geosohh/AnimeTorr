# -*- coding: utf-8 -*-
"""
Manages the system tray icon.

The icon is only shown while:
    1. the application's main window is open
    2. downloader is running
"""
__author__ = 'Sohhla'


from PyQt4 import QtGui
from shared import constant
from message_box import show_yes_no_message


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    """
    Defines how the system tray icon looks and the actions available.
    """

    def __init__(self, app_controller, main_window):
        """
        :type app_controller: QtCore.QObject
        :param app_controller: Connects manager <-> downloader.

        :type main_window: WindowMain
        :param main_window: Used to show the main window.
        """
        super(SystemTrayIcon, self).__init__(QtGui.QIcon(QtGui.QPixmap(":/images/images/icon.png")))
        self.setToolTip(constant.TRAY_MESSAGE_TITLE)

        menu = QtGui.QMenu()
        action_manage = menu.addAction("Open AnimeTorr")
        action_exit = menu.addAction("Exit")
        self.setContextMenu(menu)
        action_manage.triggered.connect(self.clicked_open)
        action_exit.triggered.connect(self.clicked_exit)
        # noinspection PyUnresolvedReferences
        self.activated.connect(self.clicked)  # PyCharm doesn't recognize activated.connect()...

        self.main_window = main_window
        self.app_controller = app_controller

    def clicked(self, click_type):
        """
        User clicked / double-clicked the icon.

        :type click_type: int
        :param click_type: http://doc.qt.io/qt-4.8/qsystemtrayicon.html#ActivationReason-enum
        """
        if click_type==QtGui.QSystemTrayIcon.DoubleClick:
            self.clicked_open()

    def clicked_open(self):
        """
        User clicked "Open AnimeTorr" option; show main window.
        """
        self.main_window.show()

    def clicked_exit(self):
        """
        User clicked "Exit" option; close application.
        """
        selection = show_yes_no_message("Exit program","Are you sure you want to exit AnimeTorr?")
        if selection == QtGui.QMessageBox.Yes:
            self.app_controller.quit()