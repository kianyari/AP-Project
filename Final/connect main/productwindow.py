import MainWindow
import main
import DigikalaFinal
import Category
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QPushButton, QSizePolicy, QVBoxLayout, QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QFont, QIcon
import pandas as pd
from functools import partial


class ProductWindow(QtWidgets.QMainWindow):
    """
    errorLabel: shows any error happen when hit favorite, category, compare
    mainPriceProduct: shows price of digikala
    productName : shows name of digikala
    productPhoto: set digikala photo
    visitDigikalBtn: go to the digikala link of product
    compareBtn: add to compare list -> verify then save the data
    addCategoryBtn: add to category list -> verify then save the data
    addFavoriteBtn: add to favorite list -> verify then save the data
    backBtn: go to the main window
    2 scroll area for details and sellers that shows information properly
    """
    def __init__(self, product_name, matched_sellers, product_details, database_address):
        """create the whole up information and set the thing in their order"""
        super(ProductWindow, self).__init__()
        self.ui_address = "main ui\\product info.ui"
        loadUi(self.ui_address, self)
        database = pd.read_csv(database_address, usecols=range(1,6)) # remove the untitle from the df
        database = database.set_index("name")
        selected_product = database.loc[product_name]
        self.pixmap = QPixmap("image src\\" + product_name)
        self.productName.setText(product_name)
        self.mainPriceProduct.setText(str(selected_product.price))
        self.productPhoto.setPixmap(self.pixmap)
        self.visitDigikalBtn.clicked.connect(partial(ProductWindow.visit_seller, selected_product.url))
        self.backBtn.clicked.connect(ProductWindow.go_back)
        self.addFavoriteBtn.clicked.connect(partial(self.add_to_favorite, selected_product, product_details))
        self.compareBtn.clicked.connect(partial(self.add_to_compare, selected_product, product_details))
        self.addCategoryBtn.clicked.connect(partial(self.add_to_category, selected_product))

        # if no sellers founded for product
        if len(matched_sellers.index) == 0:
            self.label_notfound = QLabel(self.scrollAreaWidgetContents_2)
            self.label_notfound.setObjectName(u"label notfound")
            self.label_notfound.setGeometry(QtCore.QRect(330, 10, 451, 61))
            font4 = QFont()
            font4.setPointSize(14)
            self.label_notfound.setFont(font4)
            self.label_notfound.setStyleSheet(u"color: rgb(255, 0, 0);")
            self.label_notfound.setText("هیچ فروشنده ای برای محصول شما یافت نشد.")

        else:
            # create the matched sellers list
            matched_sellers = (matched_sellers.reset_index().drop_duplicates(subset='name', keep='last').set_index('name'))
            self.scrollAreaShops.setWidgetResizable(True)
            self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents_2)
            self.verticalLayout_2.setObjectName(u"verticalLayout_2")
            # set each seller and detail in their order
            for idx in range(len(matched_sellers)):
                font1 = QFont()
                font1.setPointSize(10)
                self.pushButton = QPushButton(self.scrollAreaWidgetContents_2)
                self.pushButton.setObjectName(u"pushButton")
                self.pushButton.setFont(font1)
                self.pushButton.setStyleSheet(u"QPushButton{\n"
                    "	\n"
                    "	background-color: rgba(0, 0, 0, 0);\n"
                    "}\n"
                    "\n"
                    "QPushButton:hover{\n"
                    "	\n"
                    "	background-color: rgb(141, 212, 212, 20);\n"
                    "}")
                self.pushButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                seller_info = matched_sellers.iloc[idx]
                self.pushButton.setText(seller_info.name)
                self.pushButton.clicked.connect(partial(ProductWindow.visit_seller, seller_info.url))
                
                font_price = QFont()
                font_price.setPointSize(9)
                self.label_2 = QLabel(self.scrollAreaWidgetContents_2)
                self.label_2.setObjectName(u"label_2")
                # self.label_2.setGeometry(QtCore.QRect(10, 10 + idx * 40, 200, 40))
                self.label_2.setFont(font_price)
                self.label_2.setStyleSheet(u"border: 1px solid rgba(0, 0, 0, 0);\n"
                    "border-bottom-color: rgbrgb(157, 178, 191);\n"
                    "border-radius: 0px;"
                    )
                self.label_2.setWordWrap(True)
                self.label_2.setText(str(seller_info.price))
                self.verticalLayout_2.addWidget(self.pushButton)
                self.verticalLayout_2.addWidget(self.label_2)
                
        self.scrollAreaDetails.setWidgetResizable(True)
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        # write details in its order
        for key, value in product_details.items():
            self.label_3 = QLabel(self.scrollAreaWidgetContents)
            self.label_3.setObjectName(u"label_3")
            self.label_3.setStyleSheet(u"background-color: rgba(141, 212, 212, 20);\n"
                "border: 1px solid rgba(0, 0, 0, 0);\n")
            self.label_3.setWordWrap(True)
            self.label_3.setText(key)

            self.label_4 = QLabel(self.scrollAreaWidgetContents)
            self.label_4.setObjectName(u"label_4")
            self.label_4.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);\n"
                "border: 1px solid rgba(0, 0, 0, 0);\n"
                "border-bottom-color: rgb(157, 178, 191);\n"
                "border-radius: 0px;")
            self.label_4.setWordWrap(True)
            self.label_4.setText(value)
            self.verticalLayout.addWidget(self.label_3)
            self.verticalLayout.addWidget(self.label_4)

    @staticmethod
    def visit_seller(seller_url):
        """open url of seller adv"""
        import webbrowser
        webbrowser.open(seller_url)

    @staticmethod
    def go_back():
        """go to the main window"""
        main_window = MainWindow.mainWindow()
        main.Main.widget.addWidget(main_window)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)

    def add_to_favorite(self, product_info, product_details):
        """
        add it to favorite list using favorite module
        check verification of product and favorite list
        """
        try:
            product_info.to_csv("favorite list\\df fixer.csv")
            fixed_df = pd.read_csv("favorite list\\df fixer.csv", index_col=0)
            fixed_df = fixed_df.T.reset_index()
            fixed_df.columns = ["name", "price", "url", "id", "category_id" ]
            last_favorites = pd.read_csv("favorite list\\favorite.csv", index_col=0)
            if fixed_df["name"].values[0] in list(last_favorites["name"]):
                self.errorLabel.setText("این محصول قبلا ثبت شده است.")
            else:
                merged_favorites = pd.concat([last_favorites, fixed_df], axis=0)
                merged_favorites.to_csv("favorite list\\favorite.csv")

        except:
            product_info.to_csv("favorite list\\df fixer.csv")
            df = pd.read_csv("favorite list\\df fixer.csv", index_col=0)
            df = df.T.reset_index()
            df.columns = ["name", "price", "url", "id", "category_id" ]
            df.to_csv("favorite list\\favorite.csv", index=False)
        
    def add_to_compare(self, product_info, product_details):
        """
        add it to compare list using compare module
        check verification of product and compare list
        """
        try:
            product_info["detail"] = product_details
            last_compare = pd.read_csv("compare list\\compare.csv", index_col=0)
            row, col = last_compare.shape        
            if col == 2:
                self.errorLabel.setText("لیست مقایسه پر است.")
            elif product_info.category_id == int(list(last_compare.loc["category_id"])[0]):
                merged_favorites = pd.concat([last_compare, product_info], axis=1)
                merged_favorites.to_csv("compare list\\compare.csv")
            else:
                self.errorLabel.setText("امکان مقایسه وجود ندارد.")

        except:
            product_info["detail"] = product_details
            product_info.to_csv("compare list\\compare.csv")

    def category_proccess(self, product_info):
        """add clean data to category"""
        name = self.get_category_name.text()
        category_names = open("category_names.txt", "r+")
        if name not in category_names.read():

            category_names.write("\n" + name)
            
            DigikalaFinal.Digikala.add_category(selected_product= product_info, category_name=name)
            info = pd.read_csv(f"category/{name}.csv", index_col=0)
            new_info = info._append({'name': product_info.name, 'price': product_info.price, 'url': product_info.url, 'id': product_info.id, 'category_id': product_info.category_id}, ignore_index=True)
            new_info.to_csv(f"category/{name}.csv")
        else:
            info = pd.read_csv(f"category/{name}.csv", index_col=0)
            new_info = info._append({'name': product_info.name, 'price': product_info.price, 'url': product_info.url, 'id': product_info.id, 'category_id': product_info.category_id}, ignore_index=True)
            new_info.to_csv(f"category/{name}.csv")
        
        category_names.close()
        
        
        
    def add_to_category(self, product_info):
        """organize and cleaning data and get input the name from the user"""
        self.get_category_name = QLineEdit(self.widget_3)
        self.get_category_name.setObjectName(u"lineEdit")
        self.get_category_name.setGeometry(QtCore.QRect(290, 330, 241, 31))
        self.get_category_name.setStyleSheet(u"background-color: rgb(82, 109, 130);")
        self.get_category_name.setPlaceholderText("نام دسته بندی را وارد کنید.")
        self.get_category_name.show()
        self.sendCategoryName = QPushButton(self.widget_3)
        self.sendCategoryName.setObjectName(u"sendCategoryName")
        self.sendCategoryName.setGeometry(QtCore.QRect(259, 330, 31, 28))
        icon3 = QIcon()
        icon3.addFile(u"main ui/check.png", QtCore.QSize(), QIcon.Normal, QIcon.Off)
        self.sendCategoryName.setIcon(icon3)
        self.sendCategoryName.show()
        # after click button send name the category with name is ready to go to the category module
        self.sendCategoryName.clicked.connect(partial(self.category_proccess, product_info)) 

        

        