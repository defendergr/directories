import sys
import traceback

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QProcess, QThreadPool, QObject, pyqtSignal, QRunnable, pyqtSlot
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QMessageBox, QListWidget, QListWidgetItem, QAbstractItemView

from iconExtract import IconExtract



class Worker(QRunnable):
    def __init__(self, fn):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn

    @pyqtSlot()
    def run(self):
        self.fn()


class Ui_Dialog(object):
    def __init__(self):
        self.filesDict = IconExtract().extract()
        self.appItems = QListWidget()
        self.process = QProcess()
        self.thread = QThreadPool()


    def setupUi(self, dialog):

        dialog.setObjectName("Dialog")
        dialog.resize(627, 444)
        self.scrollArea = QtWidgets.QScrollArea(dialog)
        self.scrollArea.setGeometry(QtCore.QRect(20, 20, 411, 401))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.appItems.setGeometry(QtCore.QRect(0, 0, 409, 399))
        # self.appItems.setAlternatingRowColors(True)
        self.appItems.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        self.scrollArea.setWidget(self.appItems)

        self.install = QtWidgets.QPushButton(dialog)
        self.install.setGeometry(QtCore.QRect(440, 400, 75, 24))
        self.install.setObjectName("install")

        self.exit = QtWidgets.QPushButton(dialog)
        self.exit.setGeometry(QtCore.QRect(530, 400, 75, 24))
        self.exit.setObjectName("exit")

        self.install.setText("Install")
        self.exit.setText("Exit")

        self.install.clicked.connect(self.proc)
        self.exit.clicked.connect(self.stop)
        QtCore.QMetaObject.connectSlotsByName(dialog)

        num = 1
        for i in self.filesDict:
            vars()[f"self.img{num}"] = QPixmap(r'./setup/icons/'+i['img']+'.png')

            vars()[f'self.app{num}'] = QListWidgetItem(QIcon(vars()[f"self.img{num}"]), f"{i['img']}")
            self.appItems.addItem(vars()[f'self.app{num}'])

            num += 1
        print(self.appItems.count())


    def proc(self):
        worker = Worker(self.start)
        self.thread.start(worker)


    def start(self):
        listItems = []
        self.install.setEnabled(False)

        for item in range(0, self.appItems.count()):
            if self.appItems.item(item).isSelected():
                listItems.append(self.filesDict[item]['path'])

        for setup in listItems:
            self.process.start(setup)

            print(setup, self.process.state())
            self.process.waitForFinished()

        self.install.setEnabled(True)

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
