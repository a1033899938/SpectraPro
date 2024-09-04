from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt


class ListManager:
    def __init__(self, main_window, list_widget, treeManager, figureWidget):
        """Initialization"""
        print("ListManager is instantiating...")
        self.parent = main_window
        self.listWidget = list_widget
        self.treeManager = treeManager
        self.model = self.treeManager.model
        self.figureWidget = figureWidget

        self.checked_files_data = None

    def import_checked_files(self):
        try:
            self.checked_files_data = []  # clear cache every time
            self.listWidget.clear()
            root_item = self.model.invisibleRootItem()
            get_checked_files_data = self.get_checked_files_data(root_item)
            for file_data in get_checked_files_data:
                file_name = QListWidgetItem(file_data['text'])
                file_name.setData(1, file_data['file_path'])
                self.listWidget.addItem(file_name)
        except Exception as e:
            print(f"  |--> Error importing checked files: {e}")

    def get_checked_files_data(self, item):
        for row in range(item.rowCount()):
            # get child item's check item
            child_item = item.child(row, 0)
            child_item_check = item.child(row, 1)
            chile_item_type = item.child(row, 2)
            child_item_file_path = item.child(row, 3)
            if chile_item_type:
                chile_item_type = chile_item_type.text()
            if child_item_check.checkState() and chile_item_type == 'File':
                data = {
                    'text': child_item.text(),
                    'file_path': child_item_file_path.text(),
                }
                self.checked_files_data.append(data)
            if child_item.hasChildren():
                self.get_checked_files_data(child_item)
        return self.checked_files_data

    class CustomListWidget(QListWidget):
        def __init__(self, figureWidget):
            super().__init__()
            # enable dragging
            self.setDragEnabled(True)
            self.setDropIndicatorShown(True)
            self.setDefaultDropAction(Qt.MoveAction)
            self.setAcceptDrops(True)

            self.figureWidget = figureWidget

        def mouseDoubleClickEvent(self, event):
            print("You are clicking the list widget:", end=' ')
            print(self.item(0).text())

        def mousePressEvent(self, event):
            try:
                if event.button() == Qt.LeftButton:
                    index = self.indexAt(event.pos())
                    if not index.isValid():
                        return
                list_item = self.itemAt(event.pos())
                if list_item:
                    self.figureWidget.deal_with_this_file(list_item)
            except Exception as e:
                print(f"  |--> Error mousePressEvent: {e}")