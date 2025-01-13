if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
from src.Worker import QueryWorker
# ===========================================================================================

# Controller
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.threads = [] #여러 thread 사용
        # --------------------------
        table_names = self.model.sql.get_table_names()
        self.view.set_table_names(table_names)
        self.view.tableComboBtn.clicked.connect(self.handle_tableComboBtn)
    # -------------------------------------------------------------------------------------------
    # thread 생성 후 view와 연결
    def handle_tableComboBtn(self):
        table_name = self.view.tableComboBox.currentText().strip()
        query = f"SELECT * FROM {table_name}"

        thread = QueryWorker(self.model,query,table_name)
        thread.result_signal.connect(self.view.update_table_data)
        thread.finished.connect(lambda: self.cleanup_thread(thread))
        self.threads.append(thread) #목록에 추가
        thread.start()
    # --------------------------
    # 스레드 종료 시 호출 
    def cleanup_thread(self, thread):
        self.threads.remove(thread) #목록에서 제거 
        thread.deleteLater()
