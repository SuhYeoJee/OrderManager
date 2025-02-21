
from src.imports.pyqt5_imports import *
from src.imports.config import DATETIME_FORMAT
import types
# --------------------------
from src.module.BaseUI import BaseUI
# ===========================================================================================
def disable_wheel_event(widget):
    """ 기존 위젯의 wheelEvent를 덮어씌워서 포커스가 없을 때 휠 이벤트를 무시함 """
    original_wheel_event = widget.wheelEvent  # 기존 메서드 백업
    def new_wheel_event(self, event):
        event.ignore()
    widget.wheelEvent = types.MethodType(new_wheel_event, widget)  # 바운드 메서드로 등록
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
        self.scrollLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scroll_inner_widgets = []
        self.item_groups = []
        self.pre_response = None
        # --------------------------
        self.loadBtn.clicked.connect(self.on_load)
        self.submitBtn.clicked.connect(self.on_insert_submit)
        self.addBtn.clicked.connect(self.add_grid)
    # --------------------------
    def on_insert_submit(self):
        inputs = self.get_inner_widgets_data()
        print(inputs)
        # inputs.pop('id')
        # inputs.pop('reg_date')
        # inputs.pop('update_date')
        # self.data = self._add_request_header(inputs)
        # self.insert_request.emit(self.data)
        self.close()
    # --------------------------
    def add_grid(self):
        """ordersInnerWidget을 복제하여 스크롤 영역에 추가 """
        ordersInnerWidget = QWidget()
        loadUi("./ui/ordersInnerWidget.ui", ordersInnerWidget)

        self.scrollAreaWidgetContents.setMinimumHeight(self.scrollAreaWidgetContents.height() + 350) #위젯 높이 늘리기
        ordersInnerWidget.label.setText(f"Group {len(self.scroll_inner_widgets)+1}") #라벨변경
        self.scrollLayout.addWidget(ordersInnerWidget)
        self.scroll_inner_widgets.append(ordersInnerWidget)

        ordersInnerWidget.item_loadBtn.clicked.connect(lambda: self.set_itemComboBoxs(ordersInnerWidget))

        # item_groupLoad아이템 세팅 테스트 
        # 아이템 그룹 선택값에 따라 필터링
        ordersInnerWidget.item1ComboBox.addItems(['']+self.pre_response[2][2]['item'])
    # --------------------------
    def set_itemComboBoxs(self,ordersInnerWidget):
        print(ordersInnerWidget.label.text())
    
    
    
    
    def get_inner_widgets_data(self):
        '''{idx:{col:val}}'''
        return {idx: self.get_inputs(inner_widget) for idx, inner_widget in enumerate(self.scroll_inner_widgets)}
    def on_pre_response(self,pre_response): #pre_response 사용안함
        '''다이얼로그 사전정보: 전체 cols,테이블에 존재하는 id목록, 외래키 제약'''
        self.pre_response = pre_response
        self.add_grid()
        return 

class SpWidget(BaseUI):
    insert_request = pyqtSignal(tuple)
    set_request = pyqtSignal(tuple)
    def __init__(self,parent=None):
        super().__init__('widget','sp',parent)
        loadUi(f"./ui/spWidget.ui", self) 
        self.init_sp_dialog()
        self.input_widgets = self.get_input_widgets()
        [disable_wheel_event(x) for x in self.input_widgets]
    
    def init_sp_dialog(self):
        # 배경색
        palette = self.scrollAreaWidgetContents.palette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255))
        self.scrollAreaWidgetContents.setPalette(palette)
        self.scrollAreaWidgetContents.setAutoFillBackground(True)

    def on_pre_response(self,pre_response): #pre_response 사용안함
        '''다이얼로그 사전정보: 전체 cols,테이블에 존재하는 id목록, 외래키 제약'''
        return 

    def on_json_response(self,json_response):
        if self.request_header[1] != json_response[1]: return 
        self.set_datas_from_json_response(json_response)
        self.set_request.emit(('widget','sp',json_response[2]))
