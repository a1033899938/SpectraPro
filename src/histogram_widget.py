import time
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from src import set_figure


class HistogramWidget(QWidget):
    def __init__(self, width=6, height=4, dpi=100, parent=None):
        try:
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
        except Exception as e:
            print(f"Error HistogramWidget.init:\n  |--> {e}")

    def initHist(self):
        try:
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
        except Exception as e:
            print(f"Error HistogramWidget.initHist:\n  |--> {e}")

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
            print(f"Error HistogramWidget.show_hist:\n  |--> {e}")

    def draw_rectangle(self):
        try:
            face_color = (0.5, 0.1, 0.9, 0.6)
            self.rect = Rectangle((self.x_min, 0), self.x_span, self.y_max, linewidth=1, edgecolor='red',
                                  facecolor=face_color, linestyle='-')
            self.ax.add_patch(self.rect)
        except Exception as e:
            print(f"Error HistogramWidget.draw_rectangle:\n  |--> {e}")

    def on_press(self, event):
        try:
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
        except Exception as e:
            print(f"Error HistogramWidget.on_press:\n  |--> {e}")

    def on_move(self, event):
        try:
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
        except Exception as e:
            print(f"Error HistogramWidget.on_move:\n  |--> {e}")

    def on_release(self, event):
        try:
            self.dragging_xmin = False
            self.dragging_xmax = False
            self.dragging_xmid = False
        except Exception as e:
            print(f"Error HistogramWidget.on_release:\n  |--> {e}")

    def update_figure(self):
        try:
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
        except Exception as e:
            print(f"Error HistogramWidget.update_figure:\n  |--> {e}")

    def receive_parameters_from_figure(self, figure_xylim=None, show_flag=None):
        try:
            if figure_xylim:
                self.figure_xylim = figure_xylim
            elif show_flag:
                self.show_flag = show_flag
        except Exception as e:
            print(f"Error HistogramWidget.receive_parameters_from_figure:\n  |--> {e}")