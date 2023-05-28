import sys
import re
import hashlib
import requests
import json
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from cryptography.fernet import Fernet
from login import Ui_login_form
from home import Ui_home_form
from buatakun import Ui_buat_akun_Form


def encr(data):
    key = b'6uNyOfjhKw8E2WwW2WQZ2rzQh0mkrNzXzf7KNLby9Zs='
    fernet = Fernet(key)

    ts = time.localtime()
    tnow = time.strftime("%Y-%m-%d %H:%M:%S", ts)

    # print("Masukkan Suhu:")
    # input_suhu = input("> ") + "tubesPPLJ"
    encData = fernet.encrypt(data.encode())
    return encData

def password_check(passwd):
    SpecialSym =['$', '@', '#', '%']
    val = True
    global response
    response=""
    if len(passwd) < 6:
        print('length should be at least 6')
        response = "" + "length should be at least 6, "
        val = False
    if len(passwd) > 20:
        print('length should be not be greater than 8')
        response = response + "length should be not be greater than 8, "
        val = False
 
    # Check if password contains at least one digit, uppercase letter, lowercase letter, and special symbol
    has_digit = False
    has_upper = False
    has_lower = False
    has_sym = False
    for char in passwd:
        if ord(char) >= 48 and ord(char) <= 57:
            has_digit = True
        elif ord(char) >= 65 and ord(char) <= 90:
            has_upper = True
        elif ord(char) >= 97 and ord(char) <= 122:
            has_lower = True
        elif char in SpecialSym:
            has_sym = True
 
    if not has_digit:
        print('Password should have at least one numeral')
        response = response + "Password should have at least one numeral, "
        val = False
    if not has_upper:
        print('Password should have at least one uppercase letter')
        response = response + "Password should have at least one uppercase letter, "
        val = False
    if not has_lower:
        print('Password should have at least one lowercase letter')
        response = response + "Password should have at least one lowercase letter, "
        val = False
    if not has_sym:
        print('Password should have at least one of the symbols $@#')
        response = response + "Password should have at least one of the symbols $@# "
        val = False
 
    return val

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        # loadUi("login.ui", self) 
        self.ui = Ui_login_form()
        self.ui.setupUi(self)
        # self.session = requests.Session()
        self.ui.loginbutton.clicked.connect(self.loginfunction)
        self.ui.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.buatakunbutton.clicked.connect(self.gotocreate)
        self.ui.responsetext.hide()

    def loginfunction(self):
        global username
        
        username=self.ui.username.text()
        password=self.ui.password.text()
        validinput=password_check(password)
        if(validinput):
            hash_pass=hashlib.sha256(password.encode('utf-8')).hexdigest()
            login=True
            print("Login berhasil", username, " ", password, " ", hash_pass)
            
            new_acc = {
                "username": username,
                "password": password,
                "full_name": username
            }
            url_postacc = "http://192.168.43.214:8000/login"
            try:
                post_response = requests.post(url_postacc, json=new_acc)
                # data = json.loads(post_response.text)
                post_response_json = post_response.json()
                print(post_response_json)
                global token
                token=str(post_response_json["token"])
                print(token)
                # Process the JSON data
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e}")
            
            if 'token' in post_response_json:
                self.gotoindex()
            else: 
                tokenresponse="Token not found in response."
                self.ui.responsetext.setText(tokenresponse)
                self.ui.responsetext.show()
                
        else:
            print("Input tidak valid")
            self.ui.responsetext.setText(response)
            self.ui.responsetext.show()
    
    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoindex(self):
        index=Index()
        widget.addWidget(index)
        widget.setCurrentIndex(widget.currentIndex()+1)        

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        # loadUi("buatakun.ui", self)
        self.ui = Ui_buat_akun_Form()
        self.ui.setupUi(self)

        self.ui.registerbutton.clicked.connect(self.createaccfunction)
        self.ui.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.confirm_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.kembalibutton.clicked.connect(self.gotohome)
        self.ui.responseregtext.hide()

    def createaccfunction(self):
        username=self.ui.username.text()
        password=self.ui.password.text()
        validinput=password_check(password)
        self.ui.responseregtext.setText(response)
        self.ui.responseregtext.show()
        if validinput==True:
            if self.ui.password.text()==self.ui.confirm_password.text():
                password=self.ui.password.text()
                if (password_check(password)==True):
                    password_valid=self.ui.password.text()
                    hash_pass=hashlib.sha256(password_valid.encode('utf-8')).hexdigest()

                    new_acc = {
                        "username": username,
                        "password": password_valid,
                        "full_name": username,
                    }
                    url_postacc = "http://192.168.43.214:8000/register"

                    try:
                        post_response = requests.post(url_postacc, json=new_acc)
                        # data = json.loads(post_response.text)
                        post_response_json = post_response.json()
                        print(post_response_json)
                        # Process the JSON data
                    except json.JSONDecodeError as e:
                        print(f"JSON decoding error: {e}")

                    print("Register Berhasil ", username, " ", password_valid, " ", hash_pass)
                    self.gotohome()
            else:
                print("Password tidak sesuai")
                responsereg = "Password tidak sesuai"
                self.ui.responseregtext.setText(responsereg)

    def gotohome(self):
        gotohome=Login()
        widget.addWidget(gotohome)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
