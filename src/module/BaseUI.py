
import re
from src.imports.pyqt5_imports import *
from src.imports.config import SET_HANDLERS, GET_HANDLERS, CLEAR_HANDLERS
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
        input_widgets = [w for w in self.input_widgets if w.objectName() != "idComboBox"] if keep_combos else self.input_widgets
        [handler(w) for w in input_widgets if (handler := CLEAR_HANDLERS.get(type(w)))]
        [w.clear() for w in input_widgets if (type(w)==QComboBox) and not keep_combos]

    # --------------------------
    def get_inputs(self,widget=None)->dict:
        '''모든 입력위젯의 값 {"col_name":val}로 반환 '''
        excepts = ['qt_spinbox_lineedit','sp_infoGridLayoutWidget']

        res = {self.get_key_from_object_name(w.objectName()): handler(w) 
                for w in self.get_input_widgets(widget) 
                if (handler := GET_HANDLERS.get(type(w))) and w.objectName() not in excepts
                and (w.parent() and w.parent().objectName() not in excepts)}
        print('# ------------------------------------------')
        print(res)
        return res
    # --------------------------
    def set_datas(self, datas:tuple) -> None:
        '''모든 입력 위젯에 값 설정하기 datas: row tuple'''
        data_dict = dict(zip(self.cols,datas))
        [handler(widget,value) 
            for widget in self.input_widgets 
            if (handler := SET_HANDLERS.get(type(widget))) and (value := data_dict.get(self.get_key_from_object_name(widget.objectName()))) is not None]
    # --------------------------
    def set_datas_from_json_response(self,json_response):
        json_doc = json_response[2]
        excepts = ['qt_spinbox_lineedit','sp_infoGridLayoutWidget']

        for widget in self.input_widgets:
            key = self.get_key_from_object_name(widget.objectName())
            try:
                data_type,data_name = key.split('_',1)
            except:
                continue
            if data_name == 'spinbox_lineedit':
                continue
            if data_type == 'loads':
                table_name,col_name = data_name.split('_',1)
                try:
                    val = json_doc[data_type][table_name][col_name]
                except:
                    continue
            elif data_type in ['inputs','autos']:
                try:
                    val = json_doc[data_type][data_name]
                except:
                    print(data_type,data_name)
                    val = None
            else:
                continue

            val = val if val else 0
            SET_HANDLERS.get(type(widget))(widget,val)


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
            ... # 해당 id 없음
        else:
            self.clear(True)
            self.set_datas(datas)

