from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsProxyWidget, QSizePolicy
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QResizeEvent


class FigureManager(QGraphicsView):
    def __init__(self, figureWidget):
        try:
            super().__init__()
            self.figureWidget = figureWidget

            self.scene = QGraphicsScene(self)
            self.setScene(self.scene)

            proxy = QGraphicsProxyWidget()
            proxy.setWidget(self.figureWidget)
            proxy.setGeometry(QRectF(0, 0, self.figureWidget.width(), self.figureWidget.height()))
            proxy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            self.setSceneRect(QRectF(self.figureWidget.width()*0.1, self.figureWidget.height()*0.1,
                                     self.figureWidget.width()*0.8, self.figureWidget.height()*0.8))
            self.scene.addItem(proxy)

            self.setFixedSize(self.figureWidget.width(), self.figureWidget.height())
        except Exception as e:
            print(f"Error FigureManager.init:\n  |--> {e}")