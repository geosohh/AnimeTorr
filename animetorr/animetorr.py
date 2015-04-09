# -*- coding: utf-8 -*-
"""
AnimeTorr main script, responsible for starting the application (both manager and downloader).
"""
__author__ = 'Sohhla'


import os
import sys
import shutil
import inspect
from PyQt4 import QtGui,QtCore,QtNetwork
from manager.system_tray_icon import SystemTrayIcon
from manager.main import WindowMain
from downloader.downloader import Downloader
from shared.log import LoggerManager
from shared import db
from shared import constant


class Main(QtCore.QObject):
    """
    Main class, instantiated when the application starts.
    Creates main window/system tray icon, and stops the user from opnening more than one instance of the application.
    It also starts/stops the downloader when the user requests or during auto-start on Windows startup.
    """

    def __init__(self):
        QtCore.QObject.__init__(self)

        # Make sure the required folders/files exist
        if not os.path.isdir(constant.DATA_PATH):
            os.makedirs(constant.DATA_PATH)
        self.log = LoggerManager().get_logger("MAIN")
        try:
            if not os.path.isfile(constant.DB_PATH):
                shutil.copyfile("dbTemplate.db",constant.DB_PATH)
        except (shutil.Error,IOError) as error:
            self.log.print_traceback(error,self.log.critical)
            sys.exit(1)
        try:
            if not os.path.isdir(constant.DEFAULT_TORRENTS_PATH):
                os.makedirs(constant.DEFAULT_TORRENTS_PATH)
        except Exception as error:
            self.log.print_traceback(error,self.log.critical)
            sys.exit(1)

        self.app = QtSingleApplication(constant.GUID,sys.argv)
        self.log.info("---STARTING APPLICATION---")
        if self.app.isRunning():
            self.log.warning("---The launch of another instance of this application will be cancelled---")
            self.app.sendMessage()
            sys.exit(0)
        self.app.messageReceived.connect(self.another_instance_opened)
        self.app.setQuitOnLastWindowClosed(False)

        self.window = None
        self.tray_icon = None

        self.thread = None
        self.downloader = None
        self.timer = None
        self.downloader_is_running = False
        self.downloader_is_restarting = False
        self.downloader_is_stopping = False

        try:
            self.window = WindowMain(self)
            self.tray_icon = SystemTrayIcon(self,self.window)
            self.tray_icon.show()

            show_gui = "-nogui" not in sys.argv
            if show_gui:
                if self.downloader_is_running:
                    self.window.downloader_started()
                else:
                    self.window.downloader_stopped()
                self.window.show()
            elif not self.window.is_visible():
                self.log.info("STARTING DOWNLOADER")
                self.start_downloader()
            self.app.exec_()
        except Exception as unforessenError:
            self.log.critical("UNFORESSEN ERROR")
            self.log.print_traceback(unforessenError,self.log.critical)
            self.show_tray_message("Unforessen error ocurred...")
            exit()

    def quit(self):
        """
        Finishes the application gracefully - at least tries to, teehee (^_^;)
        """
        if self.tray_icon is not None:
            self.tray_icon.hide()
            self.tray_icon.deleteLater()
        if self.timer is not None:
            self.timer.stop()
        if self.thread is not None and self.thread.isRunning():
            self.stop_downloader()
        #self.app.closeAllWindows()
        self.app.quit()

    def another_instance_opened(self,_):
        """
        Called when the user tries to open another instance of the application.
        Instead of allowing it, will open the current one to avoid any errors.

        :type _: QtCore.QString
        :param _: message received, see class QtSingleApplication below.
        """
        self.window.show()

    def start_downloader(self):
        """
        Starts the downloader in a thread.
        """
        # Don't know how to reproduce, but in some really rare cases the downloader might start without the user requesting it.
        # These logs try to collect information that might help pinpoint what causes that.
        # Actually, it's been so long since the last time this error was observed that I don't know if it still happens
        # or if whatever caused it was fixed...
        self.log.debug("stack ([1][3]):")
        i=0
        for item in inspect.stack():
            self.log.debug("["+str(i)+"]= "+str(item))
            i+=1
        self.log.debug("downloader_is_running: "+str(self.downloader_is_running))
        self.log.debug("downloader_is_restarting: "+str(self.downloader_is_restarting))
        self.log.debug("downloader_is_stopping: "+str(self.downloader_is_stopping))

        if not self.downloader_is_stopping:
            if self.downloader_is_restarting:
                self.log.info("RESTARTING DOWNLOADER THREAD")
                self.downloader_is_restarting = False
            else:
                self.log.info("STARTING DOWNLOADER THREAD")
                self.window.downloader_starting()
            self.thread = QtCore.QThread(self)
            self.downloader = Downloader()
            self.downloader.moveToThread(self.thread)
            self.downloader.running.connect(self.downloader_started)
            self.downloader.finish.connect(self.thread.quit)
            self.downloader.restart.connect(self.restart_downloader)
            self.downloader.showMessage.connect(self.show_tray_message)
            self.downloader.update_ui.connect(self.update_ui)
            # noinspection PyUnresolvedReferences
            self.thread.started.connect(self.downloader.execute_once)  # PyCharm doesn't recognize started.connect()...
            # noinspection PyUnresolvedReferences
            self.thread.finished.connect(self.downloader_stopped)  # PyCharm doesn't recognize finished.connect()...
            self.thread.start()
        else:
            self.downloader_is_stopping = False
            self.downloader_is_restarting = False

    def stop_downloader(self):
        """
        Stops the downloader (¬_¬)
        """
        self.log.info("TERMINATING DOWNLOADER THREAD")
        self.window.downloader_stopping()
        self.downloader_is_stopping = True
        self.downloader_is_restarting = False
        if self.thread.isRunning():
            self.downloader.stop_thread()
            thread_stopped_gracefully = self.thread.wait(300)
            if self.thread.isRunning():
                thread_stopped_gracefully = self.thread.quit()
            self.log.info("THREAD STOPPED CORRECTLY: %s" % thread_stopped_gracefully)
            if not thread_stopped_gracefully:
                self.thread.terminate()
        else:
            self.downloader_stopped()
        try:
            self.timer.stop()
        except AttributeError:
            pass  # Happens when the downloader is interrupted before being able to fully execute at least once.

    def restart_downloader(self):
        """
        Finishes the current downloader thread and starts a timer.
        When the timer times out a new downloader thread is created.
        """
        self.downloader_is_restarting = True
        self.thread.quit()
        self.log.info("THREAD FINISHED CORRECTLY: %s" % self.thread.wait(300))
        self.timer = QtCore.QTimer()
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.start_downloader)  # PyCharm doesn't recognize timeout.connect()...
        self.timer.setSingleShot(True)
        self.timer.start(db.DBManager().get_config().sleep_time*1000)

    @QtCore.pyqtSlot()
    def downloader_started(self):
        """
        Downloader thread started correctly; notifies the user.
        """
        self.downloader_is_running = True
        self.window.downloader_started()

    @QtCore.pyqtSlot()
    def downloader_stopped(self):
        """
        Downloader thread stopped correctly; notifies the user.
        """
        if not self.downloader_is_restarting:
            self.downloader_is_running = False
            self.downloader_is_stopping = False
            self.downloader_is_restarting = False
            self.window.downloader_stopped()

    @QtCore.pyqtSlot(str)
    def show_tray_message(self,message):
        """
        Uses the system tray icon to notify the user about something.

        :type message: str
        :param message: Message to be shown to the user.
        """
        # TODO: Would it be better if this were moved to manager.system_tray_icon?
        self.tray_icon.showMessage(constant.TRAY_MESSAGE_TITLE,message,QtGui.QSystemTrayIcon.Information,5000)

    @QtCore.pyqtSlot(str)
    def update_ui(self,message):
        """
        Updates the anime table in the main window.
        Also, shows a message to the user using the system tray icon.

        :type message: str
        :param message: Message to be shown to the user.
        """
        if self.window is not None:
            self.window.update_anime_table()
        self.show_tray_message(message)


