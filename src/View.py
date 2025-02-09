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
                "users":UserDialog('insert','users'),
            },
            "delete":{
                "users":UserDialog('delete','users'),
            },
            "update":{
                "users":UserDialog('update','users'),
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

    def get_table_name(self):
        return self.tableNameComboBox.currentText().strip()

    def get_select_data(self):
        table_name = self.get_table_name()
        sort_col = self.tableSortColComboBox.currentText().strip()
        sort_type = self.tableSortOpComboBox.currentText().strip()
        select_col = self.tableSelectColComboBox.currentText().strip()
        select_type = self.tableSelectOpComboBox.currentText().strip()
        select_str = self.tableSelectLineEdit.text()
        return ('select',table_name,(sort_col,sort_type),(select_col,select_type,select_str))

    # [view에 값 표시] ===========================================================================================
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

        if not self.tableSortColComboBox.count():
            self.tableSortColComboBox.clear()
            self.tableSortColComboBox.addItems(columns)
            self.tableSelectColComboBox.clear()
            self.tableSelectColComboBox.addItems(columns)

        for row_idx, row in enumerate(res):
            for col_idx, value in enumerate(row):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

# ===========================================================================================
class BaseDialog(QDialog):
    data_request = pyqtSignal(tuple)
    insert_request = pyqtSignal(tuple)
    delete_request = pyqtSignal(tuple)
    update_request = pyqtSignal(tuple)
    def __init__(self,dialog_type,table_name,parent=None):
        super().__init__(parent)
        loadUi(f"./ui/{table_name}Dialog.ui", self) 
        # --------------------------
        self.request_header = (dialog_type,table_name)
        self.on_submit = getattr(self, f"on_{dialog_type}_submit", None)
        self.data = None
        # --------------------------
        self.loadBtn.clicked.connect(self.on_load)
        self.submitBtn.clicked.connect(self.on_submit)
    # --------------------------
    def clear(self):...
    def get_inputs(self)->dict:...
    def set_datas(self,datas:tuple):...
    # --------------------------
    def on_empty_func(self,*args,**kwargs):...
    # [send request] -------------------------------------------------------------------------------------------
    def on_load(self):
        id = int(self.idComboBox.currentText())
        self.data_request.emit(self._add_request_header(id))

    def on_insert_submit(self):
        inputs = self.get_inputs()
        inputs.pop('id')
        self.data = self._add_request_header(inputs)
        self.insert_request.emit(self.data)
        self.close()

    def on_delete_submit(self):
        self.data = self._add_request_header(self.get_inputs())
        self.delete_request.emit(self.data)
        self.close()

    def on_update_submit(self):
        self.data = self._add_request_header(self.get_inputs())
        self.update_request.emit(self.data)
        self.close()
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
            [datas] = data_response[2]
        except ValueError:
            ... # 해당 id 없음
        else:
            self.set_datas(datas)


class UserDialog(BaseDialog):
    def __init__(self,dialog_type,table_name,parent=None):
        super().__init__(dialog_type,table_name,parent)
        self.cols = ['id', 'name', 'age', 'city']
    # --------------------------
    def clear(self):
        self.idComboBox.clear()
        self.nameLineEdit.clear()
        self.ageSpinBox.setValue(0) 
        self.cityLineEdit.clear()
    # --------------------------
    def get_inputs(self):
        id = self.idComboBox.currentText()
        name = self.nameLineEdit.text()
        age = self.ageSpinBox.value()
        city = self.cityLineEdit.text()
        return dict(zip(self.cols, (id,name,age,city)))
    # --------------------------
    def set_datas(self,datas:tuple):
        (id, name,age,city) = datas
        self.nameLineEdit.setText(name)
        self.ageSpinBox.setValue(age)
        self.cityLineEdit.setText(city)
    

# ===========================================================================================
import sys
from PyQt5.QtWidgets import QApplication
if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = View()
    view.show()
    sys.exit(app.exec_())
