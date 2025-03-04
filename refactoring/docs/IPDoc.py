if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# ===========================================================================================
from src.imports.config import DATE_FORMAT, DATE_KO_FORMAT
from src.imports.pyqt5_imports import QDate
from refactoring.docs.JsonManager import *
from refactoring.db.DBManager import *
from refactoring.docs.params import IPDocParam
from pprint import pprint
# ===========================================================================================
class IPDoc(JsonManager):
    def __init__(self, dbm:DBManager, p:IPDocParam):
        self.dbm = dbm
        self.p = p
        self.name = self._get_new_ip_name()
    # --------------------------
    def build_ip(self):
        self.data['inputs'] = self.p.to_dict()
        self.data['loads'] = self._load_items_from_db()
        self.data['autos'] = self._build_ip_autos()
    # -------------------------------------------------------------------------------------------

    def _get_new_ip_name(self):
        last_ip_year,last_ip_no = self._get_last_ip_year_and_no_from_db()
        now_year =str(QDate.currentDate().year())
        if last_ip_year == now_year:
            new_ip_name = f"{last_ip_year}-IP{int(last_ip_no[2:])+1:04}"
        else:
            new_ip_name = f"{now_year}-IP{1:04}"
        return new_ip_name
    # -------------------------------------------------------------------------------------------

    def _load_items_from_db(self):
        items = {}
        for i in range(1, 5):
            if item_param := getattr(self.p,f'item{i}'):
                items['item{i}'] = self.dbm.select_records_by_comparison('ip','name',item_param.name)
        return items

    def _build_ip_autos(self):
        autos = {}
        autos['name'] = self.name
        autos['due_date'] = QDate.fromString(self.p.due_date, DATE_FORMAT).toString(DATE_KO_FORMAT)
        autos['creation_date'] = QDate.currentDate().toString(DATE_KO_FORMAT)
        autos.update(self._build_ip_autos_from_loads())

    # -------------------------------------------------------------------------------------------
    def _get_last_ip_year_and_no_from_db(self):
        try:
            [last_ip_name] = self.dbm.select_records(SelectParam('ip',['name'],sort=SortParam(),limit=1))
            last_ip_year,last_ip_no = last_ip_name[1].split('-')
        except ValueError:
            last_ip_year,last_ip_no = "2000","IP0000"
        return last_ip_year,last_ip_no
    
    def _build_ip_autos_from_loads(self):
        autos = {}
        # 일단 기존 방식이 너무 구림. 
        # col_name이 seg_amount, segment_처럼 되어있는데
        # 이걸 db명에서 찾아서 씀. 
        # 개선 반드시 필요함 

        return autos

    # ===========================================================================================