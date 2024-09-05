from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle
from src import read_file, set_figure, numerical_transform


class FigureWidget(QWidget):
    def __init__(self, main_window, histogramWidget, width=6, height=4, dpi=100):
        try:
            super().__init__()
            # initialize
            self.parent = main_window
            self.histogramWidget = histogramWidget

            # create main figure object
            self.fig = plt.figure(figsize=(width, height), dpi=dpi)
            self.ax = self.fig.add_subplot(111)
            self.canvas = FigureCanvas(self.fig)

            # set layout of this instantiation
            layout = QVBoxLayout()
            layout.addWidget(self.canvas)
            self.setLayout(layout)

            # read data and file name
            self.list_item_name = None
            self.list_item_path = None
            self.data = None
            self.fig_title = None

            # canvas range
            self.canvas_xylim = None
            self.canvas_origin_xylim = None
            self.canvas_origin_xylim2 = None

            # mouse event
            self.press = False
            self.initFig()
            self.last_click_x = 0
            self.last_click_y = 0
            self.last_click_time = 0

            # rectangle-figure
            self.rect = None
            self.rect_x_min = None
            self.rect_y_min = None
            self.rect_x_span = None
            self.rect_y_span = None
            self.spin_box_min = None
            self.spin_box_max = None

            self.show_flag = 'image'
            self.draw_rect_flag = False
            self.ax2 = None
        except Exception as e:
            print(f"Error FigureWidget.init:\n  |--> {e}")

    def initFig(self):
        try:
            self.setFocusPolicy(Qt.StrongFocus)  # Enable focus to receive mouse events

            self.fig.canvas.mpl_connect('scroll_event', self.call_back)
            self.fig.canvas.mpl_connect("button_press_event", self.on_press)
            self.fig.canvas.mpl_connect("button_release_event", self.on_release)
            self.fig.canvas.mpl_connect("motion_notify_event", self.on_move)
        except Exception as e:
            print(f"Error FigureWidget.initFig:\n  |--> {e}")

    def deal_with_this_file(self, list_item):
        try:
            # read data and file name
            self.list_item_name = list_item.data(0)
            self.list_item_path = list_item.data(1)

            self.fig_title = self.list_item_name

            self.read_data()

            self.show_figue()
        except Exception as e:
            print(f"Error FigureWidget.deal_with_this_file:\n  |--> {e}")

    def read_data(self):
        try:
            if self.spin_box_min is None and self.spin_box_max is None:
                self.data = read_file.read_spe(self.list_item_path, strip='all')
                print("full strip.")
            elif self.spin_box_min and self.spin_box_max:
                self.data = read_file.read_spe(self.list_item_path, strip=[self.spin_box_min, self.spin_box_max])
                print(f"strip range is: {self.spin_box_min, self.spin_box_max}")
            else:
                print("Please input minimum and maximum of strip range.")
        except Exception as e:
            print(f"Error FigureWidget.read_data:\n  |--> {e}")

    def show_figue(self):
        try:
            if self.show_flag == 'image':
                self.show_image(self.data, fig_title=self.fig_title)
                self.histogramWidget.show_hist()
            elif self.show_flag == 'graph':
                self.show_graph(self.data, fig_title=self.fig_title)
            elif self.show_flag == 'Image&Graph':
                self.show_image(self.data, fig_title=self.fig_title)
                self.histogramWidget.show_hist()
                self.show_graph(self.data, fig_title=self.fig_title)
            else:
                print("Error show_flag.")
        except Exception as e:
            print(f"Error FigureWidget.show_figue:\n  |--> {e}")

    def show_image(self, data, fig_title='default title'):
        try:
            x = data['wavelength']
            y = data['strip']
            z = data['intensity_image']

            # Ensure x and y are 1D arrays and z is a 2D array
            x = np.array(x)
            y = np.array(y)
            z = np.array(z)

            self.ax.clear()
            self.ax.imshow(z, aspect='auto', extent=[x.min(), x.max(), y.min(), y.max()], origin='lower')
            set_figure.set_text(self.ax, title=fig_title)
            set_figure.set_tick(self.ax, xbins=6, ybins=10)

            self.canvas_xylim = [x.min(), x.max(), y.min(), y.max()]
            self.canvas_origin_xylim = self.canvas_xylim
            self.pass_parameters_to_hist(self.data, self.ax, self.canvas, self.canvas_xylim, self.canvas_origin_xylim,
                                         self.show_flag, self.rect)
            self.parent.set_spin_box_lim(self.canvas_origin_xylim)

            self.canvas.draw()
            self.draw_rect_flag = False
        except Exception as e:
            print(f"Error FigureWidget.show_image:\n  |--> {e}")

    def show_graph(self, data, fig_title='default title'):
        try:
            x = data['wavelength']
            y = data['intensity']

            # Ensure x and y are 1D arrays and z is a 2D array
            x = np.array(x)
            y = np.array(y)

            if self.show_flag == 'Image&Graph':
                self.ax2.clear()
                self.ax2.plot(x, y)
                self.ax2.set_xlim([x.min(), x.max()])
                self.ax2.set_ylim([y.min(), y.max()])
                set_figure.set_text(self.ax2, title=fig_title)
                set_figure.set_tick(self.ax2, xbins=6, ybins=10)
            else:
                self.ax.clear()
                self.ax.plot(x, y)
                self.ax.set_xlim([x.min(), x.max()])
                self.ax.set_ylim([y.min(), y.max()])
                set_figure.set_text(self.ax, title=fig_title)
                set_figure.set_tick(self.ax, xbins=6, ybins=10)
            if self.show_flag != 'Image&Graph':
                self.canvas_origin_xylim = [x.min(), x.max(), y.min(), y.max()]
            else:
                self.canvas_origin_xylim2 = [x.min(), x.max(), y.min(), y.max()]
            self.pass_parameters_to_hist(self.data, self.ax, self.canvas, self.canvas_xylim, self.canvas_origin_xylim,
                                         self.show_flag, self.rect)

            self.canvas.draw()
        except Exception as e:
            print(f"Error FigureWidget.show_graph:\n  |--> {e}")

    def on_press(self, event):
        try:
            if event.inaxes:  # if mouse in axes
                if event.button == 1:  # click left equals 1, while right equals 2
                    self.press = True
                    current_time = time.time()
                    self.last_click_x = event.xdata  # get X coordinate of mouse
                    self.last_click_y = event.ydata  # get Y coordinate of mouse

                    if current_time - self.last_click_time < 0.3:
                        if event.inaxes == self.ax:
                            self.canvas_xylim = self.canvas_origin_xylim
                            self.pass_parameters_to_hist(self.data, self.ax, self.canvas, self.canvas_xylim,
                                                         self.canvas_origin_xylim, self.show_flag, self.rect)
                            event.inaxes.set_xlim(self.canvas_xylim[0], self.canvas_xylim[1])
                            event.inaxes.set_ylim(self.canvas_xylim[2], self.canvas_xylim[3])
                        elif event.inaxes == self.ax2:
                            self.canvas_xylim = self.canvas_origin_xylim2
                            event.inaxes.set_xlim(self.canvas_xylim[0], self.canvas_xylim[1])
                            event.inaxes.set_ylim(self.canvas_xylim[2], self.canvas_xylim[3])
                        else:
                            print("move on wrong ax.")
                        self.fig.canvas.draw_idle()
                    self.last_click_time = current_time
        except Exception as e:
            print(f"Error FigureWidget.on_press:\n  |--> {e}")

    def on_move(self, event):
        try:
            if event.inaxes and self.press:
                x = event.xdata - self.last_click_x
                y = event.ydata - self.last_click_y

                x_min, x_max = event.inaxes.get_xlim()
                y_min, y_max = event.inaxes.get_ylim()

                x_min -= x
                x_max -= x
                y_min -= y
                y_max -= y

                self.canvas_xylim = [x_min, x_max, y_min, y_max]
                self.pass_parameters_to_hist(self.data, self.ax, self.canvas,
                                             self.canvas_xylim, self.canvas_origin_xylim, self.show_flag, self.rect)

                event.inaxes.set_xlim(self.canvas_xylim[0], self.canvas_xylim[1])
                event.inaxes.set_ylim(self.canvas_xylim[2], self.canvas_xylim[3])
                self.fig.canvas.draw_idle()  # Draw immediately
        except Exception as e:
            print(f"Error FigureWidget.on_move:\n  |--> {e}")

    def on_release(self, event):
        try:
            if self.press:
                self.press = False  # 鼠标松开，结束移动
        except Exception as e:
            print(f"Error FigureWidget.on_release:\n  |--> {e}")

    def call_back(self, event):
        try:
            if event.inaxes:
                x_min, x_max = event.inaxes.get_xlim()
                y_min, y_max = event.inaxes.get_ylim()

                x_range = (x_max - x_min) / 10
                y_range = (y_max - y_min) / 10

                if event.button == 'up':
                    new_x_min, new_x_max = x_min + x_range, x_max - x_range
                    new_y_min, new_y_max = y_min + y_range, y_max - y_range

                elif event.button == 'down':
                    new_x_min, new_x_max = x_min - x_range, x_max + x_range
                    new_y_min, new_y_max = y_min - y_range, y_max + y_range

                self.canvas_xylim = [new_x_min, new_x_max, new_y_min, new_y_max]
                self.pass_parameters_to_hist(self.data, self.ax, self.canvas,
                                             self.canvas_xylim, self.canvas_origin_xylim, self.show_flag, self.rect)

                event.inaxes.set_xlim(self.canvas_xylim[0], self.canvas_xylim[1])
                event.inaxes.set_ylim(self.canvas_xylim[2], self.canvas_xylim[3])
                self.fig.canvas.draw_idle()  # Redraw the canvas
        except Exception as e:
            print(f"Error FigureWidget.call_back:\n  |--> {e}")

    def toggle_image_and_graph(self, index):
        try:
            if index == 0 or index == 1 or index == 2:
                if index == 0:
                    if self.show_flag == 'Image&Graph':
                        self.ax.remove()
                        self.ax2.remove()
                        self.ax = self.fig.add_subplot(111)

                    self.show_flag = 'image'
                    self.read_data()
                    self.show_figue()
                    self.histogramWidget.show_hist()
                elif index == 1:
                    if self.show_flag == 'Image&Graph':
                        self.ax.remove()
                        self.ax2.remove()
                        self.ax = self.fig.add_subplot(111)
                        self.canvas.draw()

                    self.show_flag = 'graph'
                    self.read_data()
                    self.show_figue()
                elif index == 2:
                    self.show_flag = 'Image&Graph'
                    self.ax.remove()
                    self.ax = self.fig.add_subplot(211)
                    self.ax2 = self.fig.add_subplot(212)
                    self.read_data()
                    self.show_figue()
                    self.fig.tight_layout()
                    self.canvas.draw()

                else:
                    print("Error combox input.")
                # self.pass_parameters_to_hist(self.data, self.ax, self.canvas,
                #                              self.canvas_xylim, self.canvas_origin_xylim, self.show_flag, self.rect)
            else:
                print("Error toggle_image_and_graph.")
            # self.pass_roi_flag()
        except Exception as e:
            print(f"Error FigureWidget.toggle_image_and_graph:\n  |--> {e}")

    def toggle_show_rect(self):
        try:
            if self.show_flag == 'graph':
                print("Only for image or Image&Graph.")
                return
            if not self.draw_rect_flag:
                self.draw_rect_flag = True
                self.draw_rectangle()
                self.fig.canvas.draw_idle()
            else:
                self.draw_rect_flag = False
                self.rect.remove()
                self.fig.canvas.draw_idle()
            # self.pass_roi_flag()
        except Exception as e:
            print(f"Error FigureWidget.toggle_show_rect:\n  |--> {e}")

    def draw_rectangle(self):
        try:
            face_color = (0.5, 0.1, 0.9, 0.6)
            if all(val is None for val in (self.rect_x_min, self.rect_y_min, self.rect_x_span, self.rect_y_span)):
                self.rect_x_min, self.rect_y_min, self.rect_x_span, self.rect_y_span \
                    = numerical_transform.transform_position_LimToSpan(self.canvas_origin_xylim[0],
                                                                       self.canvas_origin_xylim[1],
                                                                       self.canvas_origin_xylim[2],
                                                                       self.canvas_origin_xylim[3])
            self.rect = Rectangle((self.rect_x_min - self.rect_x_span * 0.2, self.rect_y_min), self.rect_x_span * 1.4,
                                  self.rect_y_span,
                                  linewidth=1, edgecolor='red',
                                  facecolor=face_color, linestyle='-')
            self.ax.add_patch(self.rect)
        except Exception as e:
            print(f"Error FigureWidget.draw_rectangle:\n  |--> {e}")

    def change_rect_maxlim(self, value):
        try:
            self.rect_y_span = value - self.rect_y_min
            self.rect.set_xy((self.rect_x_min - self.rect_x_span * 0.2, self.rect_y_min))
            self.rect.set_height(self.rect_y_span)
            self.fig.canvas.draw_idle()
            self.parent.receive_spinbox_value_from_figure(value, tag='max')
            self.spin_box_max = value
            self.read_data()  # reload data for showing graph with new strip range
            if self.show_flag == 'graph' or self.show_flag == "Image&Graph":
                self.show_graph(self.data, fig_title=self.fig_title)
            self.pass_parameters_to_hist(self.data, self.ax, self.canvas, self.canvas_xylim, self.canvas_origin_xylim,
                                         self.show_flag, self.rect)
        except Exception as e:
            print(f"Error FigureWidget.change_rect_maxlim:\n  |--> {e}")

    def change_rect_minlim(self, value):
        try:
            self.rect_y_span = self.rect_y_min + self.rect_y_span - value
            self.rect_y_min = value
            self.rect.set_xy((self.rect_x_min - self.rect_x_span * 0.2, self.rect_y_min))
            self.rect.set_height(self.rect_y_span)
            self.fig.canvas.draw_idle()
            self.parent.receive_spinbox_value_from_figure(value, tag='min')
            self.spin_box_min = value
            self.read_data()  # reload data for showing graph with new strip range
            if self.show_flag == 'graph' or self.show_flag == "Image&Graph":
                self.show_graph(self.data, fig_title=self.fig_title)
            self.pass_parameters_to_hist(self.data, self.ax, self.canvas, self.canvas_xylim, self.canvas_origin_xylim,
                                         self.show_flag, self.rect)
        except Exception as e:
            print(f"Error FigureWidget.change_rect_minlim:\n  |--> {e}")

    # def pass_roi_flag(self):
    #     try:
    #         self.parent.toggle_show_roi(self.draw_rect_flag, self.show_flag)
    #     except Exception as e:
    #         print(f"Error FigureWidget.pass_roi_flag:\n  |--> {e}")

    def save_current_figure(self):
        try:
            if self.fig_title is None:
                print("No figure now.")
                return

            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            pic_dir = os.path.join(parent_dir, 'saved_picture')
            default_filename = self.fig_title
            default_filename, _ = os.path.splitext(default_filename)  # delete ext of file
            default_filepath = os.path.join(pic_dir, default_filename)

            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Current Figure", default_filepath,
                                                       "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)",
                                                       options=options)
            if file_path:
                self.fig.savefig(file_path)
        except Exception as e:
            print(f"Error FigureWidget.save_current_figure:\n  |--> {e}")

    def pass_parameters_to_hist(self, data, ax, canvas, canvas_xylim, canvas_origin_xylim, show_flag, rect):
        try:
            self.histogramWidget.receive_parameters_from_figure(data, ax, canvas, canvas_xylim, canvas_origin_xylim,
                                                                show_flag, rect)
        except Exception as e:
            print(f"Error FigureWidget.pass_parameters_to_hist:\n  |--> {e}")