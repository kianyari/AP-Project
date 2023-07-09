from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget, QLayout
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QFont 
import pandas as pd
from functools import partial
import Category
import main
import MainWindow
import os
import DigikalaFinal
import productwindow
import Menu



class CompareWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(CompareWindow, self).__init__()
        self.ui_address = "side programs ui\\compare.ui"
        loadUi(self.ui_address, self)
        self.goHomeBtn.clicked.connect(CompareWindow.go_home)
        self.clearCompareList.clicked.connect(self.clearcompare)
        try:
            products = pd.read_csv("compare list/compare.csv", index_col=0)
            products = products.T.reset_index()
        except:
            return 
        
        if len(products['index']) == 2:
            first_product_name = products.loc[0, 'index']
            first_product_price = products.loc[0, 'price']
            first_product_detail = eval(products.loc[0, 'detail'])
            second_product_name = products.loc[1, 'index']
            second_product_price = products.loc[1, 'price']
            second_product_detail = eval(products.loc[1, 'detail'])
            
            self.nameProduct1.setText(first_product_name)
            self.priceProduct1.setText(first_product_price)
            self.pixmap1 = QPixmap("image src\\" + first_product_name)
            self.photoProduct1.setPixmap(self.pixmap1)
            
            self.nameProduct2.setText(second_product_name)
            self.priceProduct2.setText(second_product_price)
            self.pixmap2 = QPixmap("image src\\" + second_product_name)
            self.photoProduct2.setPixmap(self.pixmap2)

            self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
            self.verticalLayout.setObjectName(u"verticalLayout")
            
            self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents_2)
            self.verticalLayout_2.setObjectName(u"verticalLayout2")
            
            
            for key, value in first_product_detail.items():
                self.label_2 = QLabel(self.scrollAreaWidgetContents)
                self.label_2.setObjectName(u"label_2")
                # self.label_2.setGeometry(QtCore.QRect(0, 0, 450, 60))
                self.label_2.setWordWrap(True)
                self.label_3 = QLabel(self.scrollAreaWidgetContents)
                self.label_3.setObjectName(u"label_3")
                # self.label_3.setGeometry(QtCore.QRect(0, 60, 450, 60))
                self.label_3.setWordWrap(True)
                self.label_3.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);\n"
                "border: 1px solid rgba(0, 0, 0, 0);\n"
                "border-bottom-color: rgb(157, 178, 191);\n"
                "border-radius: 0px;")
                self.scrollAreaDetails.setWidget(self.scrollAreaWidgetContents)
                self.label_2.setText(key)
                self.label_3.setText(value)

                self.verticalLayout.addWidget(self.label_2)
                self.verticalLayout.addWidget(self.label_3)

        
        
        
            for key, value in second_product_detail.items():
                self.label_4 = QLabel(self.scrollAreaWidgetContents_2)
                self.label_4.setObjectName(u"label_4")
                # self.label_4.setGeometry(QtCore.QRect(0, 0, 450, 60))
                self.label_4.setWordWrap(True)
                self.label_5 = QLabel(self.scrollAreaWidgetContents_2)
                self.label_5.setObjectName(u"label_5")
                # self.label_5.setGeometry(QtCore.QRect(0, 60, 450, 60))
                self.label_5.setWordWrap(True)
                self.label_5.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);\n"
                "border: 1px solid rgba(0, 0, 0, 0);\n"
                "border-bottom-color: rgb(157, 178, 191);\n"
                "border-radius: 0px;")
                self.scrollAreaDetails_2.setWidget(self.scrollAreaWidgetContents_2)
                # self.widget_3 = QWidget(self.widget)
                # self.widget_3.setObjectName(u"widget_3")
                # self.widget_3.setGeometry(QtCore.QRect(130, 300, 450, 631))
                # self.widget_3.setStyleSheet(u"QWidget{\n"
                #     "	background-color: rgb(0, 0, 0, 70);\n"
                #     "	border-radius: 10px;\n"
                #     "}\n"
                #     "\n"
                #     "QWidget:hover{\n"
                #     "	background-color: rgba(71, 78, 104, 50);\n"
                #     "\n"
                #     "}")
                self.label_4.setText(key)
                self.label_5.setText(value)
                self.verticalLayout_2.addWidget(self.label_4)
                self.verticalLayout_2.addWidget(self.label_5)

        # if len(products['index']) == :
        #     pass
            


        
           

    @staticmethod
    def go_home():
        main_window = MainWindow.mainWindow()
        main.Main.widget.addWidget(main_window)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)


    def clearcompare(self):
        try:
            os.remove("compare list/compare.csv")
        except:
            pass
        menue = Menu.MenuWindow()
        main.Main.widget.addWidget(menue)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)