# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../qt/qt_main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(457, 560)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(10, 0, 10, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.buttonsBar = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonsBar.sizePolicy().hasHeightForWidth())
        self.buttonsBar.setSizePolicy(sizePolicy)
        self.buttonsBar.setMinimumSize(QtCore.QSize(0, 70))
        self.buttonsBar.setMaximumSize(QtCore.QSize(500, 70))
        self.buttonsBar.setObjectName(_fromUtf8("buttonsBar"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.buttonsBar)
        self.horizontalLayout_3.setContentsMargins(0, 10, 0, 10)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.button_start = QtGui.QPushButton(self.buttonsBar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_start.sizePolicy().hasHeightForWidth())
        self.button_start.setSizePolicy(sizePolicy)
        self.button_start.setMinimumSize(QtCore.QSize(259, 50))
        self.button_start.setMaximumSize(QtCore.QSize(259, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.button_start.setFont(font)
        self.button_start.setAutoFillBackground(False)
        self.button_start.setStyleSheet(_fromUtf8("QPushButton {\n"
"    border-image: url(:/images/images/start_button_border.png);\n"
" }\n"
"\n"
" QPushButton:pressed {\n"
"    border-image: url(:/images/images/start_button_border_pressed.png);\n"
" }"))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/start.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_start.setIcon(icon1)
        self.button_start.setIconSize(QtCore.QSize(28, 28))
        self.button_start.setObjectName(_fromUtf8("button_start"))
        self.horizontalLayout_3.addWidget(self.button_start)
        self.line = QtGui.QFrame(self.buttonsBar)
        self.line.setMinimumSize(QtCore.QSize(10, 0))
        self.line.setMaximumSize(QtCore.QSize(10, 16777215))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout_3.addWidget(self.line)
        self.button_add = QtGui.QPushButton(self.buttonsBar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_add.sizePolicy().hasHeightForWidth())
        self.button_add.setSizePolicy(sizePolicy)
        self.button_add.setMinimumSize(QtCore.QSize(0, 50))
        self.button_add.setMaximumSize(QtCore.QSize(120, 50))
        self.button_add.setStyleSheet(_fromUtf8("QPushButton {\n"
"     border: 1px solid #8f8f91;\n"
"     border-radius: 4px;\n"
"     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                       stop: 0 #f6f7fa, stop: 1 #dadbde);\n"
"     padding-left: 6px;\n"
"     padding-right: 6px;\n"
" }\n"
"\n"
" QPushButton:pressed {\n"
"     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                       stop: 0 #dadbde, stop: 1 #f6f7fa);\n"
" }\n"
"\n"
" QPushButton:flat {\n"
"     border: none;\n"
" }"))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_add.setIcon(icon2)
        self.button_add.setObjectName(_fromUtf8("button_add"))
        self.horizontalLayout_3.addWidget(self.button_add)
        self.button_remove = QtGui.QPushButton(self.buttonsBar)
        self.button_remove.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_remove.sizePolicy().hasHeightForWidth())
        self.button_remove.setSizePolicy(sizePolicy)
        self.button_remove.setMinimumSize(QtCore.QSize(0, 50))
        self.button_remove.setMaximumSize(QtCore.QSize(120, 50))
        self.button_remove.setStyleSheet(_fromUtf8("QPushButton {\n"
"     border: 1px solid #8f8f91;\n"
"     border-radius: 4px;\n"
"     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                       stop: 0 #f6f7fa, stop: 1 #dadbde);\n"
"     padding-left: 6px;\n"
"     padding-right: 6px;\n"
" }\n"
"\n"
" QPushButton:pressed {\n"
"     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                       stop: 0 #dadbde, stop: 1 #f6f7fa);\n"
" }\n"
"\n"
" QPushButton:flat {\n"
"     border: none;\n"
" }"))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/remove.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_remove.setIcon(icon3)
        self.button_remove.setObjectName(_fromUtf8("button_remove"))
        self.horizontalLayout_3.addWidget(self.button_remove)
        self.verticalLayout_2.addWidget(self.buttonsBar)
        self.layout_table_area = QtGui.QVBoxLayout()
        self.layout_table_area.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.layout_table_area.setContentsMargins(-1, 0, -1, -1)
        self.layout_table_area.setSpacing(0)
        self.layout_table_area.setObjectName(_fromUtf8("layout_table_area"))
        self.verticalLayout_2.addLayout(self.layout_table_area)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.text_anime_status = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_anime_status.sizePolicy().hasHeightForWidth())
        self.text_anime_status.setSizePolicy(sizePolicy)
        self.text_anime_status.setMinimumSize(QtCore.QSize(0, 25))
        self.text_anime_status.setMaximumSize(QtCore.QSize(16777215, 25))
        self.text_anime_status.setObjectName(_fromUtf8("text_anime_status"))
        self.horizontalLayout.addWidget(self.text_anime_status, QtCore.Qt.AlignLeft)
        self.text_downloader_status = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_downloader_status.sizePolicy().hasHeightForWidth())
        self.text_downloader_status.setSizePolicy(sizePolicy)
        self.text_downloader_status.setMinimumSize(QtCore.QSize(0, 25))
        self.text_downloader_status.setMaximumSize(QtCore.QSize(16777215, 25))
        self.text_downloader_status.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.text_downloader_status.setObjectName(_fromUtf8("text_downloader_status"))
        self.horizontalLayout.addWidget(self.text_downloader_status, QtCore.Qt.AlignRight)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 457, 21))
        self.menubar.setMouseTracking(True)
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_file = QtGui.QMenu(self.menubar)
        self.menu_file.setMouseTracking(True)
        self.menu_file.setObjectName(_fromUtf8("menu_file"))
        self.menu_downloader = QtGui.QMenu(self.menubar)
        self.menu_downloader.setMouseTracking(True)
        self.menu_downloader.setObjectName(_fromUtf8("menu_downloader"))
        self.menu_help = QtGui.QMenu(self.menubar)
        self.menu_help.setMouseTracking(True)
        self.menu_help.setObjectName(_fromUtf8("menu_help"))
        MainWindow.setMenuBar(self.menubar)
        self.action_options = QtGui.QAction(MainWindow)
        self.action_options.setObjectName(_fromUtf8("action_options"))
        self.action_close = QtGui.QAction(MainWindow)
        self.action_close.setObjectName(_fromUtf8("action_close"))
        self.action_start_downloader = QtGui.QAction(MainWindow)
        self.action_start_downloader.setIcon(icon1)
        self.action_start_downloader.setObjectName(_fromUtf8("action_start_downloader"))
        self.action_add = QtGui.QAction(MainWindow)
        self.action_add.setIcon(icon2)
        self.action_add.setObjectName(_fromUtf8("action_add"))
        self.action_remove = QtGui.QAction(MainWindow)
        self.action_remove.setEnabled(False)
        self.action_remove.setIcon(icon3)
        self.action_remove.setObjectName(_fromUtf8("action_remove"))
        self.action_show_log = QtGui.QAction(MainWindow)
        self.action_show_log.setObjectName(_fromUtf8("action_show_log"))
        self.action_about = QtGui.QAction(MainWindow)
        self.action_about.setObjectName(_fromUtf8("action_about"))
        self.menu_file.addAction(self.action_options)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_close)
        self.menu_downloader.addAction(self.action_start_downloader)
        self.menu_downloader.addSeparator()
        self.menu_downloader.addAction(self.action_add)
        self.menu_downloader.addAction(self.action_remove)
        self.menu_help.addAction(self.action_show_log)
        self.menu_help.addAction(self.action_about)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_downloader.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "AnimeTorr", None))
        self.button_start.setText(_translate("MainWindow", "Start search", None))
        self.button_add.setText(_translate("MainWindow", "Add new\n"
"anime", None))
        self.button_remove.setText(_translate("MainWindow", "Remove\n"
"selected", None))
        self.text_anime_status.setText(_translate("MainWindow", "999 anime added, 999 enabled.", None))
        self.text_downloader_status.setText(_translate("MainWindow", "Starting application...", None))
        self.menu_file.setTitle(_translate("MainWindow", "File", None))
        self.menu_downloader.setTitle(_translate("MainWindow", "Anime", None))
        self.menu_help.setTitle(_translate("MainWindow", "Help", None))
        self.action_options.setText(_translate("MainWindow", "Options", None))
        self.action_close.setText(_translate("MainWindow", "Close", None))
        self.action_start_downloader.setText(_translate("MainWindow", "Start searching", None))
        self.action_add.setText(_translate("MainWindow", "Add new Anime", None))
        self.action_remove.setText(_translate("MainWindow", "Remove selected", None))
        self.action_show_log.setText(_translate("MainWindow", "Show Log", None))
        self.action_about.setText(_translate("MainWindow", "About", None))

import qt_resources_rc
