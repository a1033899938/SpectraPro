from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from src import read_file, set_figure
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle

import time
import os
from PyQt5.QtWidgets import QFileDialog


class FigureWidget(QWidget):
    def __init__(self, main_window, histogramWidget, width=6, height=4, dpi=100):
        super().__init__()
        self.parent = main_window
        self.histogramWidget = histogramWidget

        self.fig = plt.figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # mouse event
        self.initFig()
        self.lastx = 0
        self.lasty = 0
        self.originxmin = 0
        self.originxmax = 0
        self.originymin = 0
        self.originymax = 0
        self.last_click_time = 0
        self.figure_xylim = None
        self.press = False

        self.show_flag = 'image'
        self.fig_title = None
        self.draw_rect_flag = False

    def initFig(self):
        try:
            self.setFocusPolicy(Qt.StrongFocus)  # Enable focus to receive mouse events

            self.fig.canvas.mpl_connect('scroll_event', self.call_back)
            self.fig.canvas.mpl_connect("button_press_event", self.on_press)
            self.fig.canvas.mpl_connect("button_release_event", self.on_release)
            self.fig.canvas.mpl_connect("motion_notify_event", self.on_move)
        except Exception as e:
            print(f"  |--> Error initFig: {e}")

    def deal_with_this_file(self, list_item):
        list_item_name = list_item.data(0)
        list_item_path = list_item.data(1)
        self.data = read_file.read_spe(list_item_path)
        self.fig_title = list_item_name
        self.show_figue()

    def show_figue(self):
        if self.show_flag == 'image':
            self.show_image(self.data, fig_title=self.fig_title)
            self.histogramWidget.show_hist(self.data, self.ax, self.canvas)
        elif self.show_flag == 'graph':
            self.show_graph(self.data, fig_title=self.fig_title)
        else:
            print("Error show_flag.")

    def show_image(self, data, fig_title='default title'):
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

        self.figure_xylim = [x.min(), x.max(), y.min(), y.max()]
        self.pass_parameters_to_hist(figure_xylim=self.figure_xylim)
        self.originxmin, self.originxmax = x.min(), x.max()
        self.originymin, self.originymax = y.min(), y.max()
        self.figure_origin_xylim = [self.originxmin, self.originxmax, self.originymin, self.originymax]

        if self.draw_rect_flag:
            self.draw_rectangle()
        self.canvas.draw()

    def show_graph(self, data, fig_title='default title'):
        x = data['wavelength']
        y = data['intensity']

        # Ensure x and y are 1D arrays and z is a 2D array
        x = np.array(x)
        y = np.array(y)

        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.set_xlim([x.min(), x.max()])
        self.ax.set_ylim([y.min(), y.max()])
        set_figure.set_text(self.ax, title=fig_title)
        set_figure.set_tick(self.ax, xbins=6, ybins=10)
        self.canvas.draw()

        self.figure_xylim = [x.min(), x.max(), y.min(), y.max()]
        self.pass_parameters_to_hist(figure_xylim=self.figure_xylim)
        self.originxmin, self.originxmax = x.min(), x.max()
        self.originymin, self.originymax = y.min(), y.max()

    def draw_rectangle(self):
        try:
            face_color = (0.5, 0.1, 0.9, 0.6)
            self.rect_x_min = self.figure_origin_xylim[0]
            self.rect_y_min = self.figure_origin_xylim[2]
            self.rect_x_span = self.figure_origin_xylim[1] - self.figure_origin_xylim[0]
            self.rect_y_span = self.figure_origin_xylim[3] - self.figure_origin_xylim[2]
            self.rect = Rectangle((self.rect_x_min - self.rect_x_span * 0.2, self.rect_y_min), self.rect_x_span * 1.4,
                                  self.rect_y_span,
                                  linewidth=1, edgecolor='red',
                                  facecolor=face_color, linestyle='-')
            self.ax.add_patch(self.rect)
        except Exception as e:
            print(f"  |--> Error draw_rectangle: {e}")

    def change_rect_maxlim(self, value):
        try:
            self.rect_y_span = value - self.rect_y_min
            self.rect.set_xy((self.rect_x_min - self.rect_x_span * 0.2, self.rect_y_min))
            self.rect.set_height(self.rect_y_span)
            self.fig.canvas.draw_idle()
        except Exception as e:
            print(f"  |--> Error change_rect_maxlim: {e}")

    def change_rect_mimlim(self, value):
        try:
            self.rect_y_span = self.rect_y_min + self.rect_y_span - value
            self.rect_y_min = value
            self.rect.set_xy((self.rect_x_min - self.rect_x_span * 0.2, self.rect_y_min))
            self.rect.set_height(self.rect_y_span)
            self.fig.canvas.draw_idle()
        except Exception as e:
            print(f"  |--> Error change_rect_maxlim: {e}")

    # def change_roi_span(self, value):
    #     if

    def on_press(self, event):
        try:
            if event.inaxes:  # if mouse in axes
                if event.button == 1:  # click left equals 1, while right equals 2
                    self.press = True
                    current_time = time.time()
                    self.lastx = event.xdata  # get X coordinate of mouse
                    self.lasty = event.ydata  # get Y coordinate of mouse

                    if current_time - self.last_click_time < 0.3:
                        self.figure_xylim = [self.originxmin, self.originxmax, self.originymin, self.originymax]
                        self.pass_parameters_to_hist(figure_xylim=self.figure_xylim)
                        event.inaxes.set_xlim(self.originxmin, self.originxmax)
                        event.inaxes.set_ylim(self.originymin, self.originymax)
                        self.fig.canvas.draw_idle()
                    self.last_click_time = current_time
        except Exception as e:
            print(f"  |--> Error on_press: {e}")

    def on_move(self, event):
        try:
            if event.inaxes and self.press:
                x = event.xdata - self.lastx
                y = event.ydata - self.lasty

                x_min, x_max = event.inaxes.get_xlim()
                y_min, y_max = event.inaxes.get_ylim()

                x_min -= x
                x_max -= x
                y_min -= y
                y_max -= y

                self.figure_xylim = [x_min, x_max, y_min, y_max]
                self.pass_parameters_to_hist(figure_xylim=self.figure_xylim)
                event.inaxes.set_xlim(x_min, x_max)
                event.inaxes.set_ylim(y_min, y_max)
                self.fig.canvas.draw_idle()  # Draw immediately
        except Exception as e:
            print(f"  |--> Error on_move: {e}")

    def on_release(self, event):
        if self.press:
            self.press = False  # 鼠标松开，结束移动

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

                event.inaxes.set_xlim(new_x_min, new_x_max)
                event.inaxes.set_ylim(new_y_min, new_y_max)

                self.figure_xylim = [new_x_min, new_x_max, new_y_min, new_y_max]
                self.pass_parameters_to_hist(figure_xylim=self.figure_xylim)
                self.fig.canvas.draw_idle()  # Redraw the canvas
        except Exception as e:
            print(f"  |--> Error call_back: {e}")

    def toggle_image_and_graph(self, index):
        try:
            if index == 0 or index == 1:
                if index == 0:
                    self.show_flag = 'image'
                    self.show_image(self.data, fig_title=self.fig_title)
                    self.histogramWidget.show_hist(self.data, self.ax, self.canvas)
                elif index == 1:
                    self.show_flag = 'graph'
                    self.show_graph(self.data, fig_title=self.fig_title)
                else:
                    print("Error combox input.")
                self.pass_parameters_to_hist(show_flag=self.show_flag)
            else:
                print("Error toggle_image_and_graph.")
            self.pass_roi_flag()
        except Exception as e:
            print(f"  |--> Error toggle_image_and_graph: {e}")

    def toggle_show_rect(self):
        try:
            if self.show_flag != 'image':
                print("Only for image.")
                return
            if not self.draw_rect_flag:
                self.draw_rect_flag = True
                self.draw_rectangle()
                self.fig.canvas.draw_idle()
            else:
                self.draw_rect_flag = False
                self.rect.remove()
                self.fig.canvas.draw_idle()
            self.pass_roi_flag()
        except Exception as e:
            print(f"  |--> Error toggle_show_rect: {e}")

    def pass_roi_flag(self):
        self.parent.toggle_show_roi(self.draw_rect_flag, self.show_flag, self.figure_origin_xylim)

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
            print(f"  |--> Error save_current_figure: {e}")

    def pass_parameters_to_hist(self, figure_xylim=None, show_flag=None):
        if figure_xylim:
            self.histogramWidget.receive_parameters_from_figure(figure_xylim=figure_xylim)
        if show_flag:
            self.histogramWidget.receive_parameters_from_figure(show_flag=show_flag)