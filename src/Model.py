if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
from src.module.SqlliteInterface import SqlliteInterface
from src.module.QueryBuilder import QueryBuilder
from src.module.IP_maker import IPMaker
from src.module.SP_maker import SPMaker
# --------------------------
import json
from datetime import datetime
from pprint import pprint
from src.imports.config import DB_PATH,ORDERS_TABLE_COLS
# ===========================================================================================
# Model
class Model():
    def __init__(self):
        self.sql = SqlliteInterface(DB_PATH)
        self.qb = QueryBuilder()
        self.ipm = IPMaker(self)
        self.spm = SPMaker(self)
        self.table_names = self.sql.get_table_names()

    def get_insert_data(self,insert_request):
        query,bindings = self.qb.get_insert_query(insert_request[1],insert_request[2])
        res = self.sql.execute_query(query,bindings)
        return self._add_response_header(insert_request,res)
    
    def get_orders_insert_request(self,insert_request):
        datas = insert_request[2]
        infos = {k:v for k,v in datas.items() if not isinstance(k,int)}
        infos['name']= self._get_new_order_name()

        i = 0
        while i in datas:
            self._handle_order_insert(datas[i],infos)
            i += 1
        return self._add_response_header(insert_request,True) 


    def _get_ip_inputs_from_orders_inputs(self,items,infos):
        ip_inputs =  {
            'infos': {
                "group": items.get('group', ''),
                "engrave": items.get('engrave', ''),
            },
            **{f'item{i}': {} if (f'item{i}' not in items or items.get(f'amount{i}', 0) == 0) 
                else {"item": items.get(f'item{i}', ''), "amount": items.get(f'amount{i}', 0), "code": items.get(f'code{i}', '')} 
                for i in range(1, 5)}
        }
        ip_inputs['infos'].update(infos)
        return ip_inputs


    def _get_new_order_name(self):
        try:
            [last_order] = self.sql.execute_query('SELECT * FROM orders ORDER BY id DESC LIMIT 1;')
            year,no = last_order[1].split('-')
        except ValueError:
            year,no = "2000","00000"
        if year == str(datetime.now().year):
            order_name = f"{year}-{int(no)+1:05}"
        else:
            order_name = f"{str(datetime.now().year)}-{1:05}"
        return order_name
    
    def _get_new_order_code(self):
        try:
            [last_order] = self.sql.execute_query('SELECT * FROM orders ORDER BY id DESC LIMIT 1;')
            code = int(last_order[2])+1 if last_order[1].split('-')[0] == str(datetime.now().year) else 1
        except ValueError:
            code = 1
        return code

    def _handle_order_insert(self, items, infos):
        ip_inputs = self._get_ip_inputs_from_orders_inputs(items, infos)
        if not any(ip_inputs.get(f'item{x}', {}) for x in range(1, 5)):
            return 
        ip = self.ipm.get_new_ip(ip_inputs)# ip 생성
        sps = self._create_and_insert_sps(ip)# sp 생성 및 삽입
        for idx,sp in enumerate(sps):
            ip['autos'][f'sp_{idx+1}'] = sp.get('autos', {}).get('name')
        else:
            self.ipm.write_json_file(ip,f"./doc/ip/{ip['autos']['name']}.json")
        self._insert_orders(items, infos, ip, sps)
        self._insert_ip(ip, sps)

    def _create_and_insert_sps(self, ip):
        sps = []
        for i in range(1, 3):
            seg_key = f"segment_{i}"
            if seg_key not in ip["autos"]:
                break
            sp = self.spm.get_new_sp({
                "name": ip["autos"].get(seg_key),
                "workload": ip["autos"].get(f"seg{i}_amount")
            })
            sps.append(sp)
            
            sp_data = {
                'name': sp.get('autos', {}).get('name'),
                'segment': sp.get('inputs', {}).get('name'),
                'ip': ip.get('autos', {}).get('name'),
                'path': f"./doc/sp/{sp.get('autos', {}).get('name', 'unknown')}.json"
            }
            self._execute_insert('sp', sp_data)
            self._execute_update('segment', {'sp_recent': sp_data['name']},
                                 {'comparison': [('name', '=', sp_data['segment'])]})
        return sps

    def _insert_orders(self, items, infos, ip, sps):
        for i in range(1, 5):
            if items.get(f'amount{i}', 0) == 0:
                break
            order = {
                "name": infos.get("name", ""),
                "code": self._get_new_order_code(),
                "customer": infos.get("customer", ""),
                "item": items.get(f"item{i}"),
                "group": items.get(f"item{i}", "").split(" ")[0] if items.get(f"item{i}") else None,
                "amount": items.get(f"amount{i}"),
                "engrave": items.get("engrave"),
                "order_date": infos.get("order_date"),
                "due_date": infos.get("due_date"),
                "description": infos.get("description"),
                "ip": ip.get("autos", {}).get("name"),
            }
            
            for j, sp in enumerate(sps[:2]):
                order.update({
                    f"segment_{j+1}": sp.get("inputs", {}).get("name"),
                    f"bond_{j+1}": sp.get("loads", {}).get("bond", {}).get("name"),
                    f"seg{j+1}_net": sp.get("inputs", {}).get("workload"),
                    f"seg{j+1}_work": sp.get("autos", {}).get("segment_work"),
                    f"sp_{j+1}": sp.get("autos", {}).get("name"),
                })
            
            self._execute_insert('orders', order)
            self._execute_update('item', {'ip_recent': ip.get('autos', {}).get('name')},
                                 {'comparison': [('name', '=', order['item'])]})
    
    def _insert_ip(self, ip, sps):
        ip_data = {
            'name': ip.get('autos', {}).get('name'),
            'group': ip.get('inputs', {}).get('infos', {}).get('group'),
            'sp_1': sps[0].get('autos', {}).get('name') if len(sps) > 0 else None,
            'sp_2': sps[1].get('autos', {}).get('name') if len(sps) > 1 else None,
            'path': f"./doc/ip/{ip.get('autos', {}).get('name', 'unknown')}.json"
        }
        self._execute_insert('ip', ip_data)

    def _execute_insert(self, table, data):
        query, bindings = self.qb.get_insert_query(table, data)
        self.sql.execute_query(query, bindings)
    
    def _execute_update(self, table, data, condition):
        query, bindings = self.qb.get_update_query(table, data, condition)
        self.sql.execute_query(query, bindings)

    # ===========================================================================================

    def get_json_data(self,json_request):
        table_name,json_path = json_request[1],json_request[2]
        res = self._read_json_file(json_path)
        return self._add_response_header(json_request,res)

    def _read_json_file(SELF,json_path):
        with open(json_path, 'r',encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data
    
    def get_delete_data(self,delete_request):
        query,bindings = self.qb.get_delete_query(delete_request[1],where_option={'comparison':[('id','=',delete_request[2]['id'])]})
        res = self.sql.execute_query(query,bindings)
        return self._add_response_header(delete_request,res)
    
    def get_update_data(self,update_request):
        id_val = update_request[2].pop('id')
        query,bindings = self.qb.get_update_query(update_request[1],update_request[2],where_option={'comparison':[('id','=',id_val)]})
        res = self.sql.execute_query(query,bindings)
        return self._add_response_header(update_request,res)
    
    def get_select_data(self,select_request):
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
            else:
                where_option = {}
        
            query,bindings = self.qb.get_select_query(select_request[1],where_option=where_option,sort_option=select_request[2])
            res = [col_names] + self.sql.execute_query(query,bindings)
        except Exception as e: # 올바르지 않은 검색 쿼리
            res = [('error',)] + [('올바르지 않은 검색 쿼리.',),(e.__str__(),),(e.__doc__,)]

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
        if table_request[0] == "ordersTable":
            col_names = ORDERS_TABLE_COLS
            query,bindings = self.qb.get_select_query('orders',col_names,{'isnull':[('shipping_date',True)]},('code','오름차순'))
        else:
            col_names = self.get_table_col_names(table_request[1])
            query,bindings = f"SELECT * FROM {table_request[1]}",[]
        res = [col_names] + self.sql.execute_query(query,bindings)
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
    