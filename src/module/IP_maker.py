if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# ===========================================================================================
from src.imports.config import DATE_FORMAT, DATE_KO_FORMAT
from src.imports.pyqt5_imports import QDate
import json
from pprint import pprint
# ===========================================================================================
class IPMaker():
    def __init__(self,model):
        self.model = model

    def get_new_ip(self,inputs):
        ip = self._make_new_ip(inputs)
        self.write_json_file(ip,f"./doc/ip/{ip['autos']['name']}.json")
        return ip

    def get_new_ip_name(self):
        try:
            [last_ip] = self.model.sql.execute_query('SELECT * FROM ip ORDER BY id DESC LIMIT 1;')
            year,no = last_ip[1].split('-')
        except ValueError:
            year,no = "2000","IP0000"

        now_year =str(QDate.currentDate().year())
        if year == now_year:
            ip_name = f"{year}-IP{int(no[2:])+1:04}"
        else:
            ip_name = f"{now_year}-IP{1:04}"
        return ip_name
    
    def get_data_by_name(self,table_name,name):
        request = ('select',table_name,('id','오름차순'),('name','=',name))
        response = self.model.get_select_data(request)
        try:
            res = dict(zip(response[2][0],response[2][1]))
        except IndexError:
            # 해당 데이터 없음
            res = dict(zip(response[2][0],['']*len(response[2][0])))
        return res
 
    def _make_new_ip(self,inputs:dict):
        ip = {}
        ip['inputs'] = inputs
        # --------------------------
        ip['loads'] = {}
        for i in range(1, 5):
            item_key = f'item{i}'
            if ip['inputs'].get(item_key, {}).get('item') is not None:
                ip['loads'][item_key] = self.get_data_by_name('item', ip['inputs'][item_key]['item'])
        # --------------------------
        ip['autos'] = {}
        ip['autos']['name'] = self.get_new_ip_name()
        ip['autos']['creation_date'] = QDate.currentDate().toString(DATE_KO_FORMAT)
        ip['autos']['due_date'] = QDate.fromString("2000-01-01", DATE_FORMAT).toString(DATE_KO_FORMAT)
        ip['autos'].update(self._get_autos_from_loads(ip))
        
        # --------------------------
        pprint(ip)
        return ip
        
    def _get_autos_from_loads(self, ip):
        autos = {}
        segs, subs, shanks = {}, {}, {}
        engraves, welding, dressing, paint = '','','',''

        def process_item(item, category, idx_range, tracker):
            """autos에 등록, 수량 누산 (shank, seg, sub)"""
            if category == 'seg':
                db_name = 'segment_'
            elif category == 'sub':
                db_name = 'submaterial_'
            elif category == 'sha':
                db_name = 'shank'
            else:
                db_name = category
            for idx in idx_range:
                name = item.get(f"{db_name}{idx}")
                amount = item.get(f"{category}{idx}_amount", 0)
                if name:
                    if name in tracker:
                        autos[f"{category}{tracker[name]}_amount"] += amount * item_amount
                    else:
                        tracker[name] = len(tracker) + 1
                        autos[f"{db_name}{tracker[name]}"] = name
                        autos[f"{category}{tracker[name]}_amount"] = amount * item_amount

        engraves, weldings, dressings, paints = [],[],[],[]
        for item_idx in range(1, 5):
            item = ip["loads"].get(f"item{item_idx}", {})
            item_amount = int(ip["inputs"].get(f"item{item_idx}", {}).get("amount", 0))
            process_item(item, "sha", [""], shanks)  # shank: 단일
            process_item(item, "seg", range(1, 3), segs)  # segment: 최대 2개
            process_item(item, "sub", range(1, 3), subs)  # submaterial: 최대 2개
            autos[f'item{item_idx}'] = item.get('name',' ').split(' ')[-1]
            
            engraves.append(item.get('engrave', ''))
            weldings.append(item.get('welding', ''))
            dressings.append(item.get('dressing', ''))
            paints.append(item.get('paint', ''))

        for key, values in zip(["engrave", "welding", "dressing", "paint"], [engraves, weldings, dressings, paints]):
            ip["autos"][key] = ("\n".join(x or "" for x in values)).strip()

        return autos

    def write_json_file(self,data,json_path)->None:
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def _read_json_file(json_path):
        with open(json_path, 'r',encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data

    def get_test_inputs(self):
        inputs = {
            'infos':{
                "group":"group1",
                "engrave":"engrave_a",
            },
            'item1':{
                "item":'TEST ITEM',
                'amount':3,
                "code":''
            },
            'item2':{
                "item":'TEST ITEM2',
                'amount':3,
                "code":''
            },
            'item3':{},
            'item4':{}
        }
        return inputs
    
    def run_test(self):
        inputs = self.get_test_inputs()
        self.get_new_ip(inputs)

