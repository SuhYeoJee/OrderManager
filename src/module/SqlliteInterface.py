import sqlite3

class SqlliteInterface():
    def __init__(self,db_path:str='mydatabase.db'):
        self.db_path = db_path
        self.connect = None
        self.cursor = None
    # -------------------------------------------------------------------------------------------
    def ensure_connect(func):
        def wrapper(self, *args, **kwargs):
            self.connect = sqlite3.connect(self.db_path)
            self.cursor = self.connect.cursor()
            result = func(self, *args, **kwargs)
            self.connect.commit()
            self.connect.close()
            return result
        return wrapper
    
    @ensure_connect
    def get_table_names(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        return [table[0] for table in tables]

    @ensure_connect
    def execute_query(self,query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        print('# ------------------------------------------')
        print(query)
        print(rows)
        print('# ------------------------------------------')
        return rows
    
# ===========================================================================================
if __name__ == '__main__':
    sqli = SqlliteInterface()
    sqli.execute_query('SELECT id FROM users')
    # sqli.execute_query("INSERT INTO users (name, age, city) VALUES ('Bob', '25', 'Busan')")
    # sqli.execute_query('SELECT * FROM users')