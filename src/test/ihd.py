from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QLineEdit, QComboBox, 
    QHBoxLayout, QApplication, QWidget
)
import sys

class DynamicFormDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dynamic Form")
        self.layout = QVBoxLayout(self)

        # + 버튼
        self.add_button = QPushButton("+ 추가")
        self.add_button.clicked.connect(self.add_input_field)
        self.layout.addWidget(self.add_button)

        self.input_fields = []  # 동적으로 추가된 입력창을 저장하는 리스트

    def add_input_field(self):
        """새로운 입력 필드 추가"""
        input_layout = QHBoxLayout()  # 수평 레이아웃으로 관리

        line_edit = QLineEdit(self)
        combo_box = QComboBox(self)
        combo_box.addItems(["옵션 1", "옵션 2", "옵션 3"])

        remove_button = QPushButton("-")
        remove_button.clicked.connect(lambda: self.remove_input_field(input_layout))

        input_layout.addWidget(line_edit)
        input_layout.addWidget(combo_box)
        input_layout.addWidget(remove_button)

        self.layout.insertLayout(self.layout.count() - 1, input_layout)
        self.input_fields.append((line_edit, combo_box, input_layout))

    def remove_input_field(self, input_layout):
        """입력 필드 제거"""
        for widget in input_layout.children():
            if isinstance(widget, QWidget):
                widget.deleteLater()
        self.layout.removeItem(input_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = DynamicFormDialog()
    dialog.exec_()
