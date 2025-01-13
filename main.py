if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------
import sys
from PyQt5.QtWidgets import QApplication
from src.Model import Model
from src.View import View
from src.Controller import Controller
# ===========================================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = Model()
    view = View()
    controller = Controller(model, view)
    # --------------------------
    view.show()
    sys.exit(app.exec_())
