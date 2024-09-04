import sys
# main window objects
from PyQt5.QtWidgets import (QLabel, QTextEdit, QPushButton, QComboBox, QSpinBox,
                             QMainWindow, QApplication, QWidget,
                             QHBoxLayout, QVBoxLayout, QGridLayout)
from PyQt5.QtCore import Qt
# math
import matplotlib
# my modules
from src.menu_actions import MenuActions
from src.tree_manager import TreeManager
from src.list_manager import ListManager
from src.figure_manager import FigureManager
from src.roi_manager import RoiManager
from src.figure_widget import FigureWidget
from src.histogram_widget import HistogramWidget
from src.output_redirector import OutputRedirector
matplotlib.use("Qt5Agg")


class MyMainWindow(QMainWindow):

    def __init__(self):
        print("MyMainWindow is instantiating...")
        super().__init__()
        """Objects"""
        self.menubar = None
        self.fileMenu = None
        self.cacheMenu = None

        # left_hbox1
        self.spectrumFileLabel = None
        self.spectrumFileTextEdit = None

        # left_hbox2
        self.spectraFolderLabel = None
        self.spectraFolderTextEdit = None

        # tree
        self.treeView = None
        self.treeManager = None

        # list
        self.listWidget = None
        self.listManager = None

        # menuActions
        self.menuActions = None

        # left_hbox3
        self.treeCollapseButton = None
        self.allItemUncheckButton = None

        # left_hbox4
        self.toggleShowTreeButton = None
        self.importCheckedFilesButton = None

        # right_hbox1
        self.histogramWidget = None
        self.roiManager = None
        self.figureWidget = None
        self.figureManager = None

        # right_box2
        self.layoutComboBox = None
        self.outputTextEdit = None
        self.showRoiButton = None
        self.roiUpperSpinBox = None
        self.roiLowerSpinBox = None
        self.showOutputButton = None
        self.saveFigureButton = None

        # slot flag
        self.show_layout_flag = None
        self.show_roi_flag_now = False
        self.draw_rect_flag = None
        self.show_flag = None
        """Initialize ui"""
        self.initUI()

    def initUI(self):
        self.createUiObjects()
        self.setLayout()

    def createUiObjects(self):
        """ Set main window parameters"""
        print("Initializing UI")
        try:
            # set window position, title and so on...
            self.setGeometry(200, 200, 2400, 1200)
            self.setWindowTitle('SpectraPro')
            self.statusBar().showMessage('Ready')

            """Create menubar objects"""
            # create objects
            self.menubar = self.menuBar()
            self.fileMenu = self.menubar.addMenu('&File')
            self.cacheMenu = self.menubar.addMenu('&Cache')

            """Create main window objects"""
            # right_hbox2
            # self.outputTextEdit = QTextEdit()
            # self.outputTextEdit.setReadOnly(True)
            # sys.stdout = OutputRedirector(self.outputTextEdit)
            # sys.stderr = OutputRedirector(self.outputTextEdit)

            # left_hbox1
            self.spectrumFileLabel = QLabel('File path')
            self.spectrumFileTextEdit = QTextEdit()
            self.spectrumFileTextEdit.setReadOnly(True)  # Set to read-only for file path display
            self.spectrumFileTextEdit.setFixedHeight(30)  # Set height for QTextEdit

            # left_hbox2
            self.spectraFolderLabel = QLabel('File folder')
            self.spectraFolderTextEdit = QTextEdit()
            self.spectraFolderTextEdit.setReadOnly(True)  # Set to read-only for file path display
            self.spectraFolderTextEdit.setFixedHeight(30)  # Set height for QTextEdit

            # tree
            self.treeView = TreeManager.CustomTreeView()
            self.treeView.setMinimumWidth(1000)
            self.treeManager = TreeManager(self, self.treeView)  # Manage the tree actions and slots by self.treeManager

            """Add custom actions to menu and connect to slots."""
            self.menuActions = MenuActions(self, self.treeManager)
            self.fileMenu.addAction(self.menuActions.select_spectrum_file_action())  # add a custom action instant
            self.fileMenu.addAction(self.menuActions.select_spectra_file_folder_action())
            self.cacheMenu.addAction(self.menuActions.save_cache_action())
            self.cacheMenu.addAction(self.menuActions.load_cache_action())

            # right_hbox1
            self.histogramWidget = HistogramWidget(width=8, height=2, dpi=100)
            self.roiManager = RoiManager(self.histogramWidget, width=250, height=850)
            self.figureWidget = FigureWidget(self, self.histogramWidget, width=12, height=8, dpi=100)
            self.figureManager = FigureManager(self.figureWidget, width=1250, height=850)

            # right_hbox2
            self.layoutComboBox = QComboBox(self)
            self.layoutComboBox.addItem("Image")
            self.layoutComboBox.addItem("Graph")
            self.layoutComboBox.currentIndexChanged.connect(self.figureWidget.toggle_image_and_graph)
            self.layoutComboBox.setFixedHeight(50)
            self.layoutComboBox.setFixedWidth(150)

            self.showRoiButton = QPushButton("Show ROI")
            self.showRoiButton.clicked.connect(self.figureWidget.toggle_show_rect)
            self.showRoiButton.setFixedHeight(50)
            self.showRoiButton.setFixedWidth(150)

            self.roiUpperSpinBox = QSpinBox()
            self.roiUpperSpinBox.setEnabled(False)
            self.roiUpperSpinBox.setFixedHeight(50)
            self.roiUpperSpinBox.setFixedWidth(70)
            self.roiUpperSpinBox.valueChanged.connect(self.figureWidget.change_rect_maxlim)
            self.roiLowerSpinBox = QSpinBox()
            self.roiLowerSpinBox.setEnabled(False)
            self.roiLowerSpinBox.setFixedHeight(50)
            self.roiLowerSpinBox.setFixedWidth(70)
            self.roiLowerSpinBox.valueChanged.connect(self.figureWidget.change_rect_mimlim)

            self.showOutputButton = QPushButton("Show Layout")
            # self.showOutputButton.clicked.connect(self.toggle_show_layout)
            self.showOutputButton.setFixedHeight(50)
            self.showOutputButton.setFixedWidth(150)

            self.saveFigureButton = QPushButton("Save Figure")
            self.saveFigureButton.clicked.connect(self.figureWidget.save_current_figure)
            self.saveFigureButton.setFixedHeight(50)
            self.saveFigureButton.setFixedWidth(150)

            # list
            self.listWidget = ListManager.CustomListWidget(self.figureWidget)
            self.listWidget.setMinimumWidth(1000)
            self.listManager = ListManager(self, self.listWidget, self.treeManager, self.figureWidget)

            # left_hbox3
            self.treeCollapseButton = QPushButton('Collapse All')  # add a button to collapse all nodes
            self.treeCollapseButton.clicked.connect(self.treeManager.collapse_tree)
            self.allItemUncheckButton = QPushButton('Uncheck All')  # add a button to uncheck all items
            self.allItemUncheckButton.clicked.connect(self.treeManager.uncheck_all_items)

            # left_hbox4
            self.toggleShowTreeButton = QPushButton("Show Tree")  # add a button to show/hide treeview
            self.toggleShowTreeButton.setChecked(True)  # Set initial status
            self.toggleShowTreeButton.clicked.connect(self.treeManager.toggle_show_tree)
            self.importCheckedFilesButton = QPushButton("Import Checked Files")  # add a button to show/hide checked files
            self.importCheckedFilesButton.clicked.connect(self.listManager.import_checked_files)
        except Exception as e:
            print(f"Error main.createUiObjects:\n  |--> {e}")

    def setLayout(self):
        """box manager"""
        try:
            # left box
            left_hbox1 = QHBoxLayout()
            left_hbox1.addWidget(self.spectrumFileLabel)
            left_hbox1.addWidget(self.spectrumFileTextEdit)

            left_hbox2 = QHBoxLayout()
            left_hbox2.addWidget(self.spectraFolderLabel)
            left_hbox2.addWidget(self.spectraFolderTextEdit)

            left_hbox3 = QHBoxLayout()
            left_hbox3.addWidget(self.treeCollapseButton)
            left_hbox3.addWidget(self.allItemUncheckButton)

            left_hbox4 = QHBoxLayout()
            left_hbox4.addWidget(self.toggleShowTreeButton)
            left_hbox4.addWidget(self.importCheckedFilesButton)

            left_vbox = QVBoxLayout()
            left_vbox.addLayout(left_hbox1)
            left_vbox.addLayout(left_hbox2)
            left_vbox.addWidget(self.treeView)
            left_vbox.addWidget(self.listWidget)
            left_vbox.addLayout(left_hbox3)
            left_vbox.addLayout(left_hbox4)

            # right_hbox1
            right_hbox1 = QHBoxLayout()
            right_hbox1.addWidget(self.figureManager)
            right_hbox1.addWidget(self.roiManager)

            # roi grid box
            roi_grid_box = QGridLayout()
            roi_grid_box.addWidget(self.showRoiButton, 0, 0, 1, 2)
            roi_grid_box.addWidget(self.roiUpperSpinBox, 1, 0)
            roi_grid_box.addWidget(self.roiLowerSpinBox, 1, 1)

            # right vbox1
            right_vbox1 = QVBoxLayout()
            right_vbox1.addWidget(self.layoutComboBox)
            right_vbox1.addLayout(roi_grid_box)
            right_vbox1.addWidget(self.showOutputButton)
            right_vbox1.addWidget(self.saveFigureButton)

            right_vbox1.setAlignment(self.layoutComboBox, Qt.AlignLeft)
            right_vbox1.setAlignment(roi_grid_box, Qt.AlignLeft)
            right_vbox1.setAlignment(self.showRoiButton, Qt.AlignLeft)
            right_vbox1.setAlignment(self.showOutputButton, Qt.AlignLeft)
            right_vbox1.setAlignment(self.saveFigureButton, Qt.AlignLeft)

            # right hbox2
            right_hbox2 = QHBoxLayout()
            right_hbox2.addLayout(right_vbox1)
            # right_hbox2.addStretch(1)
            # right_hbox2.addWidget(self.outputTextEdit)

            # right box
            right_vbox = QVBoxLayout()
            right_vbox.addLayout(right_hbox1)
            right_vbox.addLayout(right_hbox2)

            main_hbox = QHBoxLayout()
            main_hbox.addLayout(left_vbox)
            main_hbox.addLayout(right_vbox)

            central_widget = QWidget()
            central_widget.setLayout(main_hbox)
            self.setCentralWidget(central_widget)

            self.show()
        except Exception as e:
            print(f"Error main.setLayout:\n  |--> {e}")

    def toggle_show_layout(self):
        try:
            if self.show_layout_flag:
                self.outputTextEdit.setVisible(False)
                self.show_layout_flag = 0
            else:
                self.outputTextEdit.setVisible(True)
                self.show_layout_flag = 1
        except Exception as e:
            print(f"Error main.toggle_show_layout:\n  |--> {e}")

    def toggle_show_roi(self, draw_rect_flag, show_flag, figure_xylim):
        try:
            self.draw_rect_flag = draw_rect_flag
            self.show_flag = show_flag
            self.figure_xylim = figure_xylim
            if self.show_roi_flag_now:
                self.roiUpperSpinBox.setEnabled(False)
                self.roiLowerSpinBox.setEnabled(False)
                self.show_roi_flag_now = False
            else:
                if self.draw_rect_flag is True and self.show_flag == 'image':
                    self.roiUpperSpinBox.setEnabled(True)
                    self.roiLowerSpinBox.setEnabled(True)
                    print(figure_xylim)
                    self.roiUpperSpinBox.setMinimum(self.figure_xylim[2])
                    self.roiUpperSpinBox.setMaximum(self.figure_xylim[3])
                    self.roiLowerSpinBox.setMinimum(self.figure_xylim[2])
                    self.roiLowerSpinBox.setMaximum(self.figure_xylim[3])
                    self.roiUpperSpinBox.setValue(self.figure_xylim[3])
                    self.roiLowerSpinBox.setValue(self.figure_xylim[2])
                    self.show_roi_flag_now = True
        except Exception as e:
            print(f"Error main.toggle_show_roi:\n  |--> {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMainWindow()
    sys.exit(app.exec_())