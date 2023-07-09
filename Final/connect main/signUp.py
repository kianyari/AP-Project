import sys 
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import pandas as pd
import login
import main
import MainWindow

class SignUp(QtWidgets.QMainWindow):
    # our offline database -> data.csv
    csv_address = "login code\\data.csv"
    df = pd.read_csv(csv_address)
    def __init__(self):
        super(SignUp, self).__init__()
        self.ui_address = "login form ui\\sign up.ui"
        loadUi(self.ui_address, self)

        self.signUpBtn.clicked.connect(self.sign_up)
        self.showPass.stateChanged.connect(self.show_pass)
        self.loginAccBtn.clicked.connect(self.goto_login)

        
    @staticmethod
    def is_valid_email(email):
        """Check validation of Email that should be <example@gamil.com> form"""
        import re   
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
        if(re.search(regex,email)):   
            return True
        return False

    @staticmethod
    def is_strong_password(password):
        """Check security of password -> number + lowercase + uppercase + symbol"""
        import re
        # Check if the password has at least 6 characters
        if len(password) < 6:
            return False
        # Check if the password contains at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False
        # Check if the password contains at least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False
        # Check if the password contains at least one digit
        if not re.search(r'\d', password):
            return False
        # Check if the password contains at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        # If all the conditions are set, the password is valid
        return True

    @staticmethod
    def verify_information(username, email, password, re_password):
        """
        verifiacte information
            check all fields are filled
            username should not be duplicated
            validation of email address form
            strongness of password
            pass and its confirm being the same

        """
        if len(username) == 0 or len(email) == 0 or len(password) == 0 or len(re_password) == 0:
            return "All fields are required to be filled."

        if len(SignUp.df.loc[SignUp.df.username == username]) != 0:
            return "This name is already taken."

        if not SignUp.is_valid_email(email): # staticmethod that check validation of email 
            return "Email address is invalid."

        if not SignUp.is_strong_password(password):
            return "The password is too weak"

        if re_password != password:
            return "Password & confirm password do not match."
        
        return True


    def sign_up(self):
        result_verification = self.verify_information(
            self.usernameInput.text(),
            self.emailInput.text(),
            self.passwordInput.text(),
            self.confirmPassInput.text()
            )
        if result_verification == True:
            new_user = pd.DataFrame(
                {
                    "username": self.usernameInput.text(),
                    "password": self.passwordInput.text(),
                    "email": self.emailInput.text()
                },
                index =[0]
                )
            SignUp.df = pd.concat([new_user, SignUp.df]).reset_index(drop = True)
            SignUp.df.to_csv(SignUp.csv_address, index=False)
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
            self.confirmPassInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)
            self.confirmPassInput.setEchoMode(QtWidgets.QLineEdit.Password)

    def goto_login(self):
        login_window = login.Login()
        main.Main.widget.addWidget(login_window)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)
    

