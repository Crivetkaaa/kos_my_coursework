import csv
import io
from main_win import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
import datetime


from utils.filereader import Reader
from utils.database import DB


class Interface(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.all_data = []
        self.accept_data = []
        self.combobox()
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.ui.pushButton_4.clicked.connect(self.write_to_file)
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

        # Reader.clear(True)
        # Reader.clear(False)


    def else_info(self, text='Что-то пошло не так.'):
        msg = QMessageBox()
        msg.setWindowTitle("TypeError")
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def write_to_file(self):
        text = self.history()
        try:
            Reader.write(text)
        except:
            pass

    def history(self):
        try:
            in_data = DB.execute_res(f"SELECT * FROM input_invoice WHERE product_name='{self.accept_data[0]}'")
            text = f"История товара {in_data[0][3]}\nТовар: {in_data[0][3]}.\nПриход: {in_data[0][7]}, Приходная накладная №{in_data[0][10]} от {in_data[0][2]},\nгарантийный талон поставщика № {in_data[0][9]}, срок гарантии {in_data[0][8]}.\n"
            
            try:
                out_data = DB.execute_res(f"SELECT * FROM send_product WHERE product_name='{self.accept_data[0]}'")[0]
                text += f"Продано: {out_data[4]}, Товарный чек № {out_data[-3]} {out_data[0]}, гарантийный талон №{out_data[-2]}, срок гарантии до {out_data[5]}."
            except:
                text += "Товар ещё не продан"

            return text
        except:
            self.else_info('Выберите товар')

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
        count = 4 if checker else 2
        data_count = DB.execute_res(
            f"SELECT * FROM {name} WHERE product_name='{row[3]}'")
        re_count = 0
        for row in data_count:
            re_count += int(row[count])
        return re_count

    def check_date(self, name):
        in_data = DB.execute_res(f"SELECT * FROM input_invoice WHERE product_name='{name}'")
        input_date = self.ui.lineEdit.text()
        input_date_obj = datetime.datetime.strptime(input_date, '%d.%m.%Y')
        in_c = out_c = count = 0
        for row in in_data:
            db_date_obj = datetime.datetime.strptime(row[7], "%d.%m.%Y")
            if db_date_obj < input_date_obj:
                count += int(row[4])
            else:
                in_c += int(row[4])

        out_data = DB.execute_res(f"SELECT * FROM send_product WHERE product_name='{name}'")
        
        for row in out_data:
            db_date_obj = datetime.datetime.strptime(row[4], "%d.%m.%Y")
            if db_date_obj < input_date_obj:
                count -= int(row[2])
            else:
                out_c += int(row[2])
        return in_c, out_c, count

    def generate_table(self, data):
        i = 0
        for row in data:
            self.ui.tableWidget.setRowCount(i+1)
            
            try:
                in_count, out_count, counts = self.check_date(row[3])
                end_counts = in_count-out_count+counts

            except:
                in_count = self.get_count(True, row)
                out_count = self.get_count(False, row)
                counts = 0
                end_counts = in_count-out_count
            
            name = QtWidgets.QTableWidgetItem(row[3])
            count = QtWidgets.QTableWidgetItem(str(counts))
            in_c = QtWidgets.QTableWidgetItem(str(in_count))
            out_c = QtWidgets.QTableWidgetItem(str(out_count))
            remainder = QtWidgets.QTableWidgetItem(str(end_counts))
            mini_data = [row[3], counts, in_count, out_count, end_counts]
            self.all_data.append(mini_data)
            self.ui.tableWidget.setItem(i, 0, name)
            self.ui.tableWidget.setItem(i, 1, count)
            self.ui.tableWidget.setItem(i, 2, in_c) 
            self.ui.tableWidget.setItem(i, 3, out_c)
            self.ui.tableWidget.setItem(i, 4, remainder)
            i += 1
            i = self.update_table(i, row[3], True)
            i = self.update_table(i, row[3], False)

    def update_table(self, i, name, checker):
        table_name = 'input_invoice' if checker else 'send_product'
        num_list = [2, -1, 4, 2, 7] if checker else [0, -1, 2, 3, 4]
        in_data = DB.execute_res(
            f"SELECT * FROM {table_name} WHERE product_name='{name}'")
        for row in in_data:
            print(row)
            date = datetime.datetime.strptime(row[num_list[4]], '%d.%m.%Y')
            try:
                in_date = datetime.datetime.strptime(self.ui.lineEdit.text(), '%d.%m.%Y')
            except:
                in_date = datetime.datetime.strptime('01.01.0001', '%d.%m.%Y')
            if date > in_date:
                self.ui.tableWidget.setRowCount(i+1)
                company_name = QtWidgets.QTableWidgetItem(
                    f"{row[num_list[0]]}, Номер накладной: {row[num_list[1]]}")
                count = QtWidgets.QTableWidgetItem(f"{row[num_list[2]]}")
                self.ui.tableWidget.setItem(i, 0, company_name)
                self.ui.tableWidget.setItem(i, num_list[3], count)
                print(num_list[3], row[num_list[2]])
                if table_name == 'input_invoice':
                    mini_date = [ f"{row[num_list[0]]} Номер накладной: {row[num_list[1]][0:-1]}", 0, row[4], 0, 0]
                else:
                    mini_date = [ f"{row[num_list[0]]} Номер накладной: {row[num_list[1]][0:-1]}", 0, 0, row[2], 0]
                self.all_data.append(mini_date)
                i += 1
        return i
    
    def save_table(self):
        print("g")
        with open('files/array.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for row in self.all_data:
                writer.writerow(row)

    def table(self):
        try:
            data = self.get_DB_data()
            self.generate_table(data)
            self.save_table()
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
