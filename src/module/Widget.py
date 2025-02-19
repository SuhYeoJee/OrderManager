
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


class SpWidget(BaseUI):
    insert_request = pyqtSignal(tuple)
    def __init__(self,parent=None):
        super().__init__('widget','sp',parent)
        loadUi(f"./ui/spWidget.ui", self) 
        # --------------------------
        # 이제 여기에 다이얼로그 기능을 얼마나 가져와야 하는가. 
        # 다이얼로그보다 불러오는건 적고 대신 계산이 들어가야함.  
        # 클리어, 로드는 필요함
        # --------------------------
        self.init_sp_dialog()
        self.input_widgets = self.get_input_widgets()
        [disable_wheel_event(x) for x in self.input_widgets]
    
    def init_sp_dialog(self):
        # 배경색
        palette = self.scrollAreaWidgetContents.palette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255))
        self.scrollAreaWidgetContents.setPalette(palette)
        self.scrollAreaWidgetContents.setAutoFillBackground(True)

    def on_pre_response(self,pre_response):
        '''다이얼로그 사전정보: 전체 cols,테이블에 존재하는 id목록, 외래키 제약'''
        if self.request_header[1] != pre_response[1]: return 
        self.cols = pre_response[2][0]
        self.set_ids(pre_response[2][1])
        print(pre_response)
        # 내가 지금 뭘 하고싶냐면 
        # sp를 볼거야
        # 쓰지는 않고 보기만 할거야 

        # id 세팅한다음 섭밋하면
        # path 가져와서 
        # path 내용(sp.json) 내놓으라그래서
        # 값 세팅. 

import types

def disable_wheel_event(widget):
    """ 기존 위젯의 wheelEvent를 덮어씌워서 포커스가 없을 때 휠 이벤트를 무시함 """
    original_wheel_event = widget.wheelEvent  # 기존 메서드 백업

    def new_wheel_event(self, event):
        event.ignore()
        # if not self.hasFocus():
        #     event.ignore()  # 부모(스크롤 영역)로 이벤트 전달
        # else:
        #     original_wheel_event(event)  # 원래 동작 수행

    widget.wheelEvent = types.MethodType(new_wheel_event, widget)  # 바운드 메서드로 등록
