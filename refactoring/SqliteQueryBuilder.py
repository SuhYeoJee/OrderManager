
import re
from src.imports.config import DEFAULT_VALS
from itertools import chain # 리스트 평탄화


def safe_get(lst:list, index:int, default=None):
    """인덱스 오류 회피"""
    result = lst[index] if 0 <= index < len(lst) else default
    return result

class SqliteQueryBuilder():
    def __init__(self):...
    # --------------------------
    def build_insert_query(self,table_name:str,column_value_pairs:dict):
        '''INSERT INTO 테이블명 (키1, 키2, ...) VALUES (?,?,...);, (값1,값2,...)'''
        column_value_pairs = self._remove_invalid_values(column_value_pairs)
        bindings = list(item.values())
        return f'''INSERT INTO "{table_name}" ({",".join([f'"{column}"' for column in column_value_pairs.keys()])}) VALUES ({",".join(['?']*len(bindings))});''',bindings
    # --------------------------
    def build_select_query(self,table_name:str,columns:list=[],where:dict={},sort:tuple=('id','오름차순')):
        '''SELECT col1, col2 ... FROM 테이블명 WHERE 조건 ORDER BY col ASC/DESC;,bindings'''
        where_clause,where_bindings = self._build_where_clause(where) if where else ('',[])
        sort_clause = self._build_sort_clause(sort)
        return f'''SELECT {",".join([f'"{x}"' for x in columns]) if columns else "*"} FROM "{table_name}" {where_clause} {sort_clause};''',where_bindings
    # --------------------------
    def build_update_query(self,table_name:str,column_value_pairs:dict,where:dict={}):
        '''UPDATE 테이블명 SET 키1 = 값1, 키2 = 값2 ... WHERE 조건;,bindings'''
        column_value_pairs = self._remove_invalid_values(column_value_pairs)
        where_clause,where_bindings = self._build_where_clause(where) if where else ('',[])
        bindings = list(column_value_pairs.values()) + where_bindings
        return f'''UPDATE "{table_name}" SET {','.join([f'''"{column}" = ?''' for column in column_value_pairs.keys()])} {where_clause};''',bindings
    # --------------------------
    def build_delete_query(self,table_name:str,where:dict={}):
        '''DELETE FROM 테이블명 WHERE 조건'''
        where_clause,where_bindings = self._build_where_clause(where) if where else ('',[])
        return f'''DELETE FROM "{table_name}" {where_clause};''',where_bindings
    # --------------------------
    def build_delete_query_by_column_value_pairs(self,table_name:str,column_value_pairs:dict):
        '''DELETE FROM 테이블명 WHERE 조건 - column_value_pairs 일치하는 항목 삭제'''
        column_value_pairs = self._remove_invalid_values(column_value_pairs)
        sub_where_clause = 'WHERE ' + " AND ".join([f'''"{column}" = ?''' for column in column_value_pairs.keys()])
        bindings = list(column_value_pairs.values())
        where_str = f'''WHERE id = (SELECT MAX(id) FROM {table_name} {sub_where_clause})''' # 중복이 있으면 id가 가장 큰 것을 삭제
        return f'''DELETE FROM "{table_name}" {where_str};''',bindings
    # -------------------------------------------------------------------------------------------
    @staticmethod
    def _build_sort_clause(sort:tuple)->str:
        '''sort절 작성: sort:{column_name:str, is_desc:bool}'''
        sort_clause = f'''ORDER BY {safe_get(sort,0)} {"DESC" if safe_get(sort,1) else "ASC"}'''
        return sort_clause
    # --------------------------
    def _build_where_clause(self,where:dict)->str:
        '''
        comparison: >,<,=,!=,>=,<=
            [(컬럼,연산자,값)]
        between: BETWEEN ... AND ...
            [(컬럼,시작값,끝값)]
        inlist: IN (...)
            [(컬럼,[목록])]
        likepattern: LIKE
            [(컬럼,패턴)]
        isnull: IS NULL / IS NOT NULL
            [(컬럼,True(값 부재)),(컬럼,False(값 존재))]

        조건식 논리를 스트링으로 입력 (기본: AND 연결)
        논리: AND, OR, NOT
        logic = '{comparison[0]} AND {comparison[1]} OR NOT {between[0]}'
        '''
        logic = where.pop('logic',None)

        conditions = {}
        for key,val in where.items():
            conditions[f'{key}s'], conditions[f'{key}_bindings'] = getattr(self, f'_build_{key}_clause')(val)

        where_clause, bindings = self._combine_where_clauses(conditions,logic)

        return where_clause, bindings
    # -------------------------------------------------------------------------------------------
    def _combine_where_clauses(self,conditions,logic):
        '''옵션을 결합해서 반환'''
        if logic:
            where_clause, bindings = self._combine_where_with_logic(conditions,logic)
        else:
            where_clause, bindings = self._combine_where_with_and(conditions)
        return where_clause, bindings
    # -------------------------------------------------------------------------------------------
    def _combine_where_with_and(self,conditions):
        '''모든 조건을 AND로 결합'''
        where_clause = 'WHERE '
        bindings = []
        for key,val in conditions.items():
            if 'bindings' in key:
                bindings.extend(list(chain.from_iterable(val)) if isinstance(val[0], list) else val)
            else:
                where_clause += ' AND '.join([val for key,val in conditions.items() if 'bindings' not in key])
        return where_clause, bindings
    # --------------------------
    def _combine_where_with_logic(self,conditions,logic):
        '''모든 조건을 format str에 맞게 결합'''
        where_clause = 'WHERE ' +  logic.format(**conditions)
        bindings = self._extract_bindings(conditions,logic)
        return where_clause, bindings
    # -------------------------------------------------------------------------------------------
    def _extract_bindings(self,conditions,logic):
        '''format str 순서로 bindings 추출'''
        condition_names = re.findall(r'\{(.*?)\}', logic)
        bindings = []
        for condition_name in condition_names:
            condition_key,index = condition_name.split('[')
            index = int(index.rstrip(']'))
            if isinstance(condition:= conditions[condition_key][index],list):
                bindings.extend(condition)
            else:
                bindings.append(condition)
        return bindings
    # -------------------------------------------------------------------------------------------
    @staticmethod
    def _build_comparison_clause(options:list):
        '''비교연산자 where절 작성'''
        comparisons = bindings = []
        for option in options: # option:(열이름, 연산자, 값)
            col,op,val = option
            comparisons.append(f'''"{col}" {op} ?''')
            bindings.append(val)
        return comparisons,bindings
    
    @staticmethod
    def _build_between_clause(options:list):
        betweens = bindings = []
        for option in options: # option:(열이름, 시작값, 끝값)
            col,start,end = option
            betweens.append(f'''"{col}" BETWEEN ? AND ?''')
            bindings.append([start,end])
        return betweens,bindings
    
    @staticmethod
    def _build_inlist_clause(options:list):
        inlists = bindings = []
        for option in options: # option:(열이름, 리스트:list)
            col,vals = option
            inlists.append(f'''"{col}" IN ({','.join(['?']*len(vals))})''')
            bindings.append(vals)
        return inlists,bindings
    
    @staticmethod
    def _build_like_clause(options:list):
        likes = bindings = []
        for option in options: # option:(열이름, 패턴:str)
            col,pattern = option
            likes.append(f'''"{col}" LIKE ?''')
            bindings.append(pattern)
        return likes,bindings
    
    @staticmethod
    def _build_isnull_clause(options:list):
        isnulls = bindings = []
        for option in options: # option:(열이름, is_null:bool)
            col,flag = option
            isnulls.append(f'''"{col}" IS {'' if flag else 'NOT'} NULL''')
        return isnulls,bindings
    # -------------------------------------------------------------------------------------------
    def _remove_invalid_values(self,d: dict) -> dict:
        '''무효값/기본값 키:값쌍 제거'''
        return {k: v for k, v in d.items() if v not in DEFAULT_VALS}

# ===========================================================================================
if __name__ == '__main__':
    sqb = SqliteQueryBuilder()
    # res = qb._get_where_str(comparison=[('col1','<',13),('col2','=',13)],between=[('col3',13,39),('col4',1,300)],inlist=[('col5',[1,2,3,43])],likepattern=[('col6','%afse%')],isnull=[('col7',True),('col8',False)], \
    #                         logic_str='{comparison[0]} AND {comparison[1]} OR {between[0]} AND NOT {between[1]} AND {inlist[0]} OR {likepattern[0]} AND {isnull[0]} AND {isnull[1]}')
    # print(res)
    # res = qb.get_insert_query('users',{'name':'Tom','age':23,'city':'Seoul'})
    # print(res)
    # res = qb.get_select_query('users',['name','city'],{'comparison':[('age','>=',25)]})
    # print(res)
    # res = qb.get_update_query('users',{'name':'Tom','age':23},{'likepattern':[('city','S%')]})
    # print(res)
    # res = qb.get_delete_query('users',{'comparison':[('name','=','Tom')]})
    # print(res)
    # res = qb.get_delete_query_by_item('users',{'name':'Tom','city':'busan','age':24})
    # print(res)

