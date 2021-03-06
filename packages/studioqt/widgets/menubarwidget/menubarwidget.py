#Embedded file name: C:/Users/hovel/Dropbox/packages/studiolibrary/1.23.2/build27/studiolibrary/packages/studioqt\widgets\menubarwidget\menubarwidget.py
import logging
from studioqt import QtGui
from studioqt import QtCore
from studioqt import QtWidgets
import studioqt
logger = logging.getLogger(__name__)

class MenuBarWidget(QtWidgets.QFrame):
    ICON_COLOR = QtGui.QColor(255, 255, 255)
    SPACING = 5
    DEFAULT_EXPANDED_HEIGHT = 38
    DEFAULT_COLLAPSED_HEIGHT = 10

    def __init__(self, parent = None):
        QtWidgets.QFrame.__init__(self, parent)
        self._dpi = 1
        self._expanded = True
        self._expandedHeight = self.DEFAULT_EXPANDED_HEIGHT
        self._collapsedHeight = self.DEFAULT_COLLAPSED_HEIGHT
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self.SPACING)
        self.setLayout(layout)
        self._leftToolBar = QtWidgets.QToolBar(self)
        self._rightToolBar = QtWidgets.QToolBar(self)
        self._leftToolBar.layout().setSpacing(self.SPACING)
        self._rightToolBar.layout().setSpacing(self.SPACING)
        self.layout().addWidget(self._leftToolBar)
        self.layout().addWidget(self._rightToolBar)

    def dpi(self):
        return self._dpi

    def setDpi(self, dpi):
        self._dpi = dpi
        self.update()

    def update(self):
        self.refreshSize()
        self.updateIconColor()

    def refreshSize(self):
        self.setChildrenHeight(self.height())
        if self.isExpanded():
            self.expand()
        else:
            self.collapse()

    def updateIconColor(self):
        color = self.palette().color(self.foregroundRole())
        color = studioqt.Color.fromColor(color)
        self.setIconColor(color)

    def addLeftAction(self, text):
        action = QtWidgets.QAction(text, self._leftToolBar)
        self._leftToolBar.addAction(action)
        return action

    def addRightAction(self, text):
        action = QtWidgets.QAction(text, self._rightToolBar)
        self._rightToolBar.addAction(action)
        return action

    def widgets(self):
        widgets = []
        for i in range(0, self.layout().count()):
            w = self.layout().itemAt(i).widget()
            if isinstance(w, QtWidgets.QWidget):
                widgets.append(w)

        return widgets

    def findToolButton(self, text):
        button1 = self._findToolButton(self._leftToolBar, text)
        button2 = self._findToolButton(self._rightToolBar, text)
        return button1 or button2

    def _findToolButton(self, toolBar, text):
        for child in toolBar.children():
            if isinstance(child, QtWidgets.QAction):
                if child.text() == text:
                    return toolBar.widgetForAction(child)

    def actions(self):
        actions = []
        children = self._leftToolBar.children()
        children.extend(self._rightToolBar.children())
        for child in children:
            if isinstance(child, QtWidgets.QAction):
                actions.append(child)

        return actions

    def isExpanded(self):
        return self._expanded

    def setExpandedHeight(self, height):
        self._expandedHeight = height
        self.setChildrenHeight(height)

    def expandedHeight(self):
        return int(self._expandedHeight * self.dpi())

    def expand(self):
        self._expanded = True
        height = self.expandedHeight()
        self.setFixedHeight(height)
        self.setChildrenHeight(height)
        self.updateIconColor()

    def collapse(self):
        self._expanded = False
        height = self.collapsedHeight()
        self.setFixedHeight(height)
        self.setChildrenHeight(0)
        self.updateIconColor()

    def collapsedHeight(self):
        return int(self._collapsedHeight * self.dpi())

    def setIconColor(self, color):
        for action in self.actions():
            icon = action.icon()
            icon = studioqt.Icon(icon)
            icon.setColor(color)
            action.setIcon(icon)

    def setChildrenHidden(self, value):
        for w in self.widgets():
            w.setHidden(value)

    def setChildrenHeight(self, height):
        for w in self.widgets():
            w.setFixedHeight(height)

        width = height + self.SPACING * self.dpi()
        self._leftToolBar.setFixedHeight(height)
        self._leftToolBar.setIconSize(QtCore.QSize(width, height - 5))
        self._rightToolBar.setFixedHeight(height)
        self._rightToolBar.setIconSize(QtCore.QSize(width, height - 5))

    def resizeEvent(self, *args, **kwargs):
        self.refreshSize()

    def mousePressEvent(self, *args, **kwargs):
        self.expand()


def showExample():
    """
    Run a simple example of the widget.
    
    :rtype: QtWidgets.QWidget
    """
    with studioqt.app():

        def triggered():
            print 'Triggered'

        def triggered2():
            print 'Triggered2'

        widget = studioqt.MenuBarWidget()
        icon = studioqt.icon('add')
        action = widget.addLeftAction('New Item')
        action.setIcon(icon)
        action.triggered.connect(triggered)
        lineedit = QtWidgets.QLineEdit()
        widget.layout().insertWidget(1, lineedit)
        widget.setExpandedHeight(35)
        icon = studioqt.icon('settings')
        action = widget.addRightAction('Settings')
        action.setIcon(icon)
        action.triggered.connect(triggered2)
        widget.show()
        return widget


if __name__ == '__main__':
    showExample()
