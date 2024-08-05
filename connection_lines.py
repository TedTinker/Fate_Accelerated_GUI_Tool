from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class ConnectionLines(QWidget):
    def __init__(self, mdi_area, parent=None):
        super().__init__(parent)
        self.mdi_area = mdi_area
        self.lines = []

    def add_line(self, start_widget, end_widget):
        self.lines.append((start_widget, end_widget))
        self.update()

    def remove_lines_connected_to(self, widget):
        self.lines = [line for line in self.lines if line[0] != widget and line[1] != widget]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        for start_widget, end_widget in self.lines:
            if start_widget.isVisible() and end_widget.isVisible():
                start_rect = start_widget.geometry()
                end_rect = end_widget.geometry()
                start_point = start_rect.center()
                end_point = end_rect.center()
                painter.drawLine(start_point, end_point)

    def update_lines(self):
        self.update()
