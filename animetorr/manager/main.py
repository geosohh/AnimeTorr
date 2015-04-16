# -*- coding: utf-8 -*-
"""
Main window.
"""
__author__ = 'Sohhla'


from functools import partial
from PyQt4 import QtCore
from qt.main import Ui_MainWindow
from about import WindowAbout
from add import WindowAdd
from log import WindowLog
from options import WindowOptions
from message_box import *
from shared import db
from shared import torrent_application
from shared.strings import *


class WindowMain():
    """
    Creates main window.
    """

    # noinspection PyUnresolvedReferences
    # ^ because PyCharm doesn't recognize triggered.connect()...
    def __init__(self,app_controller):
        """
        :type app_controller: QtCore.QObject
        :param app_controller: Connects manager <-> downloader.
        """
        self.window = AnimeTorrMainWindow(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)

        self.app_controller = app_controller

        # Connect buttons/actions
        self.ui.action_about.triggered.connect(self.clicked_about)
        self.ui.action_add.triggered.connect(self.clicked_add)
        self.ui.action_remove.triggered.connect(self.clicked_remove)
        self.ui.action_show_log.triggered.connect(self.clicked_log)
        self.ui.action_start_downloader.triggered.connect(self.clicked_start)
        self.ui.action_options.triggered.connect(self.clicked_options)
        self.ui.action_close.triggered.connect(self.clicked_close)
        self.ui.button_add.clicked.connect(self.clicked_add)
        self.ui.button_remove.clicked.connect(self.clicked_remove)
        self.ui.button_start.clicked.connect(self.clicked_start)

        self.anime_table = AnimeTable(self.ui.centralwidget,self)
        self.ui.layout_table_area.addWidget(self.anime_table)
        self.update_anime_table()

    def show(self):
        """
        Shows main window.
        """
        if self.window.isVisible():
            self.window.activateWindow()
        else:
            self.window.show()
            self.window.activateWindow()
            if db.DBManager().get_config().first_use:
                try:
                    torrent_application.fullpath()
                except WindowsError:
                    show_ok_message("Initial configuration","No application to download torrents has been found.\n"
                                                            "Please go to [Options] and select one.\n\n"
                                                            "Press OK to open [Options].")
                    self.clicked_options()
                db.DBManager().get_config().update_first_use(False)
            self.ui.buttonsBar.setMaximumWidth(self.ui.buttonsBar.width())

    def update_anime_table(self):
        """
        Gets anime data from the DB and updates anime table.
        """
        anime_list = db.DBManager().get_anime_list()
        self.anime_table.update_table(anime_list)
        self.update_anime_table_status()

    def update_anime_table_status(self):
        """
        Updates number of animes added/enabled.
        """
        anime_list = db.DBManager().get_anime_list()
        anime_added = len(anime_list)
        anime_enabled = len([anime for anime in anime_list if anime.enabled])
        self.ui.text_anime_status.setText("{0:d} animes added, {1:d} enabled.".format(anime_added,anime_enabled))

    def clicked_about(self):
        """
        User clicked "About".
        """
        dialog_about = WindowAbout(self.window)
        dialog_about.show()

    def clicked_add(self):
        """
        User clicked "Add".
        """
        dialog_add = WindowAdd(self.window,self)
        dialog_add.show()

    def clicked_remove(self):
        """
        User selected one or more anime and clicked "Remove".
        """
        selected_animes = self.anime_table.selected_animes()
        if len(selected_animes)>1:
            msg_text = "Are you sure you want to remove the selected anime?\n" \
                       "This action cannot be undone!\n\n" \
                       "If you just want to temporarily stop searching for new episodes, disable the anime instead of removing them.\n\n" \
                       "Animes selected:\n"
            for anime in selected_animes:
                msg_text+=anime+"\n"
        else:
            msg_text = "Are you sure you want to remove the selected anime?\n" \
                       "This action cannot be undone!\n\n" \
                       "If you just want to temporarily stop searching for new episodes, disable the anime instead of removing it.\n\n" \
                       "Anime selected: "+selected_animes[0]
        selection = show_yes_no_message("Remove anime",msg_text)
        if selection == QtGui.QMessageBox.Yes:
            for anime_name in selected_animes:
                db.DBManager().remove_anime(anime_name)
            self.update_anime_table()

    def clicked_log(self):
        """
        User clicked "Show Log".
        """
        dialog_log = WindowLog(self.window)
        dialog_log.show()

    def clicked_options(self):
        """
        User clicked "Options".
        """
        # TODO: Remove this limitation...
        if self.app_controller.downloader_is_running:
            show_ok_message("Searching anime","Please stop the search before opening the Options menu.")
        else:
            dialog_options = WindowOptions(self.window)
            dialog_options.show()

    def downloader_starting(self):
        """
        Downloader is starting; update downloader status indicator.
        """
        self.ui.text_downloader_status.setText("Starting search...")
        self.anime_table.set_items_are_selectable(False)
        self.ui.button_add.setEnabled(False)
        self.ui.button_remove.setEnabled(False)

    def downloader_started(self):
        """
        Downloader started; update downloader status indicator.
        """
        self.ui.button_start.setStyleSheet("QPushButton {"
                                           "   border-image: url(:/images/images/stop_button_border.png);"
                                           "}"
                                           "QPushButton:pressed {"
                                           "   border-image: url(:/images/images/stop_button_border_pressed.png);"
                                           "}")
        self.ui.button_start.setText("Stop search")
        self.ui.action_start_downloader.setText("Stop search")
        self.ui.text_downloader_status.setText("Search activated")
        self.anime_table.set_items_are_selectable(False)

    def downloader_stopping(self):
        """
        Downloader is stopping; update downloader status indicator.
        """
        self.ui.text_downloader_status.setText("Stopping search...")

    def downloader_stopped(self):
        """
        Downloader stopped; update downloader status indicator.
        """
        self.ui.button_start.setStyleSheet("QPushButton {"
                                           "   border-image: url(:/images/images/start_button_border.png);"
                                           "}"
                                           "QPushButton:pressed {"
                                           "   border-image: url(:/images/images/start_button_border_pressed.png);"
                                           "}")
        self.ui.button_start.setText("Start search")
        self.ui.action_start_downloader.setText("Start search")
        self.ui.text_downloader_status.setText("Search stopped")
        self.anime_table.set_items_are_selectable(True)
        self.ui.button_add.setEnabled(True)

    def clicked_start(self):
        """
        User clicked "Start Search".
        """
        if self.app_controller.downloader_is_running:
            self.app_controller.stop_downloader()
        else:
            try:
                torrent_application.fullpath()
                self.app_controller.start_downloader()
            except WindowsError:
                show_ok_message("Error","No application to download torrents has been found.\n"
                                        "Please go to [Options] and select one.\n\n"
                                        "Press OK to open [Options].")
                self.clicked_options()

    def clicked_close(self):
        """
        User tried to close the window.
        """
        if self.app_controller.downloader_is_running:
            self.window.hide()
        else:
            selection = show_yes_no_message("Exit application","Are you sure you want to exit AnimeTorr?")
            if selection == QtGui.QMessageBox.Yes:
                self.app_controller.quit()
            return selection==QtGui.QMessageBox.Yes

    def is_visible(self):
        """
        :rtype: bool
        :return If the window is visible (opened) or not (system tray icon only).
        """
        return self.window.isVisible()


