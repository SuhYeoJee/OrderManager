from PyQt5.QtWidgets import QDialog, QApplication, QScrollArea, QWidget
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

class WidgetPrinter(QDialog):
    def __init__(self, widget: QWidget, parent=None):
        super().__init__(parent)
        self.widget = widget  # 프린트할 위젯을 저장

    def save_widget_as_image(self):
        """ 주어진 위젯을 캡처하여 QPixmap으로 반환 """
        total_width = self.widget.size().width()
        total_height = self.widget.size().height()

        pixmap = QPixmap(total_width, total_height)
        pixmap.fill(Qt.white)  # 배경을 흰색으로 설정

        # QPainter로 위젯 렌더링
        painter = QPainter(pixmap)
        self.widget.render(painter)
        painter.end()

        return pixmap

    def print_widget(self):
        """ 위젯을 프린트 미리보기 다이얼로그를 통해 출력 """
        pixmap = self.save_widget_as_image()

        # 프린터 설정
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)  # A4 크기
        printer.setOrientation(QPrinter.Portrait)  # 세로 모드

        # 프린트 미리보기 다이얼로그 생성
        preview_dialog = QPrintPreviewDialog(printer)
        preview_dialog.paintRequested.connect(lambda p: self.draw_pixmap_on_paper(p, pixmap))
        preview_dialog.exec_()

    def draw_pixmap_on_paper(self, printer, pixmap):
        """ 프린터에 QPixmap 이미지를 그려줌 """
        painter = QPainter(printer)

        # A4 페이지 크기
        page_rect = printer.pageRect()
        page_width = page_rect.width()
        page_height = page_rect.height()

        # 원본 이미지 크기
        image_width = pixmap.width()
        image_height = pixmap.height()

        # 원본 비율 유지하면서 스케일링
        scale_factor = min(page_width / image_width, page_height / image_height)
        scaled_width = int(image_width * scale_factor)
        scaled_height = int(image_height * scale_factor)

        # 중앙 배치 좌표 계산
        x_offset = (page_width - scaled_width) // 2
        y_offset = (page_height - scaled_height) // 2

        # 스케일링된 이미지 그리기
        painter.drawPixmap(x_offset, 0, pixmap.scaled(scaled_width, scaled_height, Qt.KeepAspectRatio))
        painter.end()

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        # UI 파일을 로드합니다.
        loadUi(f"./ui/spWidget.ui", self)
    # MyDialog 클래스 내부에서 사용 예시
    def print_image(self):
        scroll_area = self.findChild(QScrollArea, "scrollArea")
        scroll_contents = scroll_area.widget()  # 실제 컨텐츠 위젯 가져오기

        printer = WidgetPrinter(scroll_contents, self)
        printer.print_widget()

if __name__ == "__main__":
    app = QApplication([])
    m = MyDialog()
    m.show()
    m.print_image()
    app.exec_()
