if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# ===========================================================================================
from src.Model import Model
from src.module.IP_maker import IPMaker

if __name__ == "__main__":
    m = Model()
    ipm = IPMaker(m)
    ip = ipm._make_new_ip({"item_group": '3\"6OR60'})
    ipm.write_json_file(ip,'./config/iptest.json')