import sqlite3
import json

def export_sqlite_metadata(db_path, output_file):
    """
    SQLite DB에 존재하는 모든 테이블과 트리거 정보를 JSON 파일로 저장
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 테이블 정보 가져오기
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
    tables = {}
    for name, sql in cursor.fetchall():
        cursor.execute(f"PRAGMA table_info({name})")
        columns = {col[1]: col[2] for col in cursor.fetchall()}
        tables[name] = {"columns": columns}
    
    # 트리거 정보 가져오기
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='trigger'")
    triggers = {}
    for name, sql in cursor.fetchall():
        cursor.execute(f"SELECT type FROM sqlite_master WHERE name='{name}'")
        trigger_type = "AFTER UPDATE" if "AFTER UPDATE" in sql else "UNKNOWN"
        triggers[name] = {"type": trigger_type, "query": sql}
    
    # JSON 데이터 생성
    metadata = {"segment": {"table": tables, "trigger": triggers}}
    
    # JSON 파일 저장
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    
    conn.close()

export_sqlite_metadata("./config/NOVA.db", "./doc/db_schema.json")