class AnimeTable(QtGui.QTableWidget):
    """
    Table with all anime added.
    """

    def __init__(self, parent,main_window):
        super(AnimeTable, self).__init__(parent)
        #self.log = LoggerManager().get_logger("MainGUI-AnimeTable")

        #Headers
        self.setColumnCount(3)  #enabled, name, episode
        header_enabled = QtCore.QString("Enabled")
        header_name = QtCore.QString("Name")
        header_episode = QtCore.QString("Episode")
        self.setHorizontalHeaderLabels([header_enabled, header_name, header_episode])
        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().hide()

        #Columns size
        """
        # Three ways to measure text width in pixels (http://stackoverflow.com/a/8638114):
        print "enabled width="+str(QtGui.QFontMetrics(self.font()).width(header_enabled))
        print "enabled rect ="+str(QtGui.QFontMetrics(self.font()).boundingRect(header_enabled).width())
        print "enabled size ="+str(QtGui.QFontMetrics(self.font()).size(QtCore.Qt.TextSingleLine, header_enabled).width())
        """
        self.setColumnWidth(0, QtGui.QFontMetrics(self.font()).width(header_enabled)+20)
        self.setColumnWidth(2, QtGui.QFontMetrics(self.font()).width(header_enabled)+20)
        self.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Fixed)
        self.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.Fixed)
        self.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)

        #Sorting
        self.setSortingEnabled(True)
        self.horizontalHeader().setSortIndicatorShown(False)

        #Item selection
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        #Signals
        # noinspection PyUnresolvedReferences
        self.cellDoubleClicked.connect(self.cell_double_clicked)  # PyCharm doesn't recognize cellDoubleClicked.connect()...
        # noinspection PyUnresolvedReferences
        self.itemSelectionChanged.connect(self.item_selection_changed)  # PyCharm doesn't recognize itemSelectionChanged.connect()...

        #Other stuff
        self.setCornerButtonEnabled(False)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        #Table data
        self.data = {}
        self.anime_list = []

        #Used to edit and update main window
        self.main_window = main_window
        self.allow_row_selection = True

    def update_anime_enabled(self,anime,checkbox,checkbox_state):
        """
        Update enabled/disable status for an anime.

        :type anime: db.Anime
        :param anime: Anime to be updated.

        :param checkbox: What checkbox the user clicked

        :param checkbox_state: If the checkbox is now checked or not.
        """
        anime.update_enabled(checkbox_state==QtCore.Qt.Checked)
        self.main_window.update_anime_table_status()
        #self.update_table()
        #return

        #without this "for", sorting by enabled won't work
        cell_widget = checkbox.parentWidget()
        for row in range(0,self.rowCount()):
            if self.cellWidget(row,0)==cell_widget:
                #self.setSortingEnabled(False)
                self.item(row,0).set_key(checkbox_state==QtCore.Qt.Checked)
                #self.takeItem(row,0)
                #newitem = MyTableWidgetItem("",checkbox_state==QtCore.Qt.Checked)
                #self.setItem(row, 0, newitem)
                #self.setSortingEnabled(True)

    def selected_animes(self):
        """
        :rtype: list[str]
        :return: list with animes the user selected (click, ctrl+click).
        """
        selected_animes = []
        for row in range(0,self.rowCount()):
            if self.item(row,1).isSelected():
                selected_animes.append(read_qt_text(self.item(row,1).text()))
        selected_animes.sort()
        return selected_animes

    def item_selection_changed(self):
        """
        Enables the "Remove" button when an anime is selected.
        """
        if self.allow_row_selection:
            enable_button = False
            for row in range(0,self.rowCount()):
                if self.item(row,1).isSelected():
                    enable_button = True
                    break
            self.main_window.ui.button_remove.setEnabled(enable_button)

    def cell_double_clicked(self,row,_):
        """
        User double-clicked an anime, open [Add window] to edit it.

        :type row: int
        :param row: Row the user clicked.

        :param _: column, not used.
        """
        if self.allow_row_selection:
            anime_selected = read_qt_text(self.item(row,1).text())
            for anime in self.anime_list:
                if anime.name==anime_selected:
                    dialog_add = WindowAdd(self.main_window.window,self.main_window,editing=True,anime_to_edit=anime)
                    dialog_add.show()
                    break
        else:
            show_ok_message("Search activated","Please stop the search before editing an anime.")

    def update_table(self, anime_list = None):
        """
        Updates (re-creates) the anime table.

        :type anime_list: list[Anime]
        :param anime_list: List with all anime.
        """
        self.setSortingEnabled(False)  #Re-activated later. Otherwise, The table gets messed up
        self.clearContents()
        if anime_list is not None:
            self.anime_list = anime_list
        self.setRowCount(len(self.anime_list))
        self.data.clear()
        self.data = {0: [], 1: [], 2: [], 3: []}
        for anime in self.anime_list:
            self.data[0].append(anime.enabled)
            self.data[1].append(anime.name)
            self.data[2].append(str(anime.episode))
            self.data[3].append(anime)
        for column, key in enumerate(sorted(self.data.keys())):
            if key!=3:
                for row, item in enumerate(self.data[key]):
                    if type(item)==bool:
                        checkbox_widget = QtGui.QWidget()
                        checkbox = QtGui.QCheckBox()
                        checkbox.setChecked(item)
                        # noinspection PyUnresolvedReferences
                        checkbox.stateChanged.connect(partial(self.update_anime_enabled,self.data[3][row],checkbox))  # PyCharm doesn't recognize stateChanged.connect()...
                        layout = QtGui.QHBoxLayout(checkbox_widget)
                        layout.addWidget(checkbox)
                        layout.setAlignment(QtCore.Qt.AlignCenter)
                        layout.setContentsMargins(0,0,0,0)
                        checkbox_widget.setLayout(layout)
                        self.setCellWidget(row,column,checkbox_widget)
                        newitem = MyTableWidgetItem("",item)  #Used to sort the table
                        self.setItem(row, column, newitem)
                    else:
                        newitem = MyTableWidgetItem(item,item)
                        self.setItem(row, column, newitem)
        for row in range(self.rowCount()):
            text_height = self.fontMetrics().boundingRect(read_qt_text(self.item(row,1).text())).height()
            row_height = text_height+12
            self.setRowHeight(row, row_height)
        self.setSortingEnabled(True)
        self.sortItems(1,QtCore.Qt.AscendingOrder)  #automatically sort by anime name

    def set_items_are_selectable(self,bool_value):
        """
        Enables/disables anime editing/removal.

        :param bool_value: If anime editing/removal is allowed or not.
        """
        self.allow_row_selection = bool_value
        if self.allow_row_selection:
            for row in range(0,self.rowCount()): self.cellWidget(row,0).setEnabled(True)
            self.setStyleSheet("")
        else:
            for row in range(0,self.rowCount()): self.cellWidget(row,0).setEnabled(False)
            self.setStyleSheet("color: rgb(120, 120, 120);")


