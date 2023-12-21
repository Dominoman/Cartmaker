# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QTableView, QToolBar, QVBoxLayout, QWidget)
import icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionE_xit = QAction(MainWindow)
        self.actionE_xit.setObjectName(u"actionE_xit")
        icon = QIcon()
        icon.addFile(u":/Buttons/door", QSize(), QIcon.Normal, QIcon.Off)
        self.actionE_xit.setIcon(icon)
        self.actionAdd_file_s = QAction(MainWindow)
        self.actionAdd_file_s.setObjectName(u"actionAdd_file_s")
        icon1 = QIcon()
        icon1.addFile(u":/Buttons/add", QSize(), QIcon.Normal, QIcon.Off)
        self.actionAdd_file_s.setIcon(icon1)
        self.actionAdd_file_s.setMenuRole(QAction.NoRole)
        self.actionDelete_file_s = QAction(MainWindow)
        self.actionDelete_file_s.setObjectName(u"actionDelete_file_s")
        self.actionDelete_file_s.setEnabled(False)
        icon2 = QIcon()
        icon2.addFile(u":/Buttons/delete", QSize(), QIcon.Normal, QIcon.Off)
        self.actionDelete_file_s.setIcon(icon2)
        self.actionDelete_file_s.setMenuRole(QAction.NoRole)
        self.actionUp = QAction(MainWindow)
        self.actionUp.setObjectName(u"actionUp")
        self.actionUp.setEnabled(False)
        icon3 = QIcon()
        icon3.addFile(u":/Buttons/up", QSize(), QIcon.Normal, QIcon.Off)
        self.actionUp.setIcon(icon3)
        self.actionUp.setMenuRole(QAction.NoRole)
        self.actionDown = QAction(MainWindow)
        self.actionDown.setObjectName(u"actionDown")
        self.actionDown.setEnabled(False)
        icon4 = QIcon()
        icon4.addFile(u":/Buttons/down", QSize(), QIcon.Normal, QIcon.Off)
        self.actionDown.setIcon(icon4)
        self.actionDown.setMenuRole(QAction.NoRole)
        self.action_Open_crt = QAction(MainWindow)
        self.action_Open_crt.setObjectName(u"action_Open_crt")
        icon5 = QIcon()
        icon5.addFile(u":/Buttons/folder", QSize(), QIcon.Normal, QIcon.Off)
        self.action_Open_crt.setIcon(icon5)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.horizontalHeader().setCascadingSectionResizes(True)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.tableView)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")

        self.verticalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName(u"menu_File")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setEnabled(True)
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.toolBar.setFloatable(False)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menu_File.addAction(self.action_Open_crt)
        self.menu_File.addAction(self.actionAdd_file_s)
        self.menu_File.addAction(self.actionDelete_file_s)
        self.menu_File.addAction(self.actionUp)
        self.menu_File.addAction(self.actionDown)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionE_xit)
        self.toolBar.addAction(self.actionAdd_file_s)
        self.toolBar.addAction(self.actionDelete_file_s)
        self.toolBar.addAction(self.actionUp)
        self.toolBar.addAction(self.actionDown)

        self.retranslateUi(MainWindow)
        self.actionE_xit.triggered.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CRT Builder", None))
        self.actionE_xit.setText(QCoreApplication.translate("MainWindow", u"E&xit", None))
        self.actionAdd_file_s.setText(QCoreApplication.translate("MainWindow", u"Add file(s)...", None))
#if QT_CONFIG(shortcut)
        self.actionAdd_file_s.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+A", None))
#endif // QT_CONFIG(shortcut)
        self.actionDelete_file_s.setText(QCoreApplication.translate("MainWindow", u"Delete file(s)", None))
#if QT_CONFIG(shortcut)
        self.actionDelete_file_s.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+D", None))
#endif // QT_CONFIG(shortcut)
        self.actionUp.setText(QCoreApplication.translate("MainWindow", u"Up", None))
#if QT_CONFIG(shortcut)
        self.actionUp.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Up", None))
#endif // QT_CONFIG(shortcut)
        self.actionDown.setText(QCoreApplication.translate("MainWindow", u"Down", None))
#if QT_CONFIG(shortcut)
        self.actionDown.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Down", None))
#endif // QT_CONFIG(shortcut)
        self.action_Open_crt.setText(QCoreApplication.translate("MainWindow", u"&Open crt...", None))
#if QT_CONFIG(shortcut)
        self.action_Open_crt.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.menu_File.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

