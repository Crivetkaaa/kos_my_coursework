from main_win import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys

from utils.filereader import Reader
from utils.database import DB


class Interface(QtWidgets.QWidget):    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.accept_data = []
        self.combobox()
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.ui.pushButton_2.clicked.connect(self.accept_product)
        self.ui.pushButton_3.clicked.connect(self.table)

    def get_DB_data(self, checker=True):
        count = 0
        name = 'input_invoice' if checker else 'send_product'
        text = f"SELECT * FROM {name} WHERE "
        for name in self.accept_data:
            if count < 1:
                text += f"product_name='{name}'"
                count += 1
            else:
                text += f" OR product_name='{name}'"
        return DB.execute_res(text)

    def get_count(self, checker, data, i):
        name = 'input_invoice' if checker else 'send_product'
        count = 4 if checker else 3
        data_count = DB.execute_res(f"SELECT * FROM {name} WHERE product_name='{data[i][3]}'")
        re_count = 0
        for row in data_count:
            re_count += int(row[count])
        return re_count
            

    def table(self):
        data = self.get_DB_data()
        out_data = self.get_DB_data(False)
        print(data)
        print(out_data)
       

    def accept_product(self):
        name = self.ui.comboBox.currentText()
        self.accept_data.append(name)
        self.combobox()

    def raw_data(self, data):
        send_data = []
        for row in data:
            if row[3] not in self.accept_data:
                send_data.append(row)
        return send_data

    def combobox(self):
        self.ui.comboBox.clear()
        data = self.get_data()
        data = self.raw_data(data)
        for row in data:
            self.ui.comboBox.addItem(row[3])

    def get_data(self):
        data = DB.execute_res("SELECT * FROM input_invoice")
        return data

def main():
    app = QtWidgets.QApplication(sys.argv)
    mywin = Interface()
    mywin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()