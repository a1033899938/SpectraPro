import sys
import os
import time
# main window objects
from PyQt5.QtWidgets import QLabel, QTextEdit, QPushButton, QComboBox, QSpinBox
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
# math
import numpy as np
import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import MaxNLocator

# my modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import set_figure
from src.menu_actions import MenuActions
from src.tree_manager import TreeManager
from src.list_manager import ListManager
from src.figure_manager import FigureManager
from src.roi_manager import RoiManager
from src.figure_widget import FigureWidget

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

        # slot
        self.show_layout_flag = None
        self.show_roi_flag_now = False
        self.draw_rect_flag = None
        self.show_flag = None
        """Initialize ui"""
        self.initUI()

    def initUI(self):
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
            print("ss")
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

            """box manager"""
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
            print(f"Error initUI:\n  |--> {e}")

    def toggle_show_layout(self):
        if self.show_layout_flag:
            self.outputTextEdit.setVisible(False)
            self.show_layout_flag = 0
        else:
            self.outputTextEdit.setVisible(True)
            self.show_layout_flag = 1

    def toggle_show_roi(self, draw_rect_flag, show_flag, figure_xylim):
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











class HistogramWidget(QWidget):
    def __init__(self, width=6, height=4, dpi=100, parent=None):
        super().__init__(parent)

        self.fig = plt.figure(figsize=(width, height), dpi=dpi)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.rect = None
        self.last_click_time = 0
        self.start_xmin = None
        self.start_xmax = None
        self.start_xmid = None
        self.dragging_xmin = False
        self.dragging_xmax = False
        self.dragging_xmid = False
        self.rect_edge_size = 1
        self.figure_xylim = None
        self.show_flag = 'image'

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def initHist(self):
        self.ax.tick_params(axis='both', which='major', labelsize=8)  # 设置主刻度字体大小
        self.ax.tick_params(axis='both', which='minor', labelsize=8)  # 设置次刻度字体大小
        self.ax.xaxis.set_major_locator(MaxNLocator(nbins=6))  # 设置x轴刻度的最大数量为6
        self.ax.yaxis.set_major_locator(MaxNLocator(nbins=6))  # 设置y轴刻度的最大数量为6
        self.ax.set_xlabel('Intensity', fontsize=8)
        self.ax.set_ylabel('Frequency', fontsize=8)
        self.ax.set_title(f'Histogram', fontsize=10)

        self.setFocusPolicy(Qt.StrongFocus)

        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)

    def show_hist(self, data, figure_ax, figure_canvas):
        try:
            self.data = data
            self.figure_ax = figure_ax
            self.figure_canvas = figure_canvas

            self.intensity_1d = data['intensity_image'].flatten()
            self.ax.clear()
            self.ax.hist(self.intensity_1d, bins=30, color='blue', density=False)
            self.initHist()

            self.x_min, self.x_max = min(self.intensity_1d), max(self.intensity_1d)
            self.x_span = self.x_max - self.x_min
            self.ax.set_xlim(self.x_min - self.x_span * 0.1, self.x_max + self.x_span * 0.1)

            hist, _ = np.histogram(self.intensity_1d, bins=30)
            self.y_max = max(hist)
            self.ax.set_ylim(0, self.y_max * 1.1)

            self.draw_rectangle()

            self.rect_edge_size = self.x_span / 30

            # self.fig.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"  |--> Error initHistogram: {e}")

    def draw_rectangle(self):
        try:
            face_color = (0.5, 0.1, 0.9, 0.6)
            self.rect = Rectangle((self.x_min, 0), self.x_span, self.y_max, linewidth=1, edgecolor='red',
                                  facecolor=face_color, linestyle='-')
            self.ax.add_patch(self.rect)
        except Exception as e:
            print(f"  |--> Error draw_rectangle: {e}")

    def on_press(self, event):
        if event.inaxes != self.ax or self.show_flag == 'graph':
            return

        # 计算矩形的边缘区域
        rect_bbox = self.rect.get_bbox()
        if rect_bbox.y0 <= event.ydata <= rect_bbox.y1:
            if abs(event.xdata - rect_bbox.x0) < self.rect_edge_size:
                self.dragging_xmin = True
                self.start_xmin = rect_bbox.x0
            elif abs(event.xdata - rect_bbox.x1) < self.rect_edge_size:
                self.dragging_xmax = True
                self.start_xmax = rect_bbox.x1
            elif rect_bbox.x0 + self.rect_edge_size < event.xdata < rect_bbox.x1 - self.rect_edge_size:
                self.dragging_xmid = True
                self.start_xmid = event.xdata
                self.start_xmid_pos = rect_bbox.x0
            else:
                print("Error pressing.")

        current_time = time.time()

        if current_time - self.last_click_time < 0.3:
            self.rect.set_xy((self.x_min, 0))
            self.rect.set_width(self.x_span)
            self.fig.canvas.draw_idle()
            self.update_figure()
        self.last_click_time = current_time

    def on_move(self, event):
        if event.inaxes != self.ax or self.show_flag == 'graph':
            return

        if not self.dragging_xmin and not self.dragging_xmax and not self.dragging_xmid:
            return
        else:
            rect_bbox = self.rect.get_bbox()
            self.start_xmin = rect_bbox.x0
            self.start_xmax = rect_bbox.x1
            if self.dragging_xmin:
                dx = event.xdata - self.start_xmin
                new_x = self.start_xmin + dx
                self.rect.set_xy((new_x, 0))
                new_width = max(self.rect.get_width() - dx, 0)
                self.rect.set_width(new_width)
            elif self.dragging_xmax:
                dx = event.xdata - self.start_xmax
                new_width = max(self.rect.get_width() + dx, 0)
                self.rect.set_width(new_width)
            elif self.dragging_xmid:
                dx = event.xdata - self.start_xmid
                new_x = self.start_xmid_pos + dx
                self.rect.set_xy((new_x, 0))
            else:
                print("Error dragging.")

            self.update_figure()
            self.fig.canvas.draw()

    def on_release(self, event):
        self.dragging_xmin = False
        self.dragging_xmax = False
        self.dragging_xmid = False

    def update_figure(self):
        x = self.data['wavelength']
        y = self.data['strip']
        z = self.data['intensity_image']
        rect_bbox = self.rect.get_bbox()

        x = np.array(x)
        y = np.array(y)
        z = np.array(z)

        self.figure_title = self.figure_ax.get_title()
        self.figure_ax.clear()
        self.figure_ax.imshow(z, aspect='auto', extent=[x.min(), x.max(), y.min(), y.max()], origin='lower',
                              vmin=rect_bbox.x0, vmax=rect_bbox.x1)
        # self.figure_ax.set_xlim()
        if self.figure_xylim:
            self.figure_ax.set_xlim(self.figure_xylim[0], self.figure_xylim[1])
            self.figure_ax.set_ylim(self.figure_xylim[2], self.figure_xylim[3])

        set_figure.set_text(self.figure_ax, title=self.figure_title)
        set_figure.set_tick(self.figure_ax, xbins=6, ybins=10)
        self.figure_canvas.draw()

    def receive_parameters_from_figure(self, figure_xylim=None, show_flag=None):
        if figure_xylim:
            self.figure_xylim = figure_xylim
        elif show_flag:
            self.show_flag = show_flag


class OutputRedirector:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, message):
        self.text_edit.insertPlainText(message)
        self.text_edit.ensureCursorVisible()

    def flush(self):
        # This method is needed for Python 3.x
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMainWindow()
    sys.exit(app.exec_())
