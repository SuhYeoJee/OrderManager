if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# ===========================================================================================
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QComboBox, QLineEdit, QPlainTextEdit,QDateTimeEdit,QDateEdit,QSpinBox, QDoubleSpinBox
from PyQt5.QtCore import pyqtSignal,QDateTime
from PyQt5.QtGui import QPalette, QColor
import json
import re
# --------------------------
DATETIME_FORMAT = "yyyy-MM-dd HH:mm:ss"
# ===========================================================================================
class SpDialog(QDialog):
    def __init__(self):
        super().__init__()

        uic.loadUi("./ui/spDialog.ui", self)
        self.inner_widget = uic.loadUi("./ui/ipWidget.ui")

        # 배경색 
        palette = self.inner_widget.palette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255))
        self.inner_widget.setPalette(palette)
        self.inner_widget.setAutoFillBackground(True)

        # 스크롤 
        self.inner_widget.setMinimumSize(self.inner_widget.size())
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.inner_widget)

        self.input_widgets = self.get_input_widgets()
        self.set_sp_vals()

    def __read_json_file(self,json_path):
        with open(json_path, 'r',encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data

    def set_sp_vals(self):
        sp = self.__read_json_file('./sp/2025-SP0002-25-0001.json')
        self.set_datas(sp)

    def set_datas(self, sp) -> None:
        set_handlers = {
            QLineEdit: lambda widget, value: widget.setText(str(value)),
            QComboBox: lambda widget, value: (widget.addItem(str(value)) if widget.findText(str(value)) == -1 else None, widget.setCurrentText(str(value)))[1],
            QSpinBox: lambda widget, value: widget.setValue(int(value)),
            QDoubleSpinBox: lambda widget, value: widget.setValue(float(value)),
            QPlainTextEdit: lambda widget, value: widget.setPlainText(str(value)),
            QDateTimeEdit: lambda widget, value: widget.setDateTime(QDateTime.fromString(value,DATETIME_FORMAT)),
            QDateEdit: lambda widget, value: widget.setDateTime(QDateTime.fromString(value,DATETIME_FORMAT)),
        }

        for widget in self.input_widgets:
            print('# ------------------------------------------')
            print(widget.objectName())
            key = self.get_key_from_object_name(widget.objectName())
            try:
                data_type,data_name = key.split('_',1)
            except:
                continue
            if data_name == 'spinbox_lineedit':
                continue
            print(data_type)
            print(data_name)
            if data_type == 'loads':
                table_name,col_name = data_name.split('_',1)
                if col_name in ['dia1','dia2','dia3']:
                    ...
                val = sp[data_type][table_name][col_name]
            else:
                try:
                    val = sp[data_type][data_name]
                except:
                    print(data_type,data_name)
                    val = None
            val = val if val else 0
            set_handlers.get(type(widget))(widget,val)

    
    def get_input_widgets(self):
        input_widgets = self.inner_widget.findChildren((QLineEdit, QComboBox, QDateTimeEdit,QDateEdit,QPlainTextEdit,QSpinBox,QDoubleSpinBox))
        return [widget for widget in input_widgets if widget.objectName()]
    def get_key_from_object_name(self,object_name):
        # col_name = 첫 번째 대문자 이전
        match = re.match(r'^[^A-Z]*', object_name)
        return match.group(0) if match else object_name
    

if __name__ == "__main__":
    app = QApplication([])

    dialog = SpDialog()
    dialog.show()

    app.exec_()
