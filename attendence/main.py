import sys,os
from xml.etree.ElementInclude import include
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import addproduct,addmember,sellings,style
from PIL import Image
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon,QImage, QPalette, QBrush

con=sqlite3.connect("products.db")
cur=con.cursor()
import json
import cv2
from align_custom import AlignCustom
from face_feature import FaceFeature
from mtcnn_detect import MTCNNDetect
from tf_graph import FaceRecGraph
import time
import numpy as np
import requests
FRGraph = FaceRecGraph()
aligner = AlignCustom()
extract_feature = FaceFeature(FRGraph)
face_detect = MTCNNDetect(FRGraph, scale_factor=2)
################ Layout for Display Member #######################
image_WindowIcon = "face_button.png"
image_DisplayMember="back1.jpg"
image_TrainingMember="trainingpic.jpg"
image_Golive="desktop.jpg"
image_MemberValidation="memberval.jpg"
image_MemberVerification="memberveri.jpg"
class tmessage():
    def __init__(self):
        self.bot_token = '1564550462:AAHG5k3pioPzgerui_UDDNoQCRybHumTSC0'
        self.bot_chatID = '-422499420'

    def telegram_bot_sendtext(self, operator_message):
        self.send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + self.bot_chatID + '&parse_mode=Markdown&text=' + operator_message
        requests.get(self.send_text)
