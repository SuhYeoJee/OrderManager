from src.imports.pyqt5_imports import *
DATETIME_FORMAT = "yyyy-MM-dd HH:mm:ss"
DATE_FORMAT = "yyyy-MM-dd"
DATE_KO_FORMAT = "yyyy년 M월 d일"
DB_PATH='./config/NOVA.db'
DEFAULT_VALS = ("", " ","0","0.00","2000-01-01","2000-01-01 00:00:00",None, 0, QDateTime(2000, 1, 1, 0, 0),QDate(2000, 1, 1))
GET_HANDLERS = {
    QLineEdit: lambda widget: widget.text(),
    QComboBox: lambda widget: widget.currentText(),
    QSpinBox: lambda widget: widget.value(),
    QDoubleSpinBox: lambda widget: widget.value(),
    QPlainTextEdit: lambda widget: widget.toPlainText(),
    QDateTimeEdit: lambda widget: widget.dateTime().toString(DATETIME_FORMAT),
    QDateEdit: lambda widget: widget.date().toString(DATE_FORMAT),
}
SET_HANDLERS = {
    QLineEdit: lambda widget, value: widget.setText(str(value)),
    QComboBox: lambda widget, value: (widget.addItem(str(value)) if widget.findText(str(value)) == -1 else None, widget.setCurrentText(str(value)))[1],
    QSpinBox: lambda widget, value: widget.setValue(int(value)),
    QDoubleSpinBox: lambda widget, value: widget.setValue(float(value)),
    QPlainTextEdit: lambda widget, value: widget.setPlainText(str(value)),
    QDateTimeEdit: lambda widget, value: widget.setDateTime(QDateTime.fromString(value,DATETIME_FORMAT)),
    QDateEdit: lambda widget, value: widget.setDate(QDate.fromString(value,DATE_FORMAT)),
    QLabel: lambda widget, value: (
        widget.setPixmap(
            QPixmap(value).scaled(widget.width(), widget.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        ) or widget.setAlignment(Qt.AlignCenter)
        if not QPixmap(value).isNull() else widget.setText("이미지 로드 실패")
    ) if isinstance(value, str) else None
}
CLEAR_HANDLERS = {
    QLineEdit: lambda widget: widget.clear(),
    QComboBox: lambda widget: widget.setCurrentText(""),
    QSpinBox: lambda widget: widget.setValue(0),
    QDoubleSpinBox: lambda widget: widget.setValue(0),
    QPlainTextEdit: lambda widget: widget.clear(),
    QDateTimeEdit: lambda widget: widget.setDateTime(QDateTime(2000, 1, 1, 0, 0)),
    QDateEdit: lambda widget: widget.setDate(QDate(2000, 1, 1)),
    QLabel: lambda widget: widget.clear()
}
ORDERS_TABLE_COLS = ["id","order_date","customer","name","code","item","amount","ip","sp_1","segment_1","bond_1","seg1_net","seg1_work","due_date","sp_2","segment_2","bond_2","seg2_net","seg2_work","description"]
