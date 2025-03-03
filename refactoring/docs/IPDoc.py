if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# ===========================================================================================
from src.imports.config import DATE_FORMAT, DATE_KO_FORMAT
from src.imports.pyqt5_imports import QDate
from refactoring.docs.JsonManager import *
from pprint import pprint
# ===========================================================================================
class IPDoc(JsonManager):
    def __init__(self):
        ...
        # ipdoc 생성

        # ipdoc이 db에 접근하는 방법 
        # 1. 하위에 dbm을 갖는다. 어쨌든 독립적으로 써서 상관없음
        # 2. model을 인자로 받아 갖는다. 

        # 이거를 별도 dbm으로 쓴다음에 워커를 태워보내 


class model:
    def __init__(self):
        self.db = DBManager()

    def new_ip(self,path):
        return IPDoc(path).new_ip()

    # IPDoc.new_ip가 DBManager 필요할 때 가장 적절한 방법
    # 1. IPDoc.DBManager()
    # 2. IPDoc(path,self.db).new_ip() <- 이게나음