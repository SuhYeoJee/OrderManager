if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# ===========================================================================================
from src.imports.config import DATE_FORMAT, DATE_KO_FORMAT
from src.imports.pyqt5_imports import QDate

from refactoring.db import DBManager,InsertParam,SelectParam,SortParam
from refactoring.docs.JsonManager import JsonManager
from refactoring.docs.params import SPDocParam
from refactoring.utils.SafeList import SafeList

class SPDoc(JsonManager):
    def __init__(self,dbm,p:SPDocParam):
        self.dbm =dbm
        self.p = p
        self.name = self._get_new_sp_name()
        self.file_path = f'./test/{self.name}.json'
        # self.file_path = f'./doc/sp/{self.name}.json'
        super().__init__(self.file_path)

        self.build_sp()

    @JsonManager.auto_save
    def build_sp(self):
        self.data['inputs'] = self.p.to_dict()
        self.data['loads'] = self._load_segment()
        self.data['autos'] = self._build_autos()
    # -------------------------------------------------------------------------------------------
    def _get_new_sp_name(self):
        last_sp_year,last_sp_no = self._get_last_sp_year_and_no_from_db()
        now_year =str(QDate.currentDate().year())
        if last_sp_year == now_year:
            new_sp_name = f"{last_sp_year}-SP{int(last_sp_no[2:])+1:04}"
        else:
            new_sp_name = f"{now_year}-SP{1:04}"
        # recent_sp_name = ''
        # new_sp_name = f"{new_sp_name}-{recent_sp_name}" # 이거 진짜 최선인지 물어보기
        return new_sp_name
    # -------------------------------------------------------------------------------------------

    def _load_segment(self):
        items = SafeList(self.dbm.select_records_by_comparison('segment','name',self.p.name)).safe_get(0)
        return items

    # -------------------------------------------------------------------------------------------
    def _get_last_sp_year_and_no_from_db(self):
        try:
            [last_sp_name] = self.dbm.select_records(SelectParam('sp',['name'],sort=SortParam(),limit=1))
            last_sp_year,last_sp_no = last_sp_name[1].split('-')
        except ValueError:
            last_sp_year,last_sp_no = "2000","SP0000"
        return last_sp_year,last_sp_no
    




# ===========================================================================================