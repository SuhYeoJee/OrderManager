if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox,QTableWidgetItem
from PyQt5.QtCore import pyqtSignal
from PyQt5.uic import loadUi
# --------------------------
from src.Dialog import UserDialog
# ===========================================================================================

class View(QMainWindow):
    pre_request = pyqtSignal(tuple)
    def __init__(self):
        super().__init__()
        loadUi("./ui/MainWindow.ui", self)
        # --------------------------
        self.dialogs = {
            "insert":{
                "users":UserDialog('insert','users'),
                "my_table4":UserDialog('insert','my_table4'),
            },
            "delete":{
                "users":UserDialog('delete','users'),
                "my_table4":UserDialog('delete','my_table4'),
            },
            "update":{
                "users":UserDialog('update','users'),
                "my_table4":UserDialog('update','my_table4'),
            }
        }
    # -------------------------------------------------------------------------------------------
    
    def get_dialog(self,dialog_type,table_name):
        dialog = self.dialogs[dialog_type][table_name]
        self.pre_request.emit((dialog_type,table_name))
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
import sys
from PyQt5.QtWidgets import QApplication
if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = View()
    view.show()
    sys.exit(app.exec_())
