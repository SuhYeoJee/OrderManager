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

    def get_items_by_group_name(self,group_name):
        request = ('select','item',('id','오름차순'),('item_group','=',group_name))
        response = self.model.select_data(request)
        return {val[3]:dict(zip(response[2][0],val)) for val in response[2][1:]}

    def _make_new_ip(self,inputs:dict):
        ip = {}
        ip['inputs'] = inputs
        # --------------------------
        ip['loads'] = {}
        ip['loads']['item'] = self.get_items_by_group_name(ip['inputs']['item_group'])
        # --------------------------
        ip['autos'] = {}
        ip['autos']['name'] = self.get_ip_name()
        ip['autos']['creation_date'] = datetime.now().strftime("%Y년 %m월 %d일")
        # --------------------------
        pprint(ip)
        return ip
    

    def 그러니까_아마_입력이_이런모양(self):
        inputs={
            'item1':{
                    "name":"2025-00041",
                    "code": "001",
                    "customer":"강낭콩",
                    "item":"3\"6OR60CW",
                    "item_group":"3\"6OR60",
                    "amount":10,
                    "engrave":"engr",
                    "order_date":"2025-02-19",
                    "due_date":"2025-02-28"
                },
            'item2':{
                    "name":"2025-00041",
                    "code": "002",
                    "customer":"강낭콩",
                    "item":"3\"6OR60CCW",
                    "item_group":"3\"6OR60",
                    "amount":10,
                    "engrave":"engr",
                    "order_date":"2025-02-19",
                    "due_date":"2025-02-28"
            }
        }
        return inputs
    


    def write_json_file(self,data,json_path)->None:
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def _read_json_file(json_path):
        with open(json_path, 'r',encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data
