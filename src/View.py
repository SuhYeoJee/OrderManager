if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem, QPushButton, QDialog, QLineEdit
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
    # -------------------------------------------------------------------------------------------
        self.tableInsertBtn.clicked.connect(self.show_insert_dialog)
    # ===========================================================================================
    def show_insert_dialog(self):
        dialog = InsertDialog(self)
        dialog.exec_()

    def show_error(self, message):
        """에러 메시지를 표시합니다."""
        QMessageBox.critical(self, "Error", message)
    # ===========================================================================================
    def set_table_names(self, table_names):
        """콤보박스에 테이블 목록을 설정합니다."""
        self.tableComboBox.clear()
        self.tableComboBox.addItems(table_names)

    def update_table_data(self, res):
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
# Insert Dialog (UI 로드 후 처리)
class InsertDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("./ui/insertDialog.ui", self)  # insertDialog.ui 파일 로드

    #     # UI 요소 접근
    #     self.name_input = self.findChild(QLineEdit, "nameInput")  # QLineEdit 객체 접근
    #     self.submit_button = self.findChild(QPushButton, "submitButton")  # QPushButton 객체 접근

    #     # 버튼 클릭 이벤트 연결
    #     self.submit_button.clicked.connect(self.on_submit)

    # def on_submit(self):
    #     # 사용자가 입력한 값을 가져옵니다.
    #     name = self.name_input.text()
    #     print(f"Submitted Name: {name}")
    #     self.accept()  # Dialog 닫기


# ===========================================================================================
import sys
from PyQt5.QtWidgets import QApplication
if __name__ == "__main__":
    # MVC 초기화
    app = QApplication(sys.argv)
    view = View()
    view.show()
    sys.exit(app.exec_())
