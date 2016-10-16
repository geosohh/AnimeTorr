# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../qt/qt_options.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(489, 379)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setContentsMargins(-1, 7, -1, -1)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.checkbox_autostart = QtGui.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.checkbox_autostart.setFont(font)
        self.checkbox_autostart.setChecked(True)
        self.checkbox_autostart.setObjectName(_fromUtf8("checkbox_autostart"))
        self.verticalLayout_3.addWidget(self.checkbox_autostart)
        self.checkbox_notification = QtGui.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.checkbox_notification.setFont(font)
        self.checkbox_notification.setChecked(True)
        self.checkbox_notification.setObjectName(_fromUtf8("checkbox_notification"))
        self.verticalLayout_3.addWidget(self.checkbox_notification)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setContentsMargins(-1, 7, -1, -1)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.text_search_frequency = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_search_frequency.sizePolicy().hasHeightForWidth())
        self.text_search_frequency.setSizePolicy(sizePolicy)
        self.text_search_frequency.setMinimumSize(QtCore.QSize(30, 0))
        self.text_search_frequency.setMaximumSize(QtCore.QSize(30, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.text_search_frequency.setFont(font)
        self.text_search_frequency.setMouseTracking(False)
        self.text_search_frequency.setMaxLength(3)
        self.text_search_frequency.setFrame(True)
        self.text_search_frequency.setEchoMode(QtGui.QLineEdit.Normal)
        self.text_search_frequency.setCursorPosition(2)
        self.text_search_frequency.setAlignment(QtCore.Qt.AlignCenter)
        self.text_search_frequency.setObjectName(_fromUtf8("text_search_frequency"))
        self.horizontalLayout_2.addWidget(self.text_search_frequency)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.checkbox_prefer_rss = QtGui.QCheckBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.checkbox_prefer_rss.setFont(font)
        self.checkbox_prefer_rss.setChecked(True)
        self.checkbox_prefer_rss.setObjectName(_fromUtf8("checkbox_prefer_rss"))
        self.verticalLayout_4.addWidget(self.checkbox_prefer_rss)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_6.setContentsMargins(-1, 7, -1, -1)
        self.verticalLayout_6.setSpacing(7)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.groupbox_utorrent_location = QtGui.QGroupBox(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupbox_utorrent_location.sizePolicy().hasHeightForWidth())
        self.groupbox_utorrent_location.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupbox_utorrent_location.setFont(font)
        self.groupbox_utorrent_location.setObjectName(_fromUtf8("groupbox_utorrent_location"))
        self.groupbox_app_vertical_layout = QtGui.QVBoxLayout(self.groupbox_utorrent_location)
        self.groupbox_app_vertical_layout.setContentsMargins(-1, 7, -1, 11)
        self.groupbox_app_vertical_layout.setObjectName(_fromUtf8("groupbox_app_vertical_layout"))
        self.radio_use_default_app = QtGui.QRadioButton(self.groupbox_utorrent_location)
        self.radio_use_default_app.setMaximumSize(QtCore.QSize(410, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radio_use_default_app.setFont(font)
        self.radio_use_default_app.setChecked(True)
        self.radio_use_default_app.setObjectName(_fromUtf8("radio_use_default_app"))
        self.groupbox_app_vertical_layout.addWidget(self.radio_use_default_app)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(7)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.radio_use_another_app = QtGui.QRadioButton(self.groupbox_utorrent_location)
        self.radio_use_another_app.setText(_fromUtf8(""))
        self.radio_use_another_app.setObjectName(_fromUtf8("radio_use_another_app"))
        self.horizontalLayout_3.addWidget(self.radio_use_another_app)
        self.text_app_path = QtGui.QLineEdit(self.groupbox_utorrent_location)
        self.text_app_path.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.text_app_path.setFont(font)
        self.text_app_path.setText(_fromUtf8(""))
        self.text_app_path.setReadOnly(False)
        self.text_app_path.setObjectName(_fromUtf8("text_app_path"))
        self.horizontalLayout_3.addWidget(self.text_app_path)
        self.button_app_path = QtGui.QPushButton(self.groupbox_utorrent_location)
        self.button_app_path.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_app_path.sizePolicy().hasHeightForWidth())
        self.button_app_path.setSizePolicy(sizePolicy)
        self.button_app_path.setMinimumSize(QtCore.QSize(45, 0))
        self.button_app_path.setMaximumSize(QtCore.QSize(45, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.button_app_path.setFont(font)
        self.button_app_path.setStyleSheet(_fromUtf8("QPushButton {\n"
"     border: 1px solid #8f8f91;\n"
"     border-radius: 4px;\n"
"     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                       stop: 0 #f6f7fa, stop: 1 #dadbde);\n"
"     padding-left: 4px;\n"
"     padding-right: 4px;\n"
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
        self.button_app_path.setObjectName(_fromUtf8("button_app_path"))
        self.horizontalLayout_3.addWidget(self.button_app_path)
        self.groupbox_app_vertical_layout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_6.addWidget(self.groupbox_utorrent_location)
        self.groupbox_anime_folder = QtGui.QGroupBox(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupbox_anime_folder.sizePolicy().hasHeightForWidth())
        self.groupbox_anime_folder.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupbox_anime_folder.setFont(font)
        self.groupbox_anime_folder.setObjectName(_fromUtf8("groupbox_anime_folder"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.groupbox_anime_folder)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.text_anime_folder = QtGui.QLineEdit(self.groupbox_anime_folder)
        self.text_anime_folder.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.text_anime_folder.setFont(font)
        self.text_anime_folder.setText(_fromUtf8(""))
        self.text_anime_folder.setReadOnly(False)
        self.text_anime_folder.setObjectName(_fromUtf8("text_anime_folder"))
        self.horizontalLayout_6.addWidget(self.text_anime_folder)
        self.button_anime_folder = QtGui.QPushButton(self.groupbox_anime_folder)
        self.button_anime_folder.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_anime_folder.sizePolicy().hasHeightForWidth())
        self.button_anime_folder.setSizePolicy(sizePolicy)
        self.button_anime_folder.setMinimumSize(QtCore.QSize(45, 0))
        self.button_anime_folder.setMaximumSize(QtCore.QSize(45, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.button_anime_folder.setFont(font)
        self.button_anime_folder.setStyleSheet(_fromUtf8("QPushButton {\n"
"     border: 1px solid #8f8f91;\n"
"     border-radius: 4px;\n"
"     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                       stop: 0 #f6f7fa, stop: 1 #dadbde);\n"
"     padding-left: 4px;\n"
"     padding-right: 4px;\n"
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
        self.button_anime_folder.setObjectName(_fromUtf8("button_anime_folder"))
        self.horizontalLayout_6.addWidget(self.button_anime_folder)
        self.verticalLayout_6.addWidget(self.groupbox_anime_folder)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_save = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_save.sizePolicy().hasHeightForWidth())
        self.button_save.setSizePolicy(sizePolicy)
        self.button_save.setMinimumSize(QtCore.QSize(75, 25))
        self.button_save.setMaximumSize(QtCore.QSize(16777215, 25))
        self.button_save.setStyleSheet(_fromUtf8("QPushButton {\n"
"     border: 1px solid #8f8f91;\n"
"     border-radius: 4px;\n"
"     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                       stop: 0 #f6f7fa, stop: 1 #dadbde);\n"
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
        self.button_save.setObjectName(_fromUtf8("button_save"))
        self.horizontalLayout.addWidget(self.button_save)
        self.button_cancel = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_cancel.sizePolicy().hasHeightForWidth())
        self.button_cancel.setSizePolicy(sizePolicy)
        self.button_cancel.setMinimumSize(QtCore.QSize(75, 25))
        self.button_cancel.setMaximumSize(QtCore.QSize(16777215, 25))
        self.button_cancel.setStyleSheet(_fromUtf8("QPushButton {\n"
"     border: 1px solid #8f8f91;\n"
"     border-radius: 4px;\n"
"     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                       stop: 0 #f6f7fa, stop: 1 #dadbde);\n"
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
        self.button_cancel.setObjectName(_fromUtf8("button_cancel"))
        self.horizontalLayout.addWidget(self.button_cancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Options", None))
        self.groupBox.setTitle(_translate("Dialog", "UI preferences", None))
        self.checkbox_autostart.setText(_translate("Dialog", "Auto-start on Windows startup", None))
        self.checkbox_notification.setText(_translate("Dialog", "Show notification when a new episode has been found", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Search preferences", None))
        self.label.setText(_translate("Dialog", "Check for new episodes every", None))
        self.text_search_frequency.setText(_translate("Dialog", "60", None))
        self.label_2.setText(_translate("Dialog", "minutes.", None))
        self.checkbox_prefer_rss.setText(_translate("Dialog", "Advanced: Use RSS instead of HTML (Nyaa only)", None))
        self.groupBox_3.setTitle(_translate("Dialog", "Torrent preferences", None))
        self.groupbox_utorrent_location.setTitle(_translate("Dialog", "Application", None))
        self.radio_use_default_app.setText(_translate("Dialog", "Use default application", None))
        self.text_app_path.setPlaceholderText(_translate("Dialog", "Select another application", None))
        self.button_app_path.setText(_translate("Dialog", "...", None))
        self.groupbox_anime_folder.setTitle(_translate("Dialog", "Default anime download folder (uTorrent only)", None))
        self.text_anime_folder.setPlaceholderText(_translate("Dialog", "Select folder", None))
        self.button_anime_folder.setText(_translate("Dialog", "...", None))
        self.button_save.setText(_translate("Dialog", "Save", None))
        self.button_cancel.setText(_translate("Dialog", "Cancel", None))

import qt_resources_rc
