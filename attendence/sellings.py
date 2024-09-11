import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import style

con=sqlite3.connect("products.db")
cur=con.cursor()

defaultImg="store.png"

class SellProducts(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Recognition")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,1350,750)
        self.setFixedSize(self.size())
        self.UI()
        self.show()


    def UI(self):
        self.widgets()
        self.layouts()

    def start(self):
        pass
    def exit(self):
        pass

    def widgets(self):
        ###################top layout's widgets############
        self.sellProductImg=QLabel()
        self.img=QPixmap('icons/shop.png')
        self.sellProductImg.setPixmap(self.img)
        self.sellProductImg.setAlignment(Qt.AlignCenter)
        self.titleText=QLabel("Face Recognition")
        self.titleText.setAlignment(Qt.AlignCenter)
        self.startBtn=QPushButton("Start")
        self.startBtn.clicked.connect(self.start)
        self.exitBtn=QPushButton("Exit")
        self.exitBtn.clicked.connect(self.exit)
        ###################bottom layout's widgets##########

    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QVBoxLayout()
        self.bottomLayout=QFormLayout()
        self.topFrame=QFrame()
        self.topFrame.setStyleSheet(style.sellProductTopFrame())
        self.bottomFrame=QFrame()
        self.bottomFrame.setStyleSheet(style.sellProductBottomFrame())
        self.bottomFrame.setLayout(self.bottomLayout)
        self.bottomLayout.addRow(QLabel(""),self.startBtn)
        self.bottomLayout.addRow(QLabel(""),self.exitBtn)
        ############add widgets###########
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.sellProductImg)
        self.topFrame.setLayout(self.topLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)