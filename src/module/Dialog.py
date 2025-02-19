
from src.imports.pyqt5_imports import *
import re
import config 
# --------------------------
from src.module.BaseUI import BaseUI
from src.module.SqlliteInterface import SqlliteInterface
# --------------------------
from src.imports.config import DATETIME_FORMAT, DB_PATH
TABLES = SqlliteInterface(DB_PATH).get_table_names()
# ===========================================================================================
class BaseDialog(BaseUI):
    insert_request = pyqtSignal(tuple)
    delete_request = pyqtSignal(tuple)
    update_request = pyqtSignal(tuple)
    json_request = pyqtSignal(tuple)
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

# # SpDialog에 sp view 추가
# class_name = "SpDialog"
# if class_name in globals():
#     cls = globals()[class_name]  # 클래스 가져오기

#     def _on_view_sp_submit(self):
#         path = self.get_inputs()['path']
#         print(path)
#         self.json_request.emit(self._add_request_header(path))
#     setattr(cls, "_on_view_sp_submit", _on_view_sp_submit)
    
#     def _init_sub_dialog(self):
#         self.sub_dialog = QDialog(self)
#         self.sub_dialog_inner_widget = loadUi("./ui/spWidget.ui")
#         layout = QVBoxLayout(self)
#         # 스크롤
#         self.sub_dialog.scroll_area = QScrollArea(self)
#         self.sub_dialog_inner_widget.setMinimumSize(self.sub_dialog_inner_widget.size())
#         self.sub_dialog.scroll_area.setWidgetResizable(True)
#         self.sub_dialog.scroll_area.setWidget(self.sub_dialog_inner_widget)
#         # 배경색
#         palette = self.sub_dialog_inner_widget.palette()
#         palette.setColor(QPalette.Background, QColor(255, 255, 255))
#         self.sub_dialog_inner_widget.setPalette(palette)
#         self.sub_dialog_inner_widget.setAutoFillBackground(True)

#         self.sub_dialog_inner_input_widgets = self.get_input_widgets(self.sub_dialog_inner_widget)
#         layout.addWidget(self.sub_dialog.scroll_area)
#         self.sub_dialog_inner_widget.pushButton.clicked.connect(cls._on_view_sp_submit)
#     setattr(cls, "_init_sub_dialog", _init_sub_dialog)

#     def on_json_response(self,json_response):
#         sp = json_response
#         _set_sp_datas(sp)
#         ...
#     setattr(cls, "on_json_response", on_json_response)

#     def _set_sp_datas(self, sp) -> None:
#         set_handlers = {
#             QLineEdit: lambda widget, value: widget.setText(str(value)),
#             QComboBox: lambda widget, value: (widget.addItem(str(value)) if widget.findText(str(value)) == -1 else None, widget.setCurrentText(str(value)))[1],
#             QSpinBox: lambda widget, value: widget.setValue(int(value)),
#             QDoubleSpinBox: lambda widget, value: widget.setValue(float(value)),
#             QPlainTextEdit: lambda widget, value: widget.setPlainText(str(value)),
#             QDateTimeEdit: lambda widget, value: widget.setDateTime(QDateTime.fromString(value,DATETIME_FORMAT)),
#             QDateEdit: lambda widget, value: widget.setDateTime(QDateTime.fromString(value,DATETIME_FORMAT)),
#         }

#         for widget in self.input_widgets:
#             print('# ------------------------------------------')
#             print(widget.objectName())
#             key = self.get_key_from_object_name(widget.objectName())
#             try:
#                 data_type,data_name = key.split('_',1)
#             except:
#                 continue
#             if data_name == 'spinbox_lineedit':
#                 continue
#             print(data_type)
#             print(data_name)
#             if data_type == 'loads':
#                 table_name,col_name = data_name.split('_',1)
#                 if col_name in ['dia1','dia2','dia3']:
#                     ...
#                 val = sp[data_type][table_name][col_name]
#             else:
#                 try:
#                     val = sp[data_type][data_name]
#                 except:
#                     print(data_type,data_name)
#                     val = None
#             val = val if val else 0
#             set_handlers.get(type(widget))(widget,val)
#     setattr(cls, "_set_sp_datas", _set_sp_datas)



