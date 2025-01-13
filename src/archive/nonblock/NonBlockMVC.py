if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
import random
import time
# Model
class Model:
    def get_random_list(self):
        print('loading...')
        time.sleep(5)
        print('completed')
        return random.choice([[1],[2,2],[3,3,3],[4,4,4,4]])
# ===========================================================================================
from PyQt5.QtCore import QThread, pyqtSignal
# Worker
class Worker(QThread):
    result_signal = pyqtSignal(list) #signal로 리스트 결과 전달 
    # --------------------------
    def __init__(self, model):
        super().__init__()
        self.model = model
    # -------------------------------------------------------------------------------------------
    # model 함수 실행 후 result_signal을 통해 결과를 보냄 
    def run(self):
        result = self.model.get_random_list()
        self.result_signal.emit(result)
# ===========================================================================================
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton
from PyQt5.uic import loadUi
# View
class View(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("./src/archive/nonblock/view.ui", self)  # .ui 파일 로드
        # --------------------------
        self.text_area = self.findChild(QTextEdit, "textArea")
        self.run_button = self.findChild(QPushButton, "runButton")
        self.run_button.clicked.connect(self.on_run_button_clicked)
    # -------------------------------------------------------------------------------------------
    # run_button 클릭시 동작 
    def on_run_button_clicked(self):
        self.text_area.append("Running...")
    # --------------------------
    # result_signal 결과 전달시 동작 (ctrl가 worker에 연결)
    def update_text_area(self, result):
        self.text_area.append(str(result))
# ===========================================================================================
# Controller
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.threads = [] #여러 thread 사용
        # --------------------------
        self.view.run_button.clicked.connect(self.handle_run_button)
    # -------------------------------------------------------------------------------------------
    # thread 생성 후 view와 연결
    def handle_run_button(self):
        thread = Worker(self.model)
        thread.result_signal.connect(self.view.update_text_area)
        thread.finished.connect(lambda: self.cleanup_thread(thread))
        self.threads.append(thread) #목록에 추가
        thread.start()
    # --------------------------
    # 스레드 종료 시 호출 
    def cleanup_thread(self, thread):
        self.threads.remove(thread) #목록에서 제거 
        thread.deleteLater()
# ===========================================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = Model()
    view = View()
    controller = Controller(model, view)
    # --------------------------
    view.show()
    sys.exit(app.exec_())
