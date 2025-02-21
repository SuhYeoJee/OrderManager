
from src.imports.pyqt5_imports import *
# --------------------------
from src.module.Dialog import *
from src.module.Widget import *
# ===========================================================================================

class View(QMainWindow):
    pre_request = pyqtSignal(tuple)
    json_request = pyqtSignal(tuple)
    def __init__(self,tables):
        super().__init__()
        loadUi("./ui/MainWindow.ui", self)
        self.ordersTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.pushButton.clicked.connect(lambda: self.get_dialog('widget','orders'))
        # --------------------------
        self.dialog_infos = {table: globals().get(f"{table.capitalize()}Dialog") for table in tables}
        self.dialogs = {action: {key: cls(action, key) for key, cls in self.dialog_infos.items()} for action in ['view', 'insert', 'delete', 'update']}
        self.dialogs['widget']={}
        self.dialogs['widget']['orders'] = OrdersWidget()
        self.dialogs['widget']['sp'] = SpWidget()
        [self.dialogs[action]['sp'].pushButton.clicked.connect(lambda: self.get_sp_widget(self.dialogs[action]['sp'])) for action in ['view', 'insert', 'delete', 'update']]
    # -------------------------------------------------------------------------------------------
    def get_dialog(self,dialog_type,table_name):
        dialog = self.dialogs[dialog_type][table_name]
        dialog.clear()
        if dialog_type != 'view': # 추가 db 조회 없음
            self.pre_request.emit((dialog_type,table_name))
        dialog.show()
        return dialog
    
    def show_error(self, message:str):
        """에러 메시지 표시"""
        QMessageBox.critical(self, "Error", str(message))

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

    def get_sp_widget(self,sp_dialog):
        sp_widget = self.get_dialog('widget','sp')
        sp_path = sp_dialog.get_inputs()['path']
        if sp_path:
            self.json_request.emit(('widget','sp', sp_path))

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

        if response[0] == 'ordersTable': #tab1
            tableWidget = self.ordersTableWidget
            merge_flag = True
            def cut_datetime(lst):
                for i, sublist in enumerate(lst):
                    sublist = list(sublist)
                    sublist[1] = sublist[1].split(' ')[0] if sublist[1] else ''
                    sublist[-2] = sublist[-2].split(' ')[0] if sublist[-2] else ''
                    lst[i] = tuple(sublist)
                return lst
            res = cut_datetime(res)
        else:
            tableWidget = self.tableWidget
            merge_flag = False
            if not self.tableSortColComboBox.count():
                self.tableSortColComboBox.clear()
                self.tableSortColComboBox.addItems(columns)
                self.tableSelectColComboBox.clear()
                self.tableSelectColComboBox.addItems(columns)

        tableWidget.setColumnCount(len(columns))
        tableWidget.setRowCount(len(res))
        tableWidget.setHorizontalHeaderLabels(columns)

        for row_idx, row in enumerate(res):
            for col_idx, value in enumerate(row):
                if col_idx == 0:
                    btn = QPushButton(str(value))
                    view_request = (response[1],columns,row)
                    btn.clicked.connect(lambda _, v=view_request: self.set_view_dialog(v))
                    tableWidget.setCellWidget(row_idx, col_idx, btn)
                elif value:
                    tableWidget.setItem(row_idx, col_idx,QTableWidgetItem(str(value)))
                else:
                    tableWidget.setItem(row_idx, col_idx,QTableWidgetItem(str('')))

        if merge_flag:
            self.merge_cells(tableWidget)

    def merge_cells(self,tableWidget):
        """name 값이 일치하는 것 중 동일한 셀 병합"""
        start_row = 0
        try:
            current_value = tableWidget.item(0, 3).text()  # 기준 name
        except AttributeError:
            return 

        for row in range(1, tableWidget.rowCount()):
            item_value = tableWidget.item(row, 3).text()  # 현재 name

            if item_value != current_value:
                if row - start_row > 1:
                    self._merge_row_range(tableWidget,start_row, row - 1)
                start_row = row
                current_value = item_value
            # 마지막 row에서 병합 처리
            elif row == tableWidget.rowCount() - 1 and row - start_row > 0: 
                self._merge_row_range(tableWidget,start_row, row)

    def _merge_row_range(self,tableWidget, start_row, end_row):
        """주어진 범위에 대해 모든 열의 값이 동일하면 병합"""
        for col in range(1,tableWidget.columnCount()): #col(1) id 제외
            start_row = 0
            current_text = tableWidget.item(0, col).text() if tableWidget.item(0, col) else ''

            for row in range(start_row, end_row+1):
                item_text = tableWidget.item(row, col).text() if tableWidget.item(row, col) else ''
                if item_text != current_text:
                    if row - start_row > 1:
                        tableWidget.setSpan(start_row, col, row - start_row, 1)
                    start_row = row
                    current_text = item_text
            if end_row > start_row: #표 끝까지
                tableWidget.setSpan(start_row, col, end_row - start_row + 1, 1)

    def set_view_dialog(self,view_request):
        dialog = self.get_dialog('view',view_request[0])
        dialog.cols = view_request[1]
        dialog.set_datas(view_request[2])

# ===========================================================================================
import sys
if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = View()
    view.show()
    sys.exit(app.exec_())
