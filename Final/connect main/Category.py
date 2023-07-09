import main
import MainWindow
import categoryProduct
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import pandas as pd
from functools import partial
import io


class categoryWindow(QtWidgets.QMainWindow):
    """
    goHomeBtn and profileInfoBtn: go to the main window and shows user information
    product1-15: buttons by click on each directory you can see its products in it
    we have maximum 15 productsin category window -> by default we will give 10 of them to user
    user can add its products to the new or exist category
    """
    category_names = []
    category_names_file = open("category_names.txt", "r") # save the names to use after closing program
    for name in category_names_file:
        name = name.replace("\n", "") # clean the names of we saved before
        category_names.append(name) # add to list to use them now
    category_names_file.close()
    
    def __init__(self):
        """
        create the frist look of program 
        """
        super(categoryWindow, self).__init__()
        self.ui_address = "side programs ui\\category.ui" # ui address of this module
        loadUi(self.ui_address, self) # actualli connect the graphic from the ui file into the backend
        self.goHomeBtn.clicked.connect(categoryWindow.go_home)
        count_categories = len(categoryWindow.category_names)

        # hide the extra buttons 
        for idx in range(count_categories, 15):
            eval(f"self.product{idx + 1}.setStyleSheet(u'color: rgba(0, 0, 0, 0);')")
        
        for idx in range(len(categoryWindow.category_names)):
            # connect each buttons to its target
            eval(f"self.product{idx+1}.clicked.connect(partial(categoryWindow.click_category,categoryWindow.category_names[{idx}]))")
            # set the name of each button in it
            eval(f"self.product{idx+1}.setText(categoryWindow.category_names[{idx}])")
            
    @staticmethod
    def go_home():
        """go to the main window by this method"""
        main_window = MainWindow.mainWindow()
        main.Main.widget.addWidget(main_window)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)

    @staticmethod
    def click_category(category_name):
        """when clicked each category you can see its products"""
        category_product = categoryProduct.categoryProductWindow(category_name)
        main.Main.widget.addWidget(category_product)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)


    