telegram_message = tmessage()
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Tracking")
        self.setWindowIcon(QIcon('icons/'+image_WindowIcon))
        #self.setStyleSheet("background-color: neon;")
        self.setGeometry(450,150,1250,1050)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.toolBar()
        self.tabWigdet()
        self.widgets()
        self.layouts()
        # self.displayProducts()
        self.displayMembers()
        self.displayattendenceTable()
        # self.getStatistics()

    def toolBar(self):
        self.tb=self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        #####################Toolbar Buttons############
        ####################Add Product################
        # self.addProduct=QAction(QIcon('icons/add.png'),"Add Product",self)
        # self.tb.addAction(self.addProduct)
        # self.addProduct.triggered.connect(self.funcAddProduct)
        # self.tb.addSeparator()
        ######################Add Member################
        self.addMember=QAction(QIcon('icons/users.png'),"Add Member",self)
        self.tb.addAction(self.addMember)
        self.addMember.triggered.connect(self.funcAddMember)
        self.tb.addSeparator()
        ######################Face Recognition###############
        # self.sellProduct = QAction(QIcon('icons/sell.png'),"Real Time Feed",self)
        # self.tb.addAction(self.sellProduct)
        # self.sellProduct.triggered.connect(self.funcSellProducts)
        # self.tb.addSeparator()

    def tabWigdet(self):
        self.tabs=QTabWidget()
        self.tabs.blockSignals(True)
        self.tabs.currentChanged.connect(self.tabChanged)
        self.setCentralWidget(self.tabs)
        # self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()
        # self.tabs.addTab(self.tab1,"Products")
        self.tabs.addTab(self.tab2,"Members")
        self.tabs.addTab(self.tab3,"Attendence")


    def widgets(self):
        self.attendenceImg = "attendence.PNG"
        #######################Tab1 Widgets###############
        ####################Main left layout widget##########
        # self.productsTable = QTableWidget()
        # self.productsTable.setColumnCount(6)
        # self.productsTable.setColumnHidden(0,True)
        # self.productsTable.setHorizontalHeaderItem(0,QTableWidgetItem("Product Id"))
        # self.productsTable.setHorizontalHeaderItem(1,QTableWidgetItem("Product Name"))
        # self.productsTable.setHorizontalHeaderItem(2,QTableWidgetItem("Manufacturer"))
        # self.productsTable.setHorizontalHeaderItem(3,QTableWidgetItem("Price"))
        # self.productsTable.setHorizontalHeaderItem(4,QTableWidgetItem("Qouta"))
        # self.productsTable.setHorizontalHeaderItem(5,QTableWidgetItem("Availbility"))
        # self.productsTable.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        # self.productsTable.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        # self.productsTable.doubleClicked.connect(self.selectedProduct)


        ########################Right top layout widgets#######################
        # self.searchText=QLabel("Search")
        # self.searchEntry=QLineEdit()
        # self.searchEntry.setPlaceholderText("Search For Products")
        # self.searchButton=QPushButton("Search")
        # self.searchButton.clicked.connect(self.searchProducts)
        # self.searchButton.setStyleSheet(style.searchButtonStyle())
        ##########################Right middle layout widgets###########
        # self.allProducts=QRadioButton("All Products")
        # self.avaialableProducts=QRadioButton("Available")
        # self.notAvaialableProducts=QRadioButton("Not Available")
        # self.listButton=QPushButton("List")
        # self.listButton.clicked.connect(self.listProducts)
        # self.listButton.setStyleSheet(style.listButtonStyle())
        ########################Tab2 Widgets#########################
        self.membersTable=QTableWidget()
        self.membersTable.setColumnCount(4)
        self.membersTable.setHorizontalHeaderItem(0,QTableWidgetItem("Member ID"))
        self.membersTable.setHorizontalHeaderItem(1,QTableWidgetItem("Member Name"))
        self.membersTable.setHorizontalHeaderItem(2,QTableWidgetItem("Member email"))
        self.membersTable.setHorizontalHeaderItem(3,QTableWidgetItem("Phone"))
        self.membersTable.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.membersTable.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        self.membersTable.horizontalHeader().setSectionResizeMode(3,QHeaderView.Stretch)
        self.membersTable.doubleClicked.connect(self.selectedMember)
        self.memberSearchText=QLabel("Search Members")
        self.memberSearchEntry=QLineEdit()
        self.memberSearchButton=QPushButton("Search")
        self.memberSearchButton.clicked.connect(self.searchMembers)
        ##########################Tab3 widgets#####################
        self.CenterFrame = QLabel()
        self.CenterImage = QPixmap("img/{0}".format(self.attendenceImg))
        self.CenterFrame.setPixmap(self.CenterImage)
        self.attendenceTable=QTableWidget()
        self.attendenceTable.setColumnCount(4)
        self.attendenceTable.setHorizontalHeaderItem(0, QTableWidgetItem("Serial Number"))
        self.attendenceTable.setHorizontalHeaderItem(1, QTableWidgetItem("Member Name"))
        self.attendenceTable.setHorizontalHeaderItem(2, QTableWidgetItem("Member email"))
        self.attendenceTable.setHorizontalHeaderItem(3, QTableWidgetItem("Phone"))
        self.attendenceTable.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.attendenceTable.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        self.attendenceTable.horizontalHeader().setSectionResizeMode(3,QHeaderView.Stretch)
        self.attendenceLabel=QLabel()
        self.totalMemberLabel=QLabel()
        self.imageSearchEntry=QLineEdit()
        self.attendenceFileButton=QPushButton("upload a photo from file")
        self.attendenceFileButton.clicked.connect(self.takeattendenceFile)
        self.attendenceCamButton=QPushButton("Take A Picture")
        self.attendenceCamButton.clicked.connect(self.takeAttendenceCam)
        self.attendenceIPCAMButton=QPushButton("Take a Live feed from IPcam")
        self.attendenceIPCAMButton.clicked.connect(self.takeAttendenceIpCam)
        self.sendMessagebutton = QPushButton("Send messages")
        self.sendMessagebutton.clicked.connect(self.sendMessage)
        self.Refreshbutton = QPushButton("Refresh")
        self.Refreshbutton.clicked.connect(self.RefreshDb)





    def layouts(self):
        ######################Tab1 layouts##############
        self.mainLayout=QHBoxLayout()

        self.mainLeftLayout=QVBoxLayout()
        self.mainRightLayout=QVBoxLayout()
        self.rightTopLayout=QHBoxLayout()
        self.rightMiddleLayout=QHBoxLayout()
        self.topGroupBox=QGroupBox("Search Box")
        self.topGroupBox.setStyleSheet(style.searchBoxStyle())
        self.middleGroupBox=QGroupBox("List Box")
        self.middleGroupBox.setStyleSheet(style.listBoxStyle())
        self.bottomGroupBox=QGroupBox()
        #################Add widgets###################
        ################Left main layout widget###########
        # self.mainLeftLayout.addWidget(self.productsTable)
        ########################Right top layout widgets#########
        # self.rightTopLayout.addWidget(self.searchText)
        # self.rightTopLayout.addWidget(self.searchEntry)
        # self.rightTopLayout.addWidget(self.searchButton)
        # self.topGroupBox.setLayout(self.rightTopLayout)
        #################Right middle layout widgets##########
        # self.rightMiddleLayout.addWidget(self.allProducts)
        # self.rightMiddleLayout.addWidget(self.avaialableProducts)
        # self.rightMiddleLayout.addWidget(self.notAvaialableProducts)
        # self.rightMiddleLayout.addWidget(self.listButton)
        # self.middleGroupBox.setLayout(self.rightMiddleLayout)

        # self.mainRightLayout.addWidget(self.topGroupBox,20)
        # self.mainRightLayout.addWidget(self.middleGroupBox,20)
        # self.mainRightLayout.addWidget(self.bottomGroupBox,60)
        # self.mainLayout.addLayout(self.mainLeftLayout,70)
        # self.mainLayout.addLayout(self.mainRightLayout,30)
        # self.tab1.setLayout(self.mainLayout)
        ######################Tab2 Layouts#####################
        self.memberMainLayout=QHBoxLayout()
        self.memberLeftLayout=QHBoxLayout()
        self.memberRightLayout=QHBoxLayout()
        self.memberRightGroupBox=QGroupBox("Search For Members")
        self.memberRightGroupBox.setContentsMargins(10,10,10,600)
        self.memberRightLayout.addWidget(self.memberSearchText)
        self.memberRightLayout.addWidget(self.memberSearchEntry)
        self.memberRightLayout.addWidget(self.memberSearchButton)
        self.memberRightGroupBox.setLayout(self.memberRightLayout)

        self.memberLeftLayout.addWidget(self.membersTable)
        self.memberMainLayout.addLayout(self.memberLeftLayout,70)
        self.memberMainLayout.addWidget(self.memberRightGroupBox,30)
        self.tab2.setLayout(self.memberMainLayout)

        #####################Tab3 layouts########################
        self.attendenceMainLayout=QHBoxLayout()
        self.attendenceLeftLayout = QVBoxLayout()
        self.righttoplayout=QHBoxLayout()
        self.rightbottomlayout = QHBoxLayout()
        self.attendenceRightLayout = QVBoxLayout()
        # self.attendenceRightLayout=QFormLayout()
        # self.statisticsGroupBox=QGroupBox("Attendence Register")
        # self.attendenceRightLayout.addRow("Total Student :",self.totalProductsLabel)
        # self.attendenceRightLayout.addRow("Total detected:",self.totalMemberLabel)
        self.righttoplayout.addWidget(self.CenterFrame)
        self.rightbottomlayout.addWidget(self.attendenceTable)
        self.attendenceRightLayout.addLayout(self.righttoplayout)
        self.attendenceRightLayout.addLayout(self.rightbottomlayout)
        self.attendenceLeftLayout.addWidget(self.imageSearchEntry)
        self.attendenceLeftLayout.addWidget(self.attendenceFileButton)
        self.attendenceLeftLayout.addWidget(self.attendenceCamButton)
        self.attendenceLeftLayout.addWidget(self.attendenceIPCAMButton)
        self.attendenceMainLayout.addLayout(self.attendenceRightLayout)
        self.attendenceLeftLayout.addWidget(self.sendMessagebutton)
        self.attendenceLeftLayout.addWidget(self.Refreshbutton)
        self.attendenceMainLayout.addLayout(self.attendenceLeftLayout)

        self.tab3.setLayout(self.attendenceMainLayout)
        # self.tabs.blockSignals(False)

    def takeattendenceFile(self):
        value = self.memberSearchEntry.text()
        self.takeattendence("file",value)


    def RefreshDb(self):
        members = cur.execute("UPDATE members set member_status='False'")
        con.commit()



    def sendMessage(self):
        members = cur.execute("SELECT * FROM members")
        for row_data in members:
            print(row_data)
            if(row_data[5] == 'True'):
                telegram_message.telegram_bot_sendtext("Member "+row_data[1]+" is present")
            else:
                telegram_message.telegram_bot_sendtext("Member " + row_data[1] + " is absent")


    def takeAttendenceCam(self):
        value = 0
        self.takeattendence("camera",value)
    def takeAttendenceIpCam(self):
        self.live = Golive()
        self.live.show()

    def funcAddProduct(self):
        self.newProduct=addproduct.AddProduct()

    def funcAddMember(self):
        self.newMember=addmember.AddMember()

    def displayProducts(self):
        self.membersTable.setFont(QFont("Times", 12))
        for i in reversed(range(self.membersTable.rowCount())):
            self.membersTable.removeRow(i)

        members = cur.execute("SELECT * FROM members")
        for row_data in members:
            row_number = self.membersTable.rowCount()
            self.membersTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.membersTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.membersTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def displayMembers(self):
        self.membersTable.setFont(QFont("Times",12))
        for i in reversed(range(self.membersTable.rowCount())):
            self.membersTable.removeRow(i)

        members=cur.execute("SELECT * FROM members")
        for row_data in members:
            row_number = self.membersTable.rowCount()
            self.membersTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.membersTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        self.membersTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def displayattendenceTable(self):
        self.attendenceTable.setFont(QFont("Times",12))
        for i in reversed(range(self.attendenceTable.rowCount())):
            self.attendenceTable.removeRow(i)
        members=cur.execute("SELECT * FROM members WHERE member_status='True'")
        for row_data in members:
            row_number = self.attendenceTable.rowCount()
            self.attendenceTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.attendenceTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        self.attendenceTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # def selectedProduct(self):
    #     global productId
    #     listProduct=[]
    #     for i in range(0,6):
    #         listProduct.append(self.productsTable.item(self.productsTable.currentRow(),i).text())
    #
    #     productId=listProduct[0]
    #     self.display=DisplayProduct()
    #     self.display.show()

    def selectedMember(self):
        global memberId
        listMember=[]
        for i in range(0,4):
            listMember.append(self.membersTable.item(self.membersTable.currentRow(),i).text())

        memberId=listMember[0]
        self.displayMember=DisplayMember()
        self.displayMember.show()

    # def searchProducts(self):
    #     value=self.searchEntry.text()
    #     if value == "":
    #         QMessageBox.information(self,"Warning","Search query cant be empty!!!")
    #
    #     else:
    #         self.searchEntry.setText("")
    #
    #         query=("SELECT product_id,product_name,product_manufacturer,product_price,product_qouta,product_availability FROM products WHERE product_name LIKE ? or product_manufacturer LIKE ?")
    #         results=cur.execute(query,('%' + value + '%','%' + value + '%')).fetchall()
    #         print(results)
    #
    #         if results == []:
    #             QMessageBox.information(self,"Warning","There is no such a product or manufacturer")
    #
    #         else:
    #             for i in reversed(range(self.productsTable.rowCount())):
    #                 self.productsTable.removeRow(i)
    #
    #             for row_data in results:
    #                 row_number = self.productsTable.rowCount()
    #                 self.productsTable.insertRow(row_number)
    #                 for column_number, data in enumerate(row_data):
    #                     self.productsTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))

    def searchMembers(self):
        value = self.memberSearchEntry.text()
        if value == "":
            QMessageBox.information(self,"Warning","Search query can not be empty")

        else:
            self.memberSearchEntry.setText("")
            query=("SELECT * FROM members WHERE member_name LIKE ? or member_email LIKE ? or member_phone LIKE ?")
            results=cur.execute(query,('%' + value + '%', '%' + value + '%', '%' + value + '%')).fetchall()
            if results == []:
                QMessageBox.information(self,"Warning","There is no such a member")
            else:
                for i in reversed(range(self.membersTable.rowCount())):
                    self.membersTable.removeRow(i)

                for row_data in results:
                    row_number = self.membersTable.rowCount()
                    self.membersTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.membersTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def findPeople(self, features_arr, positions, thres=0.6, percent_thres=70):
        '''
        :param features_arr: a list of 128d Features of all faces on screen
        :param positions: a list of face position types of all faces on screen
        :param thres: distance threshold
        :return: person name and percentage
        '''
        f = open('./facerec_128D.txt', 'r')
        data_set = json.loads(f.read());
        returnRes = [];
        for (i, features_128D) in enumerate(features_arr):
            result = "Unknown";
            smallest = sys.maxsize
            for person in data_set.keys():
                person_data = data_set[person][positions[i]];
                for data in person_data:
                    distance = np.sqrt(np.sum(np.square(data - features_128D)))
                    if (distance < smallest):
                        smallest = distance;
                        result = person;
            percentage = min(100, 100 * thres / smallest)
            if percentage <= percent_thres:
                result = "Unknown"
            returnRes.append((result, percentage))
        return returnRes

    def takeattendence(self, parameter, name):
        if(parameter == "file"):
            path = r'C:\Users\nihar\OneDrive\Desktop\Project Files\attendence\testingdata\TEST1.jpg'
            frame = cv2.imread(path)
        elif(parameter == "camera"):
            cap =  cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                cap.release()
        elif (parameter == "IP"):
            cap = cv2.VideoCapture("rtsp://admin:poli25118@192.168.0.114")
            while (True):
                ret, frame = cap.read()
                if (ret):
                    cap.release()
                    break

        try:

            rects, landmarks = face_detect.detect_face(frame, 80);  # min face size is set to 80x80
            aligns = []
            positions = []
            for (i, rect) in enumerate(rects):
                aligned_face, face_pos = aligner.align(160, frame, landmarks[i])
                if len(aligned_face) == 160 and len(aligned_face[0]) == 160:
                    aligns.append(aligned_face)
                    positions.append(face_pos)
                else:
                    print("Align face failed")  # log
            if (len(aligns) > 0):
                features_arr = extract_feature.get_features(aligns)
                recog_data = self.findPeople(features_arr, positions);
                print(recog_data)
                members = []
                for [i, j] in recog_data:
                    members.append(i)
                print(members)
                for member in members :
                    print(member)
                    self.updatestatusofmember(member)
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                                 QtGui.QImage.Format_RGB888)
                convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
                pixmap = QtGui.QPixmap(convertToQtFormat)
                resizeImage = pixmap.scaled(256, 256)
                QtWidgets.QApplication.processEvents()
                self.CenterFrame.setPixmap(resizeImage)
            self.displayattendenceTable()



        except Exception as e:
            print("error while detection   " + str(e))
    def updatestatusofmember(self, membertoupdate):
        try:
            query=("UPDATE members set member_status='True' WHERE  member_name=\'"+membertoupdate+"\'")
            results=cur.execute(query).fetchall()
            con.commit()
        # resultsnumber = results[3]
            print(str(results) +"updated")
        except:
            print(membertoupdate+"not found in db")

    # def listProducts(self):
    #     if self.allProducts.isChecked() == True:
    #         self.displayProducts()
    #
    #     elif self.avaialableProducts.isChecked():
    #         query=("SELECT product_id,product_name,product_manufacturer,product_price,product_qouta,"
    #                "product_availability FROM products WHERE product_availability='Available'")
    #         products=cur.execute(query).fetchall()
    #         print(products)
    #
    #         for i in reversed(range(self.productsTable.rowCount())):
    #             self.productsTable.removeRow(i)
    #
    #         for row_data in products:
    #             row_number = self.productsTable.rowCount()
    #             self.productsTable.insertRow(row_number)
    #             for column_number, data in enumerate(row_data):
    #                 self.productsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
    #
    #     elif self.notAvaialableProducts.isChecked():
    #         query = ("SELECT product_id,product_name,product_manufacturer,product_price,product_qouta,"
    #                  "product_availability FROM products WHERE product_availability='UnAvailable'")
    #         products = cur.execute(query).fetchall()
    #         print(products)
    #
    #         for i in reversed(range(self.productsTable.rowCount())):
    #             self.productsTable.removeRow(i)
    #
    #         for row_data in products:
    #             row_number = self.productsTable.rowCount()
    #             self.productsTable.insertRow(row_number)
    #             for column_number, data in enumerate(row_data):
    #                 self.productsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))


    # def funcSellProducts(self):
    #     self.sell = sellings.SellProducts()


    # def getStatistics(self):
    #     countProducts=cur.execute("SELECT count(product_id) FROM products").fetchall()
    #     countMembers = cur.execute("SELECT count(member_id) FROM members").fetchall()
    #     soldProducts = cur.execute("SELECT SUM(selling_quantity) FROM sellings").fetchall()
    #     totalAmount = cur.execute("SELECT SUM(selling_amount) FROM sellings").fetchall()
    #     totalAmount = totalAmount[0][0]
    #     soldProducts = soldProducts[0][0]
    #     countMembers = countMembers[0][0]
    #     countProducts = countProducts[0][0]
    #     self.totalProductsLabel.setText(str(countProducts))
    #     self.totalMemberLabel.setText(str(countMembers))
    #     self.soldProductsLabel.setText(str(soldProducts))
    #     self.totalAmountLabel.setText(str(totalAmount)+" $")

    def tabChanged(self):
        # self.getStatistics()
        # self.displayProducts()
        self.displayMembers()


