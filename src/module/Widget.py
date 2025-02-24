
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
        self.input_widgets = self.get_input_widgets()
        self.scrollLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scroll_inner_widgets = []
        self.item_groups = []
        self.pre_response = None
        # --------------------------
        self.submitBtn.clicked.connect(self.on_insert_submit)
        self.addBtn.clicked.connect(self.add_grid)
    # --------------------------
    def on_insert_submit(self):
        inputs = self.get_inputs()
        inner_widget_inputs = self.get_inner_widgets_data()
        if not inner_widget_inputs:
            return # 입력 없음
        inputs.update(inner_widget_inputs)
        pops = ['name','reg_date','update_date','group','engrave']
        pops.extend([i for s in [[f'amount{x}', f'code{x}', f'item{x}'] for x in range(1, 5)] for i in s])
        [inputs.pop(x) for x in pops]
        self.data = self._add_request_header(inputs)
        self.insert_request.emit(self.data)
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

        items = self.pre_response[2][2]['item']
        ordersInnerWidget.item_loadBtn.clicked.connect(lambda: self.set_itemComboBoxs(ordersInnerWidget,items))
        item_groups = list(set([x.split(' ')[0] for x in items]))
        ordersInnerWidget.groupComboBox.clear()
        ordersInnerWidget.groupComboBox.addItems(['']+item_groups)
    # --------------------------
    def set_itemComboBoxs(self,ordersInnerWidget,items):
        item_group = ordersInnerWidget.groupComboBox.currentText()
        items = [i for i in items if i.startswith(item_group)]

        [getattr(ordersInnerWidget, f"item{i}ComboBox").clear() 
         or getattr(ordersInnerWidget, f"item{i}ComboBox").addItems([''] + items) for i in range(1, 5)]

    def clear_grids(self):
        """모든 그리드를 삭제"""
        for widget in self.scroll_inner_widgets:
            self.scrollLayout.removeWidget(widget)  
            widget.deleteLater()  
        self.scroll_inner_widgets.clear() 
        self.scrollAreaWidgetContents.setFixedHeight(10)
        
    def get_inner_widgets_data(self):
        '''{idx:{col:val}}'''
        return {idx: self.get_inputs(inner_widget) for idx, inner_widget in enumerate(self.scroll_inner_widgets)}
    
    def on_pre_response(self,pre_response): #pre_response 사용안함
        '''다이얼로그 사전정보: 전체 cols,테이블에 존재하는 id목록, 외래키 제약'''
        if self.request_header[1] != pre_response[1]: return 
        self.pre_response = pre_response
        self.cols = pre_response[2][0]
        self.set_fks(pre_response[2][2])

class SpWidget(BaseUI):
    insert_request = pyqtSignal(tuple)
    set_request = pyqtSignal(tuple)
    def __init__(self,parent=None):
        super().__init__('widget','sp',parent)
        loadUi(f"./ui/spWidget.ui", self) 
        self.init_sp_dialog()
        self.input_widgets = self.get_input_widgets()
        self.input_widgets.append(self.loads_segment_model_imgLabel)
        [disable_wheel_event(x) for x in self.input_widgets]
        self.submitBtn.clicked.connect(self.close)
    
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

class IpWidget(BaseUI):
    insert_request = pyqtSignal(tuple)
    set_request = pyqtSignal(tuple)
    def __init__(self,parent=None):
        super().__init__('widget','ip',parent)
        loadUi(f"./ui/ipWidget.ui", self) 
        self.init_ip_dialog()
        self.input_widgets = self.get_input_widgets()
        self.input_widgets.append(self.loads_item1_imageLabel)
        [disable_wheel_event(x) for x in self.input_widgets]
        self.submitBtn.clicked.connect(self.close)
    
    def init_ip_dialog(self):
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
        self.set_request.emit(('widget','ip',json_response[2]))
