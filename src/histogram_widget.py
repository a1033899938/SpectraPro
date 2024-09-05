import time
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from src import set_figure, numerical_transform


class HistogramWidget(QWidget):
    def __init__(self, width=6, height=4, dpi=100, parent=None):
        try:
            super().__init__(parent)
            # create histogram figure object
            self.fig = plt.figure(figsize=(width, height), dpi=dpi)
            self.canvas = FigureCanvas(self.fig)
            self.ax = self.fig.add_subplot(111)

            # hist
            self.intensity_hist = None

            # get figure objects and parameters from figure
            self.data = None
            self.figure_ax = None
            self.figure_canvas = None
            self.figure_canvas_xylim = None
            self.figure_canvas_origin_xylim = None
            self.figure_show_flag = None
            self.figure_title = None
            self.figure_rect = None

            # hist range
            self.hist_x_min = None
            self.hist_x_max = None
            self.hist_y_min = None
            self.hist_y_max = None
            self.hist_x_span = None

            # create rectangle object
            self.rect = None

            # rectangle range
            self.rect_edge_size = None
            self.rect_x_min = None
            self.rect_x_max = None
            self.rect_y_min = None
            self.rect_x_span = None
            self.rect_y_span = None

            # mouse event
            self.rect_x_mid = None
            self.last_click_time = 0
            self.dragging_xmin = False
            self.dragging_xmax = False
            self.dragging_xmid = False
            self.start_xmid_pos = None
            self.figure_show_flag = 'image'

            layout = QVBoxLayout()
            layout.addWidget(self.canvas)
            self.setLayout(layout)

            self.initHist()
        except Exception as e:
            print(f"Error HistogramWidget.init:\n  |--> {e}")

    def initHist(self):
        try:
            self.ax.tick_params(axis='both', which='major', labelsize=8)  # set font size of major text
            self.ax.tick_params(axis='both', which='minor', labelsize=8)  # set font size of minor text
            self.ax.xaxis.set_major_locator(MaxNLocator(nbins=6))  # set max number of x tick
            self.ax.yaxis.set_major_locator(MaxNLocator(nbins=6))  # set max number of y tick
            self.ax.set_xlabel('Intensity', fontsize=8)
            self.ax.set_ylabel('Frequency', fontsize=8)
            self.ax.set_title(f'Histogram', fontsize=10)

            self.setFocusPolicy(Qt.StrongFocus)

            self.fig.canvas.mpl_connect('button_press_event', self.on_press)
            self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
            self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        except Exception as e:
            print(f"Error HistogramWidget.initHist:\n  |--> {e}")

    def receive_parameters_from_figure(self, data, ax, canvas, canvas_xylim, canvas_origin_xylim, show_flag, rect):
        try:
            self.data = data
            self.figure_ax = ax
            self.figure_canvas = canvas
            self.figure_canvas_xylim = canvas_xylim
            self.figure_canvas_origin_xylim = canvas_origin_xylim
            self.figure_show_flag = show_flag
            self.figure_rect = rect
        except Exception as e:
            print(f"Error HistogramWidget.receive_parameters_from_figure:\n  |--> {e}")

    def show_hist(self):
        try:
            if self.data is None or 'intensity_image' not in self.data:
                print("No data or 'intensity_image' key is missing.")
                return
            self.intensity_hist = np.array(self.data['intensity_image']).flatten()
            self.ax.clear()
            self.ax.hist(self.intensity_hist, bins=30, color='blue', density=False)
            self.initHist()

            # set hist xlim
            self.hist_x_min, self.hist_x_max = min(self.intensity_hist), max(self.intensity_hist)
            self.hist_x_span = self.hist_x_max - self.hist_x_min
            self.ax.set_xlim(self.hist_x_min - self.hist_x_span * 0.1, self.hist_x_max + self.hist_x_span * 0.1)

            # set hist ylim
            hist, _ = np.histogram(self.intensity_hist, bins=30)

            self.hist_y_min = 0
            self.hist_y_max = max(hist)
            self.ax.set_ylim(self.hist_y_min, self.hist_y_max * 1.1)

            # set rect edge size and lim
            self.rect_edge_size = self.hist_x_span / 30
            self.rect_x_min, self.rect_y_min, self.rect_x_span, self.rect_y_span \
                = numerical_transform.transform_position_LimToSpan(
                                                                    self.hist_x_min,
                                                                    self.hist_x_max,
                                                                    self.hist_y_min,
                                                                    self.hist_y_max)

            self.draw_rectangle()

            self.canvas.draw()
        except Exception as e:
            print(f"Error HistogramWidget.show_hist:\n  |--> {e}")

    def draw_rectangle(self):
        try:
            self.rect
            face_color = (0.5, 0.1, 0.9, 0.6)
            self.rect = Rectangle((self.rect_x_min, self.rect_y_min), self.rect_x_span, self.rect_y_span, linewidth=1,
                                  edgecolor='red',
                                  facecolor=face_color, linestyle='-')
            self.ax.add_patch(self.rect)
        except Exception as e:
            print(f"Error HistogramWidget.draw_rectangle:\n  |--> {e}")

    def on_press(self, event):
        try:
            if event.inaxes != self.ax or self.figure_show_flag == 'graph':
                return

            # 计算矩形的边缘区域
            rect_bbox = self.rect.get_bbox()
            if rect_bbox.y0 <= event.ydata <= rect_bbox.y1:
                if abs(event.xdata - rect_bbox.x0) < self.rect_edge_size:
                    self.dragging_xmin = True
                    self.rect_x_min = rect_bbox.x0
                elif abs(event.xdata - rect_bbox.x1) < self.rect_edge_size:
                    self.dragging_xmax = True
                    self.rect_x_max = rect_bbox.x1
                elif rect_bbox.x0 + self.rect_edge_size < event.xdata < rect_bbox.x1 - self.rect_edge_size:
                    self.dragging_xmid = True
                    self.rect_x_mid = event.xdata
                    self.start_xmid_pos = rect_bbox.x0
                else:
                    print("Error pressing.")

            current_time = time.time()

            if current_time - self.last_click_time < 0.3:
                self.rect.set_xy((self.hist_x_min, 0))
                self.rect.set_width(self.hist_x_span)
                self.fig.canvas.draw_idle()
                self.update_figure()
            self.last_click_time = current_time
        except Exception as e:
            print(f"Error HistogramWidget.on_press:\n  |--> {e}")

    def on_move(self, event):
        try:
            if event.inaxes != self.ax or self.figure_show_flag == 'graph':
                return

            if not self.dragging_xmin and not self.dragging_xmax and not self.dragging_xmid:
                return
            else:
                rect_bbox = self.rect.get_bbox()
                self.rect_x_min = rect_bbox.x0
                self.rect_x_max = rect_bbox.x1
                if self.dragging_xmin:
                    dx = event.xdata - self.rect_x_min
                    new_x = self.rect_x_min + dx
                    self.rect.set_xy((new_x, 0))
                    new_width = max(self.rect.get_width() - dx, 0)
                    self.rect.set_width(new_width)
                elif self.dragging_xmax:
                    dx = event.xdata - self.rect_x_max
                    new_width = max(self.rect.get_width() + dx, 0)
                    self.rect.set_width(new_width)
                elif self.dragging_xmid:
                    dx = event.xdata - self.rect_x_mid
                    new_x = self.start_xmid_pos + dx
                    self.rect.set_xy((new_x, 0))
                else:
                    print("Error dragging.")

                if self.figure_show_flag != 'graph':
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
            self.figure_ax.imshow(z, aspect='auto', extent=self.figure_canvas_origin_xylim, origin='lower',
                                  vmin=rect_bbox.x0, vmax=rect_bbox.x1)
            self.figure_ax.set_xlim(self.figure_canvas_xylim[0], self.figure_canvas_xylim[1])
            self.figure_ax.set_ylim(self.figure_canvas_xylim[2], self.figure_canvas_xylim[3])

            set_figure.set_text(self.figure_ax, title=self.figure_title)
            set_figure.set_tick(self.figure_ax, xbins=6, ybins=10)

            # if self.figure_show_flag == 'Image&Graph':
            #     self.figure_ax.add_patch(self.figure_rect)

            self.figure_canvas.draw()
        except Exception as e:
            print(f"Error HistogramWidget.update_figure:\n  |--> {e}")
