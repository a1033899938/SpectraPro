import os
import json
from PyQt5.QtWidgets import QTreeView, QHeaderView, QStyledItemDelegate, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QColor
from PyQt5.QtCore import QDir, Qt
from src.general_methods import GeneralMethods


class TreeManager:
    """Tree Actions"""

    def __init__(self, main_window, treeView):
        """Initialization"""
        try:
            print("TreeManager is instantiating...")
            self.parent = main_window
            self.treeView = treeView
            self.model = None
            self.folder_dir = QDir()
            self.fileFilters = None

            self.initTree()
        except Exception as e:
            print(f"Error TreeManager.init:\n  |--> {e}")

    def initTree(self):
        try:
            print("Initializing tree...")
            self.model = QStandardItemModel()  # Manage the item in self.treeView through a model
            self.treeView.setModel(self.model)  # Manage the tree actions and slots
            self.treeView.setHeaderHidden(False)  # show header
            # Set custom delegate for the 1st row of tree view
            self.treeView.setItemDelegateForColumn(0, self.CustomDelegate())
        except Exception as e:
            print(f"Error TreeManager.initTree:\n  |--> {e}")

    def loadDirectory(self, spectra_file_folder_path):
        """Load directory and show in tree view"""
        try:
            print("Loading directory...")
            self.spectra_file_folder_path = spectra_file_folder_path
            # initialize model
            self.model.clear()  # Clear existing items
            self.model.setHorizontalHeaderLabels(['File Name', '✔', 'Type', 'File Path'])

            # set header of the tree view
            header = self.parent.treeView.header()  # Set the first column to be resizable but with a default width
            header.setSectionResizeMode(0, QHeaderView.Interactive)  # Set the first column to be resizable
            header.resizeSection(0, int(self.parent.base_tree_width)*0.7)  # Set width of the first column to 700 pixels
            header.setSectionResizeMode(1, QHeaderView.Interactive)
            header.resizeSection(1, int(self.parent.base_tree_width)*0.01)
            header.setSectionResizeMode(2, QHeaderView.Interactive)
            header.resizeSection(2, int(self.parent.base_tree_width)*0.08)
            header.setSectionResizeMode(3, QHeaderView.Interactive)
            header.resizeSection(3, int(self.parent.base_tree_width) * 0.5)

            # add items to model
            self.addFolderItems(self.spectra_file_folder_path, self.model.invisibleRootItem())
        except Exception as e:
            print(f"Error TreeManager.loadDirectory:\n  |--> {e}")

    def addFolderItems(self, spectra_file_folder_path, parent_item):
        try:
            self.folder_dir.setPath(spectra_file_folder_path)
            self.fileFilters = ['*.txt', '*.spe', '*.h5']  # Select the file types to show
            self.folder_dir.setNameFilters(self.fileFilters)

            # Add files with filters
            files = self.folder_dir.entryList(QDir.Files | QDir.NoDotAndDotDot)

            for file_name in files:
                item = QStandardItem(file_name)
                item.setEditable(False)

                item_check = QStandardItem()
                item_check.setCheckable(True)
                item_check.setEditable(False)

                file_path = self.folder_dir.filePath(file_name)
                item_file_path = QStandardItem(file_path)
                item_file_path.setEditable(False)

                item_type = QStandardItem('File')
                item_type.setEditable(False)
                parent_item.appendRow([item, item_check, item_type, item_file_path])

            # Add directories without filters
            dirs = QDir(spectra_file_folder_path).entryList(QDir.Dirs | QDir.NoDotAndDotDot)

            for folder_name in dirs:
                item = QStandardItem(folder_name)
                item.setEditable(False)
                item.setIcon(QIcon.fromTheme('folder'))

                item_check = QStandardItem()
                item_check.setCheckable(True)
                item_check.setEditable(False)

                file_path = self.folder_dir.filePath(folder_name)
                item_file_path = QStandardItem(file_path)
                item_file_path.setEditable(False)

                item_type = QStandardItem('Folder')
                item_type.setEditable(False)
                parent_item.appendRow([item, item_check, item_type, item_file_path])

                # Recursively add subfolders
                self.addFolderItems(self.folder_dir.filePath(folder_name), item)
            # If iterate through all elements, return to previous directory
            self.folder_dir.cdUp()
        except Exception as e:
            print(f"Error TreeManager.addFolderItems:\n  |--> {e}")

    class CustomTreeView(QTreeView):
        """Rewrite some slots for double left-clicking, right press and slot: 'check/uncheck all item'."""

        def __init__(self, parent=None):
            super().__init__(parent)

        # rewrite the mouse double click event inherit from parent
        def mouseDoubleClickEvent(self, event):
            try:
                # get index of double click position
                index = self.indexAt(event.pos())
                if not index.isValid() or event.button() == Qt.RightButton:
                    return

                # get item from model
                item_index = index.siblingAtColumn(0)
                item_check_index = index.siblingAtColumn(1)
                item = self.model().itemFromIndex(item_index)
                item_check = self.model().itemFromIndex(item_check_index)
                # Toggle check state for the clicked item
                new_state_is_check = not item_check.checkState()

                if item_check is not None:
                    # exchange check state
                    item_check.setCheckState(Qt.Checked if new_state_is_check else Qt.Unchecked)

                # Check if item is a folder
                if item.hasChildren():
                    self.toggle_check_state_for_children(item, new_state_is_check)

                # other logic of double clicking
                super().mouseDoubleClickEvent(event)
            except Exception as e:
                print(f"Error TreeManager.CustomTreeView.mouseDoubleClickEvent:\n  |--> {e}")

        def toggle_check_state_for_children(self, parent_item, check):
            try:
                for row in range(parent_item.rowCount()):
                    child_item = parent_item.child(row, 0)
                    child_item_check = parent_item.child(row, 1)
                    child_item_check.setCheckState(Qt.Checked if check else Qt.Unchecked)
                    if child_item.hasChildren():
                        self.toggle_check_state_for_children(child_item, check)
            except Exception as e:
                print(f"Error TreeManager.CustomTreeView.toggle_check_state_for_children:\n  |--> {e}")

        def mousePressEvent(self, event):
            try:
                if event.button() == Qt.RightButton:
                    index = self.indexAt(event.pos())
                    if not index.isValid():
                        return

                    item_index = index.siblingAtColumn(0)
                    item = self.model().itemFromIndex(item_index)
                    new_state_is_expand = not self.isExpanded(item_index)
                    if item.hasChildren():  # 检查是否是文件夹
                        if new_state_is_expand:
                            self.expand(item_index)  # 展开这一级文件夹
                        else:
                            self.collapse(item_index)
                super().mousePressEvent(event)
            except Exception as e:
                print(f"Error TreeManager.CustomTreeView.mousePressEvent:\n  |--> {e}")

    class CustomDelegate(QStyledItemDelegate):
        def paint(self, painter, option, index):
            try:
                # Call base class paint method
                super().paint(painter, option, index)

                # Get the item and its check state
                item_index = index.siblingAtColumn(0)
                item = index.model().itemFromIndex(item_index)
                item_check_index = index.siblingAtColumn(1)
                item_check = index.model().itemFromIndex(item_check_index)

                item_type_index = index.siblingAtColumn(2)
                item_type = index.model().itemFromIndex(item_type_index)
                if item_type:
                    item_type = item_type.text()

                if not item_check:
                    return

                if item_check.checkState() == Qt.Checked:
                    # Setting item's color according to item_type
                    painter.save()
                    if item_type == 'File':
                        painter.fillRect(option.rect, QColor(144, 238, 144, alpha=100))  # light green
                    elif item_type == 'Folder':
                        painter.fillRect(option.rect, QColor(128, 0, 128, alpha=80))  # light purple
                        # painter.fillRect(option.rect, QColor(173, 216, 230, alpha=150))  # light blue
                    else:
                        painter.fillRect(option.rect, QColor(255, 0, 0, alpha=150))  # light red
                    painter.restore()
            except Exception as e:
                print(f"Error TreeManager.CustomDelegate.paint:\n  |--> {e}")

    def collapse_tree(self):
        """Define a slot to collapse all nodes in the tree view."""
        try:
            print("Collapsing all nodes in the tree view...")
            self.treeView.collapseAll()
        except Exception as e:
            print(f"Error TreeManager.CustomDelegate.collapse_tree:\n  |--> {e}")

    def uncheck_all_items(self):
        """Define a slot to uncheck all items in 2nd column(item_check) in the tree view."""
        try:
            print("Unchecking all items in the tree view...")
            parent_item = self.model.invisibleRootItem()
            self.childItemUncheck(parent_item)
        except Exception as e:
            print(f"Error TreeManager.CustomDelegate.uncheck_all_items:\n  |--> {e}")

    def childItemUncheck(self, parent_item):
        """To uncheck all child items, grandchild items..."""
        try:
            for row in range(parent_item.rowCount()):
                child_item = parent_item.child(row, 0)
                child_item_check = parent_item.child(row, 1)
                child_item_check.setCheckState(False)
                if child_item.hasChildren():
                    self.childItemUncheck(child_item)
        except Exception as e:
            print(f"Error TreeManager.CustomDelegate.childItemUncheck:\n  |--> {e}")

    def toggle_show_tree(self):
        try:
            print("Toggling tree view visibility...")
            if self.treeView.isVisible():
                self.treeView.hide()
            else:
                self.treeView.show()
        except Exception as e:
            print(f"Error TreeManager.CustomDelegate.toggle_show_tree:\n  |--> {e}")

    def input_name_head_and_save_cache(self):
        try:
            ask_flag = 0
            save_flag = 0
            cache_name_head, ok = GeneralMethods.input_dialog(self.parent, title='Input name head of cache',
                                                              property_name='name head')

            if ok:
                if cache_name_head:
                    if (os.path.exists(os.path.join('cache', cache_name_head + '_tree_state.json'))
                            or os.path.exists(os.path.join('cache', cache_name_head + '_filefolder.json'))):
                        ask_flag = 1
                    else:
                        save_flag = 1
                else:
                    if (os.path.exists(os.path.join('cache', 'tree_state.json'))
                            or os.path.exists(os.path.join('cache', 'filefolder.json'))):
                        ask_flag = 1
                    else:
                        save_flag = 1

                if ask_flag:
                    reply = QMessageBox.question(self.parent, "Confirmation", 'The file is exist, continue?',
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        save_flag = 1

                if save_flag:
                    self.save_cache(cache_name_head)
            else:
                print("You cancel inputting name head.")

        except Exception as e:
            print(f"Error TreeManager.CustomDelegate.input_name_head_and_save_cache:\n  |--> {e}")

    def save_cache(self, cache_name_head):
        try:
            self.save_spectra_file_folder(cache_name_head=cache_name_head)
            self.save_tree_state(cache_name_head=cache_name_head)
        except Exception as e:
            print(f"Error TreeManager.save_cache:\n  |--> {e}")

    def save_tree_state(self, cache_name_head=''):
        try:
            """A method to save tree items' and their check status to a json file."""
            print("Saving the tree states!")
            if cache_name_head:
                self.tree_state_name = cache_name_head + '_tree_state.json'
            else:
                self.tree_state_name = 'tree_state.json'
            # Save the root path and check states of all items
            root_item = self.model.invisibleRootItem()
            data = self.get_item_data(root_item)

            # Save data to a json file
            with open(os.path.join('cache', self.tree_state_name), 'w') as f:  # if not exist, create one
                json.dump(data, f, indent=4)
            print("  |--> Json: 'tree_state.json' has been saved.")
        except Exception as e:
            print(f"Error TreeManager.save_tree_state:\n  |--> {e}")

    def get_item_data(self, item):
        """Get all tree items' state data."""
        try:
            item_index = item.index()
            item_check_index = item_index.siblingAtColumn(1)
            item_check = item.model().itemFromIndex(item_check_index)
            item_check_data = Qt.Checked if item_check and item_check.checkState() == Qt.Checked else False

            item_type_index = item_index.siblingAtColumn(2)
            item_type = item.model().itemFromIndex(item_type_index)
            item_type = item_type.text() if item_type else ''

            item_file_path_index = item_index.siblingAtColumn(3)
            item_file_path = item.model().itemFromIndex(item_file_path_index)
            file_path = item_file_path.text() if item_file_path else ''

            data = {
                'text': item.text(),
                'checked': item_check_data,
                'type': item_type,
                'file_path': file_path,
                'children': []
            }

            for row in range(item.rowCount()):
                child_item = item.child(row, 0)
                child_item_check = item.child(row, 1)

                if child_item:
                    child_item_data = self.get_item_data(child_item)
                    data['children'].append(child_item_data)
            return data
        except Exception as e:
            print(f"Error TreeManager.get_item_data:\n  |--> {e}")

    def select_json_file_and_load_cache(self):
        try:
            json_file_path = GeneralMethods.select_json_file_through_dialog()
            json_file_name = os.path.basename(json_file_path)
            if '_tree_state.json' in json_file_name or '_filefolder.json' in json_file_name:
                if '_tree_state.json' in json_file_name:
                    cache_name_head = json_file_name.replace('_tree_state.json', '')
                else:
                    cache_name_head = json_file_name.replace('_filefolder.json', '')
                self.load_file_folder(cache_name_head + '_filefolder.json')
                self.load_tree_state(cache_name_head + '_tree_state.json')
            elif 'tree_state.json' in json_file_name or 'filefolder.json' in json_file_name:
                self.load_file_folder('filefolder.json')
                self.load_tree_state('tree_state.json')
            else:
                print("Error input json file.")
        except Exception as e:
            print(f"Error TreeManager.select_json_file_and_load_cache:\n  |--> {e}")

    def load_tree_state(self, tree_state_json_file_name):
        """A method to load tree items from a json file."""
        try:
            print("Loading tree state from json...")
            self.tree_state_json_file_name = tree_state_json_file_name

            # Load data from a json file
            with open(os.path.join('cache', self.tree_state_json_file_name), 'r') as f:
                print("  |--> Opening 'tree_state.json'...")
                data = json.load(f)
                self.set_item_data(self.model.invisibleRootItem(), data)
        except Exception as e:
            print(f"Error TreeManager.load_tree_state:\n  |--> {e}")

    def set_item_data(self, item, data):
        """Recursively set the item data from JSON to the tree."""
        try:
            for row in range(item.rowCount()):
                # get child item's check item
                child_item = item.child(row, 0)
                child_item_check = item.child(row, 1)
                child_item_data = data['children'][row]

                child_item_check.setCheckState(child_item_data['checked'])

                # if child_item has at least one child, repeat.
                if child_item.rowCount():
                    self.set_item_data(child_item, child_item_data)
        except Exception as e:
            print(f"Error TreeManager.set_item_data:\n  |--> {e}")

    def save_spectra_file_folder(self, cache_name_head=''):
        try:
            if cache_name_head:
                self.file_folder_json_file_name = cache_name_head + '_filefolder.json'
            else:
                self.file_folder_json_file_name = 'filefolder.json'

            data = {
                'text': self.parent.spectra_file_folder_path,
            }

            with open(os.path.join('cache', self.file_folder_json_file_name), 'w') as f:  # if not exist, create one
                json.dump(data, f, indent=4)
            print("  |--> Json: 'filefolder.json' has been saved")
        except Exception as e:
            print(f"Error TreeManager.save_spectra_file_folder:\n  |--> {e}")

    def load_file_folder(self, file_folder_json_file_name):
        try:
            with open(os.path.join('cache', file_folder_json_file_name), 'r') as f:
                print("  |--> Opening 'filefolder.json'...")
                data = json.load(f)
                file_folder_path = data['text']
                self.loadDirectory(file_folder_path)
                self.parent.spectra_file_folder_path = file_folder_path
        except Exception as e:
            print(f"Error TreeManager.load_file_folder:\n  |--> {e}")