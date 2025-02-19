if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import QDialog, QComboBox, QVBoxLayout,QScrollArea,QLineEdit, QPlainTextEdit,QDateTimeEdit,QDateEdit,QSpinBox, QDoubleSpinBox
from PyQt5.QtCore import pyqtSignal,QDateTime
from PyQt5.QtGui import QPalette, QColor
from PyQt5.uic import loadUi
from PyQt5 import uic
import re
# --------------------------
from src.module.SqlliteInterface import SqlliteInterface
# --------------------------
DB_PATH='./config/NOVA.db'
DATETIME_FORMAT = "yyyy-MM-dd HH:mm:ss"
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

