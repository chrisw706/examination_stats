import sqlite3
import sys
import datetime

from collections import defaultdict
from stats_ui_window import Ui_StatWindow
from PyQt5 import QtCore, QtGui, QtWidgets

class MainWindow_EXEC():

    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_StatWindow()
        self.ui.setupUi(MainWindow)

        with open('examiners_names.txt','r') as examiners:
            for line in examiners.readlines():
                self.ui.comboBox.addItem(line.strip())



        self.device_list = []
        self.ui.pushButton.clicked.connect(self.add_device)
        self.ui.pushButton_4.clicked.connect(self.remove_record)
        self.ui.pushButton_2.clicked.connect(self.add_list)
        self.ui.pushButton_3.clicked.connect(QtCore.QCoreApplication.instance().quit)

        MainWindow.show()
        sys.exit(app.exec_())



    def add_device(self):
        device_values = defaultdict()
        device_values['case_number'] = self.ui.lineEdit.text()
        device_values['item_number'] = self.ui.lineEdit_2.text()
        device_values['manufacture'] = self.ui.lineEdit_3.text()
        device_values['model_'] = self.ui.lineEdit_4.text()
        device_values['crime_code'] = self.ui.lineEdit_6.text()
        device_values['requesting'] = self.ui.lineEdit_5.text()
        device_values['examiner'] = str(self.ui.comboBox.currentText())

        if "" in (device_values['case_number'],device_values['item_number'],
        device_values['manufacture'],device_values['model_'],
        device_values['crime_code'],device_values['requesting']):
            self.error_box()
        else:
            all_items = True
            if self.ui.radioButton_11.isChecked():
                device_values['device'] = "Computer"
            elif self.ui.radioButton_10.isChecked():
                device_values['device'] = "Phone"
            elif self.ui.radioButton_12.isChecked():
                device_values['device'] = "Hard Drive"
            elif self.ui.radioButton_13.isChecked():
                device_values['device'] = "Thumbdrive/Media Card"
            elif self.ui.radioButton_14.isChecked():
                device_values['device'] = "Vehilce"
            else:
                all_items = False
                self.error_box(message = "Please Select Device Type")

            if self.ui.radioButton.isChecked():
                device_values['security'] = "Password Protected"
            elif self.ui.radioButton_9.isChecked():
                device_values['security'] = "Unlocked"
            else:
                all_items = False
                self.error_box(message = "Please Select Security")

            if self.ui.checkBox_2.isChecked():
                device_values['secure_start'] = "Enabled"
            else: device_values['secure_start'] = "No"

            if self.ui.checkBox_3.isChecked():
                device_values['logical'] = "Yes"
            else: device_values['logical'] = "No"
            if self.ui.checkBox_4.isChecked():
                device_values['file_system'] = "Yes"
            else: device_values['file_system'] = "No"

            if self.ui.checkBox_5.isChecked():
                device_values['physical'] = "Yes"
            else: device_values['physical'] = "No"

            if self.ui.checkBox_8.isChecked():
                device_values['lt_greykey'] = "Yes"
            else: device_values['lt_greykey'] = "No"

            if self.ui.checkBox_6.isChecked():
                device_values['greykey'] = "Yes"
            else: device_values['greykey'] = "No"

            if self.ui.checkBox_7.isChecked():
                device_values['no_extraction'] = "No Extraction"
            else: device_values['no_extraction'] = "Extracted"

            device_values['date'] = datetime.datetime.now().strftime('%m/%d/%Y')

            if all_items == True:
                self.device_list.append(device_values)

                self.ui.tableWidget.insertRow(0)
                self.ui.tableWidget.setItem(0 , 0, QtWidgets.QTableWidgetItem(device_values['date']))
                self.ui.tableWidget.setItem(0 , 1, QtWidgets.QTableWidgetItem(device_values['device']))
                self.ui.tableWidget.setItem(0 , 2, QtWidgets.QTableWidgetItem(device_values['case_number']))
                self.ui.tableWidget.setItem(0 , 3, QtWidgets.QTableWidgetItem(device_values['item_number']))
                self.ui.tableWidget.setItem(0 , 4, QtWidgets.QTableWidgetItem(device_values['manufacture']))
                self.ui.tableWidget.setItem(0 , 5, QtWidgets.QTableWidgetItem(device_values['model_']))

                self.ui.lineEdit_2.setText("")
                self.ui.lineEdit_3.setText("")
                self.ui.lineEdit_4.setText("")
                self.ui.checkBox_2.setChecked(False)
                self.ui.checkBox_3.setChecked(False)
                self.ui.checkBox_4.setChecked(False)
                self.ui.checkBox_5.setChecked(False)
                self.ui.checkBox_6.setChecked(False)
                self.ui.checkBox_7.setChecked(False)
                self.ui.checkBox_8.setChecked(False)
            else: all_items = True


    def remove_record(self):
        row = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.removeRow(row)


    def add_list(self):
        manufacture = self.ui.lineEdit_3.text()
        if manufacture != "":
            self.error_box(message = "Dont forget to add the phone")
        else:
            self.ui.lineEdit.setText("")
            self.ui.lineEdit_2.setText("")
            self.ui.lineEdit_3.setText("")
            self.ui.lineEdit_4.setText("")
            self.ui.lineEdit_6.setText("")
            self.ui.lineEdit_5.setText("")
            count = self.ui.tableWidget.rowCount()
            if count > 0:
                self.ui.tableWidget.setRowCount(0)
                with open('path.txt','r') as my_path:
                    path = my_path.read()
                con = sqlite3.connect(path)
                cur = con.cursor()
                for item in self.device_list:
                    val = (item['date'],item['case_number'],item['item_number'],item['manufacture'],
                    item['model_'],item['crime_code'],item['requesting'],
                    item['examiner'],item['device'],item['security'],
                    item['secure_start'],item['logical'],item['file_system'],
                    item['physical'],item['lt_greykey'],item['greykey'],item['no_extraction'])
                    sql = "INSERT INTO entries (date,case_number,item_number,manufacture,model_,crime_code,requesting,examiner,device,security,secure_start,logical,file_system,physical,lt_greykey,greykey,no_extraction) VALUES (?,?, ?, ?, ?, ?, ?, ?,?, ?,?,?,?,?,?,?,?)"
                    cur.execute(sql,val)
                    con.commit()
                con.close()

    @staticmethod
    def error_box(message = 'Please fill out all fields!'):
        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setIcon(QtWidgets.QMessageBox.Warning)
        error_dialog.setWindowTitle('Error')
        error_dialog.setText(f'{message}')
        error_dialog.setStandardButtons(QtWidgets.QMessageBox.Close)
        error_dialog.exec()


if __name__ == "__main__":
    MainWindow_EXEC()