# noinspection PyPep8Naming
# ^ because it's not my class. Also, it uses the same convention as QtGui.QApplication.
class QtSingleApplication(QtGui.QApplication):
    """
    Copyright (c) 2013, user763305 (http://stackoverflow.com/questions/12712360/qtsingleapplication-for-pyside-or-pyqt)
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:
    1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
    disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
    following disclaimer in the documentation and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
    USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    """
    #http://doc.qt.digia.com/solutions/4/qtsingleapplication/qtsingleapplication.html#messageReceived
    messageReceived = QtCore.pyqtSignal(QtCore.QString)

    def __init__(self, guid, *argv):
        super(QtSingleApplication, self).__init__(*argv)
        self._id = guid
        self._activationWindow = None
        self._activateOnMessage = False

        # Is there another instance running?
        self._outSocket = QtNetwork.QLocalSocket()
        self._outSocket.connectToServer(self._id)
        self._isRunning = self._outSocket.waitForConnected()

        if self._isRunning:
            # Yes, there is.
            self._outStream = QtCore.QTextStream(self._outSocket)
            self._outStream.setCodec('UTF-8')
        else:
            # No, there isn't.
            self._outSocket = None
            self._outStream = None
            self._inSocket = None
            self._inStream = None
            self._server = QtNetwork.QLocalServer()
            self._server.listen(self._id)
            # noinspection PyUnresolvedReferences
            self._server.newConnection.connect(self._onNewConnection)  # PyCharm doesn't recognize newConnection.connect()...

    def isRunning(self):
        """
        See: http://doc.qt.digia.com/solutions/4/qtsingleapplication/qtsingleapplication.html#isRunning
        :rtype: bool
        :return: If the application is running or not.
        """
        return self._isRunning

    def sendMessage(self):
        """
        Notifies the other (already running) instance of the application so that it can be opened, while this one is discarded.
        See: http://doc.qt.digia.com/solutions/4/qtsingleapplication/qtsingleapplication.html#sendMessage
        """
        if not self._outStream:
            return False
        # noinspection PyStatementEffect
        self._outStream << ".\n"  # PyCharm doesn't recognize << operator (http://doc.qt.io/qt-4.8/qtextstream.html#operator-lt-lt-4)
        self._outStream.flush()
        self._outSocket.waitForBytesWritten()

    def _onNewConnection(self):
        if self._inSocket:
            self._inSocket.readyRead.disconnect(self._onReadyRead)
        self._inSocket = self._server.nextPendingConnection()
        if not self._inSocket:
            return
        self._inStream = QtCore.QTextStream(self._inSocket)
        self._inStream.setCodec('UTF-8')
        self._inSocket.readyRead.connect(self._onReadyRead)
        if self._activateOnMessage:
            self.activateWindow()

    def _onReadyRead(self):
        while True:
            msg = self._inStream.readLine()
            if not msg: break
            self.messageReceived.emit(msg)


if __name__ == '__main__':
    Main()