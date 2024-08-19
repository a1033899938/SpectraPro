import os
import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QWidget, QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout)
from PyQt5.QtWidgets import (QLabel, QLineEdit, QTextEdit, QPushButton)
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import (QTreeView, QFileSystemModel)
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import QColor, QPainter
import json
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5 import (QtWidgets, QtCore, QtGui)
from PyQt5.QtGui import QCloseEvent


class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        """Menu objects"""
        self.menubar = None
        self.fileMenu = None
        self.cacheMenu = None

        """Main window objects"""
        self.spectrumFileLabel = None
        self.spectrumFileTextEdit = None
        self.spectrumFolderLabel = None
        self.spectrumFolderTextEdit = None
        self.treeView = None
        self.listWidget = None
        self.treeCollapseButton = None
        self.allItemUncheckButton = None
        self.toggleShowTreeButton = None
        self.importCheckedFilesButton = None

        """Signals and slots"""
        self.treeManager = None
        self.menuActions = None
        self.listManager = None

        """Rewrite slot react to close event"""
        self.mainWindowManager = None

        """Initialize ui"""
        self.initUI()

    def initUI(self):
        """ Set main window parameters"""
        print("Initializing ui")
        # set window position, title and so on...
        self.setGeometry(200, 200, 1200, 900)
        self.setWindowTitle('SpectraPro')
        self.statusBar().showMessage('Ready')

        """Create menubar objects"""
        # create objects
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')
        self.cacheMenu = self.menubar.addMenu('&Cache')

        """Create main window objects"""
        # hbox1
        self.spectrumFileLabel = QLabel('File path')
        self.spectrumFileTextEdit = QTextEdit()
        self.spectrumFileTextEdit.setReadOnly(True)  # Set to read-only for file path display
        self.spectrumFileTextEdit.setFixedHeight(30)  # Set height for QTextEdit

        # hbox2
        self.spectrumFolderLabel = QLabel('File directory')
        self.spectrumFolderTextEdit = QTextEdit()
        self.spectrumFolderTextEdit.setReadOnly(True)  # Set to read-only for file path display
        self.spectrumFolderTextEdit.setFixedHeight(30)  # Set height for QTextEdit

        # tree
        self.treeView = TreeManager.CustomTreeView()
        self.treeManager = TreeManager(self, self.treeView)  # Manage the tree actions and slots by self.treeManager
        # self.treeView.hide()

        # list widget
        self.listWidget = ListManager.CustomListWidget()
        self.listManager = ListManager(self, self.treeManager, self.listWidget)

        # hbox3
        self.treeCollapseButton = QPushButton('Collapse All')  # add a button to collapse all nodes
        self.treeCollapseButton.clicked.connect(self.treeManager.treeCollapse)
        self.allItemUncheckButton = QPushButton('Uncheck All')  # add a button to uncheck all items
        self.allItemUncheckButton.clicked.connect(self.treeManager.allItemUncheck)

        # hbox4
        # add a button to show/hide treeview
        self.toggleShowTreeButton = QPushButton("Show tree")
        self.toggleShowTreeButton.setChecked(True)  # Set initial status
        self.toggleShowTreeButton.clicked.connect(self.treeManager.toggleShowTree)
        # add a button to show/hide checked files
        self.importCheckedFilesButton = QPushButton("Import checked files")
        self.importCheckedFilesButton.clicked.connect(self.listManager.importCheckedFiles)

        """Add custom actions to menu and connect to slots."""
        self.menuActions = MenuActions(self,
                                       self.treeManager)  # define self(main window) as parent object of self.menuActions
        self.fileMenu.addAction(self.menuActions.chooseSpectrumFileAction())  # add a custom action instant
        self.fileMenu.addAction(self.menuActions.chooseSpectrumFolderAction())

        """Add custom slot react to main window close event."""
        self.mainWindowManager = MainWindowManager(self, self.menuActions, self.treeManager)
        """Add a custom action to menu and connect to slot."""
        self.cacheMenu.addAction(self.mainWindowManager.saveCacheAction())

        """box manager"""
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.spectrumFileLabel)
        hbox1.addWidget(self.spectrumFileTextEdit)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.spectrumFolderLabel)
        hbox2.addWidget(self.spectrumFolderTextEdit)

        hbox3 = QVBoxLayout()
        hbox3.addWidget(self.treeCollapseButton)
        hbox3.addWidget(self.allItemUncheckButton)

        hbox4 = QVBoxLayout()
        hbox4.addWidget(self.toggleShowTreeButton)
        hbox4.addWidget(self.importCheckedFilesButton)

        hbox5 = QHBoxLayout()
        hbox5.addLayout(hbox3)
        hbox5.addLayout(hbox4)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.treeView)
        vbox.addWidget(self.listWidget)
        # vbox.addStretch(0)
        vbox.addLayout(hbox5)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        self.show()

    def closeEvent(self, event: QCloseEvent):
        # deal with close event by self.actions
        self.mainWindowManager.closeEvent(event)