###############################################################


################ Layout for Display Member #######################

class DisplayMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Member Details")
        self.setWindowIcon(QIcon('icons/'+image_WindowIcon))
        self.setGeometry(450,150,1250,1050)
        oImage = QImage("img/"+image_DisplayMember)
        sImage = oImage.scaled(QSize(250,250))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.memberDetails()
        self.widgets()
        self.layouts()


    def memberDetails(self):
        global memberId
        query=("SELECT * FROM members WHERE member_id=?")
        member=cur.execute(query,(memberId,)).fetchone()
        self.memberName=member[1]
        self.memberemail=member[2]
        self.memberPhone=member[3]
        self.memberFaceData=member[4]

    def widgets(self):
        ###############Widgets of top layout############
        self.memberImg=QLabel()
        self.img=QPixmap('icons/members.png')
        self.memberImg.setPixmap(self.img)
        self.memberImg.setAlignment(Qt.AlignCenter)
        self.titleText=QLabel("Display Member")
        self.titleText.setAlignment(Qt.AlignCenter)
        ###################widgets of bottom layout#########
        self.nameEntry=QLineEdit()
        self.nameEntry.setText(self.memberName)
        self.emailEntry=QLineEdit()
        self.emailEntry.setText(self.memberemail)
        self.phoneEntry=QLineEdit()
        self.phoneEntry.setText(self.memberPhone)
        self.updateBtn=QPushButton("Update")
        self.updateBtn.clicked.connect(self.updateMember)
        self.deleteBtn=QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.deleteMember)
        self.recognizeBtn=QPushButton("Recognize")
        self.recognizeBtn.clicked.connect(self.recognizeMember)



    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QVBoxLayout()
        self.bottomLayout=QFormLayout()
        self.topFrame=QFrame()
        self.topFrame.setStyleSheet(style.memberTopFrame())
        self.bottomFrame=QFrame()
        self.bottomFrame.setStyleSheet(style.memberBottomFrame())
        ##############add widgets######3
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.memberImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("Name: "),self.nameEntry)
        self.bottomLayout.addRow(QLabel("email: "),self.emailEntry)
        self.bottomLayout.addRow(QLabel("Phone: "),self.phoneEntry)
        self.bottomLayout.addRow(QLabel(""),self.updateBtn)
        self.bottomLayout.addRow(QLabel(""),self.deleteBtn)
        self.bottomLayout.addRow(QLabel(""),self.recognizeBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)


    def recognizeMember(self):
        global memberId
        if(self.memberFaceData == "Not_Present"):
            mbox = QMessageBox.question(self, "Info", "Please look look into the camera the training will start soon ....",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if mbox == QMessageBox.Yes:
                self.TrainingMember=TrainingMember()
                self.TrainingMember.show()
                self.close()
            else:
                self.close()
        else:
            mbox=QMessageBox.question(self,"Warning","You have been registered already would u like to verify",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if mbox == QMessageBox.Yes:
                self.MemberVerification=MemberVerification()
                self.MemberVerification.show()
                self.close()
            else:
                self.close()


    def deleteMember(self):
        global memberId
        mbox=QMessageBox.question(self,"Warning","Are you sure to delete this member",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)

        if mbox == QMessageBox.Yes:
            try:
                query="DELETE FROM members WHERE member_id=?"
                cur.execute(query,(memberId,))
                con.commit()
                QMessageBox.information(self,"Info","Member has been deleted!")
                self.close()
            except:
                QMessageBox.information(self,"Info","Member has not been deleted!")
                self.close()
        else:
            self.close()


    def updateMember(self):
        global memberId
        name = self.nameEntry.text()
        email = self.emailEntry.text()
        phone = self.phoneEntry.text()

        if (name and email and phone !=""):
            try:
                query="UPDATE members set member_name=?, member_email=?, member_phone=? WHERE member_id=?"
                cur.execute(query,(name,email,phone,memberId))
                con.commit()
                QMessageBox.information(self,"Info","Member has been updated!")
                self.close()
            except:
                QMessageBox.information(self,"Info","Member has been updated!")

        else:
            QMessageBox.information(self, "Info", "Fields can not be empty!")


###############################################################


################ Layout for registration#######################


class TrainingMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Training Face")
        self.setWindowIcon(QIcon('icons/'+image_WindowIcon))
        self.setGeometry(450,150,1250,1050)
        oImage = QImage("img/"+image_TrainingMember)
        sImage = oImage.scaled(QSize(1850,1050))                   # resize Image to widgets size
        palette = QPalette()
        self.setFixedSize(self.size())
        self.UI()
        self.show()
        self.start()

    def start(self):
        centercount = 50
        rightcount = 50
        leftcount = 50
        person_imgs = {"Left": [], "Right": [], "Center": []};
        person_features = {"Left": [], "Right": [], "Center": []};
        f = open('./facerec_128D.txt', 'r');
        data_set = json.loads(f.read());
        cap = cv2.VideoCapture(0)
        cap1 = cv2.VideoCapture("videos/sample.mov")
        if(cap.isOpened()):
            print("Webcam started successfully")
        while(cap.isOpened() and cap1.isOpened()):
            ret,frame = cap.read()
            ret1,frame1 = cap1.read()
            if ret:
                rects, landmarks = face_detect.detect_face(frame, 80);  # min face size is set to 80x80
                for (i, rect) in enumerate(rects):
                    aligned_frame, pos = aligner.align(160, frame, landmarks[i]);
                    if pos == "Center":
                        centercount -= 1
                        if  centercount == 90:
                            fname = "./TrainedImages/" + self.memberName + ".jpg"
                            cv2.imwrite(fname, frame)
                    if pos == "Left":
                        leftcount -= 1
                        if(leftcount == 10):
                            self.bottomLeftFrame.hide()
                    if pos == "Right":
                        rightcount -= 1
                        if(rightcount == 10):
                            self.bottomRightFrame.hide()
                    if len(aligned_frame) == 160 and len(aligned_frame[0]) == 160:
                        person_imgs[pos].append(aligned_frame)
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],QtGui.QImage.Format_RGB888)
                convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
                pixmap = QtGui.QPixmap(convertToQtFormat)
                resizeImage = pixmap.scaled(256, 256)
                QtWidgets.QApplication.processEvents()
            if ret1:
                rgbImage1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage1.data, rgbImage1.shape[1], rgbImage1.shape[0],QtGui.QImage.Format_RGB888)
                convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
                pixmap = QtGui.QPixmap(convertToQtFormat)
                resizeImage1 = pixmap.scaled(256, 256)
                QtWidgets.QApplication.processEvents()
            if ret is not None:
                self.topleftFrame.setPixmap(resizeImage)
            if ret1 is not None:
                self.toprightFrame.setPixmap(resizeImage1)
            if(leftcount<0 and rightcount<0 and centercount<0):
                time.sleep(3)
                cap.release()
                cap1.release()
                QMessageBox.information(self, "Info", "Member has been updated!")
                for pos in person_imgs:  # there r some exceptions here, but I'll just leave it as this to keep it simple
                    person_features[pos] = [np.mean(extract_feature.get_features(person_imgs[pos]), axis=0).tolist()]
                data_set[self.memberName] = person_features;
                f = open('./facerec_128D.txt', 'w');
                f.write(json.dumps(data_set))
                try:
                    query = ("UPDATE members set member_facedata='True' WHERE  member_name=\'" + self.memberName + "\'")
                    results = cur.execute(query).fetchall()
                    con.commit()
                    QMessageBox.information(self, "Info", "Member has been updated!")
                except:
                    QMessageBox.information(self, "Info", "Member has not been updated!")

                mbox = QMessageBox.question(self, "Info", "You have been registered Sucessfully please click to verify",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if mbox == QMessageBox.Yes:
                    self.MemberValidation = MemberValidation()
                    self.MemberValidation.show()


        # vs = cv2.VideoCapture(0);
        # # vs1 = cv2.VideoCapture("videos/sample.mov");
        # f = open('./facerec_128D.txt', 'r');
        # data_set = json.loads(f.read());
        # person_imgs = {"Left": [], "Right": [], "Center": []};
        # person_features = {"Left": [], "Right": [], "Center": []};
        # while True:
        #     _, frame = vs.read();
        #     rects, landmarks = face_detect.detect_face(frame, 80);  # min face size is set to 80x80
        #     for (i, rect) in enumerate(rects):
        #         aligned_frame, pos = aligner.align(160, frame, landmarks[i]);
        #         if len(aligned_frame) == 160 and len(aligned_frame[0]) == 160:
        #             person_imgs[pos].append(aligned_frame)
        #             convertToQtFormat = QtGui.QImage(aligned_frame.data, aligned_frame.shape[1], aligned_frame.shape[0],
        #                                              QtGui.QImage.Format_RGB888)
        #             convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
        #             pixmap = QtGui.QPixmap(convertToQtFormat)
        #             resizeImage = pixmap.scaled(80, 80)
        #             self.rightimage = QPixmap(resizeImage)
        #             # cv2.imshow("Captured face", aligned_frame)
        #     key = cv2.waitKey(1) & 0xFF
        #     if key == 30 or key == ord("q"):
        #         break
        # for pos in person_imgs: #there r some exceptions here, but I'll just leave it as this to keep it simple
        #     person_features[pos] = [np.mean(extract_feature.get_features(person_imgs[pos]),axis=0).tolist()]
        # data_set[self.memberName] = person_features;
        # f = open('./facerec_128D.txt', 'w');
        # f.write(json.dumps(data_set))




    def memberDetails(self):
        global memberId
        query=("SELECT * FROM members WHERE member_id=?")
        member=cur.execute(query,(memberId,)).fetchone()
        self.memberName=member[1]
        self.memberemail=member[2]
        self.memberPhone=member[3]
        self.memberFaceData=member[4]

    def UI(self):
        self.memberDetails()
        self.widgets()
        self.layouts()


    def widgets(self):
        #########widgets for top layout#######
        self.productImg = "reg.jpg"
        self.leftImg = "left.PNG"
        self.rightImg = "right.PNG"
        self.centertImg = "center.PNG"
        self.toprightFrame=QLabel()
        self.rightimage=QPixmap("img/{0}".format(self.productImg))
        self.toprightFrame.setPixmap(self.rightimage)
        self.toprightFrame.setAlignment(Qt.AlignCenter)
        self.topleftFrame=QLabel()
        self.leftimage=QPixmap("img/{0}".format(self.productImg))
        self.topleftFrame.setPixmap(self.leftimage)
        self.topleftFrame.setAlignment(Qt.AlignCenter)

        #############wigets for bottom layout########
        self.exitRegBtn=QPushButton("Exit")
        self.exitRegBtn.clicked.connect(self.exitReg)
        self.bottomRightFrame=QLabel()
        self.bottomRightImage=QPixmap("img/{0}".format(self.leftImg))
        self.bottomRightFrame.setPixmap(self.bottomRightImage)
        self.bottomRightFrame.setAlignment(Qt.AlignCenter)
        self.bottomLeftFrame=QLabel()
        self.bottomLeftImage=QPixmap("img/{0}".format(self.rightImg))
        self.bottomLeftFrame.setPixmap(self.bottomLeftImage)
        self.bottomLeftFrame.setAlignment(Qt.AlignCenter)
        self.bottomCenterFrame=QLabel()
        self.bottomCenterImage=QPixmap("img/{0}".format(self.centertImg))
        self.bottomCenterFrame.setPixmap(self.bottomCenterImage)
        self.bottomCenterFrame.setAlignment(Qt.AlignCenter)

    def exitReg(self):
        self.close()


    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QHBoxLayout()
        self.CenterLayout=QFormLayout()
        self.bottomLayout=QHBoxLayout()
        self.topFrame = QFrame()
        self.centerFrame = QFrame()
        self.bottomFrame = QFrame()
        #############top Widgets     ######
        self.topLayout.addWidget(self.toprightFrame)
        self.topLayout.addWidget(self.topleftFrame)
        self.topFrame.setLayout(self.topLayout)
        ###############CenterWidgets ######
        self.CenterLayout.addRow(QLabel(""),self.exitRegBtn)
        self.centerFrame.setLayout(self.CenterLayout)
        ##############bottom WIdget  ######
        self.bottomLayout.addWidget(self.bottomRightFrame)
        self.bottomLayout.addWidget(self.bottomCenterFrame)
        self.bottomLayout.addWidget(self.bottomLeftFrame)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.centerFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

################### Live Recognition  ##################


class Golive(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Recognition")
        self.setWindowIcon(QIcon('icons/'+image_WindowIcon))
        self.setGeometry(450,150,1250,1050)
        oImage = QImage("img/"+image_Golive)
        sImage = oImage.scaled(QSize(1850,1050))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)
        self.setFixedSize(self.size())
        self.UI()
        self.show()



    def UI(self):
        # self.memberDetails()
        self.widgets()
        self.layouts()

    def findPeople(self, features_arr, positions, thres=0.6, percent_thres=70):
        '''
        :param features_arr: a list of 128d Features of all faces on screen
        :param positions: a list of face position types of all faces on screen
        :param thres: distance threshold
        :return: person name and percentage
        '''
        f = open('./facerec_128D.txt', 'r')
        data_set = json.loads(f.read());
        returnRes = [];
        for (i, features_128D) in enumerate(features_arr):
            result = "Unknown";
            smallest = sys.maxsize
            for person in data_set.keys():
                person_data = data_set[person][positions[i]];
                for data in person_data:
                    distance = np.sqrt(np.sum(np.square(data - features_128D)))
                    if (distance < smallest):
                        smallest = distance;
                        result = person;
            percentage = min(100, 100 * thres / smallest)
            if percentage <= percent_thres:
                result = "Unknown"
            returnRes.append((result, percentage))
        return returnRes

    def widgets(self):
        #########widgets for Left layout#######
        self.productImg = "reg.jpg"
        self.Frame=QLabel()
        self.image=QPixmap("img/{0}".format(self.productImg))
        self.Frame.setPixmap(self.image)
        self.Frame.setAlignment(Qt.AlignCenter)
        #############wigets for bottom layout########
        self.startbutton=QPushButton("Start")
        self.startbutton.clicked.connect(self.acceptV)
        self.stopbutton=QPushButton("Stop")
        self.stopbutton.clicked.connect(self.exitV)


    def updatestatusofmember(self, membertoupdate):
        try:
            query=("UPDATE members set member_status='True' WHERE  member_name=\'"+membertoupdate+"\'")
            results=cur.execute(query).fetchall()
            con.commit()
        # resultsnumber = results[3]
            print(str(results) +"updated")
        except:
            print(membertoupdate+"not found in db")

    def acceptV(self):
        self.stopflag = False
        presenttime = time.time()
        cap = cv2.VideoCapture(0)
        while(cap.isOpened()):
            ret, frame = cap.read()
            rects, landmarks = face_detect.detect_face(frame, 80);  # min face size is set to 80x80
            aligns = []
            positions = []
            for (i, rect) in enumerate(rects):
                aligned_face, face_pos = aligner.align(160, frame, landmarks[i])
                if len(aligned_face) == 160 and len(aligned_face[0]) == 160:
                    aligns.append(aligned_face)
                    positions.append(face_pos)
                else:
                    print("Align face failed")  # log
            if (len(aligns) > 0):
                start = time.time()
                features_arr = extract_feature.get_features(aligns)
                recog_data = self.findPeople(features_arr, positions);

                stop = time.time()
                print(recog_data)
                members = []
                if(int(stop - presenttime) > 60):
                    presenttime = time.time()
                    print("updated")
                    for [i, j] in recog_data:
                        members.append(i)
                    for member in members:
                        print(member)
                        self.updatestatusofmember(member)
                seconds = str(1/(stop - start))
                print("time taken is "+seconds)
                cv2.putText(frame,"Recognition time is "+seconds+" per frame" , (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (147,20,255), 2)
                # cv2.putText(frame,str(members[0]), (40, 30),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,20,147), 2)
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                                 QtGui.QImage.Format_RGB888)
                convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
                pixmap = QtGui.QPixmap(convertToQtFormat)
                QtWidgets.QApplication.processEvents()
                self.Frame.setPixmap(pixmap)
            if (self.stopflag):
                break

    def exitV(self):
        self.stopflag = True

    def layouts(self):
        self.mainLayout=QVBoxLayout()
        #####################################
        self.mainLayout.addWidget(self.Frame)
        self.mainLayout.addWidget(self.startbutton)
        self.mainLayout.addWidget(self.stopbutton)
        self.setLayout(self.mainLayout)



########################################################



####################Layout for validation######################


class MemberValidation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Validation of Face with Member details")
        self.setWindowIcon(QIcon('icons/'+image_WindowIcon))
        self.setGeometry(450,150,1250,1050)
        oImage = QImage("img/"+image_MemberValidation)
        sImage = oImage.scaled(QSize(1850,1050))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)
        self.setFixedSize(self.size())
        self.UI()
        self.show()


    def memberDetails(self):
        global memberId
        query=("SELECT * FROM members WHERE member_id=?")
        member=cur.execute(query,(memberId,)).fetchone()
        self.memberName=member[1]
        self.memberemail=member[2]
        self.memberPhone=member[3]
        self.memberFaceData=member[4]
        self.memberFaceImage=member[5]

    def UI(self):
        self.memberDetails()
        self.widgets()
        self.layouts()


    def widgets(self):
        #########widgets for Left layout#######
        self.productImg = "reg.jpg"
        self.lefttopFrame=QLabel()
        self.topimage=QPixmap("img/{0}".format(self.productImg))
        self.lefttopFrame.setPixmap(self.topimage)
        self.lefttopFrame.setAlignment(Qt.AlignCenter)
        self.leftbottomFrame=QLabel()
        self.bottomimage=QPixmap("img/{0}".format(self.productImg))
        self.leftbottomFrame.setPixmap(self.bottomimage)
        self.leftbottomFrame.setAlignment(Qt.AlignCenter)

        #############wigets for bottom layout########
        self.Namelable=QLabel()
        self.Namelable.setText(self.memberName)
        self.Namelable.setAlignment(Qt.AlignCenter)
        self.EmailIDlable=QLabel()
        self.EmailIDlable.setText(self.memberemail)
        self.EmailIDlable.setAlignment(Qt.AlignCenter)
        self.Phonelable=QLabel()
        self.Phonelable.setText(self.memberPhone)
        self.Phonelable.setAlignment(Qt.AlignCenter)
        self.rejectBtn=QPushButton("Accept")
        self.rejectBtn.clicked.connect(self.acceptV)
        self.acceptBtn=QPushButton("Reject")
        self.acceptBtn.clicked.connect(self.exitV)

    def acceptV(self):
        self.MemberVerification=MemberVerification()
        self.MemberVerification.show()
    def exitV(self):
        pass

    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.leftLayout=QVBoxLayout()
        self.rightLayout=QFormLayout()
        self.leftFrame = QFrame()
        self.rightFrame = QFrame()
        #############left Widgets     ######
        self.leftLayout.addWidget(self.lefttopFrame)
        self.leftLayout.addWidget(self.leftbottomFrame)
        self.leftFrame.setLayout(self.leftLayout)
        ###############right Widgets ######
        self.rightLayout.addRow(QLabel("Name"),self.Namelable)
        self.rightLayout.addRow(QLabel("Email ID"),self.EmailIDlable)
        self.rightLayout.addRow(QLabel("Phone Number"),self.Phonelable)
        self.rightLayout.addRow(QLabel(""),self.rejectBtn)
        self.rightLayout.addRow(QLabel(""),self.acceptBtn)
        self.rightFrame.setLayout(self.rightLayout)
        #####################################
        self.mainLayout.addWidget(self.leftFrame)
        self.mainLayout.addWidget(self.rightFrame)
        self.setLayout(self.mainLayout)