class MyTableWidgetItem(QtGui.QTableWidgetItem):
    """
    Source: http://stackoverflow.com/questions/12673598/python-numerical-sorting-in-qtablewidget
    """
    def __init__(self, text, sort_key):
        QtGui.QTableWidgetItem.__init__(self, text, QtGui.QTableWidgetItem.UserType)
        try:
            sort_key = int(sort_key)
        except ValueError:
            pass
        self.sort_key = sort_key

    def set_key(self,new_sort_key):
        """
        Updates the sort key (enabled/disabled) with the new value.

        :type new_sort_key: bool
        :param new_sort_key: New value
        """
        try:
            new_sort_key = int(new_sort_key)
        except ValueError:
            pass
        self.sort_key = new_sort_key

    def __lt__(self, other):
        """
        Qt uses a simple < check for sorting items, override this to use the sortKey
        """
        return self.sort_key < other.sort_key


class AnimeTorrMainWindow(QtGui.QMainWindow):
    """
    Overrides default QMainWindow class to be able to control the close window event.
    """
    def __init__(self, window, parent=None):
        super(AnimeTorrMainWindow, self).__init__(parent)
        self.window = window

    def closeEvent(self, evnt):
        """
        If the user tries to close the window, ask for confirmation.

        :type evnt: QCloseEvent
        :param evnt: Describes the close event.
        """
        close_window = self.window.clicked_close()
        if not close_window:
            evnt.ignore()