if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# -------------------------------------------------------------------------------------------

import sys
from PyQt5.QtWidgets import QApplication
from src.SqlliteInterface import SqlliteInterface
from src.test.db_viewer.db_view_view import DatabaseViewerView
from src.test.db_viewer.db_view_ctrl import DatabaseViewerController

if __name__ == "__main__":
    # MVC 초기화
    app = QApplication(sys.argv)
    model = SqlliteInterface()
    view = DatabaseViewerView()
    controller = DatabaseViewerController(model, view)

    view.show()
    sys.exit(app.exec_())
