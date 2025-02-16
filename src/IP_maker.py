if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
from datetime import datetime
import json
from pprint import pprint
from math import ceil
# --------------------------
from src.Model import Model
# ===========================================================================================
class IPMaker():
    def __init__(self,model:Model):
        self.model = model

    def get_ip_path(self):
        inputs = {}
        ip = self.make_new_ip(inputs)
        self.write_json_file(ip,ip['inputs']['path'])
        return ip['inputs']['path']

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

    def make_new_ip(self,inputs:dict):
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
    
    def __get_floated_args(self,*args):
        return [float(x) if x is not None else 0 for x in args]
    

    def write_json_file(self,data,json_path)->None:
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def __read_json_file(json_path):
        with open(json_path, 'r',encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data

if __name__ == "__main__":
    m = Model()
    ipm = IPMaker(m)
    ip = ipm.make_new_ip({"item_group": '3\"6OR60'})
    ipm.write_json_file(ip,'./config/iptest.json')