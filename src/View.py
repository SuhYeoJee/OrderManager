if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.uic import loadUi
# ===========================================================================================

class View(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("./ui/MainWindow.ui", self)
        # --------------------------
        self.load_button = self.findChild(QPushButton, "tableComboBtn")
        self.table_name_combo = self.findChild(QComboBox, "tableComboBox")  # 콤보박스
        self.table_widget = self.findChild(QTableWidget, "tableWidget")
    # -------------------------------------------------------------------------------------------
    def show_error(self, message):
        """에러 메시지를 표시합니다."""
        QMessageBox.critical(self, "Error", message)

    def set_table_names(self, table_names):
        """콤보박스에 테이블 목록을 설정합니다."""
        self.table_name_combo.clear()
        self.table_name_combo.addItems(table_names)

    def update_table_data(self, result_signal):
        if not result_signal:
            self.show_error(f"No data found in table")
            return

        # 첫 번째 행에서 컬럼 이름 추출
        columns = [f"Column {i+1}" for i in range(len(result_signal[0]))]  # 기본적으로 Column 1, Column 2, ...
        
        # View 업데이트: 테이블 구조 설정
        self.table_widget.setColumnCount(len(columns))
        self.table_widget.setRowCount(len(result_signal))
        self.table_widget.setHorizontalHeaderLabels(columns)

        # View 업데이트: 데이터 삽입
        for row_idx, row in enumerate(result_signal):
            for col_idx, value in enumerate(row):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))


# ===========================================================================================
import sys
from PyQt5.QtWidgets import QApplication
if __name__ == "__main__":
    # MVC 초기화
    app = QApplication(sys.argv)
    view = View()
    view.show()
    sys.exit(app.exec_())
