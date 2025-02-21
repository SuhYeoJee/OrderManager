
import re
from src.imports.pyqt5_imports import *
from src.imports.config import DATETIME_FORMAT
# ===========================================================================================

class BaseUI(QDialog):
    # pre 리스폰스 핸들
    # id로 로드 기능만 있는 원시 다이얼로그 
    data_request = pyqtSignal(tuple)
    def __init__(self,dialog_type,table_name,parent=None):
        super().__init__(parent)
        # --------------------------
        self.request_header = (dialog_type,table_name)
        self.cols, self.data = None, None
    
    def get_input_widgets(self,target=None):
        target = target if target else self
        input_widgets = target.findChildren((QLineEdit, QComboBox, QDateTimeEdit,QDateEdit,QPlainTextEdit,QSpinBox,QDoubleSpinBox))
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
        self.idComboBox.addItems(map(str,['']+ids))
    # --------------------------
    def clear(self,keep_combos:bool=False)->None:
        '''모든 입력위젯 비우기'''
        clear_handlers = {
            QLineEdit: lambda widget: widget.clear(),
            QComboBox: lambda widget: widget.setCurrentText("") if keep_combos else widget.clear(),
            QSpinBox: lambda widget: widget.setValue(0),
            QDoubleSpinBox: lambda widget: widget.setValue(0),
            QPlainTextEdit: lambda widget: widget.clear(),
            QDateTimeEdit: lambda widget: widget.setDateTime(QDateTime(0000, 0, 0, 0, 0)),
            QDateEdit: lambda widget: widget.setDateTime(QDateTime(0000, 0, 0, 0, 0)),
        }
        input_widgets = [w for w in self.input_widgets if w.objectName() != "idComboBox"] if keep_combos else self.input_widgets
        [handler(w) for w in input_widgets if (handler := clear_handlers.get(type(w)))]
    # --------------------------
    def get_inputs(self,widget=None)->dict:
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
        res = {self.get_key_from_object_name(w.objectName()): handler(w) 
                for w in self.get_input_widgets(widget) 
                if (handler := value_handlers.get(type(w))) and w.objectName() not in excepts}
        
        print(res)
        return res
    # --------------------------
    def set_datas(self, datas:tuple) -> None:
        '''모든 입력 위젯에 값 설정하기'''
        set_handlers = {
            QLineEdit: lambda widget, value: widget.setText(str(value)),
            QComboBox: lambda widget, value: (widget.addItem(str(value)) if widget.findText(str(value)) == -1 else None, widget.setCurrentText(str(value)))[1],
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
        if (id_text := self.idComboBox.currentText()):
            id = int(id_text)
            self.data_request.emit(self._add_request_header(id))
        else:
            return 
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
        if self.request_header[1] != data_response[1]: 
            return # 비정상 수신 
        try:
            [datas] = data_response[2]
        except ValueError:
            print('*')
            ... # 해당 id 없음
        else:
            self.clear(True)
            self.set_datas(datas)

