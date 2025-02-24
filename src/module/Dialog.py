
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
TABLES.remove('bond')
for table_name in TABLES:
    class_name = f'{table_name.capitalize()}Dialog'
    globals()[class_name] = type(class_name, (BaseDialog,), {
        '__init__': lambda self, dialog_type, table_name, parent=None: super(type(self), self).__init__(dialog_type, table_name, parent)
    })


class BondDialog(BaseDialog):
    def __init__(self, dialog_type, table_name, parent=None):
        super().__init__(dialog_type, table_name, parent)
        self._set_inner_widget()
        self.input_widgets = self.get_input_widgets()

    def _set_inner_widget(self):
        self.bondInnerWidget = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        loadUi("./ui/bondInnerWidget.ui", self.bondInnerWidget)
        self.scrollLayout.addWidget(self.bondInnerWidget)

    def _set_powder_combobox(self):
        powders = [' ',"co","fe","cu_300","cu_600","ni","cusn_67","cusn_80","w","wc","w2c","s","ag","zn"]
        for i in range(1,6):
            combo_box = self.bondInnerWidget.findChild(QComboBox, f'powder_{i}ComboBox')
            combo_box.clear()
            combo_box.addItems(powders)
        combo_box = self.bondInnerWidget.findChild(QComboBox, f'powder_6ComboBox')
        combo_box.clear()
        combo_box.addItems([' ','p2o5'])

    def set_fks(self,datas):
        super().set_fks(datas)
        self._set_powder_combobox()

    # 시그널 박아서 밀도 가져오기 




class ShippingDialog(BaseDialog):
    def __init__(self,parent=None):
        super().__init__('update','shipping',parent)

    def on_update_submit(self):
        inputs = self.get_inputs()
        inputs.pop('reg_date')
        inputs.pop('update_date')
        self.update_request.emit(('update','orders',inputs))
        self.close()