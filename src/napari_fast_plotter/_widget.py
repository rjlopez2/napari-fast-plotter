"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

import pyqtgraph as pg
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    pass


# class ExampleQWidget(QWidget):
#     # your QWidget.__init__ can optionally request the napari viewer instance
#     # in one of two ways:
#     # 1. use a parameter called `napari_viewer`, as done here
#     # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
#     def __init__(self, napari_viewer):
#         super().__init__()
#         self.viewer = napari_viewer

#         btn = QPushButton("Click me!")
#         btn.clicked.connect(self._on_click)

#         self.setLayout(QHBoxLayout())
#         self.layout().addWidget(btn)

#     def _on_click(self):
#         print("napari has", len(self.viewer.layers), "layers")


class Plotter(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        ###############################
        ######## create tabs ##########
        ###############################

        ######## pre-processing tab ########
        self.plotter = QWidget()
        self._plotter_layout = QVBoxLayout()
        self.plotter.setLayout(self._plotter_layout)
        self.tabs.addTab(self.plotter, "Plot")

        ######## Pre-processing tab ########
        ####################################
        self._plotter_layout.setAlignment(Qt.AlignTop)

        ######## pre-processing  group ########
        self.plotter_group = VHGroup(
            "my beutiful and super fast plotter", orientation="G"
        )
        self._plotter_layout.addWidget(self.plotter_group.gbox)

        # histogram view
        self._graphics_widget = pg.GraphicsLayoutWidget()
        self._graphics_widget.setBackground(None)

        self.plotter_group.glayout.addWidget(self._graphics_widget)

        # test data

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        self.p2 = self._graphics_widget.addPlot()
        axis = self.p2.getAxis("bottom")
        axis.setLabel("Distance")
        axis = self.p2.getAxis("left")
        axis.setLabel("Intensity")

        self.p2.plot(hour, temperature, pen="green", name="test")

        def update_fps(fps):
            """Update fps."""
            self.viewer.text_overlay.text = f"Rendering at: {fps:1.1f} FPS"

        self.viewer.text_overlay.visible = True
        self.viewer.window.qt_viewer.canvas.measure_fps(callback=update_fps)


class VHGroup:
    """Group box with specific layout.

    Parameters
    ----------
    name: str
        Name of the group box
    orientation: str
        'V' for vertical, 'H' for horizontal, 'G' for grid
    """

    def __init__(self, name, orientation="V"):
        self.gbox = QGroupBox(name)
        if orientation == "V":
            self.glayout = QVBoxLayout()
        elif orientation == "H":
            self.glayout = QHBoxLayout()
        elif orientation == "G":
            self.glayout = QGridLayout()
        else:
            raise Exception(f"Unknown orientation {orientation}")

        self.gbox.setLayout(self.glayout)