class MenuActions:
    """Handles menu actions and their corresponding slots."""

    def __init__(self, main_window, treeManager):
        """Initialization"""
        print("MenuActions is instantiating...")
        self.parent = main_window
        self.treeManager = treeManager
        self.model = self.treeManager.model

        self.spectrumFile = None
        self.spectrumFolder = None

        self.initMenu()

    def initMenu(self, cache_name='_filefolder_path.json'):
        print("Initializing Menu...")
        self.cache_name = cache_name
        try:
            with open(self.cache_name, 'r') as f:
                print("  |--> Opening 'filefolder_path.json'...")
                data = json.load(f)
                self.spectrumFolder = data['text']
                print("  |--> Initializing spectrum folder text...")
                self.parent.spectrumFolderTextEdit.setText(self.spectrumFolder)
                print("  |--> Initializing tree view: (1) set items...")
                self.treeManager.loadDirectory(self.spectrumFolder)
                print("  |--> Initializing tree view: (2) set items' check states...")
                self.treeManager.load_tree_state(self.model)
            pass
        except FileNotFoundError:
            print("  |--> Do not found 'filefolder_path.json'...")

    def chooseSpectrumFileAction(self):
        """Create a custom action for file selection."""
        action = QAction('Select Spectrum File', self.parent)
        action.triggered.connect(self.chooseSpectrumFile)
        return action

    def chooseSpectrumFile(self):
        """Define a custom slot to handle the 'chooseSpectrumFileAction'."""
        print("Choosing spectrum file...")
        # Open a file dialog to select a file and display the filename in the text edit.
        self.spectrumFile, _ = QFileDialog.getOpenFileName(self.parent, 'Select spectrum file', '',
                                                           'Spectrum file (*.txt *.spe *.h5 *.wxd)')
        if self.spectrumFile:
            print(f"  |--> Select file: {self.spectrumFile}")
            self.parent.spectrumFileTextEdit.setText(self.spectrumFile)

    def chooseSpectrumFolderAction(self):
        """Create a custom action for file folder selection."""
        action = QAction('Select Spectrum Folder', self.parent)
        action.triggered.connect(self.chooseSpectrumFolder)
        return action

    def chooseSpectrumFolder(self):
        """Define a custom slot to handle the 'chooseSpectrumFolderAction'."""
        print("Choosing spectrum file folder...")
        # Open a file folder dialog to select a file folder and display the file folder directory in the text edit.
        try:
            self.spectrumFolder = QFileDialog.getExistingDirectory(self.parent, 'Select directory of files', '')
            print(f"  |--> Select folder: {self.spectrumFolder}")
            self.parent.spectrumFolderTextEdit.setText(self.spectrumFolder)
            self.treeManager.loadDirectory(self.spectrumFolder)
        except Exception as e:
            print(f"  |--> Error choosing spectrum folder: {e}")

    def saveSpectrumFileFolder(self, cache_name_head=''):
        print("Saving spectrum file folder")
        self.cache_name = cache_name_head + '_filefolder_path.json'
        try:
            data = {
                'text': self.spectrumFolder,
            }
            with open(self.cache_name, 'w') as f:  # if not exist, create one
                json.dump(data, f, indent=4)
            print("  |--> Json: 'filefolder_path.json' has been saved")
        except Exception as e:
            print(f'  |--> Error saving spectrum file folder: {e}')


