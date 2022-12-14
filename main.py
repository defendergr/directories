import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QProcess, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QMessageBox

from iconExtract import IconExtract
import time

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.process = QProcess()
        Dialog.setObjectName("Dialog")
        Dialog.resize(627, 444)
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(20, 20, 411, 401))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 409, 399))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.filesDict = IconExtract().extract()

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.install = QtWidgets.QPushButton(Dialog)
        self.install.setGeometry(QtCore.QRect(440, 400, 75, 24))
        self.install.setObjectName("install")

        self.exit = QtWidgets.QPushButton(Dialog)
        self.exit.setGeometry(QtCore.QRect(530, 400, 75, 24))
        self.exit.setObjectName("exit")

        self.install.setText("Install")
        self.exit.setText("Exit")
        self.install.clicked.connect(self.start)
        self.exit.clicked.connect(self.stop)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        line = 10
        for i in self.filesDict:
            self.fileCheckBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
            self.fileLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.imgLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.img = QPixmap(r'./setup/icons/'+i['img']+'.png')
            # print(r'./setup/icons/'+i['img']+'.png')

            # print(i)

            self.fileCheckBox.setGeometry(QtCore.QRect(380, line, 16, 20))
            self.fileCheckBox.setObjectName("fileCheckBox")

            self.fileLabel.setGeometry(QtCore.QRect(40, line, 301, 20))
            self.fileLabel.setObjectName("fileLabel")
            self.fileLabel.setText(i['img'])

            self.imgLabel.setGeometry(QtCore.QRect(10, line, 16, 16))
            self.imgLabel.setObjectName("imgLabel")
            self.imgLabel.setPixmap(self.img)
            self.imgLabel.setScaledContents(True)
            self.imgLabel.setPixmap(self.img.scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio))
            self.imgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)

            line += 20



    def start(self):
        if self.fileCheckBox.isChecked():
            print(self.fileLabel.text())
        self.install.setEnabled(False)


        # for setup in self.filesDict:
        #     self.process.start(setup['path'])
        #     print(setup['path'])
            # time.sleep(3)





    def stop(self):
        sys.exit()

    def about(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('About')
        msgBox.setWindowIcon(QIcon('dimos.ico'))
        msgBox.setText("Backuper έκδοση 1.2.0 \nΓια τον Δήμο Θέρμης \nΑπό: Κωνσταντίνος Καρακασίδης")
        msgBox.exec()




if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
