#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-05-13 00:13:11 trottar"
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
import rss

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

    def __init__(self, layout,  arg, *args, **kwargs):
        QProgressBar.__init__(self, *args, **kwargs)
        self.setAlignment(Qt.AlignCenter)
        self.setValue(0)
        if self.minimum() != self.maximum():
            database.create_database(self, layout, arg)
            
            
    def onTimeout(self):
        if self.value() >= 100:
            self.timer.stop()
            self.timer.deleteLater()
            del self.timer
            return
        self.setValue(self.value() + 1)
        
class CompleterDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(CompleterDelegate, self).initStyleOption(option, index)
        option.palette.setColor(QPalette.Active, QPalette.Highlight, QColor(150, 150, 150))
        option.palette.setColor(QPalette.Active, QPalette.HighlightedText, QColor(0, 0, 0))
        option.displayAlignment = Qt.AlignCenter
        
class GUI(object):
            
    def retranslateUi(self, mainWindow):
        _translate = QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "mainWindow"))
    
    def mainwindow(self, mainWindow):

        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1224,968)
        mainWindow.setDockOptions(_DOCK_OPTS)
        mainWindow.setWindowTitle("Custom Search");
        mainWindow.setWindowFlags(Qt.FramelessWindowHint)
        
        mainWindow.mouseMoveEvent = self.mouseMoveEvent
        self.retranslateUi(mainWindow)
        QMetaObject.connectSlotsByName(mainWindow)
        
        menuBar = mainWindow.menuBar()
        closewidget = QWidget()
        closewidget.setStyleSheet('''
        QWidget {border-width: 0px;}
        ''')
        layout = QFormLayout()
        
        def minimize_pressed():
            mainWindow.setWindowState(Qt.WindowMinimized)
        
        menuTopMinimizeButton = QPushButton()
        menuTopCloseButton = QPushButton()
        menuTopMinimizeButton.setStyleSheet("*{border-image: url(icons/normal.png);background-color: rgb(100, 150, 150);width: 14px;height: 14px;border:4px outset;  border-radius: 8px;}"":pressed{ border-image: url(icons/normal.png);background-color: rgb(150, 150, 150);border:2px outset;}"":hover{ border-image: url(icons/normal.png);background-color: rgb(150, 150, 150)};")
        menuTopCloseButton.setStyleSheet("*{border-image: url(icons/close.png);background-color: rgb(100, 150, 150);width: 14px;height: 14px;border:4px outset;  border-radius: 8px;}"":pressed{ border-image: url(icons/close.png);background-color: rgb(150, 150, 150);border:2px outset;}"":hover{ border-image: url(icons/close.png);background-color: rgb(150, 150, 150);}")

        menuTopMinimizeButton.clicked.connect(minimize_pressed)
        menuTopCloseButton.clicked.connect(QApplication.instance().quit)
        
        layout.addRow(menuTopMinimizeButton,menuTopCloseButton)
        menuBar.setCornerWidget(closewidget, Qt.TopRightCorner)
        closewidget.setLayout(layout)
        
        helpMenu = menuBar.addMenu("&Help")
        shortcutMenu = helpMenu.addMenu("Shortcuts")
        shortcutMenu.addAction("Quit:\tCtrl+q".expandtabs(35))
        shortcutMenu.addAction("Search Bar:\tCtrl+s".expandtabs(29))
        shortcutMenu.addAction("Search Results:\tCtrl+r".expandtabs(25))
        shortcutMenu.addAction("Article of Day:\tCtrl+o".expandtabs(26))
        shortcutMenu.addAction("arXiv:\tCtrl+l".expandtabs(35))
        shortcutMenu.addAction("New Entry:\tCtrl+n".expandtabs(28))
        shortcutMenu.addAction("Update Database:\tCtrl+g".expandtabs(20))
        shortcutMenu.addAction("Dropdown Menu:\tCtrl+d".expandtabs(20))
        shortcutMenu.addAction("Enter 'all' in search to see all data for a dropdown topic")

        mainWindow.setContextMenuPolicy(Qt.ActionsContextMenu)
        mainWindow.addAction(QAction("&Help",mainWindow))
        separator = QAction(mainWindow)
        separator.setSeparator(True)
        mainWindow.addAction(separator)
        mainWindow.addAction(QAction("Quit:\tCtrl+q".expandtabs(35),mainWindow))
        mainWindow.addAction(QAction("Search Bar:\tCtrl+s".expandtabs(29),mainWindow))
        mainWindow.addAction(QAction("Search Results:\tCtrl+r".expandtabs(25),mainWindow))
        mainWindow.addAction(QAction("Article of Day:\tCtrl+o".expandtabs(26),mainWindow))
        mainWindow.addAction(QAction("arXiv:\tCtrl+l".expandtabs(35),mainWindow))
        mainWindow.addAction(QAction("New Entry:\tCtrl+n".expandtabs(28),mainWindow))
        mainWindow.addAction(QAction("Update Database:\tCtrl+g".expandtabs(20),mainWindow))
        mainWindow.addAction(QAction("Dropdown Menu:\tCtrl+d".expandtabs(20),mainWindow))
        mainWindow.addAction(QAction("Enter 'all' in search to see all data for a dropdown topic",mainWindow))
        
        quit_shortcut = QShortcut(QKeySequence("Ctrl+q"),mainWindow)
        quit_shortcut.activated.connect(QApplication.instance().quit)

        widget = QLabel("Welcome back, Richard!")
        widget.setMinimumSize(200,200)
        widget.setFrameStyle(widget.Box)
        mainWindow.setCentralWidget(widget)
        style = QApplication.style().standardIcon(QStyle.SP_DialogApplyButton)
        mainWindow.setStyleSheet('''
        QMainWindow {background: transparent;}
        QWidget, QListWidgetItem, QHBoxLayout, QScrollArea, QListWidget, QLineEdit{border:4px outset;  border-radius: 8px; border-color: rgb(50, 120, 120);  color: rgb(50, 0, 0);  background-color: rgb(50, 50, 50);}
        QDockWidget:close-button{background-color: rgb(50, 120, 120); subcontrol-position: right; right:10px;}
        QDockWidget:close-button:hover{background-color: rgb(150, 150, 150);}
        QDockWidget:float-button{background-color: rgb(50, 120, 120);subcontrol-position: right; right:30px;}
        QDockWidget:float-button:hover{background-color: rgb(150, 150, 150);}
        QLabel:hover, QMenu:item:selected, QMenuBar:item:selected, QListWidget:item:hover, QPushButton:hover, QLineEdit:hover, QComboBox:hover, QComboBox:item:selected{border:4px outset;  border-radius: 8px; border-color: rgb(100, 150, 150);  color: rgb(50, 0, 0);  background-color: rgb(150, 150, 150);}
        QMenu:item:pressed, QMenuBar:item:pressed, QPushButton:focus, QListWidget:item:focus, QLineEdit:focus{border:4px outset;  border-radius: 8px; border-color: rgb(100, 150, 150);  color: rgb(100, 150, 150);  background-color: rgb(50, 25, 25);}
        QScrollBar{border:4px outset;  border-radius: 8px; border-color: rgb(50, 120, 120);  color: rgb(50, 0, 0);  background-color: rgb(50, 120, 120);}
        QComboBox:drop-down{border-width: 0px;}
        QComboBox, QLineEdit, QListWidget, QPushButton, QLabel, QToolTip{color: rgb(100, 150, 150); font-weight: bold;font-size: 14pt; selection-background-color: rgb(150, 150, 150); selection-color: rgb(0, 0, 0);}
        QMenuBar, QMenu:item, QMenuBar:item{color: rgb(100, 150, 150); font-weight: bold;font-size: 14pt; selection-background-color: rgb(150, 150, 150); selection-color: rgb(0, 0, 0);}
        QDockWidget{titlebar-close-icon: url(icons/close.png); titlebar-normal-icon: url(icons/normal.png); color: rgb(100, 150, 150); font-weight: bold;font-size: 14pt; selection-background-color: rgb(150, 150, 150); selection-color: rgb(0, 0, 0);}
        QProgressBar{color: rgb(100, 150, 150); font-weight: bold; font-size: 14pt; selection-background-color: rgb(150, 150, 150); selection-color: rgb(0, 0, 0);}
        ''')
        
        def update_log(argv):
            argv = {i : argv[i] for i in sorted(argv.keys())}
            for i in sorted(argv.keys()):
                for key in argv[i]:
                    if key != 'database':
                        argv[i][key] = str(argv[i][key]).replace(',','&').replace(" '","'")
            df = pd.DataFrame.from_dict(argv, orient='index')
            df = df.to_csv('log/database_topics.log')
            sys.exit(0)
        
        def update_argv():

            f_name = "log/database_topics.log"
            try:
                up_d = {}
                inp_d = pd.read_csv(f_name)
                result = {}
                for i,row in inp_d.iterrows():
                    key = row.iloc[0].strip()
                    bookmarks = row.iloc[1].strip().strip("[").strip("]").replace("'",'').replace('&',',')
                    if 'None' in bookmarks:
                        bookmarks = [None]
                    else:
                        bookmarks = bookmarks.split(',')
                    youtube = row.iloc[2].strip().strip("[").strip("]").replace("'",'').replace('&',',')
                    if 'None' in youtube:
                        youtube = [None]
                    else:
                        youtube = youtube.split(',')
                    pdf = row.iloc[3].strip().strip("[").strip("]").replace("'",'').replace('&',',')
                    if 'None' in pdf:
                        pdf = [None]
                    else:
                        pdf = pdf.split(',')
                    database = row.iloc[4].strip().strip("[").strip("]").strip("'")
                    up_d.update({key : {'bookmarks' : bookmarks, 'youtube' : youtube, 'pdf' : pdf, 'database' : database}})
            except pd.errors.EmptyDataError:
                up_d = {}

            return up_d
        
        argv = update_argv()

        def add_topic(name,bookmarks,youtube,pdf):
            database = name.replace(' ','_').lower()
            if ',' in bookmarks:
                bookmarks = str(bookmarks.split(',')).replace(',','&').strip('')
            elif ',' not in bookmarks:
                if not bookmarks:                
                    bookmarks = [None]
                else:
                    bookmarks = [bookmarks]
            if ',' in youtube:
                youtube = str(youtube.split(',')).replace(',','&').strip('')
            elif ',' not in youtube:
                if not youtube:                
                    youtube = [None]
                else:
                    youtube = [youtube]
            if ',' in pdf:
                pdf = str(pdf.split(',')).replace(',','&').strip('')
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
                    
                    if _DOCK_COUNT == 3:
                        def article_random():
                            
                            results = searchfiles.searchfiles('mr',database.databaseDict(argv)['Must Read']['database'])
                            randnum = randint(0, len(results.index)-1)
                            for i,row in results.iterrows():
                                if randnum == i:
                                    link = row['url'].to_string(index=False)
                                    url_title = row['title'].to_string(index=False)
                                    return [link,url_title]
                        try:
                            link = article_random()[0]
                            url_title = article_random()[1]
                        except:
                            link = "https://www.google.com"
                            url_title = "ERROR: Article not found..."
                        label = QLabel("<a style='text-decoration:none;'href='{0}'; style='color:#33CAFF'>{1}</a>".format(link,url_title),toolTip = "<b>Title</b>: {1} | <b>URL</b>: <a style='text-decoration:none;'href='{0}'; style='color:rgb(100, 150, 150)'>{0}</a>".format(link,url_title))
                        label.setOpenExternalLinks(True)
                        label.setWordWrap(True)
                        label.setMinimumHeight(25)
                        label.setMaximumHeight(100)
                        def selectlink():
                            web.open(link.strip(' '))
                        link_shortcut = QShortcut(QKeySequence("Ctrl+o"),label)
                        link_shortcut.activated.connect(selectlink)
                        sub.setCentralWidget(label)
                        dock = QDockWidget("Article of the day...")
                        dock.setMinimumHeight(115)
                        dock.setMaximumHeight(115)
                        dock.setMinimumWidth(500)
                        dock.setMaximumWidth(500)
                        dock.setWidget(sub)
                        window.addDockWidget(pos, dock)
                    
                    if _DOCK_COUNT == 4:
                        def CopyLink(listwidget,listwidgetitem,url):
                            listwidget.clearSelection()
                            url = url.split('URL:')[1].split('| TYPE:')[0].strip(' ')
                            print(url)
                            clipboard = QApplication.clipboard()
                            clipboard.setText(url)
                        scrollWidget = QListWidget()
                        listWidget = QListWidget()
                        scroll_bar = QScrollArea(scrollWidget)
                        scrollAreaWidgetContents = QWidget()
                        scroll_bar.setWidget(scrollAreaWidgetContents)
                        scroll_bar.setMinimumHeight(510)
                        scroll_bar.setMinimumWidth(490)
                        scroll_bar.setMaximumHeight(510)
                        scroll_bar.setMaximumWidth(490)
                        scroll_bar.setStyleSheet("border-width: 0px;")
                        scroll_bar.move(5,5)
                        layout = QHBoxLayout(scrollAreaWidgetContents)
                        dock = QDockWidget("arXiv RSS...")
                        dock.setMaximumHeight(550)
                        dock.setMaximumWidth(500)
                        dock.setMinimumHeight(550)
                        dock.setMinimumWidth(500)
                        try:
                            for i,row in rss.import_rss().iterrows():
                                url = row['url']
                                url_title = row['title']
                                listWidgetItem = QListWidgetItem("{0}. {1}".format((i+1),url_title))
                                listWidgetItem.setToolTip("Title:{1} | URL:{0} | TYPE:{2}".format(url,url_title,row['type']))
                                listWidget.addItem(listWidgetItem)
                        except:
                            listWidgetItem = QListWidgetItem("No internet connection")
                            listWidget.addItem(listWidgetItem)
                            
                        def OpenLink(listwidget,url):
                            url = url.split('URL:')[1]
                            print(url)
                            if url.split('TYPE:')[1] == 'pdf':
                                cmd = ['evince','{}'.format(url.split('| TYPE:')[0].strip(' '))]
                                subprocess.run(cmd)
                            else:
                                web.open(url.split('| TYPE:')[0].strip(' '))
                        def select_arxiv():
                            listWidget.setFocus(True)
                        select_shortcut = QShortcut(QKeySequence("Ctrl+l"),listWidget)
                        select_shortcut.activated.connect(select_arxiv)
                        scrollAreaWidgetContents.setGeometry(QRect(0, 0, 485, 510))
                        scrollAreaWidgetContents.setStyleSheet("border-width: 0px")
                        listWidget.itemDoubleClicked.connect(lambda: OpenLink(listWidget.currentItem(),listWidget.currentItem().toolTip()))
                        listWidget.itemClicked.connect(lambda: CopyLink(listWidget,listWidget.currentItem(),listWidget.currentItem().toolTip()))
                        listWidget.itemActivated.connect(lambda: OpenLink(listWidget.currentItem(),listWidget.currentItem().toolTip()))
                        listWidget.setWordWrap(True)
                        layout.addWidget(listWidget)
                        sub.setCentralWidget(scrollWidget)
                        dock.setWidget(sub)
                        window.addDockWidget(pos, dock)
                                            
                    if _DOCK_COUNT == 5:
                        layout = QFormLayout()
                        button = QPushButton("Submit (window will close)")
                        le1 = QLineEdit()
                        la1 = QLabel("Name: ")
                        la1.setStyleSheet("border-width: 0px")
                        le2 = QLineEdit()
                        la2 = QLabel("bookmarks: ")
                        la2.setStyleSheet("border-width: 0px")
                        le3 = QLineEdit()
                        la3 = QLabel("youtube: ")
                        la3.setStyleSheet("border-width: 0px")
                        le4 = QLineEdit()
                        la4 = QLabel("pdf: ")
                        la4.setStyleSheet("border-width: 0px")
                        layout.addRow(la1,le1)
                        layout.addRow(la2,le2)
                        layout.addRow(la3,le3)
                        layout.addRow(la4,le4)
                        layout.addRow(button)
                        def select_le1():
                            le1.setFocus(True)
                        le1_shortcut = QShortcut(QKeySequence("Ctrl+n"),le1)
                        le1_shortcut.activated.connect(select_le1)
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
                        dock.setMinimumHeight(200)
                        dock.setMinimumWidth(500)
                        dock.setMaximumHeight(200)
                        dock.setMaximumWidth(500)
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
                            button.hide()
                            pbar = ProgressBar(layout=layout, arg=argv, minimum=0, maximum=100, textVisible=True,objectName="BlueProgressBar")
                            pbar.deleteLater()
                            button.show()
                            button.setText('Last updated {}'.format(date.strftime("%m/%d/%Y, %H:%M:%S")))
                        def select_button():
                            button.setFocus(True)
                        button_shortcut = QShortcut(QKeySequence("Ctrl+g"),button)
                        button_shortcut.activated.connect(select_button)
                        button.clicked.connect(lambda: button_pressed(button.setEnabled(True),date = datetime.datetime.now()))
                        dock.setMinimumHeight(75)
                        dock.setMinimumWidth(500)
                        dock.setMaximumHeight(75)
                        dock.setMaximumWidth(500)
                        dock.setFeatures(QDockWidget.DockWidgetMovable)
                        window.addDockWidget(pos, dock)
                        dockedWidget = QWidget(window)
                        dock.setWidget(dockedWidget)
                        dockedWidget.setLayout(layout)
                        
                    if _DOCK_COUNT == 1:
                        listWidget = QListWidget()
                        layout = QFormLayout()
                        le = QLineEdit()
                        le.setMinimumWidth(500)
                        le.setMaximumWidth(500)
                        def select_search():
                            le.setFocus(True)
                        le_shortcut = QShortcut(QKeySequence("Ctrl+s"),le)
                        le_shortcut.activated.connect(select_search)

                        def selectionchange():
                            print("Current selection: ",cb.currentText())
                            return cb.currentText()
                        
                        def onRet(listWidget):
                            u_inp = le.text().lower()
                            listWidget = QListWidget()
                            if selectionchange() == 'Select...':
                                results = searchfiles.searchfiles(u_inp)
                                scrollWidget = QListWidget()
                                listWidgetItem = QListWidgetItem("Select from dropdown menu...")
                                listWidget.addItem(listWidgetItem)
                                scroll_bar = QScrollArea(scrollWidget)
                                scrollAreaWidgetContents = QWidget()                                
                                scroll_bar.setWidget(scrollAreaWidgetContents)
                                scroll_bar.setMinimumHeight(830)
                                scroll_bar.setMinimumWidth(700)
                                scroll_bar.setMaximumHeight(830)
                                scroll_bar.setMaximumWidth(700)
                                scroll_bar.setStyleSheet("border-width: 0px;")
                                scroll_bar.move(5,5)
                                layout = QHBoxLayout(scrollAreaWidgetContents)
                                scrollAreaWidgetContents.setGeometry(QRect(0, 0, 700, 830))
                                scrollAreaWidgetContents.setStyleSheet("border-width: 0px")
                                layout.addWidget(listWidget)
                                scroll_bar.setStyleSheet("border : none;")
                                mainWindow.setCentralWidget(scrollWidget)
                                return results
                            
                            elif selectionchange() == "Calculator":
                                def CopyLink(listwidget,results):
                                    listwidget.clearSelection()
                                    clipboard = QApplication.clipboard()
                                    clipboard.setText(results)
                                cmd = ['./Genius/run_genius.sh','{}'.format(u_inp)]
                                results = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
                                scrollWidget = QListWidget()
                                listWidgetItem = QListWidgetItem("{} is equal to...\n".format(u_inp))
                                listWidget.addItem(listWidgetItem)
                                listWidgetItem = QListWidgetItem(results)
                                listWidget.addItem(listWidgetItem)
                                scroll_bar = QScrollArea(scrollWidget)                                
                                scrollAreaWidgetContents = QWidget()
                                scroll_bar.setWidget(scrollAreaWidgetContents)
                                scroll_bar.setMinimumHeight(830)
                                scroll_bar.setMinimumWidth(700)
                                scroll_bar.setMaximumHeight(830)
                                scroll_bar.setMaximumWidth(700)
                                scroll_bar.setStyleSheet("border-width: 0px;")
                                scroll_bar.move(5,5)
                                layout = QHBoxLayout(scrollAreaWidgetContents)
                                scrollAreaWidgetContents.setGeometry(QRect(0, 0, 700, 830))
                                scrollAreaWidgetContents.setStyleSheet("border-width: 0px")
                                listWidget.itemClicked.connect(lambda: CopyLink(listWidget,results))
                                layout.addWidget(listWidget)
                                mainWindow.setCentralWidget(scrollWidget)
                                return results
                            
                            else:
                                def CopyLink(listwidget,listwidgetitem,url):
                                    listwidget.clearSelection()
                                    if listwidgetitem.text() == "Results of keyword {}...\n".format(u_inp):
                                        print("")
                                    else:
                                        url = url.split('URL:')[1].split('| TYPE:')[0].strip(' ')
                                        print(url)
                                        clipboard = QApplication.clipboard()
                                        clipboard.setText(url)
                                if u_inp == '':
                                    results = searchfiles.searchfiles(u_inp)
                                    scrollWidget = QListWidget()
                                    listWidgetItem = QListWidgetItem("Please enter valid keyword...")
                                    listWidget.addItem(listWidgetItem)
                                    scroll_bar = QScrollArea(scrollWidget)
                                    scrollAreaWidgetContents = QWidget()
                                    scroll_bar.setWidget(scrollAreaWidgetContents)
                                    scroll_bar.setMinimumHeight(830)
                                    scroll_bar.setMinimumWidth(700)
                                    scroll_bar.setMaximumHeight(830)
                                    scroll_bar.setMaximumWidth(700)
                                    scroll_bar.setStyleSheet("border-width: 0px;")
                                    scroll_bar.move(5,5)
                                    layout = QHBoxLayout(scrollAreaWidgetContents)
                                    scrollAreaWidgetContents.setGeometry(QRect(0, 0, 700, 830))
                                    scrollAreaWidgetContents.setStyleSheet("border-width: 0px")
                                    layout.addWidget(listWidget)
                                    mainWindow.setCentralWidget(scrollWidget)
                                    return results
                                
                                if u_inp == 'all':
                                    results = searchfiles.allfiles(u_inp,database.databaseDict(argv)[selectionchange()]['database'])
                                    scrollWidget = QListWidget()
                                    listWidgetItem = QListWidgetItem("All data for {}...".format(database.databaseDict(argv)[selectionchange()]['database'].replace('/','')))
                                    listWidget.addItem(listWidgetItem)
                                    scroll_bar = QScrollArea(scrollWidget)
                                    scrollAreaWidgetContents = QWidget()
                                    scroll_bar.setWidget(scrollAreaWidgetContents)
                                    scroll_bar.setMinimumHeight(830)
                                    scroll_bar.setMinimumWidth(700)
                                    scroll_bar.setMaximumHeight(830)
                                    scroll_bar.setMaximumWidth(700)
                                    scroll_bar.setStyleSheet("border-width: 0px;")
                                    scroll_bar.move(5,5)
                                    layout = QHBoxLayout(scrollAreaWidgetContents)
                                    for i,row in results.iterrows():
                                        text = row['url'].to_string(index=False)
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

                                        elif row['type'].to_string(index=False) == 'bookmark':
                                            url = row['url'].to_string(index=False)
                                            url_title = row['title'].to_string(index=False)
                                            listWidgetItem = QListWidgetItem("\t{0}. {1}".format((i+1),url_title))
                                            listWidgetItem.setToolTip("Title:{1} | URL:{0} | TYPE:{2}".format(url,url_title,row['type'].to_string(index=False)))
                                            listWidget.addItem(listWidgetItem)

                                        elif row['type'].to_string(index=False) == 'pdf':
                                            url = row['url'].to_string(index=False)
                                            url_title = row['title'].to_string(index=False)
                                            listWidgetItem = QListWidgetItem("\t{0}. {1}".format((i+1),url_title))
                                            listWidgetItem.setToolTip("Title:{1} | URL:{0} | TYPE:{2}".format(url,url_title,row['type'].to_string(index=False)))
                                            listWidget.addItem(listWidgetItem)

                                        else:
                                            print("ERROR: Type {} not found".format(row['type'].to_string(index=False)))

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
                                                web.open(url.split('| TYPE:')[0].strip(' '))

                                    scrollAreaWidgetContents.setGeometry(QRect(0, 0, 700, 830))
                                    scrollAreaWidgetContents.setStyleSheet("border-width: 0px")
                                    listWidget.itemDoubleClicked.connect(lambda: OpenLink(listWidget.currentItem(),listWidget.currentItem().toolTip()))
                                    listWidget.itemClicked.connect(lambda: CopyLink(listWidget,listWidget.currentItem(),listWidget.currentItem().toolTip()))
                                    listWidget.itemActivated.connect(lambda: OpenLink(listWidget.currentItem(),listWidget.currentItem().toolTip()))
                                    listWidget.setWordWrap(True)
                                    def select_list():
                                        listWidget.setFocus(True)
                                    list_shortcut = QShortcut(QKeySequence("Ctrl+r"),listWidget)
                                    list_shortcut.activated.connect(select_list)
                                    layout.addWidget(listWidget)
                                    mainWindow.setCentralWidget(scrollWidget)
                                    return results
                                
                                
                                else:
                                    results = searchfiles.searchfiles(u_inp,database.databaseDict(argv)[selectionchange()]['database'])
                                    if results.empty:
                                        scrollWidget = QListWidget()
                                        listWidgetItem = QListWidgetItem("Please enter valid keyword...")
                                        listWidget.addItem(listWidgetItem)
                                        scroll_bar = QScrollArea(scrollWidget)
                                        scrollAreaWidgetContents = QWidget()
                                        scroll_bar.setWidget(scrollAreaWidgetContents)
                                        scroll_bar.setMinimumHeight(830)
                                        scroll_bar.setMinimumWidth(700)
                                        scroll_bar.setMaximumHeight(830)
                                        scroll_bar.setMaximumWidth(700)
                                        scroll_bar.setStyleSheet("border-width: 0px;")
                                        scroll_bar.move(5,5)
                                        layout = QHBoxLayout(scrollAreaWidgetContents)
                                        scrollAreaWidgetContents.setGeometry(QRect(0, 0, 700, 830))
                                        scrollAreaWidgetContents.setStyleSheet("border-width: 0px")
                                        layout.addWidget(listWidget)
                                        mainWindow.setCentralWidget(scrollWidget)
                                        
                                    else:
                                        scrollWidget = QListWidget()
                                        listWidgetItem = QListWidgetItem("Results of keyword {}...\n".format(u_inp))
                                        listWidget.addItem(listWidgetItem)
                                        scroll_bar = QScrollArea(scrollWidget)
                                        scrollAreaWidgetContents = QWidget()
                                        scroll_bar.setWidget(scrollAreaWidgetContents)
                                        scroll_bar.setMinimumHeight(830)
                                        scroll_bar.setMinimumWidth(700)
                                        scroll_bar.setMaximumHeight(830)
                                        scroll_bar.setMaximumWidth(700)
                                        scroll_bar.setStyleSheet("border-width: 0px;")
                                        scroll_bar.move(5,5)
                                        layout = QHBoxLayout(scrollAreaWidgetContents)
                                        
                                        for i,row in results.iterrows():
                                            with open('log/search_history.log', 'r+') as f:
                                                if u_inp not in f.read():
                                                    f.write(u_inp + '\n')
                                            text = row['url'].to_string(index=False)
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
                                                transcript = row['transcript'].to_string(index=False)
                                                listWidgetItem = QListWidgetItem("\t{0}. {1}".format((i+1),url_title))
                                                listWidgetItem.setToolTip("Title:{1} | URL:{0} | TYPE:{2}".format(url,url_title,row['type'].to_string(index=False)))
                                                listWidget.addItem(listWidgetItem)
                                                
                                            elif row['type'].to_string(index=False) == 'bookmark':
                                                url = row['url'].to_string(index=False)
                                                url_title = row['title'].to_string(index=False)
                                                transcript = row['transcript'].to_string(index=False)
                                                listWidgetItem = QListWidgetItem("\t{0}. {1}".format((i+1),url_title))
                                                listWidgetItem.setToolTip("Title:{1} | URL:{0} | TYPE:{2}".format(url,url_title,row['type'].to_string(index=False)))
                                                listWidget.addItem(listWidgetItem)
                                                
                                            elif row['type'].to_string(index=False) == 'pdf':
                                                url = row['url'].to_string(index=False)
                                                url_title = row['title'].to_string(index=False)
                                                transcript = row['transcript'].to_string(index=False)
                                                listWidgetItem = QListWidgetItem("\t{0}. {1}".format((i+1),url_title))
                                                listWidgetItem.setToolTip("Title:{1} | URL:{0} | TYPE:{2}".format(url,url_title,row['type'].to_string(index=False)))
                                                listWidget.addItem(listWidgetItem)
                              
                                            else:
                                                print("ERROR: Type {} not found".format(row['type'].to_string(index=False)))

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
                                                    web.open(url.split('| TYPE:')[0].strip(' '))

                                        scrollAreaWidgetContents.setGeometry(QRect(0, 0, 700, 830))
                                        scrollAreaWidgetContents.setStyleSheet("border-width: 0px")
                                        listWidget.itemDoubleClicked.connect(lambda: OpenLink(listWidget.currentItem(),listWidget.currentItem().toolTip()))
                                        listWidget.itemClicked.connect(lambda: CopyLink(listWidget,listWidget.currentItem(),listWidget.currentItem().toolTip()))
                                        listWidget.itemActivated.connect(lambda: OpenLink(listWidget.currentItem(),listWidget.currentItem().toolTip()))
                                        listWidget.setWordWrap(True)
                                        def select_list():
                                            listWidget.setFocus(True)
                                        list_shortcut = QShortcut(QKeySequence("Ctrl+r"),listWidget)
                                        list_shortcut.activated.connect(select_list)
                                        layout.addWidget(listWidget)
                                        mainWindow.setCentralWidget(scrollWidget)
                                    return results

                        with open('log/search_history.log') as f:
                            history = f.read().splitlines()
                        completer = QCompleter(history)
                        completer.setCaseSensitivity(Qt.CaseInsensitive)
                        completer.setCompletionMode(QCompleter.PopupCompletion)
                        completer.setFilterMode(Qt.MatchContains)
                        delegate = CompleterDelegate(le)
                        completer.popup().setStyleSheet("color: rgb(100, 150, 150); font-weight: bold;font-size: 14pt; border:4px outset;  border-radius: 8px; border-color: rgb(50, 120, 120); background-color: rgb(50, 50, 50);")
                        completer.popup().setItemDelegate(delegate)
                        le.setCompleter(completer)

                        cb_keys = list(database.databaseDict(argv).keys())
                        cb = QComboBox()
                        cb.setMaximumWidth(200)
                        cb.addItem('Select...')
                        cb.addItem('Calculator')
                        cb.addItems(cb_keys)
                        def showPopup():
                            cb.showPopup()
                        cb_shortcut = QShortcut(QKeySequence("Ctrl+d"),cb)
                        cb_shortcut.activated.connect(showPopup)
                        cb.currentIndexChanged.connect(selectionchange)
                        le.returnPressed.connect(lambda: onRet(listWidget))
                        layout.addRow(le,cb)
                        dock = QDockWidget("")
                        dock.setMinimumHeight(50)
                        dock.setMaximumHeight(50)
                        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
                        dock.setTitleBarWidget(QWidget())
                        window.addDockWidget(pos, dock)
                        dockedWidget = QWidget(window)
                        dock.setWidget(dockedWidget)
                        dockedWidget.setLayout(layout)
                        
                    elif _DOCK_COUNT == 2:
                        dock = QDockWidget("")
                        dock.setMinimumWidth(500)
                        dock.setMinimumHeight(875)
                        dock.setMaximumWidth(500)
                        dock.setMaximumHeight(875)
                        dock.setWidget(sub)
                        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
                        dock.setTitleBarWidget(QWidget())
                        window.addDockWidget(pos, dock)
                        if DO_SUB_DOCK_CREATION and subDocks:
                            addDocks(sub, "Sub Dock", subDocks=False)
                            window.addDockWidget(pos, dock)
                            
                    else:
                        if DO_SUB_DOCK_CREATION and subDocks:
                            addDocks(sub, "Sub Dock", subDocks=False)
                            window.addDockWidget(pos, dock)

        addDocks(mainWindow, "Custom Search")

        mainWindow.raise_()

class MyWin(QMainWindow, GUI):
    def __init__(self):
        super().__init__()
        self.mainwindow(self)
        self.dragPos = QPoint()
        
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()         
    
def main(): 
   app = QApplication(sys.argv)

   trayIcon = QSystemTrayIcon(QIcon('icons/normal.png'), parent=app)
   trayIcon.show()
   
   '''
   qp = QPalette()
   qp.setColor(QPalette.ButtonText, Qt.black)
   qp.setColor(QPalette.Window, Qt.gray)
   qp.setColor(QPalette.Button, Qt.gray)
   app.setPalette(qp)
   '''

   mainwindow = MyWin()
   mainwindow.show()
   
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
