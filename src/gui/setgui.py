#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-11-18 15:12:22 trottar"
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

class inputdialogdemo(QWidget):
    def __init__(self, parent = None):
        super(inputdialogdemo, self).__init__(parent)
        self.setMouseTracking(True)
        self.setGeometry(750, 100, 300, 300)
        
        layout = QFormLayout()
        self.le1 = QLabel("<a style='text-decoration:none;'href='https://www.tutorialspoint.com/'>tutorialspoint</a>",toolTip = "<b>Title</b>: ABC | <b>URL</b>: <a style='text-decoration:none;'href='https://www.tutorialspoint.com/'>tutorialspoint</a>")
        self.le1.setOpenExternalLinks(True)
        self.le2 = QLabel()
        self.le3 = QLabel()
        
        self.le = QLineEdit()
        self.le.returnPressed.connect(self.onClick)
		
        self.setLayout(layout)

        self.cb = QComboBox()
        layout.addRow(self.le,self.cb)
        layout.addRow(self.le1,self.le2)
        layout.addRow(None,self.le3)
        self.cb.addItem("Physics")
        self.cb.addItems(["Coding", "Thesis", "Misc"])
        self.cb.currentIndexChanged.connect(self.selectionchange)

        self.le2.setText("button 2")
        self.le3.setText("button 3")
        
        self.le2.setAlignment(Qt.AlignRight)
        self.le3.setAlignment(Qt.AlignRight)

        self.setLayout(layout)
        self.setWindowTitle("Custom Search")

    def onClick(self):
        u_inp = self.le.text()
        print(u_inp)
        
    def selectionchange(self):
        print("Items in the list are :")
	
        for count in range(self.cb.count()):
            print(self.cb.itemText(count))
        print("Current selection: ",self.cb.currentText())
        return self.cb.currentText()         
			
def main(): 
   app = QApplication(sys.argv)
   app.setStyle('WindowsVista')
   qp = QPalette()
   qp.setColor(QPalette.ButtonText, Qt.black)
   qp.setColor(QPalette.Window, Qt.gray)
   qp.setColor(QPalette.Button, Qt.gray)
   app.setPalette(qp)

   ex = inputdialogdemo()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
