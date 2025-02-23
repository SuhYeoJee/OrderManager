
from src.imports.pyqt5_imports import *
from src.imports.config import DB_PATH
# --------------------------
from src.module.BaseUI import BaseUI
from src.module.SqlliteInterface import SqlliteInterface
# --------------------------
TABLES = SqlliteInterface(DB_PATH).get_table_names()
# ===========================================================================================
class BaseDialog(BaseUI):
    insert_request = pyqtSignal(tuple)
    delete_request = pyqtSignal(tuple)
    update_request = pyqtSignal(tuple)
    def __init__(self,dialog_type,table_name,parent=None):
        super().__init__(dialog_type,table_name,parent)
        loadUi(f"./ui/{table_name}Dialog.ui", self) 
        # --------------------------
        self.on_submit = getattr(self, f"on_{dialog_type}_submit", None)
        self.input_widgets = self.get_input_widgets()
        # --------------------------
        self.loadBtn.clicked.connect(self.on_load)
        self.submitBtn.clicked.connect(self.on_submit)
    
    # [send request] -------------------------------------------------------------------------------------------
    def on_view_submit(self):
        self.close()
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
   
# ===========================================================================================
# 클래스 자동생성
for table_name in TABLES:
    class_name = f'{table_name.capitalize()}Dialog'
    globals()[class_name] = type(class_name, (BaseDialog,), {
        '__init__': lambda self, dialog_type, table_name, parent=None: super(type(self), self).__init__(dialog_type, table_name, parent)
    })
