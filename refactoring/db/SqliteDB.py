import sqlite3
import threading

class SqliteDB():
    def __init__(self,db_path:str='mydatabase.db'):
        self.db_path = db_path
        self.local = threading.local()
    # -------------------------------------------------------------------------------------------
    def ensure_connect(func):
        def wrapper(self, *args, **kwargs):
            self.local.connect = sqlite3.connect(self.db_path)
            self.local.cursor = self.local.connect.cursor()
            self.local.cursor.row_factory = sqlite3.Row 
            result = func(self, *args, **kwargs)
            self.local.connect.commit()
            self.local.connect.close()
            return result
        return wrapper
    
    @ensure_connect
    def execute_query(self,query,bindings:list=[]):
        try:
            self.local.cursor.execute(query,bindings)
            rows = self.local.cursor.fetchall()
            result = [dict(row) for row in rows] 
        except Exception as e:
            result = [{'DB error':e.__str__()}]
        print('# ------------------------------------------')
        print(query,bindings)
        print(result)
        return result
    
# ===========================================================================================
if __name__ == '__main__':
    sqli = SqliteDB()
    sqli.execute_query('SELECT id FROM users')
    # sqli.execute_query("INSERT INTO users (name, age, city) VALUES ('Bob', '25', 'Busan')")
    # sqli.execute_query('SELECT * FROM users')