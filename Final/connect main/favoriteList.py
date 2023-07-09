import main
import MainWindow
import DigikalaFinal
import productwindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget, QLayout
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QFont, QIcon
import pandas as pd
from functools import partial

class Favorites(QtWidgets.QMainWindow):
    """
    goHomeBtn: go to the main window
    every favorite product will be add to this section
    create the button and etc for each product to show the user
    capibility of remove and add to the favorite list is  in access
    """
    def __init__(self):
        """create the semi empty window plus go home button"""
        super(Favorites, self).__init__()
        self.ui_address = "side programs ui\\favorite list.ui"
        loadUi(self.ui_address, self)
        self.goHomeBtn.clicked.connect(Favorites.go_home)

        # read the dataframe that created in product window with add a product to the favorite list
        products = pd.read_csv(f"favorite list/favorite.csv", usecols=["name", "price", "url", "id", "category_id"])
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
            try:
                self.pixmap = QPixmap(f"image src\\{products.loc[idx, 'name']}.jpg")
            except:
                pass
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
            self.removeFavoriteProduct = QPushButton(self.widget_3)
            self.removeFavoriteProduct.setObjectName(u"removeFavoriteProduct")
            self.removeFavoriteProduct.setGeometry(QtCore.QRect(0, 0, 51, 51))
            self.removeFavoriteProduct.setStyleSheet(u"\n"
                "border : 2px solid rgb(122, 46, 46);\n"
                "border-radius: 25px;")
            icon3 = QIcon()
            icon3.addFile(u"side programs ui\\delete.png", QtCore.QSize(), QIcon.Normal, QIcon.Off)
            self.removeFavoriteProduct.setIcon(icon3)
            self.removeFavoriteProduct.setIconSize(QtCore.QSize(35, 37))
            self.removeFavoriteProduct.clicked.connect(partial(Favorites.remove_product, idx))
            self.pushButton = QPushButton(self.widget_3)
            self.pushButton.setObjectName(u"pushButton")
            self.pushButton.setGeometry(QtCore.QRect(90, 0, 1050, 200))
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
            self.pushButton.clicked.connect(partial(Favorites.click_product, products.loc[idx, 'name'], str(products.loc[idx, 'id'])))

    @staticmethod
    def click_product(product_name, product_id):
        """
        after click on product screen goes to the product window
        on product window we can see more details and informations about the product
        """
        product_details = DigikalaFinal.Digikala.details(product_id)
        product_database_address = f"favorite list/favorite.csv"
        df = pd.read_csv(product_database_address)
        df = df.set_index("name")
        # create an instance for product window to see more about product
        product_window = productwindow.ProductWindow(
            product_name,
            pd.DataFrame(),
            product_details,
            product_database_address,
            )
        main.Main.widget.addWidget(product_window)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)

    @staticmethod
    def remove_product(idx):
        """
        capibility of remove product from the favorite list 
        drop product from the dataframe(database)
        refresh the screen
        """
        favorite_products = pd.read_csv("favorite list\\favorite.csv", usecols=["name", "price", "url", "id", "category_id"])
        favorite_products.drop(index=idx, inplace=True) # delete a product from dataframe
        favorite_products.to_csv("favorite list\\favorite.csv")
        favorites_instance = Favorites()
        main.Main.widget.addWidget(favorites_instance)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1) # refresh the screen


    @staticmethod
    def go_home():
        """go to main window"""
        main_window = MainWindow.mainWindow()
        main.Main.widget.addWidget(main_window)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)