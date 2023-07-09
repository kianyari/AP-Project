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

class categoryProductWindow(QtWidgets.QMainWindow):
    """
    1.goBackBtn, goHomeBtn: go to the all categories oage and go to the main window
    2.add each products with its first look info to the ui in the code
    3.take care of click on each product
    """
    def __init__(self, category_name):
        """initialize home and back button and set the scroll area"""
        super(categoryProductWindow, self).__init__()
        self.ui_address = "side programs ui\\category products.ui"
        loadUi(self.ui_address, self)
        self.goBackBtn.clicked.connect(categoryProductWindow.go_back)
        self.goHomeBtn.clicked.connect(categoryProductWindow.go_home)
        products = pd.read_csv(f"category/{category_name}.csv", index_col=0)
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")

        # create the interface space for each product:
        # 3 labels for name, price and photo
        # 1 widget as parent 
        # 1 hidden button in front for tab on product
        for idx in range(len(products.index)):
            self.widget_3 = QWidget(self.scrollAreaWidgetContents)
            self.widget_3.setObjectName(u"widget_3")
            self.widget_3.setGeometry(QtCore.QRect(75, 60 + 200*idx, 1140, 200))

            

            self.widget_3.setStyleSheet(u"background-color: rgb(0, 0, 0, 0);\n"
                "border: 1px solid rgba(0, 0, 0, 0);\n"
                "border-bottom-color: rgbrgb(157, 178, 191);\n"
                "border-radius: 0px;\n"
                "padding-bottom: 7px;\n"
                "color: rgb(221, 230, 237)\n"
                "")
            self.productName = QLabel(self.widget_3)
            self.productName.setObjectName(u"productName")
            self.productName.setGeometry(QtCore.QRect(144, 20, 751, 81))
            font1 = QFont()
            font1.setPointSize(13)
            font1.setBold(True)
            font1.setWeight(75)
            self.productName.setFont(font1)
            self.productName.setStyleSheet(u"border-color: rgba(0, 0, 0, 0)")
            self.productName.setWordWrap(True)
            self.productName.setText(products.loc[idx, 'name'])
            self.productPhoto = QLabel(self.widget_3)
            self.productPhoto.setScaledContents(True)
            self.productPhoto.setObjectName(u"productPhoto")
            self.productPhoto.setGeometry(QtCore.QRect(940, 15, 170, 170))
            self.productPhoto.setStyleSheet(u"border-color: rgba(0, 0, 0, 0);")
            self.pixmap = QPixmap(f"category/img/{products.loc[idx, 'name']}.png")
            self.productPhoto.setPixmap(self.pixmap)
            self.productPrice = QLabel(self.widget_3)
            self.productPrice.setObjectName(u"productPrice")
            self.productPrice.setGeometry(QtCore.QRect(90, 130, 311, 51))
            font2 = QFont()
            font2.setPointSize(11)
            font2.setBold(True)
            font2.setWeight(75)
            self.productPrice.setFont(font2)
            self.productPrice.setText(str(products.loc[idx, 'price']))
            self.productPrice.setStyleSheet(u"border-color: rgba(0, 0, 0, 0)")
            self.pushButton = QPushButton(self.widget_3)
            self.pushButton.setObjectName(u"pushButton")
            self.pushButton.setGeometry(QtCore.QRect(0, 0, 1140, 200))
            self.pushButton.setStyleSheet(u"QPushButton{\n"
                "	background-color: rgba(0, 0, 0, 0);\n"
                "}\n"
                "\n"
                "QPushButton:hover{\n"
                "	background-color: rgba(105, 152, 171, 80);\n"
                "}")
            self.widget_3.setFixedSize(1140, 200)
            self.productName.setFixedSize(751, 81)
            self.productPhoto.setFixedSize(170, 170)
            self.productPrice.setFixedSize(311, 51)
            self.pushButton.setFixedSize(1140, 200)
            self.verticalLayout.addWidget(self.widget_3)
            self.pushButton.clicked.connect(partial(categoryProductWindow.click_product, products.loc[idx, 'name'], str(products.loc[idx, 'id']), category_name))
            
    @staticmethod
    def click_product(product_name, product_id, category_name):
        """
        after click on product screen goes to the product window
        on product window we can see more details and informations about the product
        """
        product_details = DigikalaFinal.Digikala.details(product_id)
        product_database_address = f"category/{category_name}.csv"
        
        # create the instance for producrWindow
        product_window = productwindow.ProductWindow(
            product_name,
            pd.DataFrame(),
            product_details,
            product_database_address,
            )
        main.Main.widget.addWidget(product_window)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1) # change the ui window


    @staticmethod
    def go_back():
        """go to the all category window by this method"""
        category_window = Category.categoryWindow()
        main.Main.widget.addWidget(category_window)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)

    @staticmethod
    def go_home():
        """go to the main window by this method"""
        main_window = MainWindow.mainWindow()
        main.Main.widget.addWidget(main_window)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)

