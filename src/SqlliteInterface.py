import sqlite3

class SqlliteInterface():
    def __init__(self,db_path:str='mydatabase.db'):
        self.connect = sqlite3.connect(db_path)
        self.cursor = self.connect.cursor()
    # --------------------------
    def __del__(self):
        self.connect.commit()
        self.connect.close()
    # -------------------------------------------------------------------------------------------
    def save_after(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.connect.commit()
            return result
        return wrapper
    

    def get_table_names(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        return [table[0] for table in tables]

    @save_after
    def execute_query(self,query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        print(rows)
        return rows
    
# ===========================================================================================
if __name__ == '__main__':
    sqli = SqlliteInterface()
    sqli.execute_query('SELECT * FROM users')
    sqli.execute_query("INSERT INTO users (name, age, city) VALUES ('Bob', '25', 'Busan')")
    sqli.execute_query('SELECT * FROM users')