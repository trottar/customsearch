#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-12-02 01:23:12 trottar"
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
import subprocess
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
    Qt.BottomDockWidgetArea,
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

def clickable(widget):

    class Filter(QObject):
    
        clicked = pyqtSignal()
        
        def eventFilter(self, obj, event):
        
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True
            
            return False
    
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked        

class GUI():
        
    def mainwindow():


        mainWindow = QMainWindow()
        mainWindow.resize(1024,768)
        mainWindow.setDockOptions(_DOCK_OPTS)

        widget = QLabel("MAIN APP CONTENT AREA")
        widget.setMinimumSize(200,200)
        widget.setFrameStyle(widget.Box)
        mainWindow.setCentralWidget(widget)
            
        def update_log(argv):
            s_argv = {i : argv[i] for i in sorted(argv.keys())}
            df = pd.DataFrame.from_dict(s_argv, orient='index')
            df = df.to_csv('log/database_topics.log')
            sys.exit(0)
        
        def update_argv():

            f_name = "log/database_topics.log"
            try:
                up_d = {}
                inp_d = pd.read_csv(f_name)
                for i,row in inp_d.iterrows():
                    key = row.iloc[0].strip()
                    bookmarks = row.iloc[1].strip().strip("[").strip("]").strip("'")
                    if 'None' in bookmarks:
                        bookmarks = None
                    youtube = row.iloc[2].strip().strip("[").strip("]").strip("'")
                    if 'None' in youtube:
                        youtube = None
                    pdf = row.iloc[3].strip().strip("[").strip("]").strip("'")
                    if 'None' in pdf:
                        pdf = None                        
                    database = row.iloc[4].strip().strip("[").strip("]").strip("'")
                    up_d.update({key : {'bookmarks' : [bookmarks], 'youtube' : [youtube], 'pdf' : [pdf], 'database' : database}})
            except pd.errors.EmptyDataError:
                up_d = {}

            return up_d
        
        #argv={'Test' : {'bookmarks' : [None],'youtube' : ['https://www.youtube.com/playlist?list=PLW5jnpyxgQHWuCRcMlfb6LuvF_vfEgkKU'],'pdf' : ['analysis_notes_Yero.pdf'],'database' : 'test/'}}
        argv = update_argv()

        def add_topic(name,bookmarks,youtube,pdf):
            database = name.replace(' ','_').lower()
            if ',' in bookmarks:
                bookmarks = bookmarks.split(',')
            elif ',' not in bookmarks:
                if not bookmarks:                
                    bookmarks = [None]
                else:
                    bookmarks = [bookmarks]
            if ',' in youtube:
                youtube = youtube.split(',')
            elif ',' not in youtube:
                if not youtube:                
                    youtube = [None]
                else:
                    youtube = [youtube]
            if ',' in pdf:
                pdf = pdf.split(',')
            elif ',' not in pdf:
                if not pdf:                
                    pdf = [None]
                else:
                    pdf = [pdf]                    
            argv.update({name : {'bookmarks' : bookmarks, 'youtube' : youtube, 'pdf' : pdf, 'database' : '{}/'.format(database)}})
                
            update_log(argv)
                    
        
        def addDocks(window, name, subDocks=True):
            global _DOCK_COUNT
            global _DOCK_RANGE
            
            for pos in _DOCK_POSITIONS:

                for _ in range(_DOCK_RANGE):
                    _DOCK_COUNT += 1

                    sub = QMainWindow()
                    sub.setWindowFlags(Qt.Widget)
                    sub.setDockOptions(_DOCK_OPTS)

                    if _DOCK_COUNT == 4:
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
                        label.setWordWrap(True)
                        label.setMinimumHeight(25)
                        label.setMaximumHeight(50)
                        sub.setCentralWidget(label)
                        dock = QDockWidget("Article of the day...")
                        dock.setMaximumHeight(25)
                        dock.setMinimumHeight(50)
                        dock.setMinimumWidth(300)
                        dock.setWidget(sub)
                        window.addDockWidget(pos, dock)
                        
                    if _DOCK_COUNT == 5:
                        layout = QFormLayout()
                        button = QPushButton("Submit (window will close on update)")
                        le1 = QLineEdit()
                        le2 = QLineEdit()
                        le3 = QLineEdit()
                        le4 = QLineEdit()
                        layout.addRow("Name: ",le1)
                        layout.addRow("bookmarks: ",le2)
                        layout.addRow("youtube: ",le3)
                        layout.addRow("pdf: ",le4)
                        layout.addRow(button)
                        def button_pressed(clicked):
                            button.setEnabled(False)
                            if not le1.text():
                                print('No entries entered')
                                button.setText('Please enter entries above...'.format(le1.text()))                                
                            else:
                                add_topic(le1.text(),le2.text(),le3.text(),le4.text())
                                pbar = ProgressBar(layout=layout, button=button, arg=argv, minimum=0, maximum=100, textVisible=True,objectName="BlueProgressBar")
                                pbar.deleteLater()
                            le1.clear()
                            le2.clear()
                            le3.clear()
                            le4.clear()
                            button.setEnabled(True)
                        button.clicked.connect(lambda: button_pressed(button.setEnabled(True)))
                        dock = QDockWidget("Create database topic")
                        dock.setMinimumHeight(25)
                        dock.setMinimumWidth(300)
                        dock.setWidget(sub)
                        window.addDockWidget(pos, dock)
                        dockedWidget = QWidget(window)
                        dock.setWidget(dockedWidget)
                        dockedWidget.setLayout(layout)                        
                         
                    if _DOCK_COUNT == 6:
                        layout = QFormLayout()
                        button = QPushButton('Update')
                        dock = QDockWidget("Click to update database (may take a while)")
                        layout.addRow(button)
                        def signal_accept(msg):
                            pbar.setValue(int(msg))
                            if pbar.value() == 99:
                                pbar.setValue(0)
                        def button_pressed(clicked,date):
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
                            if cb.currentText() != 'Calculator' and cb.currentText() != 'Select...' :
                                with open('log/search_history.log') as f:
                                    history = f.read().splitlines()
                                completer = QCompleter(history)
                                completer.setCaseSensitivity(Qt.CaseInsensitive)
                                le.setCompleter(completer)
                            else:
                                completer = QCompleter([])
                                le.setCompleter(completer)
                            print("Current selection: ",cb.currentText())
                            return cb.currentText()
                        
                        def onRet():
                            u_inp = le.text().lower()
                            if selectionchange() == 'Select...':
                                results = searchfiles.searchfiles(u_inp)
                                scrollWidget = QListWidget()
                                listWidget = QListWidget()
                                listWidgetItem = QListWidgetItem("Select from dropdown menu...")
                                listWidgetItem.setFlags(Qt.ItemIsSelectable)
                                listWidget.addItem(listWidgetItem)
                                listWidget.setStyleSheet("border : none;")
                                scroll_bar = QScrollArea(scrollWidget)
                                scrollAreaWidgetContents = QWidget()
                                scrollAreaWidgetContents.setGeometry(QRect(0, 0, listWidget.sizeHintForColumn(0)+20, listWidget.sizeHintForRow(0)+20))
                                scroll_bar.setWidget(scrollAreaWidgetContents)
                                scroll_bar.setMinimumHeight(635)
                                scroll_bar.setMinimumWidth(720)
                                layout = QHBoxLayout(scrollAreaWidgetContents)
                                layout.addWidget(listWidget)
                                scrollWidget.setStyleSheet("background : lightgrey;")
                                mainWindow.setCentralWidget(scrollWidget)
                                return results
                            
                            elif selectionchange() == "Calculator":
                                def CopyLink(results):
                                    clipboard = QApplication.clipboard()
                                    clipboard.setText(results)
                                cmd = ['./Genius/run_genius.sh','{}'.format(u_inp)]
                                results = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
                                scrollWidget = QListWidget()
                                listWidget = QListWidget()
                                listWidgetItem = QListWidgetItem(results)
                                listWidget.addItem(listWidgetItem)
                                listWidget.setStyleSheet("border : none;")
                                scroll_bar = QScrollArea(scrollWidget)                                
                                scrollAreaWidgetContents = QWidget()
                                scrollAreaWidgetContents.setGeometry(QRect(0, 0, listWidget.sizeHintForColumn(0)+20, listWidget.sizeHintForRow(0)+20))
                                scroll_bar.setWidget(scrollAreaWidgetContents)
                                scroll_bar.setMinimumHeight(635)
                                scroll_bar.setMinimumWidth(720)
                                layout = QHBoxLayout(scrollAreaWidgetContents)
                                listWidget.itemClicked.connect(lambda: CopyLink(results))
                                layout.addWidget(listWidget)
                                scrollWidget.setStyleSheet("background : lightgrey;")
                                mainWindow.setCentralWidget(scrollWidget)                        
                                return results
                            
                            else:
                                def CopyLink(listwidget,url):
                                    if listwidget.text() == "Results of keyword {}...\n".format(u_inp):
                                        print("")
                                    else:
                                        url = url.split('URL:')[1].split('| TYPE:')[0].strip(' ')
                                        print(url)
                                        clipboard = QApplication.clipboard()
                                        clipboard.setText(url)
                                if u_inp == '':
                                    results = searchfiles.searchfiles(u_inp)
                                    scrollWidget = QListWidget()
                                    listWidget = QListWidget()
                                    listWidgetItem = QListWidgetItem("Please enter valid keyword...")
                                    listWidget.addItem(listWidgetItem)
                                    listWidget.setStyleSheet("border : none;")
                                    scroll_bar = QScrollArea(scrollWidget)
                                    scrollAreaWidgetContents = QWidget()
                                    scrollAreaWidgetContents.setGeometry(QRect(0, 0, listWidget.sizeHintForColumn(0)+20, listWidget.sizeHintForRow(0)+20))
                                    scroll_bar.setWidget(scrollAreaWidgetContents)
                                    scroll_bar.setMinimumHeight(635)
                                    scroll_bar.setMinimumWidth(720)
                                    layout = QHBoxLayout(scrollAreaWidgetContents)
                                    layout.addWidget(listWidget)
                                    scrollWidget.setStyleSheet("background : lightgrey;")
                                    mainWindow.setCentralWidget(scrollWidget)
                                    return results
                                else:
                                    results = searchfiles.searchfiles(u_inp,database.databaseDict(argv)[selectionchange()]['database'])
                                    scrollWidget = QListWidget()
                                    listWidget = QListWidget()
                                    listWidgetItem = QListWidgetItem("Results of keyword {}...\n".format(u_inp))
                                    listWidget.addItem(listWidgetItem)
                                    listWidget.setStyleSheet("border : none;")
                                    scroll_bar = QScrollArea(scrollWidget)                                    
                                    scrollAreaWidgetContents = QWidget()
                                    scroll_bar.setWidget(scrollAreaWidgetContents)
                                    scroll_bar.setMinimumHeight(635)
                                    scroll_bar.setMinimumWidth(720)
                                    layout = QHBoxLayout(scrollAreaWidgetContents)

                                    for i,row in results.iterrows():
                                        with open('log/search_history.log', 'r+') as f:
                                            if u_inp not in f.read():
                                                f.write(u_inp + '\n')
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
                                            scrollAreaWidgetContents.setGeometry(QRect(0, 0, listWidget.sizeHintForColumn(0)+50, listWidget.sizeHintForRow(0)*i+20))
                                        else:
                                            url = row['url'].to_string(index=False)
                                            url_title = row['title'].to_string(index=False)
                                            listWidgetItem = QListWidgetItem("\t{0}. {1}".format((i+1),url_title))
                                            listWidgetItem.setToolTip("Title:{1} | URL:{0} | TYPE:{2}".format(url,url_title,row['type'].to_string(index=False)))
                                            listWidget.addItem(listWidgetItem)
                                            scrollAreaWidgetContents.setGeometry(QRect(0, 0, listWidget.sizeHintForColumn(0)+50, listWidget.sizeHintForRow(0)*i+20))
                                    def OpenLink(listwidget,url):
                                        if listwidget.text() == "Results of keyword {}...\n".format(u_inp):
                                            print("")
                                        else:
                                            url = url.split('URL:')[1]
                                            print(url)
                                            if url.split('TYPE:')[1] == 'pdf':
                                                cmd = ['evince','{}'.format(url.split('| TYPE:')[0].strip(' '))]
                                                subprocess.run(cmd)
                                            else:
                                                web.open(url)
                           
                                    listWidget.itemDoubleClicked.connect(lambda: OpenLink(listWidget.currentItem(),listWidget.currentItem().toolTip()))
                                    listWidget.itemClicked.connect(lambda: CopyLink(listWidget.currentItem(),listWidget.currentItem().toolTip()))
                                    layout.addWidget(listWidget)
                                    scrollWidget.setStyleSheet("background : lightgrey;")
                                    mainWindow.setCentralWidget(scrollWidget)
                                    return results

                        cb = QComboBox()
                        cb.setMaximumWidth(200)
                        cb.addItem('Select...')
                        cb.addItem('Calculator')
                        cb.addItems(list(database.databaseDict(argv).keys()))
                        cb.currentIndexChanged.connect(selectionchange)
                        le.returnPressed.connect(onRet)
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
        
def main(): 
   app = QApplication(sys.argv)
   app.setStyle('WindowsVista')
   qp = QPalette()
   qp.setColor(QPalette.ButtonText, Qt.black)
   qp.setColor(QPalette.Window, Qt.gray)
   qp.setColor(QPalette.Button, Qt.gray)
   app.setPalette(qp)

   mainwindow = GUI.mainwindow()
   mainwindow.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
