
from src.imports.pyqt5_imports import *
# --------------------------
from src.module.BaseUI import BaseUI
# ===========================================================================================
class OrdersWidget(BaseUI):
    insert_request = pyqtSignal(tuple)
    def __init__(self,parent=None):
        super().__init__('widget','orders',parent)
        loadUi(f"./ui/ordersWidget.ui", self) 
        # --------------------------
        # 이제 여기에 다이얼로그 기능을 얼마나 가져와야 하는가. 
        # 다이얼로그보다 불러오는건 적고 대신 계산이 들어가야함. 
        # 클리어, 로드는 필요함
        # --------------------------
        self.input_widgets = self.get_input_widgets()
        # --------------------------
        self.loadBtn.clicked.connect(self.on_load)
        self.submitBtn.clicked.connect(self.on_insert_submit)
    # --------------------------
    def on_insert_submit(self):
        inputs = self.get_inputs()
        inputs.pop('id')
        inputs.pop('reg_date')
        inputs.pop('update_date')
        self.data = self._add_request_header(inputs)
        self.insert_request.emit(self.data)
        self.close()