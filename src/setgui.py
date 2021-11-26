#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-11-26 15:30:02 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
import webbrowser as web
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse
import urllib.request
import datetime
import sys,json, time

from random import randint

import searchfiles
import database

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

class ProgressBar(QProgressBar):

    def __init__(self, layout, button,  arg, *args, **kwargs):
        #super(ProgressBar, self).__init__(*args, **kwargs)
        QProgressBar.__init__(self, *args, **kwargs)
        self.setValue(0)
        if self.minimum() != self.maximum():
            database.create_database(self, layout, button, arg)
            
            
    def onTimeout(self):
        if self.value() >= 100:
            self.timer.stop()
            self.timer.deleteLater()
            del self.timer
            return
        self.setValue(self.value() + 1)

class test():
        
    def mainwindow():


        mainWindow = QMainWindow()
        mainWindow.resize(1024,768)
        mainWindow.setDockOptions(_DOCK_OPTS)

        widget = QLabel("MAIN APP CONTENT AREA")
        widget.setMinimumSize(300,200)
        widget.setFrameStyle(widget.Box)
        mainWindow.setCentralWidget(widget)

        argv={'Test' : {'bookmarks' : [None],'youtube' : ['https://www.youtube.com/playlist?list=PLW5jnpyxgQHWuCRcMlfb6LuvF_vfEgkKU'],'database' : 'test/'},'Test2' : {'bookmarks' : ['Dogs'],'youtube' : [None],'database' : 'test2/'}}
        
        def addDocks(window, name, subDocks=True):
            global _DOCK_COUNT
            global _DOCK_RANGE
            
            for pos in _DOCK_POSITIONS:

                for _ in range(_DOCK_RANGE):
                    _DOCK_COUNT += 1

                    sub = QMainWindow()
                    sub.setWindowFlags(Qt.Widget)
                    sub.setDockOptions(_DOCK_OPTS)

                    if _DOCK_COUNT == 3:
                        def article_random():
                            
                            results = searchfiles.searchfiles('mr',database.databaseDict(argv)['Must Read']['database'])
                            randnum = randint(0, len(results.index))
                            for i,row in results.iterrows():
                                if randnum == i:
                                    url = row['url'].to_string(index=False)
                                    url_title = row['title'].to_string(index=False)
                                    return [url,url_title]
                        try:
                            url = article_random()[0]
                            url_title = article_random()[1]
                        except:
                            url = "https://www.google.com"
                            url_title = "ERROR: Article not found..."
                        label = QLabel("<a style='text-decoration:none;'href='{0}'>{1}</a>".format(url,url_title),toolTip = "<b>Title</b>: {1} | <b>URL</b>: <a style='text-decoration:none;'href='{0}'>{0}</a>".format(url,url_title))
                        label.setOpenExternalLinks(True)
                        label.setMinimumHeight(25)
                        label.setMaximumHeight(25)
                        sub.setCentralWidget(label)
                        dock = QDockWidget("Article of the day...")
                        dock.setMaximumHeight(25)
                        dock.setMinimumHeight(25)
                        dock.setMinimumWidth(300)
                        dock.setMaximumHeight(100)
                        dock.setWidget(sub)
                        window.addDockWidget(pos, dock)
                        
                    if _DOCK_COUNT == 4:
                        layout = QFormLayout()
                        button = QPushButton('Update')
                        dock = QDockWidget("Click to update database (may take a while)")
                        layout.addRow(button)
                        def signal_accept(msg):
                            pbar.setValue(int(msg))
                            if pbar.value() == 99:
                                pbar.setValue(0)
                        def button_pressed(clicked,date):
                            #button.deleteLater()
                            button.setEnabled(False)
                            pbar = ProgressBar(layout=layout, button=button, arg=argv, minimum=0, maximum=100, textVisible=True,objectName="BlueProgressBar")
                            pbar.deleteLater()
                            button.setText('Last updated {}'.format(date.strftime("%m/%d/%Y, %H:%M:%S")))
                            button.setEnabled(True)
                        button.clicked.connect(lambda: button_pressed(button.setEnabled(True),date = datetime.datetime.now()))
                        dock.setMinimumHeight(25)
                        dock.setMinimumWidth(300)
                        dock.setMaximumWidth(300)
                        dock.setFeatures(QDockWidget.DockWidgetMovable)
                        window.addDockWidget(pos, dock)
                        dockedWidget = QWidget(window)
                        dock.setWidget(dockedWidget)
                        dockedWidget.setLayout(layout)
                        
                    if _DOCK_COUNT == 1:
                        layout = QFormLayout()
                        le = QLineEdit()
                        le.setMinimumWidth(500)
                        
                        def selectionchange():
                            print("Current selection: ",cb.currentText())
                            return cb.currentText()
                        
                        def onRet():
                            u_inp = le.text()
                            if selectionchange() == 'Select...':
                                results = searchfiles.searchfiles(u_inp)
                                listWidget = QListWidget()
                                listWidgetItem = QListWidgetItem("Select from dropdown menu...")
                                listWidget.addItem(listWidgetItem)
                                mainWindow.setCentralWidget(listWidget)
                                return results
                            else:
                                if u_inp == '':
                                    results = searchfiles.searchfiles(u_inp)
                                    listWidget = QListWidget()
                                    listWidgetItem = QListWidgetItem("Please enter valid keyword...")
                                    listWidget.addItem(listWidgetItem)
                                    mainWindow.setCentralWidget(listWidget)
                                    return results
                                else:
                                    results = searchfiles.searchfiles(u_inp,database.databaseDict(argv)[selectionchange()]['database'])
                                    listWidget = QListWidget()
                                    listWidgetItem = QListWidgetItem("Results of keyword {}...\n".format(u_inp))
                                    listWidget.addItem(listWidgetItem)
                                    for i,row in results.iterrows():
                                        text = row['url'].to_string(index=False)
                                        #print(text)
                                        if row['type'].to_string(index=False) == 'youtube':
                                            try:
                                                with urllib.request.urlopen(text) as response:
                                                    response_text = response.read()
                                                    data = json.loads(response_text.decode())
                                            except urllib.error.HTTPError as e:
                                                if e.code in (..., 403, ...):
                                                    continue
                                            soup = BeautifulSoup(data['html'],"html.parser")
                                            url = soup.find("iframe")["src"]
                                            url_title = row['title'].to_string(index=False)
                                            listWidgetItem = QListWidgetItem("\t{0}. {1}".format((i+1),url_title))
                                            listWidgetItem.setToolTip("Title:{1} | URL:{0} | TYPE:{2}".format(url,url_title,row['type'].to_string(index=False)))
                                            listWidget.addItem(listWidgetItem)
                                        else:
                                            url = row['url'].to_string(index=False)
                                            url_title = row['title'].to_string(index=False)
                                            listWidgetItem = QListWidgetItem("\t{0}. {1}".format((i+1),url_title))
                                            listWidgetItem.setToolTip("Title:{1} | URL:{0} | TYPE:{2}".format(url,url_title,row['type'].to_string(index=False)))
                                            listWidget.addItem(listWidgetItem)
                                    def OpenLink(url):
                                        url = url.split('URL:')[1]
                                        print(url)
                                        web.open(url)
                                    listWidget.itemDoubleClicked.connect(lambda: OpenLink(listWidget.currentItem().toolTip()))
                                    listWidget.setWordWrap(True)
                                    mainWindow.setCentralWidget(listWidget)
                                    return results

                        le.returnPressed.connect(onRet)

                        cb = QComboBox()
                        cb.setMaximumWidth(200)
                        cb.addItem('Select...')
                        cb.addItems(list(database.databaseDict(argv).keys()))
                        cb.currentIndexChanged.connect(selectionchange)
                        layout.addRow(le,cb)
                        dock = QDockWidget("Search keyword below")
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
                        dock.setMaximumWidth(300)
                        dock.setMaximumHeight(500)
                        dock.setWidget(sub)
                        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
                        window.addDockWidget(pos, dock)
                        if DO_SUB_DOCK_CREATION and subDocks:
                            addDocks(sub, "Sub Dock", subDocks=False)
                            window.addDockWidget(pos, dock)
                    else:


                        if DO_SUB_DOCK_CREATION and subDocks:
                            addDocks(sub, "Sub Dock", subDocks=False)
                            window.addDockWidget(pos, dock)

        addDocks(mainWindow, "Custom Search")

        mainWindow.show()
        mainWindow.raise_()
                    
        return mainWindow
    
# Define a stream, custom class, that reports data written to it, with a Qt signal
class EmittingStream(QObject):

    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))
    
            
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
