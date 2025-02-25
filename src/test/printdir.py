from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QApplication, QScrollArea
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,QPrintPreviewDialog
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        # UI 파일을 로드합니다.
        loadUi(f"./ui/spWidget.ui", self)

        # 프린트 버튼을 코드로 생성합니다.
        self.print_button = QPushButton("Print Grid Layout", self)

        # 버튼을 레이아웃에 추가합니다.
        layout = QVBoxLayout(self)
        layout.addWidget(self.print_button)

        # 프린트 버튼 클릭 시 동작할 연결
        self.print_button.clicked.connect(self.print_image)

    def save_scroll_area_as_image(self):
        # 스크롤 영역의 내용을 캡처하려면 스크롤 영역의 크기와 위치를 고려해야 합니다.
        scroll_area = self.findChild(QScrollArea, "scrollArea")
        scroll_contents = scroll_area.widget()  # scrollAreaWidgetContents

        # 전체 크기를 캡처하기 위해 QPixmap의 크기를 설정
        total_width = scroll_contents.size().width()
        total_height = scroll_contents.size().height()

        # QPixmap에 전체 크기 만큼 렌더링
        pixmap = QPixmap(total_width, total_height)
        pixmap.fill(Qt.white)  # 배경을 흰색으로 설정

        # QPainter로 그리기
        painter = QPainter(pixmap)
        scroll_contents.render(painter)
        painter.end()

        return pixmap


    def print_image(self):
        # 프린터 설정]
        pixmap = self.save_scroll_area_as_image()
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)  # A4 크기
        printer.setOrientation(QPrinter.Portrait)  # 세로 모드

        # 프린트 미리보기 다이얼로그 생성
        preview_dialog = QPrintPreviewDialog(printer)
        preview_dialog.paintRequested.connect(lambda p: self.draw_pixmap_on_paper(p, pixmap))
        preview_dialog.exec_()

    def draw_pixmap_on_paper(self,printer, pixmap):
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
        x_offset = (page_width - scaled_width) // 2 +30
        y_offset = (page_height - scaled_height) // 2

        # 스케일링된 이미지 그리기
        painter.drawPixmap(x_offset, 0, pixmap.scaled(scaled_width, scaled_height, Qt.KeepAspectRatio))
        painter.end()



if __name__ == "__main__":
    app = QApplication([])
    dialog = MyDialog()
    dialog.show()
    app.exec_()
