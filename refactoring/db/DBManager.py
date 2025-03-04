from refactoring.db.SqliteDB import SqliteDB
from refactoring.db.params import InsertParam,SelectParam,UpdateParam,DeleteParam,WhereParam,SortParam
from refactoring.db.SqliteQueryBuilder import SqliteQueryBuilder

from config import DB_PATH

class DBManager():
    def __init__(self, db_path:str=None):
        self.db = SqliteDB(db_path if db_path else DB_PATH)
        self.qb = SqliteQueryBuilder()
    # [CRUD] ===========================================================================================
    def insert_record(self,params:InsertParam):
        return self._execute_crud('insert',params)
    
    def select_records(self,params:SelectParam):
        return self._execute_crud('select',params)
    
    def update_record(self,params:UpdateParam):
        return self._execute_crud('update',params)
    
    def delete_record(self,params:DeleteParam):
        return self._execute_crud('delete',params)
    # -------------------------------------------------------------------------------------------
    def _execute_crud(self,operation,params):
        qb_func = getattr(self.qb,f"build_{operation}_query")
        query,bindings = qb_func(params)
        result = self.db.execute_query(query,bindings)
        return result
    # ===========================================================================================
    def get_table_names(self):
        query = self.qb.get_select_table_name_query()
        result = self.db.execute_query(query)
        table_names = self._extract_fields_by_key(result,'name')
        return table_names 
    
    def get_table_ids(self,table_name):
        p = SelectParam(
            table_name=table_name,
            columns=['id'],
        )
        result = self.select_records(p)
        ids = self._extract_fields_by_key(result,'id')
        return ids
    
    def get_table_col_names(self,table_name):
        query = self.qb.get_table_info_query(table_name)
        result = self.db.execute_query(query)
        col_names = self._extract_fields_by_key(result,'name')
        return col_names
    
    def get_table_col_type(self,table_name,col_name):
        query = self.qb.get_table_info_query(table_name)
        result = self.db.execute_query(query)
        return next((col['type'] for col in result if col['name'] == col_name), None)

    def select_records_by_comparison(self,table_name,column_name,value):
        p = SelectParam(
            table_name=table_name,
            where=WhereParam([(column_name,'=',value)])
        )
        return self.select_records(p)

    # -------------------------------------------------------------------------------------------
    def _extract_fields_by_key(self,records,key:str):
        return [record[key] for record in records]
    