from src.imports.pyqt5_imports import *
DATETIME_FORMAT = "yyyy-MM-dd HH:mm:ss"
DB_PATH='./config/NOVA.db'
GET_HANDLERS = {
    QLineEdit: lambda widget: widget.text(),
    QComboBox: lambda widget: widget.currentText(),
    QSpinBox: lambda widget: widget.value(),
    QDoubleSpinBox: lambda widget: widget.value(),
    QPlainTextEdit: lambda widget: widget.toPlainText(),
    QDateTimeEdit: lambda widget: widget.dateTime().toString(DATETIME_FORMAT),
    QDateEdit: lambda widget: widget.dateTime().toString(DATETIME_FORMAT),
}
SET_HANDLERS = {
    QLineEdit: lambda widget, value: widget.setText(str(value)),
    QComboBox: lambda widget, value: (widget.addItem(str(value)) if widget.findText(str(value)) == -1 else None, widget.setCurrentText(str(value)))[1],
    QSpinBox: lambda widget, value: widget.setValue(int(value)),
    QDoubleSpinBox: lambda widget, value: widget.setValue(float(value)),
    QPlainTextEdit: lambda widget, value: widget.setPlainText(str(value)),
    QDateTimeEdit: lambda widget, value: widget.setDateTime(QDateTime.fromString(value,DATETIME_FORMAT)),
    QDateEdit: lambda widget, value: widget.setDateTime(QDateTime.fromString(value,DATETIME_FORMAT)),
}
CLEAR_HANDLERS = {
    QLineEdit: lambda widget: widget.clear(),
    QComboBox: lambda widget: widget.setCurrentText(""),
    QSpinBox: lambda widget: widget.setValue(0),
    QDoubleSpinBox: lambda widget: widget.setValue(0),
    QPlainTextEdit: lambda widget: widget.clear(),
    QDateTimeEdit: lambda widget: widget.setDateTime(QDateTime(0000, 0, 0, 0, 0)),
    QDateEdit: lambda widget: widget.setDateTime(QDateTime(0000, 0, 0, 0, 0)),
}