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
from threading import Thread


class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.spectrumFolder = None
        self.treeActions = TreeActions(self)
        self.menuActions = MenuActions(self)
        self.initUI()

    def initUI(self):
        # set window position, title and so on...
        self.setGeometry(200, 200, 1200, 900)
        self.setWindowTitle('SpectraPro')
        self.statusBar().showMessage('Ready')

        # create manubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        colorMenu = menubar.addMenu('&Color')

        # connect menu action
        fileMenu.addAction(self.menuActions.chooseSpectrumFileAction())
        fileMenu.addAction(self.menuActions.chooseSpectrumFolderAction())

        """set main window"""
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
        # add a treeview and initialize it
        self.treeView = CustomTreeView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['File Name', 'Select'])

        # initial model from json
        self.treeActions.load_tree_state(self.model)

        self.treeView.setModel(self.model)
        self.treeView.setHeaderHidden(False)  # show header
        # Set custom delegate for the 1st row of tree view
        self.treeView.setItemDelegateForColumn(0, self.treeActions.CustomDelegate())

        # add a button to collapse the treeview
        self.treeCollapseButton = QPushButton('Collapse All')
        self.treeCollapseButton.clicked.connect(self.treeActions.treeCollapse)

        # add a button to uncheck all items
        self.allItemUncheckButton = QPushButton('Uncheck All')
        self.allItemUncheckButton.clicked.connect(self.treeActions.allItemUncheck)

        """box manager"""
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.spectrumFileLabel)
        hbox1.addWidget(self.spectrumFileTextEdit)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.spectrumFolderLabel)
        hbox2.addWidget(self.spectrumFolderTextEdit)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.treeCollapseButton)
        hbox3.addWidget(self.allItemUncheckButton)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.treeView)
        vbox.addLayout(hbox3)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        self.show()

    def closeEvent(self, event):
        # pass the filefolder
        self.mainWindowActions = MainWindowActions(self, self.treeActions, self.model, self.spectrumFolder)
        # deal with close event by self.actions
        self.mainWindowActions.closeEvent(event)


class MenuActions:
    """Menu Actions"""
    def __init__(self, parent):
        self.parent = parent

    def chooseSpectrumFileAction(self):
        action = QAction('Choose Spectrum File', self.parent)
        action.triggered.connect(self.chooseSpectrumFile)
        return action

    def chooseSpectrumFile(self):
        # Open file dialog to choose a file, and show filename in textedit
        self.spectrumFile, _ = QFileDialog.getOpenFileName(self.parent, 'Choose spectrum file', '',
                                                      'Spectrum file (*.txt *.spe *.h5 *.wxd)')
        if self.spectrumFile:
            print(f"Selected file: {self.spectrumFile}")
            self.parent.spectrumFileTextEdit.setText(self.spectrumFile)

    def chooseSpectrumFolderAction(self):
        action = QAction('Choose Spectrum Folder', self.parent)
        action.triggered.connect(self.chooseSpectrumFolder)
        return action

    def chooseSpectrumFolder(self):
        try:
            # Open folder dialog to choose a directory
            self.spectrumFolder = QFileDialog.getExistingDirectory(self.parent, 'Choose directory of files', '')
            if self.spectrumFolder:
                print(f"Selected folder: {self.spectrumFolder}")
                # Selecte the directory
                self.parent.spectrumFolderTextEdit.setText(self.spectrumFolder)
                self.parent.treeActions.loadDirectory(self.spectrumFolder)
                self.parent.spectrumFolder = self.spectrumFolder
        except Exception as e:
            print(f"Error choosing spectrum folder: {e}")


