# -*- coding: utf-8 -*-
"""
Generic funcions to show message boxes to the user.
"""
__author__ = 'Sohhla'


from PyQt4 import QtGui


def show_ok_message(title_text,message_text,icon_type=QtGui.QMessageBox.Information):
    """
    Message box with only an "OK" option.

    :type title_text: str
    :param title_text: Message box title

    :type message_text: str or unicode
    :param message_text: ...

    :type icon_type: int
    :param icon_type: http://doc.qt.io/qt-4.8/qmessagebox.html#Icon-enum
    """
    message = QtGui.QMessageBox()
    message.setIcon(icon_type)
    message.setWindowTitle(title_text)
    window_icon = QtGui.QIcon()
    window_icon.addPixmap(QtGui.QPixmap(":/images/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    message.setWindowIcon(window_icon)
    message.addButton(QtGui.QMessageBox.Ok)
    message.setText(message_text)
    message.exec_()


def show_yes_no_message(title_text,message_text):
    """
    Message box with "YES / NO" options.

    :type title_text: str
    :param title_text: Message box title

    :type message_text: str or unicode
    :param message_text: ...
    """
    message = QtGui.QMessageBox()
    message.setIcon(QtGui.QMessageBox.Question)
    message.setWindowTitle(title_text)
    window_icon = QtGui.QIcon()
    window_icon.addPixmap(QtGui.QPixmap(":/images/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    message.setWindowIcon(window_icon)
    message.addButton(QtGui.QMessageBox.Yes)
    message.addButton(QtGui.QMessageBox.No)
    message.setText(message_text)
    selection = message.exec_()
    return selection