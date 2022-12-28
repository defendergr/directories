import subprocess
import sys
import os

from PyQt6.QtCore import QThreadPool, QRunnable, pyqtSlot, QRect, QMetaObject
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QMessageBox, QListWidget, QListWidgetItem, QAbstractItemView, QApplication, QDialog, QPushButton, QScrollArea, QSplashScreen

from iconExtract import IconExtract

ver = '1.2.6'

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)







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
        pixmap = QPixmap(resource_path("images/splash.png"))
        splash = QSplashScreen(pixmap)
        splash.show()
        self.filesDict = IconExtract().extract()
        self.appItems = QListWidget()
        self.thread = QThreadPool()


    def setupUi(self, dialog):

        dialog.setObjectName("Dialog")
        dialog.resize(627, 444)
        dialog.setWindowTitle(f'Multi Installer έκδοση {ver}')
        dialog.setWindowIcon(QIcon(resource_path("images/icon.ico")))
        dialog.setFixedSize(dialog.width(), dialog.height())

        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setGeometry(QRect(20, 20, 411, 401))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.appItems.setGeometry(QRect(0, 0, 409, 399))
        # self.appItems.setAlternatingRowColors(True)
        self.appItems.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)


        self.scrollArea.setWidget(self.appItems)

        self.install = QPushButton(dialog)
        self.install.setGeometry(QRect(440, 400, 75, 24))
        self.install.setObjectName("install")

        self.exit = QPushButton(dialog)
        self.exit.setGeometry(QRect(530, 400, 75, 24))
        self.exit.setObjectName("exit")

        self.info = QPushButton(dialog)
        self.info.setGeometry(QRect(530, 20, 75, 24))
        self.info.setObjectName("info")

        self.clear = QPushButton(dialog)
        self.clear.setGeometry(QRect(510, 200, 100, 24))
        self.clear.setObjectName("clear")

        self.install.setText("Install")
        self.exit.setText("Exit")
        self.info.setText("i")
        self.clear.setText("Clear Selected")

        self.info.clicked.connect(self.about)
        self.clear.clicked.connect(self.appItems.clearSelection)
        self.install.clicked.connect(lambda: self.startProcess(self.start))
        self.exit.clicked.connect(sys.exit)

        QMetaObject.connectSlotsByName(dialog)

        num = 1
        for i in self.filesDict:
            vars()[f"self.img{num}"] = QPixmap(r'./icons/'+i['img']+'.png')

            vars()[f'self.app{num}'] = QListWidgetItem(QIcon(vars()[f"self.img{num}"]), f"{i['img']}")
            self.appItems.addItem(vars()[f'self.app{num}'])

            num += 1
            # print(i)
        print(self.appItems.count())


    def startProcess(self, process):
        worker = Worker(process)
        self.thread.start(worker)

    def start(self):
        listItems = []
        self.install.setEnabled(False)

        for item in range(0, self.appItems.count()):
            if self.appItems.item(item).isSelected():
                listItems.append(self.filesDict[item]['path'])


        for setup in listItems:
            print(setup)
            process = subprocess.Popen([setup], shell=True)
            process.wait()

        self.install.setEnabled(True)



    def about(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('About')
        msgBox.setWindowIcon(QIcon(resource_path("images/icon.ico")))
        msgBox.setText(f"Multi Installer έκδοση {ver} \nΑπό: Κωνσταντίνος Καρακασίδης")
        msgBox.exec()




if __name__=="__main__":
    app = QApplication(sys.argv)
    dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec())
