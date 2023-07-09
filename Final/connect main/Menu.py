import main
import MainWindow
import Category
import favoriteList
import compareWindow
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from functools import partial

class MenuWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        """
        1.category: 15 categories -> more info in its module
        2.favorite list: user can add and remove his favorite products from this tab
        3.compare list: compare 2 products with same category id 
        """
        super(MenuWindow, self).__init__()
        self.ui_address = "side programs ui\\menu.ui"
        loadUi(self.ui_address, self)
        self.goHomeBtn.clicked.connect(MenuWindow.go_home)
        self.gotoCategoriesBtn.clicked.connect(MenuWindow.go_categories)
        self.gotoFavoriteBtn.clicked.connect(MenuWindow.go_favorites)
        self.gotoCompareBtn.clicked.connect(MenuWindow.go_compare)

    @staticmethod
    def go_home():
        """go to main window"""
        main_window = MainWindow.mainWindow()
        main.Main.widget.addWidget(main_window)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)

    @staticmethod
    def go_categories():
        """go to categories tab -> category module can help us"""
        category_instance = Category.categoryWindow()
        main.Main.widget.addWidget(category_instance)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)

    @staticmethod
    def go_favorites():
        """go to favorites tab -> favorite module can help us"""
        favorites_instance = favoriteList.Favorites()
        main.Main.widget.addWidget(favorites_instance)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)

    @staticmethod
    def go_compare():
        """go to compare tab -> compare module can help us"""
        compare_list_instance = compareWindow.CompareWindow()
        main.Main.widget.addWidget(compare_list_instance)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)