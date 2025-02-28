import sqlite3
import threading

class SqlliteDB():
    def __init__(self,db_path:str='mydatabase.db'):
        self.db_path = db_path
        self.local = threading.local()
    # -------------------------------------------------------------------------------------------
    def ensure_connect(func):
        def wrapper(self, *args, **kwargs):
            self.local.connect = sqlite3.connect(self.db_path)
            self.local.cursor = self.local.connect.cursor()
            result = func(self, *args, **kwargs)
            self.local.connect.commit()
            self.local.connect.close()
            return result
        return wrapper
    
    @ensure_connect
    # 삭제
    def get_table_names(self):
        self.local.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        res = [table[0] for table in self.local.cursor.fetchall()]
        res.remove("sqlite_sequence")
        return res 

    @ensure_connect
    def execute_query(self,query,bindings:list=[]):
        try:
            self.local.cursor.execute(query,bindings)
            rows = self.local.cursor.fetchall()
        except Exception as e:
            rows = [('DB error',e.__str__())]
        print('# ------------------------------------------')
        print(query,bindings)
        print(rows)
        return rows
    
# ===========================================================================================
if __name__ == '__main__':
    sqli = SqlliteDB()
    sqli.execute_query('SELECT id FROM users')
    # sqli.execute_query("INSERT INTO users (name, age, city) VALUES ('Bob', '25', 'Busan')")
    # sqli.execute_query('SELECT * FROM users')