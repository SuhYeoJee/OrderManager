if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QComboBox, QTableWidget, \
    QTableWidgetItem, QPushButton, QDialog, QLineEdit, QSpinBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.uic import loadUi
# ===========================================================================================

class View(QMainWindow):
    id_request = pyqtSignal(tuple)
    def __init__(self):
        super().__init__()
        loadUi("./ui/MainWindow.ui", self)
        # --------------------------
        self.dialogs = {
            "insert":{
                "users":InsertDialog('users'),
                "sqlite_sequence":InsertDialog('sqlite_sequence')
            },
            "delete":{
                "users":DeleteDialog('users')
            },
            "update":{
                "users":UpdateDialog('users')
            }
        }
    # -------------------------------------------------------------------------------------------
    
    def get_dialog(self,dialog_type,table_name):
        dialog = self.dialogs[dialog_type][table_name]
        self.id_request.emit((dialog_type,table_name))
        dialog.clear()
        dialog.show()
        return dialog
    
    def show_error(self, message):
        """에러 메시지 표시"""
        QMessageBox.critical(self, "Error", message)
    # ===========================================================================================
    def set_table_names(self, table_names):
        """콤보박스에 테이블 목록 표시"""
        self.tableNameComboBox.clear()
        self.tableNameComboBox.addItems(table_names)

    def update_table_data(self, response):
        '''값을 받아서 테이블에 표시'''
        res = response[2]
        if not res:
            self.show_error(f"No data found in table")
            return

        columns = [f"{i}" for i in res.pop(0)]
        
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setHorizontalHeaderLabels(columns)

        for row_idx, row in enumerate(res):
            for col_idx, value in enumerate(row):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

# ===========================================================================================
class BaseDialog(QDialog):
    data_request = pyqtSignal(tuple)
    def __init__(self,table_name,parent=None):
        super().__init__(parent)
        loadUi("./ui/insertDialog.ui", self) 
        # --------------------------
        self.loadBtn.clicked.connect(self.on_load)
        self.submitBtn.clicked.connect(self.on_submit)
        # --------------------------
        self.request_header = ('insert',table_name)
        self.data = None
    # --------------------------
    def clear(self):
        self.idComboBox.clear()
        self.nameLineEdit.clear()
        self.ageSpinBox.setValue(0) 
        self.cityLineEdit.clear()

    # [send request] -------------------------------------------------------------------------------------------
    def on_load(self):
        id = int(self.idComboBox.currentText())
        self.data_request.emit(self._add_request_header(id))

    def on_submit(self):...
    # --------------------------
    def _add_request_header(self,data):
        return self.request_header+(data,)
    # [on_response] -------------------------------------------------------------------------------------------
    def on_id_response(self,id_response):
        if self.request_header[1] != id_response[1]: return 
        self.idComboBox.clear()
        self.idComboBox.addItems(map(str,id_response[2]))

    def on_data_response(self,data_response):
        if self.request_header[1] != data_response[1]: return 
        try:
            print(data_response[2])
            [(_, name,age,city)] = data_response[2]
        except ValueError:
            ... # 해당 id 없음
        else:
            self.nameLineEdit.setText(name)
            self.ageSpinBox.setValue(age)
            self.cityLineEdit.setText(city)
    def on_empty_func(self,*args,**kwargs):...
# ===========================================================================================

class InsertDialog(BaseDialog):
    insert_request = pyqtSignal(tuple)
    def __init__(self,table_name,parent=None):
        super().__init__(table_name,parent)
        # --------------------------
        self.request_header = ('insert',table_name) 
        self.data = None

    # [send request] -------------------------------------------------------------------------------------------
    def on_submit(self):
        name = self.nameLineEdit.text()
        age = self.ageSpinBox.value()
        city = self.cityLineEdit.text()
        # --------------------------
        self.data = self._add_request_header({'name':name,'age':age,'city':city})
        self.insert_request.emit(self.data)
        self.close()
# ===========================================================================================

class DeleteDialog(BaseDialog):
    delete_request = pyqtSignal(tuple)
    def __init__(self,table_name,parent=None):
        super().__init__(table_name,parent)
        # --------------------------
        self.request_header = ('delete',table_name)
        self.data = None

    # [send request] -------------------------------------------------------------------------------------------
    def on_submit(self):
        id = self.idComboBox.currentText()
        name = self.nameLineEdit.text()
        age = self.ageSpinBox.value()
        city = self.cityLineEdit.text()
        # --------------------------
        self.data = self._add_request_header({'id':id,'name':name,'age':age,'city':city})
        self.delete_request.emit(self.data)
        self.close()

# ===========================================================================================

class UpdateDialog(BaseDialog):
    update_request = pyqtSignal(tuple)
    def __init__(self,table_name,parent=None):
        super().__init__(table_name,parent)
        # --------------------------
        self.request_header = ('update',table_name)
        self.data = None

    # [send request] -------------------------------------------------------------------------------------------
    def on_submit(self):
        id = self.idComboBox.currentText()
        name = self.nameLineEdit.text()
        age = self.ageSpinBox.value()
        city = self.cityLineEdit.text()
        # --------------------------
        self.data = self._add_request_header({'id':id,'name':name,'age':age,'city':city})
        self.update_request.emit(self.data)
        self.close()

# ===========================================================================================
import sys
from PyQt5.QtWidgets import QApplication
if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = View()
    view.show()
    sys.exit(app.exec_())
