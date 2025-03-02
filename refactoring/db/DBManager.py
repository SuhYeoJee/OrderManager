from refactoring.db.SqliteDB import SqliteDB
from refactoring.db.SqliteQueryBuilder import SqliteQueryBuilder
from refactoring.db.params import *
from config import DB_PATH

class DBManager():
    def __init__(self):
        self.db = SqliteDB(DB_PATH)
        self.qb = SqliteQueryBuilder()
    # [CRUD] ===========================================================================================
    def insert_record(self,params:InsertParams):
        return self._execute_crud('insert',params)
    
    def select_records(self,params:SelectParams):
        return self._execute_crud('select',params)
    
    def update_record(self,params:UpdateParams):
        return self._execute_crud('update',params)
    
    def delete_record(self,params:DeleteParams):
        operation = 'delete' if params.where else 'delete_by_column_value_pairs_query'
        return self._execute_crud(operation,params)
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
        table_names = self._extract_fields_by_index(result)
        return table_names 
    
    def get_table_ids(self,table_name):
        SelectParams(
            table_name=table_name,
            columns='id',
        )
        result = self.select_records(SelectParams)
        ids = self._extract_fields_by_index(result)
        return ids
    
    def get_table_col_names(self,table_name):
        query = self.qb.get_table_info_query(table_name)
        result = self.db.execute_query(query)
        col_names = self._extract_fields_by_index(result,1)
        return col_names
    
    def get_table_col_type(self,table_name,col_name):
        query = self.qb.get_table_info_query(table_name)
        result = self.db.execute_query(query)
        return next((col[2] for col in result if col[1] == col_name), None)


    def select_records_by_comparison(self,table_name,column_name,value):
        SelectParams(
            table_name=table_name,
            where={'comparison':[(column_name,'=',value)]}
        )
        return self.select_records(SelectParams)

    # -------------------------------------------------------------------------------------------
    def _extract_fields_by_index(self,records,index:int=0):
        return [record[index] for record in records]
    