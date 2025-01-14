if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
from src.module.SqlliteInterface import SqlliteInterface

# Model
class Model():
    def __init__(self):
        super().__init__()  # QObject의 생성자 호출
        self.sql = SqlliteInterface()

    def insert_data(self,insert_request):
        print(__name__,insert_request)
        return insert_request

    def get_data_by_id(self,data_request):
        res = [(data_request[2],"mmm",32,"asd")]
        return self._add_response_header(data_request,res)

    def get_table_ids(self,id_request):
        res = [len(id_request[1]),2,3]
        return self._add_response_header(id_request,res)
    
    def get_all_table_items(self,table_request):
        col_names = self.get_table_col_names(table_request[1])
        query = f"SELECT * FROM {table_request[1]}"
        res = [col_names] + self.sql.execute_query(query)
        return self._add_response_header(table_request,res)

    def get_table_col_names(self,table_name):
        res = self.sql.execute_query(f"PRAGMA table_info({table_name})")
        return [column[1] for column in res]

    def _add_response_header(self,header,data):
        return header[:2]+(data,)