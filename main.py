import json

from PySide6.QtCore import (
    QRect,
    Slot,
    Qt
)
from PySide6.QtGui import (
    QFont,
    QIcon
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QLineEdit,
    QWidget,
    QLabel
)

from data import *  # getAge, getGender, and getNationality
import resources


with open("codes.json") as codes:
    countryCodes = sorted(json.load(codes))


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle(self.tr(u"Age and Gender From Name"))
        self.setWindowIcon(QIcon("://winico.png"))
        self.setFixedSize(500, 450)
        
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        
        self.enterNameLabel = QLabel(self.tr(u"Enter your name & Country Code:"), self.centralwidget)
        self.enterNameLabel.setObjectName(u"enterNameLabel")
        self.enterNameLabel.setGeometry(QRect(120, 60, 261, 51))
        self.enterNameLabel.setFont(QFont("Segoe UI", 12))
        self.enterNameLabel.setAlignment(Qt.AlignCenter)

        self.guessInfoButton = QPushButton(self.tr(u"Guess Age and Gender!"), self.centralwidget)
        self.guessInfoButton.setObjectName(u"guessInfoButton")
        self.guessInfoButton.setGeometry(QRect(160, 360, 181, 31))
        self.guessInfoButton.setFont(QFont('Segoe UI', 11))
        self.guessInfoButton.clicked.connect(self.setData)
        
        self.nameLineEdit = QLineEdit(self.centralwidget)
        self.nameLineEdit.setObjectName(u"nameLineEdit")
        self.nameLineEdit.setGeometry(QRect(140, 120, 221, 31))
        self.nameLineEdit.setFont(QFont('Segoe UI', 11))
        self.nameLineEdit.setPlaceholderText(self.tr(u"Enter your name here!"))
        self.nameLineEdit.setClearButtonEnabled(True)
        self.nameLineEdit.returnPressed.connect(self.guessInfoButton.click)
    
        self.countryComboBox = QComboBox(self.centralwidget)
        self.countryComboBox.addItems(countryCodes)
        self.countryComboBox.setObjectName(u"countryComboBox")
        self.countryComboBox.setGeometry(QRect(218, 170, 61, 22))
        self.countryComboBox.setCurrentText(self.locale().countryToCode(self.locale().territory()))
        
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(160, 210, 250, 131))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        
        self.ageLabel = QLabel(self.tr(u"Age: "), self.verticalLayoutWidget)
        self.ageLabel.setObjectName(u"ageLabel")
        self.ageLabel.setFont(QFont('Segoe UI', 11))
        self.verticalLayout.addWidget(self.ageLabel)

        self.genderLabel = QLabel(self.tr(u"Gender: "), self.verticalLayoutWidget)
        self.genderLabel.setObjectName(u"genderLabel")
        self.genderLabel.setFont(QFont('Segoe UI', 11))
        self.verticalLayout.addWidget(self.genderLabel)

        self.countryLabel = QLabel(self.tr(u"Nationality: "), self.verticalLayoutWidget)
        self.countryLabel.setObjectName(u"countryLabel")
        self.countryLabel.setFont(QFont('Segoe UI', 11))
        self.verticalLayout.addWidget(self.countryLabel)
        self.countryLabel.hide()

        self.setCentralWidget(self.centralwidget)
        self.show()
        
    @Slot()
    def setData(self):
        if not self.nameLineEdit.text():
            return
        
        curr_code = self.countryComboBox.currentText()
        curr_name = self.nameLineEdit.text().lower()
        
        self.genderLabel.setText(
            f"Gender: {getGender(curr_name, curr_code).title()}"
        )

        self.ageLabel.setText(
            f"Age: {getAge(curr_name, curr_code)}"
        )
        
        if self.countryComboBox.currentText() == "":
            country = self.locale().countryToString(self.locale().codeToCountry(getNationality(curr_name)))
            
            if country == "Default":
                country = "Country Unknown"
                
            self.countryLabel.setText(
                f"Nationality: {'Country Unknown' if country == 'Default' else country}"
            )
            
            self.countryLabel.show()
        else:
            self.countryLabel.hide()
        

if __name__ == '__main__':
    import sys
    import ctypes
    
    app = QApplication()
    app.setQuitOnLastWindowClosed(True)
    window = ApplicationWindow()
    
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("alice.InfoFromName")
    
    sys.exit(app.exec())
