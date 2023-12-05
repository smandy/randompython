#!/usr/bin/env python

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
class App(QDialog):
    def __init__(self):
        super().__init__()
        print("Init in App")
        self.title = 'PyQt5 layout - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.initUI()
 
    def initUI(self):
        print("Initui")
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.createGridLayout()
 
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        self.show()
 
    def onClick(self):
        x = self.sender()
        t = x.text()
        print("Woot on click %s %s" % (t, x))
        
        
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)

        def makeButton(a):
            ret = QPushButton(a)
            ret.clicked.connect( self.onClick)
            print("Made button %s" % ret)
            return ret
        
        layout.addWidget(makeButton('1'),0,0) 
        layout.addWidget(makeButton('2'),0,1) 
        layout.addWidget(makeButton('3'),0,2) 
        layout.addWidget(makeButton('4'),1,0) 
        layout.addWidget(makeButton('5'),1,1) 
        layout.addWidget(makeButton('6'),1,2) 
        layout.addWidget(makeButton('7'),2,0) 
        layout.addWidget(makeButton('8'),2,1) 
        layout.addWidget(makeButton('9'),2,2) 
 
        self.horizontalGroupBox.setLayout(layout)
 
def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())    

if __name__ == '__main__':
    main()

try:
    app
    dialogs
except:
    app = QApplication(sys.argv)
    dialogs = []

dialogs.append(App())
#sys.exit(app.exec_())    
    
