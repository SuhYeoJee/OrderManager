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


class QueryWorker(QThread):
    result_signal = pyqtSignal(list)  # 쿼리 결과 전달

    def __init__(self, model, query):
        super().__init__()
        self.model = model
        self.query = query

    def run(self):
        rows = self.model.sql.execute_query(self.query)
        self.result_signal.emit(rows)  # 쿼리 결과를 시그널로 방출