####################Layout for Verification######################


class MemberVerification(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Verification")
        self.setWindowIcon(QIcon('icons/'+image_WindowIcon))
        self.setGeometry(450,150,1250,1050)
        oImage = QImage("img/"+image_MemberVerification)
        sImage = oImage.scaled(QSize(1850,1050))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)
        self.setFixedSize(self.size())
        self.UI()
        self.show()


    def memberDetails(self):
        global memberId
        query=("SELECT * FROM members WHERE member_id=?")
        member=cur.execute(query,(memberId,)).fetchone()
        self.memberName=member[1]
        self.memberemail=member[2]
        self.memberPhone=member[3]
        self.memberFaceData=member[4]
        self.memberFaceImage=member[5]

    def UI(self):
        self.memberDetails()
        self.widgets()
        self.layouts()


    def widgets(self):
        #########widgets for Left layout#######
        self.productImg = "reg.jpg"
        self.lefttopFrame=QLabel()
        self.topimage=QPixmap("img/{0}".format(self.productImg))
        self.lefttopFrame.setPixmap(self.topimage)
        self.lefttopFrame.setAlignment(Qt.AlignCenter)

        #############wigets for bottom layout########
        self.Namelable=QLabel()
        self.Namelable.setText(self.memberName)
        self.Namelable.setAlignment(Qt.AlignCenter)
        self.EmailIDlable=QLabel()
        self.EmailIDlable.setText(self.memberemail)
        self.EmailIDlable.setAlignment(Qt.AlignCenter)
        self.Verification=QLabel()
        self.Verification.setText("")
        self.Verification.setAlignment(Qt.AlignCenter)
        # self.Phonelable=QLabel()
        # self.Phonelable.setText("")
        # self.Phonelable.setAlignment(Qt.AlignCenter)
        self.Phonelable=QLabel()
        self.Phonelable.setText(self.memberPhone)
        self.Phonelable.setAlignment(Qt.AlignCenter)
        self.rejectBtn=QPushButton("Capture")
        self.rejectBtn.clicked.connect(self.captureimage)
        self.acceptBtn=QPushButton("Exit")
        self.acceptBtn.clicked.connect(self.exit)

    def findPeople(self, features_arr, positions, thres=0.6, percent_thres=70):
        '''
        :param features_arr: a list of 128d Features of all faces on screen
        :param positions: a list of face position types of all faces on screen
        :param thres: distance threshold
        :return: person name and percentage
        '''
        f = open('./facerec_128D.txt', 'r')
        data_set = json.loads(f.read());
        returnRes = [];
        for (i, features_128D) in enumerate(features_arr):
            result = "Unknown";
            smallest = sys.maxsize
            for person in data_set.keys():
                person_data = data_set[person][positions[i]];
                for data in person_data:
                    distance = np.sqrt(np.sum(np.square(data - features_128D)))
                    if (distance < smallest):
                        smallest = distance;
                        result = person;
            percentage = min(100, 100 * thres / smallest)
            if percentage <= percent_thres:
                result = "Unknown"
            returnRes.append((result, percentage))
        return returnRes

    def captureimage(self):
        cap = cv2.VideoCapture(0);
        ret, frame = cap.read()
        if(ret):
            rects, landmarks = face_detect.detect_face(frame, 80);  # min face size is set to 80x80
            aligns = []
            positions = []

            for (i, rect) in enumerate(rects):
                aligned_face, face_pos = aligner.align(160, frame, landmarks[i])
                if len(aligned_face) == 160 and len(aligned_face[0]) == 160:
                    aligns.append(aligned_face)
                    positions.append(face_pos)
                else:
                    print("Align face failed")  # log
            if (len(aligns) > 0):
                time.sleep(3)

                cap.release()
                features_arr = extract_feature.get_features(aligns)
                recog_data = self.findPeople(features_arr, positions);
                # print(recog_data[0][0])
                if(recog_data[0][0] == self.memberName):
                    self.Verification.setText("Verified as : " + self.memberName)
                    mbox = QMessageBox.question(self, "Info","You have been verified Sucessfully please click Ok to retrun to main window",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if(ret):
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                                 QtGui.QImage.Format_RGB888)
                convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
                pixmap = QtGui.QPixmap(convertToQtFormat)
                resizeImage = pixmap.scaled(256, 256)
                QtWidgets.QApplication.processEvents()
            if ret is not None:
                self.lefttopFrame.setPixmap(resizeImage)
    def exit(self):
        pass

    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.leftLayout=QVBoxLayout()
        self.rightLayout=QFormLayout()
        self.leftFrame = QFrame()
        self.rightFrame = QFrame()
        #############left Widgets     ######
        self.leftLayout.addWidget(self.lefttopFrame)
        self.leftFrame.setLayout(self.leftLayout)
        ###############right Widgets ######
        self.rightLayout.addRow(QLabel("Name"),self.Namelable)
        self.rightLayout.addRow(QLabel("Email ID"),self.EmailIDlable)
        self.rightLayout.addRow(QLabel("Phone Number"),self.Phonelable)
        self.rightLayout.addRow(QLabel(""), self.Verification)
        self.rightLayout.addRow(QLabel(""),self.rejectBtn)
        self.rightLayout.addRow(QLabel(""),self.acceptBtn)
        self.rightFrame.setLayout(self.rightLayout)
        #####################################
        self.mainLayout.addWidget(self.leftFrame)
        self.mainLayout.addWidget(self.rightFrame)
        self.setLayout(self.mainLayout)