class MainWindowManager:
    """Main Window Actions"""

    def __init__(self, main_window, menuActions, treeManager):
        """Initialization"""
        print("MainWindowManager is instantiating...")
        self.parent = main_window
        self.menuActions = menuActions
        self.treeManager = treeManager
        self.model = self.treeManager.model

        self.savingThread = None
        self.saving_waiting_dialog = None
        self.saving_label = None

    def closeEvent(self, event):
        """Define close event of main window"""
        print("Closing main window...")
        self.cache_name_head = ''
        self.saveCache(self.cache_name_head)

        reply = QMessageBox.question(self.parent, 'Message',
                                     'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("  |--> You choose yes in 2nd message dialog...")
            self.parent.close()
        else:
            print("  |--> You choose no in 2nd message dialog...")
            event.ignore()

    def saveCache(self, cache_name_head):
        """A method for saving tree states and spectum file folder."""
        self.cache_name_head = cache_name_head
        reply = QMessageBox.question(self.parent, 'Confirmation',
                                     'You are to save the cache, continue?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("You choose yes in 1st message dialog...")
            # Show waiting dialog
            self.saveWaitingDialog()

            # Save the tree states, if completed, close waiting dialog
            print("  |--> Setting custom thread...")
            self.savingThread = self.SavingThread(self.menuActions, self.treeManager, self.model, self.cache_name_head)
            self.savingThread.savedSignal.connect(self.closeSavingDialog)
            print("  |--> Setting custom thread completed...")
            self.savingThread.start()
        else:
            print("  |--> You choose no in 1st message dialog...")
            pass

    def saveWaitingDialog(self):
        """A Dialog for showing 'Waiting' message until the tree states have been saved."""
        print("Showing waiting dialog when saving the tree states...")
        # 创建一个等待对话框
        self.saving_waiting_dialog = QWidget()
        self.saving_waiting_dialog.setWindowTitle('Message')
        self.saving_label = QLabel('Saving state config, please wait...')
        self.setFontSize(self.saving_label, 16)  # set font size to 16
        layout = QVBoxLayout()
        layout.addWidget(self.saving_label)
        self.saving_waiting_dialog.setLayout(layout)
        self.saving_waiting_dialog.setGeometry(400, 300, 200, 100)
        self.saving_waiting_dialog.show()

    class SavingThread(QThread):
        """Rewrite run method from QThread"""
        # different to private propeties, signal is propeties of whole class
        # so needn't define like self.saved
        savedSignal = pyqtSignal()

        def __init__(self, menuActions, treeManager, model, cache_name):
            print("SavingThread is instantiating...")
            super().__init__()
            self.menuActions = menuActions
            self.treeManager = treeManager
            self.model = model
            self.cache_name = cache_name

        def run(self):
            # Saving the tree states. This is a time-consuming task
            print("Saving the tree states...")
            if self.cache_name:
                self.treeManager.save_tree_state(self.model, tree_state_name_head=self.cache_name)
                print("  |--> Saving the spectrum file folder...")
                self.menuActions.saveSpectrumFileFolder(cache_name_head=self.cache_name)
            else:
                self.treeManager.save_tree_state(self.model)
                print("  |--> Saving the spectrum file folder...")
                self.menuActions.saveSpectrumFileFolder()

            # Emit finished signal when done, the signal then connect to closeSavingDialog
            print("  |--> Sending the signal that tree states have been saved...")
            self.savedSignal.emit()

    def closeSavingDialog(self):
        print("Closing the waiting dialog...")
        self.saving_waiting_dialog.close()

    def setFontSize(self, label, size):
        font = label.font()  # 获取当前字体
        font.setPointSize(size)  # 设置字体大小
        label.setFont(font)  # 应用字体

    def saveCacheAction(self):
        """A action for saving tree states and spectrum file folder, equal to the saveCache method closeEvent."""
        action = QAction('Save cache to json', self.parent)
        action.triggered.connect(self.saveCache)
        return action


class TreeManager:
    """Tree Actions"""

    def __init__(self, main_window, treeView):
        """Initialization"""
        print("TreeManager is instantiating...")
        self.parent = main_window
        self.treeView = treeView
        self.model = None
        self.folder_dir = QDir()
        self.fileFilters = None

        self.initTree()

    def initTree(self):
        print("Initializing tree...")
        self.model = QStandardItemModel()  # Manage the item in self.treeView through a model
        self.treeView.setModel(self.model)  # Manage the tree actions and slots
        self.treeView.setHeaderHidden(False)  # show header
        # Set custom delegate for the 1st row of tree view
        self.treeView.setItemDelegateForColumn(0, self.CustomDelegate())

    def loadDirectory(self, spectrum_folder):
        """Load directory and show in tree view"""
        print("Loading directory...")
        self.spectrum_folder = spectrum_folder
        try:
            # initialize model
            self.model.clear()  # Clear existing items
            self.model.setHorizontalHeaderLabels(['File Name', '✔', 'File Path', 'Type'])

            # set header of the tree view
            header = self.parent.treeView.header()  # Set the first column to be resizable but with a default width
            header.setSectionResizeMode(0, QHeaderView.Interactive)  # Set the first column to be resizable
            header.resizeSection(0, 700)  # Set width of the first column to 700 pixels
            header.setSectionResizeMode(1, QHeaderView.Interactive)  # Set the first column to be resizable
            header.resizeSection(1, 10)  # Set width of the first column to 700 pixels

            # add items to model
            print("  |--> Adding items to model...")
            self.addFolderItems(self.spectrum_folder, self.model.invisibleRootItem())
        except Exception as e:
            print(f"  |--> Error loading directory: {e}")

    def addFolderItems(self, spectrum_folder, parent_item):
        try:
            self.folder_dir.setPath(spectrum_folder)
            self.fileFilters = ['*.txt', '*.spe', '*.h5', '*.wxd']  # Select the file types to show
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
                parent_item.appendRow([item, item_check, item_file_path, item_type])

            # Add directories without filters
            dirs = QDir(spectrum_folder).entryList(QDir.Dirs | QDir.NoDotAndDotDot)

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
                parent_item.appendRow([item, item_check, item_file_path, item_type])

                # Recursively add subfolders
                self.addFolderItems(self.folder_dir.filePath(folder_name), item)
            # If iterate through all elements, return to previous directory
            self.folder_dir.cdUp()
        except Exception as e:
            print(f"Error adding folder items: {e}")

    class CustomTreeView(QTreeView):
        """Rewrite some slots for double left-clicking, right press and slot: 'check/uncheck all item'."""

        def __init__(self, parent=None):
            super().__init__(parent)

        # rewrite the mouse double click event inherit from parent
        def mouseDoubleClickEvent(self, event):
            # get index of double click position
            index = self.indexAt(event.pos())
            if not index.isValid() or event.button() == Qt.RightButton:
                return

            # get item from model
            item_index = index.sibling(index.row(), 0)
            item_check_index = index.sibling(index.row(), 1)
            item = self.model().itemFromIndex(item_index)
            item_check = self.model().itemFromIndex(item_check_index)
            # Toggle check state for the clicked item
            new_state_is_check = not item_check.checkState()

            if item_check is not None:
                # exchange check state
                item_check.setCheckState(Qt.Checked if new_state_is_check else Qt.Unchecked)

            # Check if item is a folder
            if item.hasChildren():
                self.toggleCheckStateForChildren(item, new_state_is_check)

            # other logic of double clicking
            super().mouseDoubleClickEvent(event)

        def toggleCheckStateForChildren(self, parent_item, check):
            for row in range(parent_item.rowCount()):
                child_item = parent_item.child(row, 0)
                child_item_check = parent_item.child(row, 1)
                child_item_check.setCheckState(Qt.Checked if check else Qt.Unchecked)
                if child_item.hasChildren():
                    self.toggleCheckStateForChildren(child_item, check)

        def mousePressEvent(self, event):
            if event.button() == Qt.RightButton:
                index = self.indexAt(event.pos())
                if not index.isValid():
                    return

                item_index = index.sibling(index.row(), 0)
                item = self.model().itemFromIndex(item_index)
                new_state_is_expand = not self.isExpanded(item_index)
                if item.hasChildren():  # 检查是否是文件夹
                    if new_state_is_expand:
                        self.expand(item_index)  # 展开这一级文件夹
                    else:
                        self.collapse(item_index)
            super().mousePressEvent(event)

    class CustomDelegate(QStyledItemDelegate):
        def paint(self, painter, option, index):
            # Call base class paint method
            super().paint(painter, option, index)

            # Get the item and its check state
            item_index = index.siblingAtColumn(0)
            item = index.model().itemFromIndex(item_index)
            item_check_index = index.siblingAtColumn(1)
            item_check = index.model().itemFromIndex(item_check_index)

            item_type_index = index.siblingAtColumn(3)
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

    def treeCollapse(self):
        """Define a slot to collapse all nodes in the tree view."""
        print("Collapsing all nodes in the tree view...")
        self.treeView.collapseAll()

    def allItemUncheck(self):
        """Define a slot to uncheck all items in 2nd column(item_check) in the tree view."""
        print("Unchecking all items in the tree view...")
        parent_item = self.model.invisibleRootItem()
        self.childItemUncheck(parent_item)

    def childItemUncheck(self, parent_item):
        """To uncheck all child items, grandchild items..."""
        for row in range(parent_item.rowCount()):
            child_item = parent_item.child(row, 0)
            child_item_check = parent_item.child(row, 1)
            child_item_check.setCheckState(False)
            if child_item.hasChildren():
                self.childItemUncheck(child_item)

    def toggleShowTree(self):
        print("Toggling tree view visibility...")
        try:
            if self.treeView.isVisible():
                self.treeView.hide()
            else:
                self.treeView.show()
        except Exception as e:
            print(f"  |--> Error toggling show tree: {e}")

    """Four methods for saving tree state"""
    def save_tree_state(self, model, tree_state_name_head=''):
        """A method to save tree items' and their check status to a json file."""
        print("Saving the tree states!")
        self.model = model
        self.tree_state_name = tree_state_name_head + '_tree_state.json'
        # Save the root path and check states of all items
        root_item = self.model.invisibleRootItem()
        data = self.get_item_data(root_item)

        # Save data to a json file
        try:
            with open(self.tree_state_name, 'w') as f:  # if not exist, create one
                json.dump(data, f, indent=4)
            print("  |--> Json: 'tree_state.json' has been saved.")
        except Exception as e:
            print(f'  |--> Error saving tree state: {e}')

    def get_item_data(self, item):
        """Get all tree items' state data."""
        try:
            item_index = item.index()
            item_check_index = item_index.siblingAtColumn(1)
            item_check = item.model().itemFromIndex(item_check_index)
            item_check_data = Qt.Checked if item_check and item_check.checkState() == Qt.Checked else False

            item_file_path_index = item_index.siblingAtColumn(2)
            item_file_path = item.model().itemFromIndex(item_file_path_index)
            file_path = item_file_path.text() if item_file_path else ''

            item_type_index = item_index.siblingAtColumn(3)
            item_type = item.model().itemFromIndex(item_type_index)
            item_type = item_type.text() if item_type else ''

            data = {
                'text': item.text(),
                'checked': item_check_data,
                'file_path': file_path,
                'type': item_type,
                'children': []
            }

            for row in range(item.rowCount()):
                child_item = item.child(row, 0)
                child_item_check = item.child(row, 1)

                if child_item:
                    child_item_data = self.get_item_data(child_item)
                    data['children'].append(child_item_data)
        except Exception as e:
            print(f"Error getting item data: {e}")
        return data

    def load_tree_state(self, model, tree_state_name='_tree_state.json'):
        """A method to load tree items from a json file."""
        print("Loading tree state from json...")
        self.model = model
        self.tree_state_name = tree_state_name

        # Load data from a json file
        try:
            with open(self.tree_state_name, 'r') as f:
                print("  |--> Opening '_tree_state.json'...")
                data = json.load(f)
                self.set_item_data(self.model.invisibleRootItem(), data)
        except FileNotFoundError:
            print("  |--> Do not found 'tree_state.json'...")

    def set_item_data(self, item, data):
        """Recursively set the item data from JSON to the tree."""
        for row in range(item.rowCount()):
            # get child item's check item
            child_item = item.child(row, 0)
            child_item_check = item.child(row, 1)
            child_item_data = data['children'][row]

            child_item_check.setCheckState(child_item_data['checked'])

            # if child_item has at least one child, repeat.
            if child_item.rowCount():
                self.set_item_data(child_item, child_item_data)


class ListManager:
    def __init__(self, main_window, treeManager, list_widget):
        """Initialization"""
        print("MenuActions is instantiating...")
        self.parent = main_window
        self.treeManager = treeManager
        self.model = self.treeManager.model
        self.listWidget = list_widget

        self.checked_files_data = []
        self.initList()

    def initList(self):
        # self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        pass

    def importCheckedFiles(self):
        """A method that import all checked items(except folder) to a list"""
        try:
            self.checked_files_data = []  # clear cache every time
            self.listWidget.clear()
            root_item = self.model.invisibleRootItem()
            get_checked_files_data = self.get_checked_files_data(root_item)
            print(get_checked_files_data)
            # items = ["Item 1", "Item 2", "Item 3", "Item 4"]
            for file_data in get_checked_files_data:
                file_name = QtWidgets.QListWidgetItem(file_data['text'])
                self.listWidget.addItem(file_name)
            # data = self.get_checked_files_data(root_item)
        except Exception as e:
            print(f"  |--> Error importing checked files: {e}")

    def get_checked_files_data(self, item):
        for row in range(item.rowCount()):
            # get child item's check item
            child_item = item.child(row, 0)
            child_item_check = item.child(row, 1)
            chile_item_type = item.child(row, 3)
            if chile_item_type:
                chile_item_type = chile_item_type.text()
            if child_item_check.checkState() and chile_item_type == 'File':
                data = {
                    'text': child_item.text(),
                    'path': []
                }
                self.checked_files_data.append(data)
            if child_item.hasChildren():
                self.get_checked_files_data(child_item)
        return self.checked_files_data

    class CustomListWidget(QtWidgets.QListWidget):
        def __init__(self):
            super().__init__()
            # enable dragging
            self.setDragEnabled(True)
            self.setDropIndicatorShown(True)
            self.setDefaultDropAction(QtCore.Qt.MoveAction)
            self.setAcceptDrops(True)

        def mouseDoubleClickEvent(self, e):
            # test start
            print("the first items")
            print(self.item(0).text())
            # test ends


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMainWindow()
    sys.exit(app.exec_())