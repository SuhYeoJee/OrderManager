if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# ===========================================================================================
from src.Model import Model
from src.module.IP_maker import IPMaker

if __name__ == "__main__":
    m = Model()
    IPMaker(m).run_test()