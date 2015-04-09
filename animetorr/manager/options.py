# -*- coding: utf-8 -*-
"""
Options window.
"""
__author__ = 'Sohhla'


import _winreg
import os
import sys
import winshell
from PyQt4 import QtCore
from qt.options import Ui_Dialog as Ui_Options
from message_box import *
from shared import db
from shared import constant
from shared import torrent_application
from shared.strings import read_qt_text


class WindowOptions():
    """
    Creates Options window.
    """

    def __init__(self, parent_window):
        self.dialog_options = OptionsDialog(self, parent_window, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.ui_options = Ui_Options()
        self.ui_options.setupUi(self.dialog_options)

        self.ui_options.text_search_frequency.setValidator(QtGui.QIntValidator(15, 999))

        # Connect buttons/radio
        self.ui_options.button_app_path.clicked.connect(self.button_app_path_clicked)
        self.ui_options.button_anime_folder.clicked.connect(self.button_anime_folder_clicked)
        self.ui_options.button_save.clicked.connect(self.button_save_clicked)
        self.ui_options.button_cancel.clicked.connect(self.button_cancel_clicked)
        self.ui_options.radio_use_default_app.toggled.connect(self.radio_use_default_app_toggled)
        self.ui_options.text_app_path.textEdited.connect(self.text_app_path_edited)

        self.default_application_path = ""
        self.load_saved_values()

    def load_saved_values(self):
        """
        Fills the Options window with the currently saved configuration.
        """
        config = db.DBManager().get_config()

        # Autostart
        if os.path.exists(os.path.join(winshell.startup(),constant.AUTOSTART_SHORTCUT_NAME)):
            self.ui_options.checkbox_autostart.setChecked(True)
        else:
            self.ui_options.checkbox_autostart.setChecked(False)

        # Show notification
        self.ui_options.checkbox_notification.setChecked(config.show_notification)

        # Search frequency
        self.ui_options.text_search_frequency.setText(str(config.sleep_time/60))  #DB saves this as seconds

        # RSS or HTML (Nyaa only)
        self.ui_options.checkbox_prefer_rss.setChecked(config.prefer_rss)

        # Application used to download torrents
        application_exe = ""
        try:
            self.default_application_path = torrent_application.default_application_fullpath()
            application_exe = torrent_application.filename(self.default_application_path)
            radio_text = self.ui_options.radio_use_default_app.text()
            self.ui_options.radio_use_default_app.setText("%s (%s)" % (radio_text,application_exe))
        except WindowsError:
            label = QtGui.QLabel()
            label.setText("Windows has no default application to open .torrent files.")
            font = QtGui.QFont()
            font.setBold(False)
            label.setFont(font)
            label.setStyleSheet("QLabel { color : red; }")
            label.setWordWrap(True)
            self.ui_options.groupbox_app_vertical_layout.insertWidget(0,label)
            self.ui_options.radio_use_default_app.setEnabled(False)
            config.update_use_default_app(False)
        if config.use_default_app:
            self.ui_options.radio_use_default_app.setChecked(True)
            self.ui_options.radio_use_another_app.setChecked(False)
            self.ui_options.text_app_path.setEnabled(False)
            self.ui_options.button_app_path.setEnabled(False)
        else:
            self.ui_options.radio_use_default_app.setChecked(False)
            self.ui_options.radio_use_another_app.setChecked(True)
            self.ui_options.text_app_path.setEnabled(True)
            self.ui_options.button_app_path.setEnabled(True)
            self.ui_options.text_app_path.setText(config.app_path)
            application_exe = torrent_application.filename(config.app_path)
        self.check_application_selected(application_exe)

        # Anime download folder
        self.ui_options.text_anime_folder.setText(config.anime_folder)

    def show(self):
        """
        Shows the Options window.
        """
        self.dialog_options.exec_()

    def check_application_selected(self,application_exe):
        """
        Enables/disables extra options according to the torrent application selected.

        :type application_exe: str or unicode
        :param application_exe:
        """
        if application_exe.lower() == "utorrent.exe":
            self.ui_options.groupbox_anime_folder.setEnabled(True)
            self.ui_options.groupbox_anime_folder.setStyleSheet("")
        else:
            self.ui_options.groupbox_anime_folder.setEnabled(False)
            self.ui_options.groupbox_anime_folder.setStyleSheet("color: rgb(120, 120, 120);")

    def radio_use_default_app_toggled(self):
        """
        Controls the torrent application selection.
        """
        if self.ui_options.radio_use_default_app.isChecked():
            self.ui_options.radio_use_default_app.setChecked(True)
            self.ui_options.radio_use_another_app.setChecked(False)
            self.ui_options.text_app_path.setEnabled(False)
            self.ui_options.button_app_path.setEnabled(False)
            application_exe = torrent_application.filename(self.default_application_path)
        else:
            self.ui_options.radio_use_default_app.setChecked(False)
            self.ui_options.radio_use_another_app.setChecked(True)
            self.ui_options.text_app_path.setEnabled(True)
            self.ui_options.button_app_path.setEnabled(True)
            application_exe = torrent_application.filename(read_qt_text(self.ui_options.text_app_path.text()))
        self.check_application_selected(application_exe)

    def text_app_path_edited(self,new_text):
        """
        To properly update the window according to what the user typed.

        :type new_text: QtCore.QString
        :param new_text: new applcation fullpath.
        """
        app_exe = torrent_application.filename(read_qt_text(new_text))
        self.check_application_selected(app_exe)

    def button_app_path_clicked(self):
        """
        Torrent application selector.
        """
        application_folder = read_qt_text(self.ui_options.text_app_path.text())
        if os.path.isdir(application_folder):
            default_path = application_folder
        else:
            default_path = constant.FILEDIALOG_DEFAULT_PATH
        filepath = QtGui.QFileDialog.getOpenFileName(QtGui.QFileDialog(), "Torrent application", default_path, "*.exe")
        if os.path.exists(filepath):
            filepath = read_qt_text(filepath)
            self.ui_options.text_app_path.setText(filepath)
            application_exe = torrent_application.filename(filepath)
            self.check_application_selected(application_exe)

    def button_anime_folder_clicked(self):
        """
        Anime download folder selector.
        """
        download_folder = read_qt_text(self.ui_options.text_anime_folder.text())
        if os.path.isdir(download_folder):
            default_path = download_folder
        else:
            default_path = constant.FILEDIALOG_DEFAULT_PATH
        filename = QtGui.QFileDialog.getExistingDirectory(QtGui.QFileDialog(), "Default anime download folder", default_path, QtGui.QFileDialog.ShowDirsOnly)
        if os.path.isdir(filename):
            self.ui_options.text_anime_folder.setText(filename)

    def button_cancel_clicked(self):
        """
        If the user made any changes, asks if he wants to discard them and then acts accordingly.
        """
        config = db.DBManager().get_config()

        hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
        windows_common_startup,_ = _winreg.QueryValueEx(hkey,"Common Startup")
        windows_common_startup = windows_common_startup.encode("utf-8","ignore")
        old_autostart = os.path.exists(windows_common_startup+"\\"+constant.AUTOSTART_SHORTCUT_NAME)

        new_autostart = self.ui_options.checkbox_autostart.isChecked()
        new_show_notification = self.ui_options.checkbox_notification.isChecked()
        try:
            new_sleep_time = int(self.ui_options.text_search_frequency.text())*60
        except ValueError:
            new_sleep_time = -1
        new_prefer_rss = self.ui_options.checkbox_prefer_rss.isChecked()
        new_use_default_app = self.ui_options.radio_use_default_app.isChecked()
        new_app_path = self.ui_options.text_app_path.text()
        new_anime_folder = self.ui_options.text_anime_folder.text()

        if old_autostart != new_autostart or \
                   config.show_notification  != new_show_notification or \
                  (config.sleep_time         != new_sleep_time and new_sleep_time!=-1) or \
                   config.prefer_rss         != new_prefer_rss or \
                   config.use_default_app    != new_use_default_app or \
                  (config.app_path           != new_app_path and new_use_default_app is False) or \
                   config.anime_folder       != new_anime_folder:
            selection = show_yes_no_message("Close without saving","All changes will be lost!\nAre you sure?")
            if selection == QtGui.QMessageBox.Yes:
                self.dialog_options.accept()
            return selection == QtGui.QMessageBox.Yes
        else:
            self.dialog_options.accept()

    def button_save_clicked(self):
        """
        Saves all changes made.
        """
        config = db.DBManager().get_config()

        error = False
        try:
            new_sleep_time = int(self.ui_options.text_search_frequency.text())*60
        except ValueError:
            new_sleep_time = -1
        if new_sleep_time == -1:
            show_ok_message("Invalid search frequency","Invalid search frequency value.\n"
                                                       "The minimum value allowed is 15 minutes.",QtGui.QMessageBox.Warning)
            error = True
        elif new_sleep_time < 900:  # 15 min
            show_ok_message("Search frequency too high!","Search frequency must be slower.\n"
                                                         "The minimum value allowed is 15 minutes.",QtGui.QMessageBox.Warning)
            error = True

        new_app_path = read_qt_text(self.ui_options.text_app_path.text())
        if (not os.path.exists(new_app_path) or not new_app_path.endswith(".exe")) and not self.ui_options.radio_use_default_app.isChecked():
            show_ok_message("Invalid application path","Invalid application selected.\n"
                                                       "Please select the appropriate application to open the .torrent files.",QtGui.QMessageBox.Warning)
            error = True

        if not self.ui_options.text_anime_folder.isEnabled():
            new_anime_folder = ""
        else:
            new_anime_folder = self.ui_options.text_anime_folder.text()
        new_use_default_app = self.ui_options.radio_use_default_app.isChecked()
        if not os.path.isdir(new_anime_folder) and (self.ui_options.text_anime_folder.isEnabled() or new_app_path.lower().endswith("utorrent.exe")):
            if new_anime_folder=="":
                if not error and (config.anime_folder!="" or new_use_default_app!=config.use_default_app):
                    selection = show_yes_no_message("No folder?","Are you sure you do not want to specify a folder for anime?\n"
                                                                 "That means uTorrent will choose where to save downloaded episodes.")
                    if selection == QtGui.QMessageBox.Yes:
                        pass
                    elif selection == QtGui.QMessageBox.No:
                        error = True
            else:
                show_ok_message("Invalid anime folder","Invalid folder to save anime",QtGui.QMessageBox.Warning)
                error = True

        if not error:
            new_autostart = self.ui_options.checkbox_autostart.isChecked()
            new_show_notification = self.ui_options.checkbox_notification.isChecked()
            new_prefer_rss = self.ui_options.checkbox_prefer_rss.isChecked()

            if new_autostart:
                with winshell.shortcut(os.path.join(winshell.startup(),constant.AUTOSTART_SHORTCUT_NAME)) as shortcut:
                    shortcut.path = sys.executable
                    shortcut.icon = sys.executable, 0
                    shortcut.arguments = '-nogui'
                    shortcut.description = constant.AUTOSTART_SHORTCUT_DESCRIPTION
            else:
                try:
                    os.remove(os.path.join(winshell.startup(),constant.AUTOSTART_SHORTCUT_NAME))
                except WindowsError: pass

            config.update_show_notification(new_show_notification)
            config.update_sleep_time(new_sleep_time)
            config.update_prefer_rss(new_prefer_rss)
            config.update_use_default_app(new_use_default_app)
            config.update_app_path(new_app_path)
            config.update_anime_folder(new_anime_folder)

            self.dialog_options.accept()


class OptionsDialog(QtGui.QDialog):
    """
    Overrides default QDialog class to be able to control the close window event.
    """
    def __init__(self, window, parent=None, window_flags=None):
        super(OptionsDialog, self).__init__(parent,window_flags)
        self.window = window

    def closeEvent(self, evnt):
        """
        If the user tries to close the window, first check if he changed any configuration.

        :type evnt: QCloseEvent
        :param evnt: Describes the close event.
        """
        close_window = self.window.button_cancel_clicked()
        if not close_window:
            # By ignoring the event it stops being processed and the window is not closed.
            evnt.ignore()