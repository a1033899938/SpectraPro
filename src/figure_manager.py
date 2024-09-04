from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsProxyWidget
from PyQt5.QtCore import QRectF


class FigureManager(QGraphicsView):
    def __init__(self, figureWidget, width=400, height=300):
        try:
            super().__init__()
            self.figureWidget = figureWidget

            self.scene = QGraphicsScene(self)
            self.setScene(self.scene)

            proxy = QGraphicsProxyWidget()
            proxy.setWidget(self.figureWidget)
            proxy.setGeometry(QRectF(0, 0, self.figureWidget.width(), self.figureWidget.height()))
            self.scene.addItem(proxy)

            self.setFixedSize(1250, 850)
        except Exception as e:
            print(f"Error FigureManager.init:\n  |--> {e}")