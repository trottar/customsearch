#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-11-18 22:43:00 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from random import randint

# Set to False - Standard docking of widgets around the main content area
# Set to True - Sub MainWindows each with their own private docking 
DO_SUB_DOCK_CREATION = True


_DOCK_OPTS = QMainWindow.AnimatedDocks
_DOCK_OPTS |= QMainWindow.AllowNestedDocks
_DOCK_OPTS |= QMainWindow.AllowTabbedDocks


_DOCK_COUNT = 0
'''
_DOCK_POSITIONS = (
    Qt.LeftDockWidgetArea,
    Qt.TopDockWidgetArea,
    Qt.RightDockWidgetArea,
    Qt.BottomDockWidgetArea
)
'''
_DOCK_POSITIONS = (
    Qt.TopDockWidgetArea,
    Qt.RightDockWidgetArea,
)

# Number of docks per area (eg. 2 in Qt.LeftDockWidgetArea if set to 2)
_DOCK_RANGE = 1


class test():
        
    def mainwindow():


        mainWindow = QMainWindow()
        mainWindow.resize(1024,768)
        mainWindow.setDockOptions(_DOCK_OPTS)

        widget = QLabel("MAIN APP CONTENT AREA")
        widget.setMinimumSize(300,200)
        widget.setFrameStyle(widget.Box)
        mainWindow.setCentralWidget(widget)
        
        def addDocks(window, name, subDocks=True):
            global _DOCK_COUNT
            global _DOCK_RANGE
            
            for pos in _DOCK_POSITIONS:

                for _ in range(_DOCK_RANGE):
                    _DOCK_COUNT += 1

                    sub = QMainWindow()
                    sub.setWindowFlags(Qt.Widget)
                    sub.setDockOptions(_DOCK_OPTS)
                        
                    if _DOCK_COUNT == 3 or _DOCK_COUNT == 4:
                        url = 'https://www.google.com'
                        url_title = 'Google'
                        label = QLabel("<a style='text-decoration:none;'href='{0}'>{1}</a>".format(url,url_title),toolTip = "<b>Title</b>: {1} | <b>URL</b>: <a style='text-decoration:none;'href='{0}'>{0}</a>".format(url,url_title))
                        label.setOpenExternalLinks(True)
                        label.setMinimumHeight(25)
                        label.setMaximumHeight(25)
                    #else:
                        #label = QLabel("%s %d content area" % (name, _DOCK_COUNT), sub)
                        #label.setMinimumHeight(25)
                        #label.setStyleSheet("background-color: rgb(%d, %d, %d)" % color)
                        sub.setCentralWidget(label)

                    if _DOCK_COUNT == 1:
                        layout = QFormLayout()
                        le = QLineEdit()
                        le.setMinimumWidth(500)

                        def onClick():
                            u_inp = le.text()
                            url_title = u_inp
                            print(u_inp)

                        le.returnPressed.connect(onClick)

                        def selectionchange():
                            print("Items in the list are :")

                            for count in range(cb.count()):
                                print(cb.itemText(count))
                            print("Current selection: ",cb.currentText())
                            return cb.currentText()         

                        cb = QComboBox()
                        cb.setMaximumWidth(200)
                        cb.addItem("Physics")
                        cb.addItems(["Coding", "Thesis", "Misc"])
                        cb.currentIndexChanged.connect(selectionchange)
                        layout.addRow(le,cb)
                        dock = QDockWidget("%s %d title bar" % (name, _DOCK_COUNT))
                        dock.setMinimumHeight(25)
                        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
                        window.addDockWidget(pos, dock)
                        dockedWidget = QWidget(window)
                        dock.setWidget(dockedWidget)
                        dockedWidget.setLayout(layout)
                    elif _DOCK_COUNT == 2:
                        dock = QDockWidget("")
                        #dock.setMaximumHeight(25)
                        dock.setMinimumHeight(25)
                        dock.setMinimumWidth(300)
                        dock.setMaximumHeight(100)
                        dock.setWidget(sub)
                        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
                        window.addDockWidget(pos, dock)
                        if DO_SUB_DOCK_CREATION and subDocks:
                            addDocks(sub, "Sub Dock", subDocks=False)
                            window.addDockWidget(pos, dock)
                    else:
                        dock = QDockWidget("%s %d title bar" % (name, _DOCK_COUNT))
                        #dock.setMaximumHeight(25)
                        dock.setMinimumHeight(25)
                        dock.setMinimumWidth(300)
                        dock.setMaximumHeight(100)
                        dock.setWidget(sub)
                        window.addDockWidget(pos, dock)

                        if DO_SUB_DOCK_CREATION and subDocks:
                            addDocks(sub, "Sub Dock", subDocks=False)
                            window.addDockWidget(pos, dock)

        addDocks(mainWindow, "Main Dock")

        mainWindow.show()
        mainWindow.raise_()
                    
        return mainWindow
                    
            
def main(): 
   app = QApplication(sys.argv)
   app.setStyle('WindowsVista')
   qp = QPalette()
   qp.setColor(QPalette.ButtonText, Qt.black)
   qp.setColor(QPalette.Window, Qt.gray)
   qp.setColor(QPalette.Button, Qt.gray)
   app.setPalette(qp)

   mainwindow = test.mainwindow()
   mainwindow.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
