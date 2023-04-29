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
        self.ui.pushButton_4.clicked.connect(self.history)
        self.ui.pushButton_3.clicked.connect(self.table)
        self.ui.pushButton.clicked.connect(self.clear)
        self.ui.pushButton_2.clicked.connect(self.accept_product)
        self.ui.pushButton_5.clicked.connect(self.update_db)

    def update_db(self):
        data = Reader.read_file(True)
        DB.input_file(data)
        data = Reader.read_file(False)
        DB.output_file(data)

        self.combobox()
        
    def else_info(self, text='Что-то пошло не так.'):
        msg = QMessageBox()
        msg.setWindowTitle("TypeError")
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()
    
    def history(self):
        pass

    def clear(self):
        self.accept_data.clear()
        self.combobox()

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
      
    def get_count(self, checker, row):
        name = 'input_invoice' if checker else 'send_product'
        count = 4 if checker else 3
        data_count = DB.execute_res(f"SELECT * FROM {name} WHERE product_name='{row[3]}'")
        re_count = 0
        for row in data_count:
            re_count += int(row[count])
        return re_count
            
    def generate_table(self, data):
        i = 0
        for row in data:
            print(row)
            self.ui.tableWidget.setRowCount(i+1)
            in_count = self.get_count(True, row)
            out_count = self.get_count(False, row)

            name =  QtWidgets.QTableWidgetItem(row[3])
            in_c = QtWidgets.QTableWidgetItem(str(in_count))
            out_c = QtWidgets.QTableWidgetItem(str(out_count))
            remainder = QtWidgets.QTableWidgetItem(str(in_count-out_count))
            self.ui.tableWidget.setItem(i, 0, name)
            self.ui.tableWidget.setItem(i, 2, in_c)
            self.ui.tableWidget.setItem(i, 3, out_c)
            self.ui.tableWidget.setItem(i, 4, remainder)
            i += 1
            i = self.update_table(i, row[3], True)
            i = self.update_table(i, row[3], False)

    def update_table(self, i, name, checker):
        table_name = 'input_invoice' if checker else 'send_product'
        num_list = [1, -1, 4, 2] if checker else [0, 2, 3, 3]
        in_data = DB.execute_res(f"SELECT * FROM {table_name} WHERE product_name='{name}'")
        for row in in_data:
            self.ui.tableWidget.setRowCount(i+1)
            company_name = QtWidgets.QTableWidgetItem(f"{row[num_list[0]]}, Номер накладной: {row[num_list[1]]}")
            count = QtWidgets.QTableWidgetItem(f"{row[num_list[2]]}")
            self.ui.tableWidget.setItem(i, 0, company_name)
            self.ui.tableWidget.setItem(i, num_list[3], count)
            i += 1
        return i
        
    def table(self):
        try:
            data = self.get_DB_data()
            self.generate_table(data)
        except:
            self.else_info(text='Выберите товар')
        

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