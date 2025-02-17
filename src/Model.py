if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
from src.module.SqlliteInterface import SqlliteInterface
from src.module.QueryBuilder import QueryBuilder
from src.module.IP_maker import IPMaker
from src.module.SP_maker import SPMaker
# --------------------------
DB_PATH='./config/NOVA.db'
# ===========================================================================================
# Model
class Model():
    def __init__(self):
        self.sql = SqlliteInterface(DB_PATH)
        self.qb = QueryBuilder()
        self.ipm = IPMaker(self)
        self.spm = SPMaker(self)
        self.table_names = self.sql.get_table_names()

    def insert_data(self,insert_request):
        table_name,items = insert_request[1],insert_request[2]
        if table_name == "orders":
            res = self._handle_order_insert(items)
        else:
            query,bindings = self.qb.get_insert_query(table_name,items)
            res = self.sql.execute_query(query,bindings)
        return self._add_response_header(insert_request,res)
    
    def _handle_order_insert(self,items):
        # ip생성
        ip_inputs = {k: items[k] for k in self.ipm.inputs if k in items}
        ip = self.ipm.get_new_ip(ip_inputs)
        items.update({'ip':ip['autos']['name']}) #order 갱신 

        # sp생성
        sps=[]
        for i in [1,2]:
            sp_inputs = {f"segment":ip["autos"][f"seg{i}"],"segment_net":ip["autos"][f"seg{i}_net"]}
            sps.append(self.spm.get_new_sp(sp_inputs))
            items.update({f'sp{i}':sps[i-1]['autos']['name']}) #order 갱신 

        self.ouputs = ["bond","segment_work","sp"]
        # 새로 생긴 ip DB에 저장
        ip_items = {'name','item_group','sp','path'}
        sp_items = {'name','segment','ip','path'}
        query,bindings = self.qb.get_insert_query('ip',ip_items)
        res = self.sql.execute_query(query,bindings)

        # order DB에 저장
        query,bindings = self.qb.get_insert_query('orders',items)
        res = self.sql.execute_query(query,bindings)
        return res







    def delete_data(self,delete_request):
        query,bindings = self.qb.get_delete_query(delete_request[1],where_option={'comparison':[('id','=',delete_request[2]['id'])]})
        res = self.sql.execute_query(query,bindings)
        return self._add_response_header(delete_request,res)
    
    def update_data(self,update_request):
        id_val = update_request[2].pop('id')
        query,bindings = self.qb.get_update_query(update_request[1],update_request[2],where_option={'comparison':[('id','=',id_val)]})
        res = self.sql.execute_query(query,bindings)
        return self._add_response_header(update_request,res)
    
    def select_data(self,select_request):
        # ('select',table_name,(sort_col,sort_type),(select_col,select_type,select_str))
        col_names = self.get_table_col_names(select_request[1])
        select_col,select_type,select_str = select_request[3]

        try:

            if select_type in ['>','<','>=','<=','=','!=']:
                col_type = self.get_table_col_type(select_request[1],select_col)
                if col_type == "INTEGER":
                    where_val = int(select_str)
                elif col_type == "REAL":
                    where_val = float(select_str)
                else:
                    where_val = str(select_str)
                where_option = {'comparison':[(select_col,select_type,where_val)]}
                
            elif select_type in ['IN']:
                where_val = [x.strip() for x in select_str.split(',')]
                where_option = {'inlist':[(select_col,where_val)]}

            elif select_type in ['LIKE']:
                where_option = {'likepattern':[(select_col,select_str)]}

            elif select_type in ['부재']:
                where_option = {'isnull':[(select_col,True)]}

            elif select_type in ['존재']:
                where_option = {'isnull':[(select_col,False)]}

            query,bindings = self.qb.get_select_query(select_request[1],where_option=where_option,sort_option=select_request[2])
            res = [col_names] + self.sql.execute_query(query,bindings)
        except Exception as e: # 올바르지 않은 검색 쿼리
            res = [('오류',)] + [('올바르지 않은 검색 쿼리.',),(e.__str__(),),(e.__doc__,)]

        return self._add_response_header(select_request,res)

    def get_data_by_id(self,data_request):
        query,bindings = self.qb.get_select_query(data_request[1],where_option={'comparison':[('id','=',data_request[2])]})
        res = self.sql.execute_query(query,bindings)
        return self._add_response_header(data_request,res)

    def get_table_ids(self,table_name):
        query,bindings = self.qb.get_select_query(table_name,['id'])
        res = [x[0] for x in self.sql.execute_query(query,bindings)]
        return res
    
    def get_all_table_items(self,table_request):
        col_names = self.get_table_col_names(table_request[1])
        query = f"SELECT * FROM {table_request[1]}"
        res = [col_names] + self.sql.execute_query(query)
        return self._add_response_header(table_request,res)

    def get_table_col_names(self,table_name):
        res = self.sql.execute_query(f"PRAGMA table_info({table_name})")
        return [column[1] for column in res]
    
    def get_table_col_type(self,table_name,col_name):
        res = self.sql.execute_query(f"PRAGMA table_info({table_name})")
        return next((col[2] for col in res if col[1] == col_name), None)

    def get_foreign_key_values(self, table_name)->dict:
        '''
        외래키 제약조건에서 사용 가능한 값을 반환. 
        조건이 없으면 None, 사용 가능한 항목이 없으면 빈 리스트 반환.
        결과는 {col_name: [val1, val2, ...]} 형태의 딕셔너리.
        '''
        res = self.sql.execute_query(f"PRAGMA foreign_key_list({table_name})")
        if not res:
            return None

        result = {}
        for fk in res:
            ref_table,col_name,ref_col = fk[2:5]
            query = f'SELECT DISTINCT "{ref_col}" FROM "{ref_table}"'
            ref_values = self.sql.execute_query(query)
            result[col_name] = [x[0] for x in ref_values] if ref_values else []
        return result if result else None

    def get_pre_infos(self,pre_request):
        '''다이얼로그 사전정보: 전체 cols,테이블에 존재하는 id목록, 외래키 제약'''
        table_name = pre_request[1]
        cols = self.get_table_col_names(table_name)
        ids = self.get_table_ids(table_name)
        fks = self.get_foreign_key_values(table_name)
        return self._add_response_header(pre_request,(cols,ids,fks))

    def _add_response_header(self,request,data):
        return request[:2]+(data,)