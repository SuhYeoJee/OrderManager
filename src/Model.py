if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
from src.module.SqlliteInterface import SqlliteInterface
from src.module.QueryBuilder import QueryBuilder

# Model
class Model():
    def __init__(self):
        self.sql = SqlliteInterface()
        self.qb = QueryBuilder()

    def insert_data(self,insert_request):
        query = self.qb .get_insert_query(insert_request[1],insert_request[2])
        res = self.sql.execute_query(query)
        return self._add_response_header(insert_request,res)

    def get_data_by_id(self,data_request):
        query = self.qb .get_select_query(data_request[1],where_option={'comparison':[('id','=',data_request[2])]})
        res = self.sql.execute_query(query)
        return self._add_response_header(data_request,res)

    def get_table_ids(self,id_request):
        query = self.qb .get_select_query(id_request[1],['id'])
        res = [x[0] for x in self.sql.execute_query(query)]
        return self._add_response_header(id_request,res)
    
    def get_all_table_items(self,table_request):
        col_names = self.get_table_col_names(table_request[1])
        query = f"SELECT * FROM {table_request[1]}"
        res = [col_names] + self.sql.execute_query(query)
        return self._add_response_header(table_request,res)

    def get_table_col_names(self,table_name):
        res = self.sql.execute_query(f"PRAGMA table_info({table_name})")
        return [column[1] for column in res]

    def _add_response_header(self,request,data):
        return request[:2]+(data,)