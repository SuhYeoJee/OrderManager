from PyQt5.QtWidgets import QMainWindow, QMessageBox, QComboBox
from PyQt5.uic import loadUi

class DatabaseViewerView(QMainWindow):
    def __init__(self):
        super().__init__()

        # .ui 파일 로드
        loadUi("./src/test/db_viewer/dbview.ui", self)

        # 버튼 및 입력 필드 설정
        self.load_button = self.findChild(type(self.load_button), "load_button")
        self.table_name_combo = self.findChild(QComboBox, "table_name_combo")  # 콤보박스
        self.table_widget = self.findChild(type(self.table_widget), "table_widget")

    def show_error(self, message):
        """에러 메시지를 표시합니다."""
        QMessageBox.critical(self, "Error", message)

    def set_table_names(self, table_names):
        """콤보박스에 테이블 목록을 설정합니다."""
        self.table_name_combo.clear()
        self.table_name_combo.addItems(table_names)
