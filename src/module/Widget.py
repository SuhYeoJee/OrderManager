
from src.imports.pyqt5_imports import *
# --------------------------
from src.module.SqlliteInterface import SqlliteInterface
# --------------------------
from src.imports.config import DATETIME_FORMAT,DB_PATH
TABLES = SqlliteInterface(DB_PATH).get_table_names()
# ===========================================================================================
class OrdersWidget(QDialog):
    data_request = pyqtSignal(tuple)
    insert_request = pyqtSignal(tuple)
    def __init__(self,parent=None):
        super().__init__(parent)
        loadUi(f"./ui/ordersWidget.ui", self) 

        # 이제 여기에 다이얼로그 기능을 얼마나 가져와야 하는가. 
        # 다이얼로그보다 불러오는건 적고 대신 계산이 들어가야함. 
        # 클리어, 로드는 필요함
        self.request_header = ('widget','orders')
        self.on_submit = getattr(self, f"on_{dialog_type}_submit", None)
        self.cols, self.data = None, None
        self.input_widgets = self.get_input_widgets()
        # --------------------------
        self.loadBtn.clicked.connect(self.on_load)
        self.submitBtn.clicked.connect(self.on_submit)


# 공통조상을 만들자..
# 조상의 조상..
