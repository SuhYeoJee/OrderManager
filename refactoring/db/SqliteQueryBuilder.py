
import re
from itertools import chain # 리스트 평탄화
from refactoring.utils.SafeList import SafeList
from refactoring.db.params import InsertParam,SelectParam,UpdateParam,DeleteParam,WhereParam,SortParam

class SqliteQueryBuilder():
    def __init__(self):...
    # -------------------------------------------------------------------------------------------
    def get_select_table_name_query(self)->str:
        return '''SELECT name FROM sqlite_master WHERE type='table';'''
    
    def get_table_info_query(self,table_name:str)->str:
        return f"PRAGMA table_info({table_name})"

    # --------------------------
    def build_insert_query(self,p:InsertParam):
        '''INSERT INTO 테이블명 (키1, 키2, ...) VALUES (?,?,...);, (값1,값2,...)'''
        column_value_pairs = p.get_filtered_column_value_pairs()
        bindings = SafeList(column_value_pairs.values())
        return f'''INSERT INTO "{p.table_name}" ({",".join([f'"{column}"' for column in column_value_pairs.keys()])}) VALUES ({",".join(['?']*len(bindings))});''',bindings
    # --------------------------
    def build_select_query(self,p:SelectParam):
        '''SELECT col1, col2 ... FROM 테이블명 WHERE 조건 ORDER BY col ASC/DESC LIMIT 값;,bindings'''
        where_clause,where_bindings = self._build_where_clause(p.where)
        sort_clause = self._build_sort_clause(p.sort)
        limit_clause = self._build_limit_clause(p.limit)
        clauses = (" "+ clauses) if (clauses:=" ".join([c for c in [where_clause,sort_clause,limit_clause] if c])) else ''
        return f'''SELECT {",".join([f'"{x}"' for x in p.columns]) if p.columns else "*"} FROM "{p.table_name}"{clauses};''',where_bindings
    # --------------------------
    def build_update_query(self,p:UpdateParam):
        '''UPDATE 테이블명 SET 키1 = 값1, 키2 = 값2 ... WHERE 조건;,bindings'''
        column_value_pairs = p.get_filtered_column_value_pairs()
        where_clause,where_bindings = self._build_where_clause(p.where) if p.where else ('',SafeList())
        bindings = SafeList(column_value_pairs.values()) + where_bindings
        clauses= " "+where_clause if where_clause else ""
        return f'''UPDATE "{p.table_name}" SET {','.join([f'''"{column}" = ?''' for column in column_value_pairs.keys()])}{clauses};''',bindings
    # --------------------------
    def build_delete_query(self,p:DeleteParam):
        '''DELETE FROM 테이블명 WHERE 조건'''
        if p.where:
            where_clause,where_bindings = self._build_where_clause(p.where)
        else:
            column_value_pairs = p.get_filtered_column_value_pairs()
            sub_where_clause = 'WHERE ' + " AND ".join([f'''"{column}" = ?''' for column in column_value_pairs.keys()])
            where_bindings = SafeList(column_value_pairs.values())
            where_clause = f'''WHERE id = (SELECT MAX(id) FROM {p.table_name} {sub_where_clause})''' # 중복이 있으면 id가 가장 큰 것을 삭제
        clauses= " "+where_clause if where_clause else ""
        return f'''DELETE FROM "{p.table_name}"{clauses};''',where_bindings
    # ===========================================================================================
    def _build_limit_clause(self,limit:int=None)->str:
        return f'''LIMIT {limit}''' if limit else ''
    def _build_sort_clause(self,p:SortParam)->str:
        '''sort절 작성: sort:{column_name:str, is_desc:bool}'''
        if p:
            sort_clause = f'''ORDER BY "{p.column_name}" {"DESC" if p.is_desc else "ASC"}'''
        else:
            sort_clause = ''
        return sort_clause
    # --------------------------
    def _build_where_clause(self,p:WhereParam)->str:
        '''
        조건식 논리를 스트링으로 입력 (기본: AND 연결)
        논리: AND, OR, NOT
        logic = '{comparison[0]} AND {comparison[1]} OR NOT {between[0]}'
        '''
        if p :
            conditions = {}
            for condition_type,options in p.get_conditions().items():
                conditions[f'{condition_type}s'], conditions[f'{condition_type}_bindings'] \
                    = getattr(self, f'_build_{condition_type}_clause')(options)

            where_clause, bindings = self._combine_where_clauses(conditions,p.logic)
        else:
            where_clause, bindings = '',[]

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
                bindings.extend(SafeList(chain.from_iterable(val)) if isinstance(val[0], list) else val)
            else:
                where_clause += ' AND '.join(val)
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
        bindings = SafeList()
        for condition_name in condition_names:
            if binding_value:= self._extract_binding_value(conditions,condition_name):
                if isinstance(binding_value,list):
                    bindings.extend(binding_value)
                else:
                    bindings.append(binding_value)
        return bindings
    # -------------------------------------------------------------------------------------------
    def _extract_binding_value(self,conditions,condition_name):
        '''logic 포맷 문으로 조건 binding값 반환'''
        condition_key,index = condition_name.split('[')
        index = int(index.rstrip(']'))
        binding_key = condition_key[:-1]+"_bindings"
        binding_value = conditions.get(binding_key,SafeList()).safe_get(index)
        return binding_value
    # --------------------------
    def _build_comparison_clause(self,options:list):
        '''비교연산자 where절 작성'''
        comparisons,bindings = SafeList(),SafeList()
        for option in options: # option:(열이름, 연산자, 값)
            col,op,val = option
            comparisons.append(f'''"{col}" {op} ?''')
            bindings.append(val)
        return comparisons,bindings
    
    def _build_between_clause(self,options:list):
        betweens,bindings = SafeList(),SafeList()
        for option in options: # option:(열이름, 시작값, 끝값)
            col,start,end = option
            betweens.append(f'''"{col}" BETWEEN ? AND ?''')
            bindings.append([start,end])
        return betweens,bindings
    
    def _build_inlist_clause(self,options:list):
        inlists,bindings = SafeList(),SafeList()
        for option in options: # option:(열이름, 리스트:list)
            col,vals = option
            inlists.append(f'''"{col}" IN ({','.join(['?']*len(vals))})''')
            bindings.append(vals)
        return inlists,bindings
    
    def _build_like_clause(self,options:list):
        likes,bindings = SafeList(),SafeList()
        for option in options: # option:(열이름, 패턴:str)
            col,pattern = option
            likes.append(f'''"{col}" LIKE ?''')
            bindings.append(pattern)
        return likes,bindings
    
    def _build_isnull_clause(self,options:list):
        isnulls,bindings = SafeList(),SafeList()
        for option in options: # option:(열이름, is_null:bool)
            col,flag = option
            isnulls.append(f'''"{col}" IS {'' if flag else 'NOT '}NULL''')
        return isnulls,bindings
