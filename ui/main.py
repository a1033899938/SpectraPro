import sys
# main window objects
from PyQt5.QtWidgets import (QLabel, QTextEdit, QPushButton, QComboBox, QSpinBox,
                             QMainWindow, QApplication, QWidget,
                             QHBoxLayout, QVBoxLayout, QGridLayout, QDesktopWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
# math
import matplotlib
# my modules
from src.ui.menu_actions import MenuActions
from src.ui.tree_manager import TreeManager
from src.ui.list_manager import ListManager
from src.ui.figure_manager import FigureManager
from src.ui.roi_manager import RoiManager
from src.ui.figure_widget import FigureWidget
from src.ui.histogram_widget import HistogramWidget
from src.ui.output_redirector import OutputRedirector
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
        self.show_roi_flag = False
        self.draw_rect_flag = None
        self.show_flag = None
        self.spinbox_lim = None
        self.spinbox_max = None
        self.spinbox_min = None

        """"""
        self.screen = QDesktopWidget().screenGeometry()  # 自动适应屏幕宽高
        self.screen_width = self.screen.width()
        self.screen_height = self.screen.height()
        self.window_width = int(self.screen_width*0.7)
        self.window_height = int(self.screen_height*0.7 - 50)

        self.base_figure_height = int(self.window_height/16)*16
        self.base_button_height = int(self.window_height/24)
        self.base_text_height = int(self.base_button_height / 5 * 3)
        self.base_tree_width = int(self.screen_width/2.5)
        """Initialize ui"""
        self.initUI()

    def initUI(self):
        self.setGlobalFont()
        self.createUiObjects()
        self.setLayout()

    def createUiObjects(self):
        """ Set main window parameters"""
        print("Initializing UI")
        try:
            # set window position, title and so on...
            self.setGeometry(int(self.window_width*0.1), int(self.window_height*0.1),
                             self.window_width, self.window_height)
            self.setWindowTitle('SpectraPro')
            self.statusBar().showMessage('Ready')

            """Create menubar objects"""
            # create objects
            self.menubar = self.menuBar()
            self.fileMenu = self.menubar.addMenu('&File')
            self.cacheMenu = self.menubar.addMenu('&Cache')

            """Create main window objects"""
            # right_hbox2
            self.outputTextEdit = QTextEdit()
            self.outputTextEdit.setReadOnly(True)
            sys.stdout = OutputRedirector(self.outputTextEdit)
            sys.stderr = OutputRedirector(self.outputTextEdit)

            # left_hbox1
            self.spectrumFileLabel = QLabel('File path')
            self.spectrumFileTextEdit = QTextEdit()
            self.spectrumFileTextEdit.setReadOnly(True)  # Set to read-only for file path display
            self.spectrumFileTextEdit.setFixedHeight(self.base_text_height)  # Set height for QTextEdit

            # left_hbox2
            self.spectraFolderLabel = QLabel('File folder')
            self.spectraFolderTextEdit = QTextEdit()
            self.spectraFolderTextEdit.setReadOnly(True)  # Set to read-only for file path display
            self.spectraFolderTextEdit.setFixedHeight(self.base_text_height)  # Set height for QTextEdit

            # tree
            self.treeView = TreeManager.CustomTreeView()
            self.treeView.setMinimumWidth(self.base_tree_width)
            self.treeManager = TreeManager(self, self.treeView)  # Manage the tree actions and slots by self.treeManager

            """Add custom actions to menu and connect to slots."""
            self.menuActions = MenuActions(self, self.treeManager)
            self.fileMenu.addAction(self.menuActions.select_spectrum_file_action())  # add a custom action instant
            self.fileMenu.addAction(self.menuActions.select_spectra_file_folder_action())
            self.cacheMenu.addAction(self.menuActions.save_cache_action())
            self.cacheMenu.addAction(self.menuActions.load_cache_action())

            # right_hbox1
            width_fW = self.base_figure_height
            height_fW = width_fW/4*3
            width_hW = height_fW
            height_hW = width_hW/4
            self.histogramWidget = HistogramWidget(width=width_hW/100,
                                                   height=height_hW/100,
                                                   dpi=100)
            self.roiManager = RoiManager(self.histogramWidget)
            self.figureWidget = FigureWidget(self, self.histogramWidget,
                                             width=width_fW/100,
                                             height=height_fW/100,
                                             dpi=100)
            self.figureManager = FigureManager(self.figureWidget)

            # right_hbox2
            self.layoutComboBox = QComboBox(self)
            self.layoutComboBox.addItem("Image")
            self.layoutComboBox.addItem("Graph")
            self.layoutComboBox.addItem("Image&Graph")
            self.layoutComboBox.currentIndexChanged.connect(self.figureWidget.toggle_image_and_graph)
            self.layoutComboBox.setFixedHeight(self.base_button_height)
            self.layoutComboBox.setFixedWidth(self.base_button_height*3)

            self.showRoiButton = QPushButton("Show ROI")
            self.showRoiButton.clicked.connect(self.figureWidget.toggle_show_rect)
            self.showRoiButton.setFixedHeight(self.base_button_height)
            self.showRoiButton.setFixedWidth(self.base_button_height*3)

            self.roiUpperSpinBox = QSpinBox()
            # self.roiUpperSpinBox.setEnabled(False)
            self.roiUpperSpinBox.setFixedHeight(self.base_button_height)
            self.roiUpperSpinBox.setFixedWidth(self.base_text_height*2)
            self.roiUpperSpinBox.valueChanged.connect(self.figureWidget.change_rect_maxlim)
            self.roiLowerSpinBox = QSpinBox()
            # self.roiLowerSpinBox.setEnabled(False)
            self.roiLowerSpinBox.setFixedHeight(self.base_button_height)
            self.roiLowerSpinBox.setFixedWidth(self.base_text_height*2)
            self.roiLowerSpinBox.valueChanged.connect(self.figureWidget.change_rect_minlim)

            self.showOutputButton = QPushButton("Show Layout")
            self.showOutputButton.clicked.connect(self.toggle_show_layout)
            self.showOutputButton.setFixedHeight(self.base_button_height)
            self.showOutputButton.setFixedWidth(self.base_button_height*3)

            self.saveFigureButton = QPushButton("Save Figure")
            self.saveFigureButton.clicked.connect(self.figureWidget.save_current_figure)
            self.saveFigureButton.setFixedHeight(self.base_button_height)
            self.saveFigureButton.setFixedWidth(self.base_button_height*3)

            # list
            self.listWidget = ListManager.CustomListWidget(self.figureWidget)
            self.listWidget.setMinimumWidth(self.base_tree_width)
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
            right_hbox2.addWidget(self.outputTextEdit)

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

    # def toggle_show_roi(self, draw_rect_flag, show_flag):
    #     try:
    #         self.draw_rect_flag = draw_rect_flag
    #         self.show_flag = show_flag
    #         if self.show_roi_flag:
    #             self.roiUpperSpinBox.setEnabled(False)
    #             self.roiLowerSpinBox.setEnabled(False)
    #             self.show_roi_flag = False
    #         else:
    #             if self.draw_rect_flag is True and self.show_flag == 'image':
    #                 self.roiUpperSpinBox.setEnabled(True)
    #                 self.roiLowerSpinBox.setEnabled(True)
    #                 self.show_roi_flag = True
    #     except Exception as e:
    #         print(f"Error main.toggle_show_roi:\n  |--> {e}")

    def set_spin_box_lim(self, canvas_origin_xylim):
        self.spinbox_lim = canvas_origin_xylim
        self.roiUpperSpinBox.setMinimum(self.spinbox_lim[2])
        self.roiUpperSpinBox.setMaximum(self.spinbox_lim[3])
        self.roiLowerSpinBox.setMinimum(self.spinbox_lim[2])
        self.roiLowerSpinBox.setMaximum(self.spinbox_lim[3])

        if self.spinbox_max and self.spinbox_min:
            self.roiUpperSpinBox.setValue(self.spinbox_max)
            self.roiLowerSpinBox.setValue(self.spinbox_min)

    def receive_spinbox_value_from_figure(self, value, tag='max'):
        if tag == 'max':
            self.spinbox_max = value
        elif tag == 'min':
            self.spinbox_min = value
        else:
            print("input: tag must be 'max' or 'min'.")

    def setGlobalFont(self):
        """
        Set the font size based on the screen resolution.
        """
        screen = QApplication.primaryScreen()
        dpi = screen.logicalDotsPerInchX()  # Get the DPI of the screen

        # Calculate font size based on DPI
        base_font_size = 12  # Base font size for 96 DPI
        scale_factor = dpi / 255.0
        font_size = base_font_size * scale_factor

        # Set the global font
        font = QFont('SimSun', round(font_size))
        QApplication.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMainWindow()
    sys.exit(app.exec_())
