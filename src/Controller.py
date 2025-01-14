if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
from src.Worker import Worker
# ===========================================================================================

# Controller
class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.threads = [] #여러 thread 사용
        # --------------------------
        table_names = self.model.sql.get_table_names()
        self.view.set_table_names(table_names)
        self.view.tableNameComboBtn.clicked.connect(self.on_table_name)
        self.view.tableInsertBtn.clicked.connect(self.on_insert)
        self.view.tableDeleteBtn.clicked.connect(self.on_delete)
        
        # --------------------------
        self.init_signals()

    def init_signals(self):
        self.view.id_request.connect(self.on_id_request)
        self.view.dialogs['insert']['users'].insert_request.connect(self.on_insert_request)
        self.view.dialogs['insert']['users'].data_request.connect(self.on_data_request)
        self.view.dialogs['delete']['users'].delete_request.connect(self.on_delete_request)
        self.view.dialogs['delete']['users'].data_request.connect(self.on_data_request)
    # [view에서 model 호출] -------------------------------------------------------------------------------------------
    def on_id_request(self,id_request):
        worker_func = "get_table_ids"
        callback_func = self.view.dialogs[id_request[0]][id_request[1]].on_id_response
        self.launch_worker(worker_func,callback_func,id_request)

    def on_insert_request(self,insert_request):
        worker_func = "insert_data"
        callback_func = self.reload_table
        self.launch_worker(worker_func,callback_func,insert_request)

    def on_delete_request(self,delete_request):
        worker_func = "delete_data"
        callback_func = self.reload_table
        self.launch_worker(worker_func,callback_func,delete_request)

    def on_data_request(self,data_request):
        worker_func = "get_data_by_id"
        callback_func = self.view.dialogs[data_request[0]][data_request[1]].on_data_response
        self.launch_worker(worker_func,callback_func,data_request)
        
    def on_table_name(self):
        worker_func = "get_all_table_items"
        callback_func = self.view.update_table_data
        data_request = ('controller',self.get_table_name_from_tableNameComboBox())
        self.launch_worker(worker_func,callback_func,data_request)

    def reload_table(self,*args): #after insert,update,delete
        self.on_table_name()

    # --------------------------
    def launch_worker(self,worker_func:str,callback_func,*args):
        thread = Worker(self.model,worker_func,*args)
        thread.worker_response.connect(callback_func)
        thread.finished.connect(lambda: self.cleanup_thread(thread))
        self.threads.append(thread) #목록에 추가
        thread.start()
    # --------------------------
    def cleanup_thread(self, thread): # 스레드 종료 시 호출 
        self.threads.remove(thread) #목록에서 제거 
        thread.deleteLater()
    # -------------------------------------------------------------------------------------------
    def on_insert(self):
        table_name = self.get_table_name_from_tableNameComboBox()
        self.view.get_insert_dialog(table_name)

    def on_delete(self):
        table_name = self.get_table_name_from_tableNameComboBox()
        self.view.get_delete_dialog(table_name)

        

    def get_table_name_from_tableNameComboBox(self):
        return self.view.tableNameComboBox.currentText().strip()
