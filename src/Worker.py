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

    def __init__(self, model, query, table_name):
        super().__init__()
        self.model = model
        self.query = query
        self.table_name = table_name

    def run(self):
        col_names = self.get_table_col_names()
        res = self.run_execute_query()
        self.result_signal.emit([col_names]+res)

    def run_execute_query(self):
        return self.model.sql.execute_query(self.query)

    def get_table_col_names(self):
        res = self.model.sql.execute_query(f"PRAGMA table_info({self.table_name})")
        return [column[1] for column in res]
