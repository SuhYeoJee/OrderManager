if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# ===========================================================================================
from datetime import datetime
import json
from pprint import pprint
# ===========================================================================================
class IPMaker():
    def __init__(self,model):
        self.model = model
        self.inputs = ["item","item_group","amount","engrave","due_date"]

    def get_new_ip(self,inputs)->str:
        ip = self._make_new_ip(inputs)
        self.write_json_file(ip,f"./ip/{ip['autos']['name']}.json")
        return ip

    def get_ip_name(self):
        [last_ip] = self.model.sql.execute_query('SELECT * FROM ip ORDER BY id DESC LIMIT 1;')
        year,no = last_ip[1].split('-')

        if year == str(datetime.now().year):
            ip_name = f"{year}-IP{int(no[2:])+1:04}"
        else:
            ip_name = f"{str(datetime.now().year)}-IP{1:04}"
        return ip_name
    
    def get_data_by_name(self,table_name,name):
        request = ('select',table_name,('id','오름차순'),('name','=',name))
        response = self.model.select_data(request)
        return dict(zip(response[2][0],response[2][1]))
    
    def get_items_by_group_name(self,group_name):
        request = ('select','item',('id','오름차순'),('item_group','=',group_name))
        response = self.model.select_data(request)
        return {val[3]:dict(zip(response[2][0],val)) for val in response[2][1:]}

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
        ip['autos']['name'] = self.get_ip_name()
        ip['autos']['creation_date'] = datetime.now().strftime("%Y년 %m월 %d일")
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
            for idx in idx_range:
                name = item.get(f"{category}{idx}")
                amount = item.get(f"{category}{idx}_amount", 0)
                if name:
                    if name in tracker:
                        autos[f"{category}{tracker[name]}_amount"] += amount * item_amount
                    else:
                        tracker[name] = len(tracker) + 1
                        autos[f"{category}{tracker[name]}"] = name
                        autos[f"{category}{tracker[name]}_amount"] = amount * item_amount

        engraves, weldings, dressings, paints = [],[],[],[]
        for item_idx in range(1, 5):
            item = ip["loads"].get(f"item{item_idx}", {})
            item_amount = int(ip["inputs"].get(f"item{item_idx}", {}).get("amount", 0))
            process_item(item, "shank", [""], shanks)  # shank: 단일
            process_item(item, "seg", range(1, 3), segs)  # segment: 최대 2개
            process_item(item, "sub", range(1, 3), subs)  # submaterial: 최대 2개
            
            engraves.append(item.get('engrave', ''))
            weldings.append(item.get('welding', ''))
            dressings.append(item.get('dressing', ''))
            paints.append(item.get('paint', ''))
        else:
            ip['autos']['engrave'] = '\n'.join(engraves)
            ip['autos']['welding'] = '\n'.join(weldings)
            ip['autos']['dressing'] = '\n'.join(dressings)
            ip['autos']['paint'] = '\n'.join(paints)
        return autos


    def get_test_inputs(self):
        inputs={
            'item1':
            {
                "name":"2025-00042",
                "code": "003",
                "customer":"강낭콩",
                "item":"TEST_ITEM",
                "item_group":"TEST_GROUP",
                "amount":10,
                "engrave":"engr",
                "order_date":"2025-02-19",
                "due_date":"2025-02-28"
            },
            'item2':
            {
                "name":"2025-00042",
                "code": "004",
                "customer":"강낭콩",
                "item":"TEST_ITEM_2",
                "item_group":"TEST_GROUP",
                "amount":10,
                "engrave":"engr",
                "order_date":"2025-02-19",
                "due_date":"2025-02-28"
            },
            'item3':{},
            'item4':{}
        }
        return inputs
    
    def run_test(self):
        inputs = self.get_test_inputs()
        self.get_new_ip(inputs)



    def write_json_file(self,data,json_path)->None:
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def _read_json_file(json_path):
        with open(json_path, 'r',encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data