class MainWindowActions:
    """Main Window Actions"""
    def __init__(self, main_window, tree_actions, model, filefolder):
        self.main_window = main_window
        self.tree_actions = tree_actions
        self.model = model
        self.filefolder = filefolder
        self.waiting_dialog = None
        # self.tree_actions.

    """set close event of main window"""
    def closeEvent(self, event):
        reply1 = QMessageBox.question(self.main_window, 'Message',
                                      'Save the tree state before quit?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply1 == QMessageBox.Yes:
            # Show waiting dialog
            self.savingDialog()
            self.savingThread = self.SavingThread(self.tree_actions, self.model, self.filefolder)
            self.savingThread.savedSignal.connect(self.closeSavingDialog)
            self.savingThread.start()
        else:
            pass
        reply2 = QMessageBox.question(self.main_window, 'Message',
                                      'Are you sure you want to quit?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply2 == QMessageBox.Yes:
            self.main_window.close()
        else:
            event.ignore()

    def savingDialog(self):
        # 创建一个等待对话框
        self.saving_dialog = QWidget()
        self.saving_dialog.setWindowTitle('Saving')
        self.saving_label = QLabel('Saving state config, please wait...')
        self.setFontSize(self.saving_label, 16)  # 设置字体大小为16
        layout = QVBoxLayout()
        layout.addWidget(self.saving_label)
        self.saving_dialog.setLayout(layout)
        self.saving_dialog.setGeometry(400, 300, 200, 100)
        self.saving_dialog.show()

    # rewrite run method from QThread
    class SavingThread(QThread):
        # different to private propeties, signal is propeties of hole class
        # so needn't define like self.saved
        savedSignal = pyqtSignal()

        def __init__(self, tree_actions, model, filefolder):
            super().__init__()
            self.tree_actions = tree_actions
            self.model = model
            self.filefolder = filefolder

        def run(self):
            # Perform the time-consuming task
            self.tree_actions.save_tree_state(self.model, self.filefolder)
            # Emit finished signal when done
            # the signal then connect to closeSavingDialog
            self.savedSignal.emit()

    def closeSavingDialog(self):
        self.saving_dialog.close()

    def setFontSize(self, label, size):
        font = label.font()  # 获取当前字体
        font.setPointSize(size)  # 设置字体大小
        label.setFont(font)  # 应用字体


class CustomTreeView(QTreeView):
    """Custom Tree View"""
    def __init__(self, parent=None):
        super().__init__(parent)

    # rewrite the mouse double click event inherit from parent
    def mouseDoubleClickEvent(self, event):
        # get index of double click position
        index = self.indexAt(event.pos())
        if not index.isValid() or event.button() == Qt.RightButton:
            return

        # get item frome model
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


class TreeActions:
    """Tree Actions"""
    def __init__(self, parent):
        self.parent = parent
        self.fileFilters = None
        self.dir = QDir()

    def loadDirectory(self, folder):
        try:
            self.parent.model.clear()  # Clear existing items
            self.parent.model.setHorizontalHeaderLabels(['File Name', 'Select'])
            header = self.parent.treeView.header()  # Set the first column to be resizable but with a default width
            header.setSectionResizeMode(0, QHeaderView.Interactive)  # Set the first column to be resizable
            header.resizeSection(0, 700)  # Set the initial width of the first column to 500 pixels

            self.addFolderItems(folder, self.parent.model.invisibleRootItem())
        except Exception as e:
            print(f"Error loading directory: {e}")

    def addFolderItems(self, folder, parent_item):
        self.if_cdUp = 0
        try:
            self.dir.setPath(folder)
            self.fileFilters = ['*.txt', '*.spe', '*.h5', '*.wxd']  # Define the file types to show
            self.dir.setNameFilters(self.fileFilters)

            # Add files with filters
            files = self.dir.entryList(QDir.Files | QDir.NoDotAndDotDot)
            for file_name in self.dir.entryList(QDir.Files | QDir.NoDotAndDotDot):
                item = QStandardItem(file_name)
                item.setEditable(False)
                check_item = QStandardItem()
                check_item.setCheckable(True)
                check_item.setEditable(False)
                parent_item.appendRow([item, check_item])

            # Add directories without filters
            dirs = QDir(folder).entryList(QDir.Dirs | QDir.NoDotAndDotDot)

            for folder_name in dirs:
                folder_item = QStandardItem(folder_name)
                folder_item.setEditable(False)
                folder_item.setIcon(QIcon.fromTheme('folder'))
                check_item = QStandardItem()
                check_item.setCheckable(True)
                check_item.setEditable(False)
                parent_item.appendRow([folder_item, check_item])

                # Recursively add subfolders
                self.addFolderItems(self.dir.filePath(folder_name), folder_item)
        except Exception as e:
            print(f"Error adding folder items: {e}")

        self.dir.cdUp()

    def treeCollapse(self):
        """Collapsing all nodes in the tree view."""
        self.parent.treeView.collapseAll()

    def allItemUncheck(self):
        parent_item = self.parent.model.invisibleRootItem()
        self.childItemUncheck(parent_item)

    def childItemUncheck(self, parent_item):
        for row in range(parent_item.rowCount()):
            child_item = parent_item.child(row, 0)
            child_item_check = parent_item.child(row, 1)
            child_item_check.setCheckState(False)
            if child_item.hasChildren():
                self.childItemUncheck(child_item)

    class CustomDelegate(QStyledItemDelegate):
        def paint(self, painter, option, index):
            # Call base class paint method
            super().paint(painter, option, index)

            # Get the item and its check state
            item_index = index.sibling(index.row(), 0)
            item = index.model().itemFromIndex(item_index)
            item_check_index = index.sibling(index.row(), 1)
            item_check = index.model().itemFromIndex(item_check_index)
            if not item_check:
                return

            if item_check.checkState() == Qt.Checked:
                # Highlight the item if it's checked
                painter.save()
                painter.fillRect(option.rect,
                                 QColor(144, 238, 144, alpha=150))  # Light green background for checked items
                painter.restore()

    """Four methods for saving tree state"""

    def save_tree_state(self, model, filefolder):
        try:
            self.model = model
            self.filefolder = filefolder
            # Save the root path and check states of all items
            root_item = self.model.invisibleRootItem()
            data = self.get_item_data(root_item)

            # Save data to a JSON file
            with open('tree_state.json', 'w') as f:  # if not exist, create one
                json.dump(data, f, indent=4)
            print("Json has been saved.")
            # Save filepath to a JSON file
            with open('file_path.json', 'w') as f:  # if not exist, create one
                json.dump(self.filefolder, f, indent=4)
            print('Filefolder has been saved')
        except Exception as e:
            print(f'Error saving tree state: {e}')

    def get_item_data(self, item):
        item_check_data = None
        item_index = item.index()
        item_check_index = item_index.sibling(item_index.row(), 1)
        item_check = item.model().itemFromIndex(item_check_index)

        item_check_data = Qt.Checked if item_check and item_check.checkState() == Qt.Checked else False

        data = {
            'text': item.text(),
            'checked': item_check_data,
            'children': []
        }

        for row in range(item.rowCount()):
            child_item = item.child(row, 0)
            child_item_check = item.child(row, 1)

            if child_item:
                child_item_data = self.get_item_data(child_item)
                child_item_check_data = Qt.Checked if child_item_check and child_item_check.checkState() == Qt.Checked else False
                data['children'].append(child_item_data)
        return data

    def load_tree_state(self, model):
        print("Loading tree state from json...")
        self.model = model
        # Load from a JSON file
        try:
            with open('tree_state.json', 'r') as f:
                data = json.load(f)
            self.set_item_data(self.model.invisibleRootItem(), data)
        except FileNotFoundError:
            print("No saved state found.")

    # def set_item_data(self, item, data):
    #     item_index = item.index()
    #     item_check_index = item_index.sibling(item_index.row(), 1)
    #     item_check = item.model().itemFromIndex(item_check_index)
    #
    #     item.setText(data['text'])
    #     item_check.checkState(data['checked'])
    #
    #     if not item_check:
    #         item_check = QStandardItem()
    #         check_item.setCheckable(True)
    #         item.appendRow([item, check_item])
    #     check_item.setCheckState(Qt.Checked if data['checked'] else Qt.Unchecked)
    #
    #     for child_data in data['children']:
    #         child_item = QStandardItem()
    #         self.set_item_data(child_item, child_data)
    #         item.appendRow([child_item, QStandardItem()])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMainWindow()
    sys.exit(app.exec_())
