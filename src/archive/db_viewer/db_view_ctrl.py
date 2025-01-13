import sqlite3
from PyQt5.QtWidgets import QTableWidgetItem

class DatabaseViewerController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # 콤보박스에 테이블 목록 설정
        table_names = self.model.get_table_names()
        self.view.set_table_names(table_names)

        # 버튼 클릭 이벤트 연결
        self.view.load_button.clicked.connect(self.load_table)

    def load_table(self):
        """콤보박스에서 선택한 테이블을 로드하고 View에 업데이트."""
        table_name = self.view.table_name_combo.currentText().strip()

        if not table_name:
            self.view.show_error("Please select a table.")
            return

        try:
            # 테이블 데이터 가져오기
            rows = self.model.execute_query(f"SELECT * FROM {table_name}")

            if not rows:
                self.view.show_error(f"No data found in table '{table_name}'.")
                return

            # 첫 번째 행에서 컬럼 이름 추출
            columns = [f"Column {i+1}" for i in range(len(rows[0]))]  # 기본적으로 Column 1, Column 2, ...
            
            # View 업데이트: 테이블 구조 설정
            self.view.table_widget.setColumnCount(len(columns))
            self.view.table_widget.setRowCount(len(rows))
            self.view.table_widget.setHorizontalHeaderLabels(columns)

            # View 업데이트: 데이터 삽입
            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    self.view.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        except sqlite3.Error as e:
            self.view.show_error(f"Error loading table: {e}")
