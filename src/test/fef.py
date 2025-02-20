if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QSize
from PyQt5.uic import loadUi

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('./ui/ordersWidget.ui', self)  # 기존 ordersWidget.ui 파일을 로드
        
        self.add_button = self.findChild(QPushButton, 'addButton')  
        self.add_button.clicked.connect(self.add_grid)

        # 기본 레이아웃 설정 (scrollArea의 레이아웃)
        self.vBoxLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.current_height = 10
        self.add_grid()

    def add_grid(self):
        inner_widget = QWidget()
        loadUi('./ui/innerWidget.ui', inner_widget)
        self.vBoxLayout.addWidget(inner_widget)
        # 위젯 높이 증가
        self.current_height += 350
        self.scrollAreaWidgetContents.setMinimumSize(QSize(self.scrollAreaWidgetContents.width(), self.current_height))

# 테스트용 main문
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyDialog()  # MyDialog 인스턴스 생성
    window.show()  # 다이얼로그 표시
    sys.exit(app.exec_())  # 애플리케이션 실행