class Index(QDialog):
    def __init__(self):
        super(Index,self).__init__()
        # loadUi("home.ui", self)
        self.ui = Ui_home_form()
        self.ui.setupUi(self)
        # self.session = requests.Session()
        self.ui.suhusubmitbutton.clicked.connect(self.sendsuhufunction)
        self.ui.Logoutbutton.clicked.connect(self.logout)
        self.ui.usernameaccount.setText(username)
        self.ui.tablemonitoringWidget.setColumnWidth(0,150)
        self.ui.tablemonitoringWidget.setColumnWidth(1,150)
        self.ui.tablemonitoringWidget.setColumnWidth(2,150)
        self.ui.tablemonitoringWidget.setColumnWidth(3,150)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.loadData)
        self.timer.start(5000)  # Refresh data every 5 seconds (adjust the interval as needed)

        self.loadData()
    
    def loadData(self):
        url = "http://192.168.43.214:8000/messages"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        response = requests.get(url, headers=headers)
        response_json = response.json()
        response_json = response_json[:100]
        print(response_json)
        # response_json = [{'received_time': '2023-05-25T04:11:11.666Z', 'id_message': 1, 'id_device': 1, 'id_user': None, 'suhu': 23.7}]
        row=0
        self.ui.tablemonitoringWidget.setRowCount(len(response_json))
        for data in response_json:
            self.ui.tablemonitoringWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(data["room"])))
            self.ui.tablemonitoringWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(data['suhu'])))
            self.ui.tablemonitoringWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data['received_time'])))

            if data['id_user'] is None:
                self.ui.tablemonitoringWidget.setItem(row, 3, QtWidgets.QTableWidgetItem("Auto"))
            else:
                self.ui.tablemonitoringWidget.setItem(row, 3, QtWidgets.QTableWidgetItem("Manual"))

            row=row+1
    
    def logout(self):
        logout=Login()
        widget.addWidget(logout)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def sendsuhufunction(self):
        datasuhu=self.ui.datasuhu.text()
        dataencr=encr(datasuhu)
        ts = time.localtime()
        tnow = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        
        suhujson = {
            "id_device": 1,
            "id_user": 1,
            "suhu": datasuhu,
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        url_sendsuhu = "http://192.168.43.214:8000/messages"
        try:
            post_response = requests.post(url_sendsuhu, headers=headers, json=suhujson)
            # data = json.loads(post_response.text)
            post_response_json = post_response.json()
            # print(post_response_json)
            # Process the JSON data
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
        
        # self.gotoindex()
        # print(new_data)

        with open("history.txt", "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0 :
                file_object.write("\n")
            # Append text at the end of file
            history = str(username + " " + tnow + " " + datasuhu + " " + str(dataencr))
            file_object.write(history)

app=QApplication(sys.argv)
mainwindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(975)
widget.setFixedHeight(823)
widget.show()
app.exec()