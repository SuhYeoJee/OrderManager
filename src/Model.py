if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
from src.module.SqlliteInterface import SqlliteInterface

# Model
class Model:
    def __init__(self):
        self.sql = SqlliteInterface()

    def handle_data(self,data):
        print(__name__,data)