#####################Display Pro##################


# class DisplayProduct(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Product Details")
#         self.setWindowIcon(QIcon('icons/face_button.png'))
#         self.setGeometry(450,150,350,600)
#         self.setFixedSize(self.size())
#         self.UI()
#         self.show()
#
#     def UI(self):
#       self.productDetails()
#       self.widgets()
#       self.layouts()
#
#
#     def productDetails(self):
#         global productId
#         query=("SELECT * FROM products WHERE product_id=?")
#         product=cur.execute(query,(productId,)).fetchone()#single item tuple=(1,)
#         self.productName=product[1]
#         self.productManufacturer=product[2]
#         self.productPrice=product[3]
#         self.productQouta=product[4]
#         self.productImg=product[5]
#         self.productStatus=product[6]
#
#     def widgets(self):
#         #################Top layouts wigdets#########
#         self.product_Img=QLabel()
#         self.img=QPixmap('img/{}'.format(self.productImg))
#         self.product_Img.setPixmap(self.img)
#         self.product_Img.setAlignment(Qt.AlignCenter)
#         self.titleText=QLabel("Update Product")
#         self.titleText.setAlignment(Qt.AlignCenter)
#
#         ##############Bottom Layout's widgets###########
#         self.nameEntry=QLineEdit()
#         self.nameEntry.setText(self.productName)
#         self.manufacturerEntry=QLineEdit()
#         self.manufacturerEntry.setText(self.productManufacturer)
#         self.priceEntry=QLineEdit()
#         self.priceEntry.setText(str(self.productPrice))
#         self.qoutaEntry=QLineEdit()
#         self.qoutaEntry.setText(str(self.productQouta))
#         self.availabilityCombo=QComboBox()
#         self.availabilityCombo.addItems(["Available","UnAvailable"])
#         self.uploadBtn=QPushButton("Upload")
#         self.uploadBtn.clicked.connect(self.uploadImg)
#         self.deleteBtn=QPushButton("Delete")
#         self.deleteBtn.clicked.connect(self.deleteProduct)
#         self.updateBtn=QPushButton("Update")
#         self.updateBtn.clicked.connect(self.updateProduct)
#
#
#
#
#     def layouts(self):
#         self.mainLayout=QVBoxLayout()
#         self.topLayout=QVBoxLayout()
#         self.bottomLayout=QFormLayout()
#         self.topFrame=QFrame()
#         self.topFrame.setStyleSheet(style.productTopFrame())
#         self.bottomFrame=QFrame()
#         self.bottomFrame.setStyleSheet(style.productBottomFrame())
#         ###############add widgets###########
#         self.topLayout.addWidget(self.titleText)
#         self.topLayout.addWidget(self.product_Img)
#         self.topFrame.setLayout(self.topLayout)
#         self.bottomLayout.addRow(QLabel("Name: "),self.nameEntry)
#         self.bottomLayout.addRow(QLabel("Manufacturer: "),self.manufacturerEntry)
#         self.bottomLayout.addRow(QLabel("Price: "),self.priceEntry)
#         self.bottomLayout.addRow(QLabel("Qouta: "),self.qoutaEntry)
#         self.bottomLayout.addRow(QLabel("Status: "),self.availabilityCombo)
#         self.bottomLayout.addRow(QLabel("Image: "),self.uploadBtn)
#         self.bottomLayout.addRow(QLabel(""),self.deleteBtn)
#         self.bottomLayout.addRow(QLabel(""),self.updateBtn)
#         self.bottomFrame.setLayout(self.bottomLayout)
#         self.mainLayout.addWidget(self.topFrame)
#         self.mainLayout.addWidget(self.bottomFrame)
#         self.setLayout(self.mainLayout)
#
#
#
#     def uploadImg(self):
#         size =(256,256)
#         self.filename,ok =QFileDialog.getOpenFileName(self,'Upload Image','','Image files (*.jpg *.png)')
#         if ok:
#             self.productImg = os.path.basename(self.filename)
#             img=Image.open(self.filename)
#             img=img.resize(size)
#             img.save("img/{0}".format(self.productImg))
#
#     def updateProduct(self):
#         global productId
#         name = self.nameEntry.text()
#         manufacturer=self.manufacturerEntry.text()
#         price=int(self.priceEntry.text())
#         qouta=int(self.qoutaEntry.text())
#         status=self.availabilityCombo.currentText()
#         defaultImg=self.productImg
#
#         if (name and manufacturer and price and qouta !=""):
#
#             try:
#                 query="UPDATE products set product_name=?, product_manufacturer =?, product_price=?,product_qouta=?, product_img=?, product_availability=? WHERE product_id=?"
#                 cur.execute(query,(name,manufacturer,price,qouta,defaultImg,status,productId))
#                 con.commit()
#                 QMessageBox.information(self,"Info","Product has been updated!")
#             except:
#                 QMessageBox.information(self, "Info", "Product has not been updated!")
#         else:
#             QMessageBox.information(self, "Info", "Fields cant be empty!")
#
#     def deleteProduct(self):
#         global productId
#
#         mbox=QMessageBox.question(self,"Warning","Are you sure to delete this product",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
#
#         if(mbox==QMessageBox.Yes):
#             try:
#                 cur.execute("DELETE FROM products WHERE product_id=?",(productId,))
#                 con.commit()
#                 QMessageBox.information(self,"Information","Product has been deleted!")
#                 self.close()
#
#             except:
#                 QMessageBox.information(self, "Information", "Product has not been deleted!")
#

def main():
    App=QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()