from qtpy import QtCore, QtGui
from qtpy.QtCore import Qt

__all__ = ("get_valid_image_layers", "SelectorListItem", "SelectorListModel")


# functions
def get_valid_image_layers(layer_list):
    """
    Extract napari images layers of 3 or more dimensions from the input list.
    """
    out = [
        layer
        for layer in layer_list
        if layer._type_string == "image"
        and layer.data.ndim >= 3
        and not layer.rgb
    ]
    return out


# classes
class SelectorListItem(QtGui.QStandardItem):
    """Subclass of QtGui.QStandardItem for usage in the napari_time_series_plotter.SelectorListModel.

    Each item is checkable and holds the reference to a napari layer. The text of the item is bound to the layer name
    and updates with it.

    Attributes:
        layer : napari.layers.Image
    """

    def __init__(self, napari_layer):
        super().__init__()
        self.layer = napari_layer
        self.setText(self.layer.name)
        self.setCheckable(True)
        self.setCheckState(Qt.Unchecked)
        self.layer.events.name.connect(self._layer_name_changed)

    # def type(self):
    #     """
    #     Return custom type code.
    #     """
    #     return 1001

    def _layer_name_changed(self, event):
        """
        Receiver for napari layer.events.name event. Updates the item text according to the new layer name.
        """
        self.setText(self.layer.name)


class SelectorListModel(QtGui.QStandardItemModel):
    """Subclass of QtGui.QStandardItemModel.

    Automatically builds from a list of QtGui.QStandardItems or derivatives.
    """

    def __init__(self, items=None):
        super().__init__()
        if items:
            for item in items:
                self.appendRow(item)

    def get_checked(self):
        """Return all items with state QtCore.Qt.Checked.

        :return: All checked items
        :rtype: List[bool]
        """
        checked = []
        for index in range(self.rowCount()):
            item = self.item(index)
            if item.checkState() == QtCore.Qt.Checked:
                checked.append(item.layer)
        return checked

    def get_item_idx_by_text(self, search_text):
        """Returns all items which text attribute matches search_text.

        :param search_text: Text to match to item.text()
        :type search_text: str

        :return: All items with item.text matching text
        :rtype: Union[List[int]]

        """
        matches = []
        for index in range(self.rowCount()):
            item = self.item(index)
            if item.text() == search_text:
                matches.append(index)
        if len(matches) == 1:
            return matches[0]
        return matches
