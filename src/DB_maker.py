if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------

import sqlite3
import json
from src.module.QueryBuilder import QueryBuilder
JSON_PATH = "./config/DB.json"

class DBMaker():
    def __init__(self,json_path:str=JSON_PATH,db_dir_path="./config/"):
        with open(json_path, 'r',encoding='UTF-8') as file:
            self.data = json.load(file)
        self.db_dir_path = db_dir_path
        self.cursor = None

    def create_table(self,table_name,table_options:dict):
        table_infos = []
        for k,v in table_options.items():
            table_infos.append(f''''{k}' {v}''')
        query = f'''CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(table_infos)});'''
        self.cursor.execute(query)

    def create_trigger(self,table_name,trigger_options:dict):
        for when,trigger_infos in trigger_options.items():
            query = f'''CREATE TRIGGER IF NOT EXISTS {trigger_infos['name']} {when} ON {table_name} BEGIN {trigger_infos['query']} END;'''
            self.cursor.execute(query)

    def insert_test_vals(self,table_name,test_vals:list):
        qb = QueryBuilder()
        for test_val in test_vals:
            query,bindings = qb.get_insert_query_with_bindings(table_name,test_val)
            self.cursor.execute(query,bindings)
        self.show_table(table_name)
        print('# ------------------------------------------')


    def show_table(self,table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    def make_db_file(self):
        for db_name in self.data:
            conn = sqlite3.connect(f'{self.db_dir_path}{db_name}.db')
            self.cursor = conn.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON;")

            for table_name,table_data in self.data[db_name].items():
                self.create_table(table_name,table_data["table"])
                self.create_trigger(table_name,table_data["trigger"])
                self.insert_test_vals(table_name,table_data["test_vals"])

            conn.commit()
            conn.close()


if __name__=="__main__":
    dbm = DBMaker()
    dbm.make_db_file()