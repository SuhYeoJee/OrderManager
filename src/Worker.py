from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    worker_response = pyqtSignal(tuple)
    # --------------------------
    def __init__(self, model, method_name:str, *args):
        super().__init__()
        self.model = model
        self.method_name = method_name
        self.args = args
    # -------------------------------------------------------------------------------------------

    def run(self):
        method = getattr(self.model, self.method_name)
        result = method(*self.args)
        self.worker_response.emit(result)
# ===========================================================================================
