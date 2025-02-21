
from datetime import datetime
import json
from pprint import pprint
from math import ceil
# ===========================================================================================
class SPMaker():
    def __init__(self,model):
        self.model = model
        self.inputs = ["segment","segment_net"]
        self.ouputs = ["bond","segment_work","sp"]

    def get_new_sp(self,inputs):
        sp = self._make_new_sp(inputs)
        self.write_json_file(sp,f"./doc/sp/{sp['autos']['name']}.json")
        return sp
    
    def get_data_by_name(self,table_name,col,val):
        request = ('select',table_name,('id','오름차순'),(col,'=',val))
        response = self.model.get_select_data(request)
        return dict(zip(response[2][0],response[2][1]))
    
    def get_new_sp_name(self,recent_sp_name):
        [last_sp] = self.model.sql.execute_query('SELECT * FROM sp ORDER BY id DESC LIMIT 1;')
        year,no,_,_ = last_sp[1].split('-')
        try:
            r_year,r_no,_,_ = recent_sp_name.split('-')
            rec = f"{r_year[2:]}-{r_no[2:]}"
        except:
            rec = "None"

        if year == str(datetime.now().year):
            sp_name = f"{year}-SP{int(no[2:])+1:04}-{rec}"
        else:
            sp_name = f"{str(datetime.now().year)}-SP{1:04}-{rec}"
        return sp_name
    # -------------------------------------------------------------------------------------------
    def _make_new_sp(self,inputs:dict):
        sp = {}
        sp['inputs'] = inputs
        # --------------------------
        sp['loads'] = {}
        sp['loads']['segment'] = self.get_data_by_name('segment','code',sp['inputs']['code'])
        sp['loads']['bond'] = self.get_data_by_name('bond','name',sp['loads']['segment']['bond'])
        # --------------------------
        sp['autos'] = {}
        sp['autos']['name'] = self.get_new_sp_name(sp['loads']['segment']['recent_sp'])
        sp['autos']['creation_date'] = datetime.now().strftime("%Y년 %m월 %d일")
        sp['autos']['concent'] = float(sp['loads']['segment']['concent'])/4.4*100
        sp['autos']['loss'] = 1.01
        sp['autos']['segment_weight'] = self.get_segment_weight(sp)
        sp['autos'].update(self.get_segment_config(sp))
        sp['autos'].update(self.get_segment_density(sp))
        sp['autos'].update(self.get_workload(sp))
        sp['autos'].update(self.get_verification(sp))
        # --------------------------
        pprint(sp)
        return sp
    # -------------------------------------------------------------------------------------------
    def _get_floated_args(self,*args):
        return [float(x) if x is not None else 0 for x in args]
    
    def get_segment_weight(self,sp):
        volume,abs_density,rel_density,loss = \
            self._get_floated_args(sp['loads']['segment']['v'],
                                    sp['loads']['bond']['density'],
                                    sp['loads']['segment']['rel_density'],
                                    sp['autos']['loss'])
        return volume * abs_density * rel_density * loss
    
    def get_segment_config(self,sp):
        segment_weight,segment_volume,segment_concent = \
            self._get_floated_args(sp['autos']['segment_weight'],
                                        sp['loads']['segment']['v'],
                                        sp['loads']['segment']['concent'])
        segment_volume = segment_volume if segment_volume else 1 #avoid zero division

        dia_weight = segment_volume * segment_concent * 0.2
        dia_volume = dia_weight /3.51
        dia_volume_rate = dia_volume / segment_volume
    
        bond_volume = segment_volume - dia_volume
        bond_volume_rate = bond_volume / segment_volume
        bond_weight = bond_volume_rate * segment_weight

        total_volume =  dia_volume + bond_volume
        total_volume_Rate = dia_volume_rate + bond_volume_rate
        total_weight = dia_weight + bond_weight

        return {'dia_weight': dia_weight, 'dia_volume': dia_volume, 'dia_volume_rate': dia_volume_rate,
               'bond_weight': bond_weight, 'bond_volume': bond_volume, 'bond_volume_rate': bond_volume_rate,
                'total_weight': total_weight, 'total_volume': total_volume, 'total_volume_Rate': total_volume_Rate}

    def get_segment_density(self,sp):
        abs_density,bond_volume_rate,dia_volume_rate,total_weight,segment_volume,segment_concent = \
            self._get_floated_args(sp['loads']['bond']['density'],
                                    sp['autos']['bond_volume_rate'],
                                    sp['autos']['dia_volume_rate'],
                                    sp['autos']['total_weight'],
                                    sp['loads']['segment']['v'],
                                    sp['loads']['segment']['concent'])
        segment_volume = segment_volume if segment_volume else 1 #avoid zero division

        theo_density1 = abs_density * bond_volume_rate + dia_volume_rate * 3.51
        theo_density2 = abs_density * bond_volume_rate + segment_concent * 0.2
        final_density = total_weight / segment_volume
        final_rel_density = final_density / theo_density1
        benchmark_density = theo_density1 * 0.94
        return {'theo_density1':theo_density1,'theo_density2':theo_density2,'final_density':final_density,'final_rel_density':final_rel_density,'benchmark_density':benchmark_density}

    def get_workload(self,sp):
        total_weight,workload,dia_weight,dia1_rate,dia2_rate,dia3_rate = \
            self._get_floated_args(sp['autos']['total_weight'],
                                    sp['inputs']['workload'],
                                    sp['autos']['dia_weight'],
                                    sp['loads']['segment']['dia1_rate'],
                                    sp['loads']['segment']['dia2_rate'],
                                    sp['loads']['segment']['dia3_rate'])
        temp_bondmix_workload = workload * (total_weight - dia_weight)
        bond_workload = ((temp_bondmix_workload + 4999) // 5000) * 5000

        try:
            segment_work = bond_workload // (total_weight - dia_weight)
        except ZeroDivisionError:
            segment_work = 0
        bondmix_workload = segment_work * (total_weight - dia_weight)

        dia1_weight = ceil(dia_weight * segment_work * dia1_rate/10)
        dia2_weight = ceil(dia_weight * segment_work * dia2_rate/10)
        dia3_weight = ceil(dia_weight * segment_work * dia3_rate/10)

        return {'bond_workload':bond_workload,'segment_work':segment_work,'bondmix_workload':bondmix_workload,
                'dia1_weight':dia1_weight,'dia2_weight':dia2_weight,'dia3_weight':dia3_weight}

    def get_verification(self,sp):
        bondmix_workload,dia1_weight,dia2_weight,dia3_weight,total_weight,segment_work =\
            self._get_floated_args(sp['autos']['bondmix_workload'],
                                    sp['autos']['dia1_weight'],
                                    sp['autos']['dia2_weight'],
                                    sp['autos']['dia3_weight'],
                                    sp['autos']['total_weight'],
                                    sp['autos']['segment_work'])

        veri_weight = bondmix_workload + dia1_weight + dia2_weight + dia3_weight
        veri_count = total_weight * segment_work
        return {'veri_weight':veri_weight,'veri_count':veri_count}
        
    # -------------------------------------------------------------------------------------------
    def write_json_file(self,data,json_path)->None:
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    # --------------------------
    def _read_json_file(json_path):
        with open(json_path, 'r',encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data

    def get_test_inputs(self):
        # ip['autos']['seg1']
        # ip['autos']['seg1_amount']
        inputs={
            "code": "SQ0000",
            "workload":120.0,
        }
        return inputs
    
    def run_test(self):
        inputs = self.get_test_inputs()
        self.get_new_sp(inputs)

