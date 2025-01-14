if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QComboBox, QTableWidget, \
    QTableWidgetItem, QPushButton, QDialog, QLineEdit, QSpinBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.uic import loadUi
# ===========================================================================================

class View(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("./ui/MainWindow.ui", self)
        # --------------------------
        self.tableComboBtn = self.findChild(QPushButton, "tableComboBtn")
        self.tableComboBox = self.findChild(QComboBox, "tableComboBox")
        self.tableWidget = self.findChild(QTableWidget, "tableWidget")
        self.tableInsertBtn = self.findChild(QPushButton, "tableInsertBtn")
        # --------------------------
        self.dialogs = {
            "insert":{
                "users":InsertDialog(table_name="users"),
                "sqlite_sequence":InsertDialog(table_name="sqlite_sequence")
            }
        }
    # -------------------------------------------------------------------------------------------
    def get_insert_dialog(self,table_name):
        dialog = self.dialogs['insert'][table_name]
        dialog.clear()
        dialog.show()
        return dialog
    

    def show_error(self, message):
        """에러 메시지 표시"""
        QMessageBox.critical(self, "Error", message)
    # ===========================================================================================
    def set_table_names(self, table_names):
        """콤보박스에 테이블 목록 표시"""
        self.tableComboBox.clear()
        self.tableComboBox.addItems(table_names)

    def update_table_data(self, res):
        '''값을 받아서 테이블에 표시'''
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
class InsertDialog(QDialog):
    insert_submitted = pyqtSignal(tuple)
    def __init__(self,table_name,parent=None):
        super().__init__(parent)
        loadUi("./ui/insertDialog.ui", self) 
        # --------------------------
        self.name_input = self.findChild(QLineEdit, "nameLineEdit")
        self.age_input = self.findChild(QSpinBox, "ageSpinBox")  
        self.city_input = self.findChild(QLineEdit, "cityLineEdit")
        self.submit_button = self.findChild(QPushButton, "submitButton")
        # --------------------------
        self.submit_button.clicked.connect(self.on_submit)
        # --------------------------
        self.table_name = table_name
        self.data = None
    # -------------------------------------------------------------------------------------------
    def on_submit(self):
        name = self.name_input.text()
        age = self.age_input.value()
        city = self.city_input.text()
        # --------------------------
        self.data = (self.table_name,{'name':name,'age':age,'city':city})
        self.insert_submitted.emit(self.data)
        self.close()
    # -------------------------------------------------------------------------------------------
    def clear(self):
        self.name_input.clear()
        self.age_input.setValue(0) 
        self.city_input.clear()
# ===========================================================================================


# ===========================================================================================
import sys
from PyQt5.QtWidgets import QApplication
if __name__ == "__main__":
    # MVC 초기화
    app = QApplication(sys.argv)
    view = View()
    view.show()
    sys.exit(app.exec_())
