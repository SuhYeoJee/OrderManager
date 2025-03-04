if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# ===========================================================================================
from src.imports.config import DATE_FORMAT, DATE_KO_FORMAT
from src.imports.pyqt5_imports import QDate
from refactoring.docs.JsonManager import *
from refactoring.db.DBManager import *
from refactoring.docs.params import IPDocParam,IPDocItemParam
from pprint import pprint
# ===========================================================================================
class IPDoc(JsonManager):
    def __init__(self,dbm,p:IPDocParam):
        self.dbm =dbm
        self.p = p
        self.name = self._get_new_ip_name()
        self.file_path = f'./test/{self.name}.json'
        super().__init__(self.file_path)
        self.max_item_idx = self._get_max_item_idx()
        # self.file_path = f'./doc/ip/{self.name}.json'

        self.build_ip()
    # --------------------------
    @JsonManager.auto_save
    def build_ip(self):
        self.data['inputs'] = self.p.to_dict()
        self.data['loads'] = self._load_items()
        self.data['autos'] = self._build_autos()
    # -------------------------------------------------------------------------------------------

    def _get_max_item_idx(self):
        for i in range(1, 5):
            if not getattr(self.p,f'item{i}'):
                return i

    def _get_new_ip_name(self):
        last_ip_year,last_ip_no = self._get_last_ip_year_and_no_from_db()
        now_year =str(QDate.currentDate().year())
        if last_ip_year == now_year:
            new_ip_name = f"{last_ip_year}-IP{int(last_ip_no[2:])+1:04}"
        else:
            new_ip_name = f"{now_year}-IP{1:04}"
        return new_ip_name
    # -------------------------------------------------------------------------------------------

    def _load_items(self):
        items = {}
        for item_idx in range(1, self.max_item_idx):
            item_param = getattr(self.p,f'item{item_idx}')
            items[f'item{item_idx}'] = self.dbm.select_records_by_comparison('item','name',item_param.name)
        
        return items

    def _build_autos(self):
        autos = self._build_autos_from_loads()
        autos['name'] = self.name
        autos['due_date'] = QDate.fromString(self.p.due_date, DATE_FORMAT).toString(DATE_KO_FORMAT)
        autos['creation_date'] = QDate.currentDate().toString(DATE_KO_FORMAT)
        return autos

    # -------------------------------------------------------------------------------------------
    def _get_last_ip_year_and_no_from_db(self):
        try:
            [last_ip_name] = self.dbm.select_records(SelectParam('ip',['name'],sort=SortParam(),limit=1))
            last_ip_year,last_ip_no = last_ip_name[1].split('-')
        except ValueError:
            last_ip_year,last_ip_no = "2000","IP0000"
        return last_ip_year,last_ip_no
    
    def _build_autos_from_loads(self):
        self.component_name_amount_pairs = {}
        self.segments,self.shanks,self.submaterials = [],[],[]
        self._extract_component_details()
        return self._build_component_details()

    # -------------------------------------------------------------------------------------------
    def _extract_component_details(self):
        for item_idx in range(1,self.max_item_idx):
            item = self.data['loads'][f'item{item_idx}']
            item_amount = getattr(self.p,f'item{item_idx}').amount
            self._extract_component_name_amount_pairs(item,item_amount)

    def _build_component_details(self):
        autos = {}
        for component_type in ['segment','shank','submaterial']:
            autos.update(self._build_component_name_and_amount(component_type))
        return autos
    # -------------------------------------------------------------------------------------------
    def _extract_component_name_amount_pairs(self,item,item_amount):
        for key in ['segment1','segment2','shank','submaterial1','submaterial2','submaterial3','submaterial4']:
            component_name = item.get(f'{key}_name', None)
            component_amount = item.get(f'{key}_amount', 0) * item_amount
            if component_name in self.component_name_amount_pairs.keys():
                self.component_name_amount_pairs[component_name]+= component_amount
            else:
                self.component_name_amount_pairs[component_name] = component_amount
                getattr(self,''.join([x for x in key if not x.isdigit()])+'s').append(component_name)

    def _build_component_name_and_amount(self,component_type):
        autos = {}
        components = [x for x in getattr(self,f'{component_type}s') if x]
        for idx,component_name in enumerate(components,start=1):
            autos[f'{component_type}{idx}_name'] = component_name
            autos[f'{component_type}{idx}_amount'] = self.component_name_amount_pairs[component_name]
        return autos

    # ===========================================================================================


CREATE_ITEM_TABLE = '''CREATE TABLE item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    segment1_name TEXT REFERENCES segment(name),
    segment1_amount INTEGER,
    segment2_name TEXT REFERENCES segment(name),
    segment2_amount INTEGER,
    shank_name TEXT REFERENCES shank(name),
    shank_amount INTEGER,
    submaterial1_name TEXT REFERENCES submaterial(name),
    submaterial1_amount INTEGER,
    submaterial2_name TEXT REFERENCES submaterial(name),
    submaterial2_amount INTEGER
);'''

CREATE_IP_TABLE = '''CREATE TABLE ip (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);'''

def dbm():
    dbm = DBManager("./test.db")
    dbm.db.execute_query("DROP TABLE IF EXISTS item")
    dbm.db.execute_query("DROP TABLE IF EXISTS ip")
    dbm.db.execute_query(CREATE_ITEM_TABLE)
    dbm.db.execute_query(CREATE_IP_TABLE)
    dbm.insert_record(InsertParam("item", 
                                  {"name": "TEST-G1 A",
                                    "segment1_name": "SQTEST1",
                                    "segment1_amount": 3,
                                    "shank_name":"DBS-CCW",
                                    "shank_amount": 1,
                                    "submaterial1_name": "PCD10",
                                    "submaterial1_amount": 1
                                   }))
    dbm.insert_record(InsertParam("item", 
                                  {"name": "TEST-G2 A",
                                    "segment1_name": "SQTEST1",
                                    "segment1_amount": 1,
                                    "segment2_name": "SQTEST2",
                                    "segment2_amount": 2,
                                    "shank_name":"SQ948-CW",
                                    "shank_amount": 1,
                                    "submaterial1_name": "PCD10",
                                    "submaterial1_amount": 1,
                                    "submaterial2_name": "PCD12",
                                    "submaterial2_amount": 2,
                                   }))
    return dbm

if __name__ == '__main__':
    ipd = IPDoc(dbm(),IPDocParam(item1=IPDocItemParam("TEST-G1 A", 1)))
 