from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsProxyWidget
from PyQt5.QtCore import QRectF
from src.general_methods import GeneralMethods


class RoiManager(QGraphicsView):
    def __init__(self, histogramWidget, width=400, height=300):
        try:
            super().__init__()
            self.histogramWidget = histogramWidget

            self.scene = QGraphicsScene(self)
            self.setScene(self.scene)

            proxy = QGraphicsProxyWidget()
            proxy.setWidget(self.histogramWidget)
            proxy.setGeometry(QRectF(0, 0, self.histogramWidget.width(), self.histogramWidget.height()))
            self.scene.addItem(proxy)

            self.setFixedSize(width, height)
            GeneralMethods.rotate_view(self, 270)
        except Exception as e:
            print(f"Error RoiManager.init:\n  |--> {e}")