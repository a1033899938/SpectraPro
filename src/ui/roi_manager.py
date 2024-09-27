from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsProxyWidget, QSizePolicy
from PyQt5.QtCore import QRectF
from src.ui.general_methods import GeneralMethods


class RoiManager(QGraphicsView):
    def __init__(self, histogramWidget):
        try:
            super().__init__()
            self.histogramWidget = histogramWidget

            self.scene = QGraphicsScene(self)
            self.setScene(self.scene)

            proxy = QGraphicsProxyWidget()
            proxy.setWidget(self.histogramWidget)
            proxy.setGeometry(QRectF(0, 0, self.histogramWidget.width(), self.histogramWidget.height()))
            proxy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            self.scene.addItem(proxy)
            self.setSceneRect(QRectF(self.histogramWidget.width() * 0.1, self.histogramWidget.height() * 0.1,
                                     self.histogramWidget.width() * 0.8, self.histogramWidget.height() * 0.8))

            self.setFixedSize(self.histogramWidget.height(), self.histogramWidget.width())
            GeneralMethods.rotate_view(self, 270)
        except Exception as e:
            print(f"Error RoiManager.init:\n  |--> {e}")