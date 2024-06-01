import interface
from PyQt5 import QtCore, QtWidgets
import requests
from datetime import datetime
import reglog_ui


USER = ""
#serverUrl = 'http://95.165.142.216:5000'
serverUrl = 'http://127.0.0.1:5000'

class Registration(QtWidgets.QMainWindow, reglog_ui.Ui_MainWindow):
    def __init__(self):
        super(Registration, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("Registration")
        self.error.setText("")
        self.label.setText("Registration")
        self.label_2.setText("Nickname")
        self.label_3.setText("Password")
        self.regButton.clicked.connect(self.reg)
        self.logButton.clicked.connect(self.open_log)

    def open_log(self):
        self.login = Login()
        self.login.show()
        self.hide()

    def reg(self):
        user_nickname = self.nicknameInput.text()
        user_password = self.passwordInput.text()

        if user_nickname == "":
            self.error.setText("Incorrect nickname!")
            return
        if user_password == "":
            self.error.setText("Incorrect password!")
            return

        if len(user_nickname) > 3:
            try:
                response = requests.post(
                    url=f"{serverUrl}/register", 
                    json={
                        'nickname': user_nickname, 
                        'password': user_password 
                        })
            except Exception as e:
                print("Server is unavailable!\n" + e)
                return

            if response.status_code == 200:
                self.error.setText("Error during registration!")
                self.nameInput.setText("")
                self.passwordInput.setText("")
                return
            
            self.error.setText("Sucesfully registered!")

            global USER
            USER = user_nickname
        else:
            self.error.setText("Nickname must be at least 4 characters long!")


        self.open_messanger()
        return


    def open_messanger(self):
        self.messenger = Messenger()
        self.messenger.show()
        self.hide()

class Login(QtWidgets.QMainWindow, reglog_ui.Ui_MainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Login")

        self.label.setText("Login")
        self.label_2.setText("Nickname")
        self.label_3.setText("Password")
        self.regButton.clicked.connect(self.open_reg)
        self.logButton.clicked.connect(self.log)
        self.error.setText("")

    def open_reg(self):
        self.registration = Registration()
        self.registration.show()
        self.hide()

    def log(self):
        user_nickname = self.nicknameInput.text()
        user_password = self.passwordInput.text()


        if user_nickname == "":
            self.error.setText("Incorrect nickname!")
            return

        if user_password == "":
            self.error.setText("Incorrect password!")
            return

        if len(user_nickname) > 0:
            try:
                response = requests.post(
                    url=f"{serverUrl}/login", 
                    json={
                        'nickname': user_nickname, 
                        'password': user_password 
                        })
            except Exception as e:
                print("Server is unavailable!\n" + e)
                return

            if response.status_code == 200:
                self.error.setText("Error during login!")
                self.nicknameInput.setText("")
                self.passwordInput.setText("")
                return

            self.error.setText("Sucesfully logged in!")

            global USER
            USER = user_nickname

        self.open_messanger()
        return


    def open_messanger(self):
        self.messenger = Messenger()
        self.messenger.show()
        self.hide()  


class Messenger(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    def __init__(self):
        super(Messenger, self).__init__()
        self.setupUi(self)
        self.after = 0
        self.sendButton.clicked.connect(self.send_message)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_message)
        self.timer.start(1000)


    def show_messages(self, message):
        item = QtWidgets.QListWidgetItem()
        dt = datetime.fromtimestamp(message['time'])

        if message['name'] == USER:
            item.setTextAlignment(QtCore.Qt.AlignRight)

        item.setText(f"{message['name']} {dt.strftime('%H:%M')}\n{message['text']}\n")
        self.listWidget.addItem(item)
    
    def get_message(self):
        try:
            response = requests.get(url=f"{serverUrl}/messages", params={'after': self.after})
        except Exception as e:
            print(e)
            return
        messages = response.json()['messages']
        for i in range(len(messages)):
            self.show_messages(messages[i])
            self.after = messages[i]['time']
            self.listWidget.scrollToBottom()

    def send_message(self):
        global USER

        name = USER
        text = self.textEdit.toPlainText()
        if len(name) > 0 and len(text) > 0:
            try:
                response = requests.post(url=f"{serverUrl}/send", json={'name': name, 'text': text})
            except Exception as e:
                item = QtWidgets.QListWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setText("Server is unavailable!\n")
                self.listWidget.addItem(item)
                print(e)
                return
            if response.status_code != 200:
                item = QtWidgets.QListWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setText(f"Incorrect message or name!\n")
                self.listWidget.addItem(item)
                return
            self.textEdit.clear()
            

if __name__ == '__main__':
    try:
        App = QtWidgets.QApplication([])
        window = Login()
        window.show()
        App.exec_()
    except KeyboardInterrupt:
        exit()