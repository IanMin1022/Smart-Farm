from PyQt5.QtWidgets import QColorDialog, QWidget, QApplication, QHBoxLayout, QLayout
from PyQt5.QtCore import Qt

class ColorWidget(QColorDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.setOptions(self.options() | QColorDialog.DontUseNativeDialog)
        self.setSizeGripEnabled(True)
        self.layout().setSizeConstraint(QLayout.SetNoConstraint)
        self.setStyleSheet('background-color: white')
        #self.setWindowFlag(Qt.Widget)
        for children in self.findChildren(QWidget):
            classname = children.metaObject().className()
            if classname not in ("QColorPicker", "QColorLuminancePicker"):
                children.hide()