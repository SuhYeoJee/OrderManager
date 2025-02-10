if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QPlainTextEdit,QDateTimeEdit,QDateEdit,QSpinBox, QDoubleSpinBox
from PyQt5.QtCore import pyqtSignal,QDateTime
from PyQt5.uic import loadUi
import re
# --------------------------
from src.module.SqlliteInterface import SqlliteInterface
# --------------------------
DB_PATH='./config/NOVA.db'
DATETIME_FORMAT = "yyyy-MM-dd HH:mm:ss"
TABLES = SqlliteInterface(DB_PATH).get_table_names()
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
        self.cols, self.data = None, None
        self.input_widgets = self.get_input_widgets()
        # --------------------------
        self.loadBtn.clicked.connect(self.on_load)
        self.submitBtn.clicked.connect(self.on_submit)
    
    def get_input_widgets(self):
        input_widgets = self.findChildren((QLineEdit, QComboBox, QDateTimeEdit,QDateEdit,QPlainTextEdit,QSpinBox,QDoubleSpinBox))
        return [widget for widget in input_widgets if widget.objectName()]
    # --------------------------
    def set_fks(self,datas):
        if datas:
            for col_name,items in datas.items():
                combobox = getattr(self,f'{col_name}ComboBox')
                combobox.clear()
                combobox.addItems(map(str,['']+items))
    # --------------------------
    def set_ids(self,ids):
        self.idComboBox.clear()
        self.idComboBox.addItems(map(str,ids))
    # --------------------------
    def clear(self)->None:
        '''모든 입력위젯 비우기'''
        clear_handlers = {
            QLineEdit: lambda widget: widget.clear(),
            QComboBox: lambda widget: widget.setCurrentIndex(0),
            QSpinBox: lambda widget: widget.setValue(0),
            QDoubleSpinBox: lambda widget: widget.setValue(0),
            QPlainTextEdit: lambda widget: widget.clear(),
            QDateTimeEdit: lambda widget: widget.setDateTime(QDateTime(2000, 1, 1, 0, 0)),
            QDateEdit: lambda widget: widget.setDateTime(QDateTime(2000, 1, 1, 0, 0)),
        }
        [handler(widget) for widget in self.input_widgets if (handler := clear_handlers.get(type(widget)))]
    # --------------------------
    def get_inputs(self)->dict:
        '''모든 입력위젯의 값 {"col_name":val}로 반환 '''
        value_handlers = {
            QLineEdit: lambda widget: widget.text(),
            QComboBox: lambda widget: widget.currentText(),
            QSpinBox: lambda widget: widget.value(),
            QDoubleSpinBox: lambda widget: widget.value(),
            QPlainTextEdit: lambda widget: widget.toPlainText(),
            QDateTimeEdit: lambda widget: widget.dateTime().toString(DATETIME_FORMAT),
            QDateEdit: lambda widget: widget.dateTime().toString(DATETIME_FORMAT),
        }
        excepts = ['qt_spinbox_lineedit']
        res = {self.get_key_from_object_name(widget.objectName()): handler(widget) 
                for widget in self.input_widgets 
                if (handler := value_handlers.get(type(widget))) and widget.objectName() not in excepts}
        
        print(res)
        return res
    # --------------------------
    def set_datas(self, datas:tuple) -> None:
        '''모든 입력 위젯에 값 설정하기'''
        set_handlers = {
            QLineEdit: lambda widget, value: widget.setText(str(value)),
            QComboBox: lambda widget, value: widget.setCurrentText(str(value)),
            QSpinBox: lambda widget, value: widget.setValue(int(value)),
            QDoubleSpinBox: lambda widget, value: widget.setValue(float(value)),
            QPlainTextEdit: lambda widget, value: widget.setPlainText(str(value)),
            QDateTimeEdit: lambda widget, value: widget.setDateTime(QDateTime.fromString(value,DATETIME_FORMAT)),
            QDateEdit: lambda widget, value: widget.setDateTime(QDateTime.fromString(value,DATETIME_FORMAT)),
        }
        data_dict = dict(zip(self.cols,datas))
        [handler(widget,value) 
            for widget in self.input_widgets 
            if (handler := set_handlers.get(type(widget))) and (value := data_dict.get(self.get_key_from_object_name(widget.objectName()))) is not None]
    # --------------------------
    def get_key_from_object_name(self,object_name):
        # col_name = 첫 번째 대문자 이전
        match = re.match(r'^[^A-Z]*', object_name)
        return match.group(0) if match else object_name
    
    def on_empty_func(self,*args,**kwargs):...
    # [send request] -------------------------------------------------------------------------------------------
    def on_load(self):
        id = int(self.idComboBox.currentText())
        self.data_request.emit(self._add_request_header(id))
    # --------------------------
    def on_insert_submit(self):
        inputs = self.get_inputs()
        inputs.pop('id')
        inputs.pop('reg_date')
        inputs.pop('update_date')
        self.data = self._add_request_header(inputs)
        self.insert_request.emit(self.data)
        self.close()
    # --------------------------
    def on_delete_submit(self):
        self.data = self._add_request_header(self.get_inputs())
        self.delete_request.emit(self.data)
        self.close()
    # --------------------------
    def on_update_submit(self):
        inputs = self.get_inputs()
        inputs.pop('reg_date')
        inputs.pop('update_date')
        self.data = self._add_request_header(inputs)
        self.update_request.emit(self.data)
        self.close()
    # --------------------------
    def _add_request_header(self,data):
        return self.request_header+(data,)
    # [on_response] -------------------------------------------------------------------------------------------
    def on_pre_response(self,pre_response):
        '''다이얼로그 사전정보: 전체 cols,테이블에 존재하는 id목록, 외래키 제약'''
        if self.request_header[1] != pre_response[1]: return 
        self.cols = pre_response[2][0]
        self.set_ids(pre_response[2][1])
        self.set_fks(pre_response[2][2])
    # --------------------------
    def on_data_response(self,data_response):
        if self.request_header[1] != data_response[1]: return 
        try:
            print(data_response[2])
            [datas] = data_response[2]
        except ValueError:
            ... # 해당 id 없음
        else:
            self.set_datas(datas)
# ===========================================================================================
# 클래스 자동생성
for table_name in TABLES:
    class_name = f'{table_name.capitalize()}Dialog'
    globals()[class_name] = type(class_name, (BaseDialog,), {
        '__init__': lambda self, dialog_type, table_name, parent=None: super(type(self), self).__init__(dialog_type, table_name, parent)
    })