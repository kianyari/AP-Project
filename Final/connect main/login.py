import sys 
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import pandas as pd
import signUp
import main
import MainWindow
import EmailSender
from functools import partial




class Login(QtWidgets.QMainWindow):
    # our offline database -> data.csv
    csv_address = "login code\\data.csv"
    df = pd.read_csv(csv_address)

    def __init__(self):
        super(Login, self).__init__()
        self.ui_address = "login form ui\\login gui.ui"
        loadUi(self.ui_address, self)
        self.loginBtn.clicked.connect(self.login)
        self.showPass.stateChanged.connect(self.show_pass)
        self.createAccBtn.clicked.connect(self.goto_sign_up)
        # for idx in range(len(Login.df.index())):
        self.forgotPass.clicked.connect(self.password_proccess)

    @staticmethod
    def verify_user(username, password):
        if len(Login.df.loc[Login.df.username == username]) == 0:
            return "Username not found"
        elif len(Login.df.loc[Login.df.password == password]) == 0:
            return "Incorrect password"
        return True

    def login(self):
        if len(self.usernameInput.text()) == 0 or len(self.passwordInput.text()) == 0:
            self.errorLabel.setText("All fields are required to be filled.")

        result_verification = self.verify_user(
            self.usernameInput.text(),
            self.passwordInput.text()
            )

        if result_verification == True:
            current_user = open("login code\\currentUser.csv", "w")
            current_user.write(self.usernameInput.text())
            main_window = MainWindow.mainWindow()
            main.Main.widget.addWidget(main_window)
            main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)
            
        else:
            self.errorLabel.setText(result_verification)


    def show_pass(self):
        if self.showPass.isChecked():
            self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)

    def goto_sign_up(self):
        signup_window = signUp.SignUp()
        main.Main.widget.addWidget(signup_window)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)\
        


    def recover_password(self):
        username = self.usernameInput.text()
        return username
        # email = Login.df[Login.df['username'] == 'mobin'].email[0]
        # password = Login.df[Login.df["username"] == username].password[0]
        # print(email, password)



    def password_proccess(self):
        username = self.recover_password()
        
        temp = Login.df[Login.df["username"] == username]
        password = temp.loc[1, 'password']
        email = temp.loc[1, 'email']
        EmailSender.EmailSender.send_email(email, password)
