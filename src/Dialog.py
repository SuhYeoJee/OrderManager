if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QPlainTextEdit,QDateTimeEdit
from PyQt5.QtCore import pyqtSignal,QDateTime
from PyQt5.uic import loadUi
# --------------------------
DATETIME_FORMAT = "yyyy-MM-dd HH:mm:ss"
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
        # --------------------------
        self.loadBtn.clicked.connect(self.on_load)
        self.submitBtn.clicked.connect(self.on_submit)
    # --------------------------
    def clear(self):...
    def set_fks(self,datas):...
    def get_inputs(self)->dict:...
    def set_datas(self,datas:tuple):...
    def set_ids(self,ids):
        self.idComboBox.clear()
        self.idComboBox.addItems(map(str,ids))
    # --------------------------
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
class UserDialog(BaseDialog):
    def __init__(self,dialog_type,table_name,parent=None):
        super().__init__(dialog_type,table_name,parent)
    # --------------------------
    def clear(self):
        self.idComboBox.clear()
        self.nameLineEdit.clear()
        self.ageSpinBox.setValue(0) 
        self.cityLineEdit.clear()

    def set_fks(self,fks:dict):
        try:
            self.idComboBox.addItems(map(str,fks['name'])) 
        except:
            ...
        # 여기서 fks를 combobox에 세팅
    # --------------------------
    def get_inputs(self):
        id = self.idComboBox.currentText()
        name = self.nameLineEdit.text()
        age = self.ageSpinBox.value()
        city = self.cityLineEdit.text()
        return dict(zip(self.cols, (id,name,age,city)))
    # --------------------------
    def set_datas(self,datas:tuple):
        (id, name,age,city) = datas
        self.nameLineEdit.setText(name)
        self.ageSpinBox.setValue(age)
        self.cityLineEdit.setText(city)

class CustomerDialog(BaseDialog):
    def __init__(self,dialog_type,table_name,parent=None):
        super().__init__(dialog_type,table_name,parent)
    # --------------------------
    def clear(self):
        self.idComboBox.clear()
        self.nameLineEdit.clear()
        self.codeLineEdit.clear()
        self.descriptionPlainTextEdit.clear()
        self.reg_dateDateTimeEdit.setDateTime(QDateTime(2000, 1, 1, 0, 0))
        self.update_dateDateTimeEdit.setDateTime(QDateTime(2000, 1, 1, 0, 0))

    def set_fks(self,fks:dict): return #외래키 없음
    # --------------------------
    def get_inputs(self):
        id = self.idComboBox.currentText()
        name = self.nameLineEdit.text()
        code = self.codeLineEdit.text()
        description = self.descriptionPlainTextEdit.toPlainText()
        reg_date = self.reg_dateDateTimeEdit.dateTime().toString(DATETIME_FORMAT)
        update_date = self.update_dateDateTimeEdit.dateTime().toString(DATETIME_FORMAT)
        return dict(zip(self.cols, (id,name,code, description,reg_date,update_date)))
    # --------------------------
    def set_datas(self,datas:tuple):
        (id,name,code, description,reg_date,update_date) = datas
        self.nameLineEdit.setText(name)
        self.codeLineEdit.setText(code)
        self.descriptionPlainTextEdit.setPlainText(description)
        self.reg_dateDateTimeEdit.setDateTime(QDateTime.fromString(reg_date,DATETIME_FORMAT))
        self.update_dateDateTimeEdit.setDateTime(QDateTime.fromString(update_date,DATETIME_FORMAT))

class PowderDialog(BaseDialog):...
class ShankDialog(BaseDialog):...
class SubmaterialDialog(BaseDialog):...
class DiamondDialog(BaseDialog):...
class BondDialog(BaseDialog):...
class SegmentDialog(BaseDialog):...
class ItemDialog(BaseDialog):...
class OrdersDialog(BaseDialog):...
class SpDialog(BaseDialog):...
class IpDialog(BaseDialog):...