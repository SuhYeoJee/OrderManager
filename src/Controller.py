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
        self.view.tableInsertBtn.clicked.connect(lambda: self.on_table_btn('insert'))
        self.view.tableDeleteBtn.clicked.connect(lambda: self.on_table_btn('delete'))
        self.view.tableUpdateBtn.clicked.connect(lambda: self.on_table_btn('update'))
        self.view.tableSelectBtn.clicked.connect(self.on_table_select_btn)
        self.view.tabWidget.currentChanged.connect(self.on_tab_changed)
        # --------------------------
        self.init_signals()
        self.on_tab_changed(0)

    def init_signals(self):
        self.view.pre_request.connect(self.on_pre_request)
        for action in ['insert', 'delete', 'update']:
            for table_name in self.view.dialog_infos.keys():
                dialog = self.view.dialogs[action][table_name]
                getattr(dialog, f'{action}_request').connect(lambda x, action=action: self.on_table_request(action, x))
                dialog.data_request.connect(self.on_data_request)
                if table_name == 'sp':
                    dialog.json_request.connect(self.on_json_request)
            
    # [view에서 model 호출] -------------------------------------------------------------------------------------------
    def on_pre_request(self,pre_request):
        worker_func = "get_pre_infos"
        callback_func = self.view.dialogs[pre_request[0]][pre_request[1]].on_pre_response
        self.launch_worker(worker_func,callback_func,pre_request)

    def on_table_request(self,request_type,request):
        worker_func = f"{request_type}_data"
        callback_func = self.reload_table
        self.launch_worker(worker_func,callback_func,request)

    def on_json_request(self,json_reqeust):
        worker_func = f"get_json_data"
        callback_func = self.view.dialogs[json_reqeust[0]][json_reqeust[1]].on_json_response
        self.launch_worker(worker_func,callback_func,json_reqeust)

    def on_data_request(self,data_request):
        worker_func = "get_data_by_id"
        callback_func = self.view.dialogs[data_request[0]][data_request[1]].on_data_response
        self.launch_worker(worker_func,callback_func,data_request)
        
    def on_table_name(self):
        worker_func = "get_all_table_items"
        callback_func = self.view.update_table_data
        data_request = ('controller',self.view.get_table_name())
        self.launch_worker(worker_func,callback_func,data_request)

    def on_tab_changed(self,index):
        '''0탭 전환시 orders 표시'''
        if index == 0:
            worker_func = "get_all_table_items"
            callback_func = self.view.update_table_data
            data_request = ('ordersTable','orders')
            self.launch_worker(worker_func,callback_func,data_request)


    def reload_table(self,*args): #after insert,update,delete
        self.on_table_name()

    def on_table_select_btn(self):
        worker_func = "select_data"
        callback_func = self.view.update_table_data
        self.launch_worker(worker_func,callback_func,self.view.get_select_data())

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
    
    def on_table_btn(self,btn_type):
        table_name = self.view.get_table_name()
        self.view.get_dialog(btn_type,table_name)
