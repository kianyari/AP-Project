import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import os
import login


class Main():
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    def run():    
        login_window = login.Login()
        Main.widget.addWidget(login_window)
        Main.widget.setFixedHeight(855)
        Main.widget.setFixedWidth(1290)
        Main.widget.show()
        Main.app.exec_()

        try:
            os.remove("products information\\digikala.csv")
            os.remove("products information\\sellers.csv")
        except:
            pass

        try:
            os.remove("compare list/compare.csv")
        except:
            pass
