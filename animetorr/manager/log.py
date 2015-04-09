# -*- coding: utf-8 -*-
"""
Log window.
"""
__author__ = 'Sohhla'


import os
from PyQt4 import QtGui, QtCore
from qt.log import Ui_Dialog as Ui_Log
from shared import constant


# TODO: Works, but waaaaaay too slow to load
class LogUpdater(QtCore.QObject):
    """
    Updates the [Log window].
    """

    finish = QtCore.pyqtSignal()
    update_ui = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(LogUpdater, self).__init__(parent)
        self.log_paused = False
        self.previous_log_file_size = 0
        self.timer = None
        self.log_lines_read = -1
        self.html_log = ""

    def start_timer(self):
        """
        Starts timer. When it times out, will update the window again.
        """
        self.timer = QtCore.QTimer()
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.update_log)  # PyCharm doesn't recognize timeout.connect()...
        self.timer.setSingleShot(True)
        self.timer.start(1000)

    def update_log(self):
        """
        Reads the log file and updates the window.
        """
        if not self.log_paused:
            try:
                log_size = os.path.getsize(constant.LOG_PATH)
            except os.error:
                log_size = -1
            if self.previous_log_file_size!=log_size and log_size!=-1:
                if self.previous_log_file_size > log_size:
                    self.log_lines_read = -1
                if self.log_lines_read == -1:
                    self.html_log = "<table style=\"font-family:'MS Shell Dlg 2',monospace; font-size:14\">"
                # reading log, converting into html
                line_i = 0
                for log_line in open(constant.LOG_PATH,'r'):
                    if line_i >= self.log_lines_read:
                        temp = log_line.split(" ## ")
                        asctime = temp[0].strip()
                        name = temp[1].strip()
                        levelname = temp[2].strip()
                        message = temp[3].strip()
                        color = "0000FF"
                        if levelname=="DEBUG":
                            color = "008000"
                        elif levelname=="INFO":
                            color = "000000"
                        elif levelname=="WARNING":
                            color = "B8860B"
                        elif levelname=="ERROR":
                            color = "FF0000"
                        elif levelname=="CRITICAL":
                            color = "8A2BE2"
                        temp = "<tr style=\"color:#"+color+";\">\
                                <td style=\"padding-right: 5px;\">"+asctime+"</td>\
                                <td style=\"padding-right: 10px;padding-left: 10px;\" align=\"center\">#</td>\
                                <td style=\"padding-right: 5px; padding-left: 5px; \" align=\"center\">"+name+"</td>\
                                <td style=\"padding-right: 10px;padding-left: 10px;\" align=\"center\">#</td>\
                                <td style=\"padding-right: 5px; padding-left: 5px; \" align=\"center\">"+levelname+"</td>\
                                <td style=\"padding-right: 10px;padding-left: 10px;\" align=\"center\">#</td>\
                                <td style=\"padding-left: 5px;\">"+message+"</td></tr>"
                        self.html_log += temp
                    line_i+=1
                self.log_lines_read = line_i
                if self.log_paused:
                    self.finish.emit()  # log paused, exiting thread
                else:
                    # sending update to GUI
                    self.update_ui.emit(self.html_log+"</table>")
                    self.previous_log_file_size = log_size
            self.start_timer()
        else:
            self.finish.emit()

    def stop_thread(self):
        """
        Stops log update.
        """
        if self.timer is not None:
            self.timer.stop()
        self.finish.emit()


class WindowLog():
    """
    Creates Log window.
    """

    def __init__(self, parent_window):
        self.dialog_log = WindowLogDialog(self, parent_window, QtCore.Qt.WindowSystemMenuHint |
                                                               QtCore.Qt.WindowMaximizeButtonHint |
                                                               QtCore.Qt.WindowTitleHint |
                                                               QtCore.Qt.Window)
        self.ui_log = Ui_Log()
        self.ui_log.setupUi(self.dialog_log)

        self.ui_log.button_pause.clicked.connect(self.pause_log)

        self.ui_log.text_log.setHtml("Loading...")

        self.log_paused = False

        self.thread = None
        self.log_updater = None
        self.create_thread()

    def show(self):
        """
        Shows Log window.
        """
        self.dialog_log.exec_()

    def create_thread(self):
        """
        Creates thread to update log.
        """
        self.thread = QtCore.QThread(self.dialog_log)
        self.log_updater = LogUpdater()
        self.log_updater.moveToThread(self.thread)
        self.log_updater.update_ui.connect(self.update_log_ui)
        self.log_updater.finish.connect(self.thread.quit)
        # noinspection PyUnresolvedReferences
        self.thread.started.connect(self.log_updater.update_log)  # PyCharm doesn't recognize started.connect()...
        self.thread.start()
        self.dialog_log.stop_thread.connect(self.log_updater.stop_thread)

    def update_log_ui(self,new_html):
        """
        Update window with new html.

        :type new_html: str
        :param new_html: ...
        """
        self.ui_log.text_log.setHtml(new_html)
        temp_cursor = self.ui_log.text_log.textCursor()
        temp_cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
        self.ui_log.text_log.setTextCursor(temp_cursor)
        self.dialog_log.repaint()
        # noinspection PyArgumentList
        QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)

    def pause_log(self):
        """
        Stops window from being updated until the user clicks the button again.
        """
        if self.log_paused:
            self.log_paused = False
            self.ui_log.button_pause.setText("Pause Log")
            self.create_thread()
        else:
            self.log_paused = True
            self.ui_log.button_pause.setText("Resume Log")
            self.dialog_log.stop_thread.emit()


class WindowLogDialog(QtGui.QDialog):
    """
    Overrides default QDialog class to be able to control the close window event.
    """
    stop_thread = QtCore.pyqtSignal()

    def __init__(self, window, parent=None, params=None):
        super(WindowLogDialog, self).__init__(parent,params)
        self.window = window

    def closeEvent(self, _):
        """
        When closing the window, stop the thread.
        :type _: QCloseEvent
        :param _: Describes the close event. Not used.
        """
        if self.window.log_updater is not None:
            self.stop_thread.emit()