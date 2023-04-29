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

    def num(self, len):
        num = [i for i in range(0, len)]
        return num

    def num_to_str(self, num):
        str_num = [str(i+1) for i in num]
        return str_num

    def get_DB_data(self):
        count = 0
        text = "SELECT * FROM input_invoice WHERE "
        for name in self.accept_data:
            if count < 1:
                text += f"product_name='{name}'"
                count += 1
            else:
                text += f" OR product_name='{name}'"
        return DB.execute_res(text)


    def table(self):
        data = self.get_DB_data()
        len_data = len(data)

        num = self.num(len_data)

        self.ui.tableWidget.setRowCount(num[-1]+1)
        self.ui.tableWidget.setVerticalHeaderLabels(self.num_to_str(num))

        for i in num:
            product_name = QtWidgets.QTableWidgetItem(data[i][3])
            data_count = DB.execute_res(f"SELECT * FROM input_invoice WHERE product_name='{data[i][3]}'")
            input_count = 0
            for row in data_count:
                input_count += int(row[4])
            
            data_count = DB.execute_res(f"SELECT * FROM send_product WHERE product_name='{data[i][3]}'")
            output_count = 0
            for row in data_count:
                output_count += int(row[3])
            remainder = input_count-output_count
            print(remainder)
            remainder = QtWidgets.QTableWidgetItem(str(remainder))
            zero = QtWidgets.QTableWidgetItem(str(0))
            input_count = QtWidgets.QTableWidgetItem(str(input_count))
            output_count = QtWidgets.QTableWidgetItem(str(output_count))
            
            self.ui.tableWidget.setItem(i, 0, product_name)
            self.ui.tableWidget.setItem(i, 1, zero)
            self.ui.tableWidget.setItem(i, 2, input_count)
            self.ui.tableWidget.setItem(i, 3, output_count)
            self.ui.tableWidget.setItem(i, 4, remainder)


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