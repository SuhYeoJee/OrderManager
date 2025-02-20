if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QLabel
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')

        # 버튼 생성
        self.pushButton = QPushButton('Open Dialogs', self)
        self.pushButton.clicked.connect(self.show_dialogs)
        self.setCentralWidget(self.pushButton)

    def show_dialogs(self):
        # 두 개의 다이얼로그 로드
        self.sp_dialog = QDialog(self)
        self.ip_dialog = QDialog(self)

        # UI 파일 불러오기
        loadUi('./ui/spDialog.ui', self.sp_dialog)
        loadUi('./ui/ipDialog.ui', self.ip_dialog)

        # 다이얼로그 동시에 표시
        self.sp_dialog.show()
        self.ip_dialog.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
