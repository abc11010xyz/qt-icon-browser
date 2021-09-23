import sys

from PySide2.QtGui import QIcon, QPalette, QColor
from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLineEdit, QListWidget, QListWidgetItem, QLabel,
                               QAbstractItemView, QStyle)


class QtIconBrowser(QWidget):

    VERSION = "0.0.1"
    TITLE = "Icon Browser"

    PIXMAP_SIZE = 16

    GRID_WIDTH = 120
    GRID_HEIGHT = 60

    PADDING = 5
    BORDER = 1

    NAME_LIST_WGT_STYLE_SHEET = """
        QListWidget {
            border: none;
        }
        QListWidget::item:selected:active {
            color: white;
            background-color: rgb(15, 130, 220);
        }
        QListWidget::item:selected:!active {
            color: azure;
            background-color: rgba(15, 130, 220, 150);
        }
    """

    ICON_LIST_WGT_STYLE_SHEET = """
        QListWidget {
            border: none;
            padding-left: -%(add)spx;
        }
        QListWidget:selected {
            outline: none;
        }
        QListWidget::item {
            border: %(border)spx solid %(base_color)s;
            padding: %(padding)spx;
            margin-top: %(padding)spx;
        }
        QListWidget::item:selected:active {
            color: black;
            border: %(border)spx solid rgb(15, 130, 220);
            border-radius: 2px;
            background-color: rgba(15, 130, 220, 50);
        }
        QListWidget::item:selected:!active {
            border: %(border)spx solid rgba(15, 130, 220, 150);
            border-radius: 2px;
            background-color: rgba(15, 130, 220, 40);
        }
    """

    def __init__(self):
        super(QtIconBrowser, self).__init__()

        self.setWindowIcon(
            self.style().standardIcon(QStyle.SP_TitleBarMenuButton)
        )
        self.setWindowTitle(QtIconBrowser.TITLE)

        self.init_ui()
        self.init_list_wgt()

    def init_ui(self):
        # WIDGET
        self.path_le = QLineEdit()
        self.path_le.setFixedSize(300, 20)
        self.path_le.setReadOnly(True)
        self.path_le.setStyleSheet("padding-left: 1px;")

        self.name_list_wgt = QListWidget()
        self.name_list_wgt.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.name_list_wgt.setStyleSheet(QtIconBrowser.NAME_LIST_WGT_STYLE_SHEET)

        self.icon_list_wgt = QListWidget()
        self.icon_list_wgt.setUniformItemSizes(True)
        self.icon_list_wgt.setViewMode(QListWidget.IconMode)
        self.icon_list_wgt.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.icon_list_wgt.setMovement(QListWidget.Static)

        # LAYOUT
        pixmap_layout = QHBoxLayout()
        pixmap_layout.addStretch()
        pixmap_layout.addWidget(QLabel("Standard Pixmap:"))
        pixmap_layout.addWidget(self.path_le)
        pixmap_layout.setSpacing(5)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(185, 185, 185))

        name_layout = QVBoxLayout()
        name_layout.setContentsMargins(1, 1, 1, 1)
        name_layout.addWidget(self.name_list_wgt)

        name_widget = QWidget()
        name_widget.setFixedWidth(240)
        name_widget.setAutoFillBackground(True)
        name_widget.setPalette(palette)
        name_widget.setLayout(name_layout)

        icon_layout = QVBoxLayout()
        icon_layout.setContentsMargins(1, 1, 1, 1)
        icon_layout.addWidget(self.icon_list_wgt)

        icon_widget = QWidget()
        icon_widget.setMinimumWidth(175)
        icon_widget.setAutoFillBackground(True)
        icon_widget.setPalette(palette)
        icon_widget.setLayout(icon_layout)

        list_wgt_layout = QHBoxLayout()
        list_wgt_layout.addWidget(name_widget)
        list_wgt_layout.addWidget(icon_widget)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(6)
        main_layout.addLayout(pixmap_layout)
        main_layout.addLayout(list_wgt_layout)

        # CONNECTION
        self.name_list_wgt.itemClicked.connect(self.on_item_clicked)
        self.icon_list_wgt.itemClicked.connect(self.on_item_clicked)

    def on_item_clicked(self, item):
        sender = self.sender()

        list_wgt = self.name_list_wgt
        if sender == self.name_list_wgt:
            list_wgt = self.icon_list_wgt

        if not sender.selectedIndexes():
            return

        row = sender.selectedIndexes()[0].row()
        list_wgt.setCurrentRow(row)
        self.scroll_to_selected_index(list_wgt)

        text = item.text()
        self.path_le.setText("QStyle.SP_{}".format(text))

    def init_list_wgt(self):
        self.scrl_bar_width = self.icon_list_wgt.verticalScrollBar().sizeHint().width()

        self.style_sheet = {
            "base_color": self.icon_list_wgt.palette().base().color().name(),
            "padding": QtIconBrowser.PADDING,
            "border": QtIconBrowser.BORDER,
        }

        self.set_item_size()
        self.set_list_wgt()

    def set_item_size(self):
        item_width = QtIconBrowser.GRID_WIDTH + QtIconBrowser.BORDER*2 + QtIconBrowser.PADDING*2
        item_height = QtIconBrowser.GRID_HEIGHT + QtIconBrowser.BORDER*2 + QtIconBrowser.PADDING
        
        self.item_size = QSize(item_width, item_height)

        self.item_width = item_width + QtIconBrowser.PADDING*2
        if self.item_width % 2:
            self.item_width += 1
        
        self.item_height = item_height
        if self.item_height % 2:
            self.item_height += 1

    def set_list_wgt(self):
        i = 0
        while True:
            pixmap = QStyle.StandardPixmap(i)

            name = str(pixmap).rsplit(".", 1)[-1]
            icon = self.style().standardIcon(pixmap)

            if not name.startswith("SP_"):
                break

            pixmap = icon.pixmap(QtIconBrowser.PIXMAP_SIZE)
            name = name[3:]

            if pixmap.size().width() > 0:
                self.name_list_wgt.addItem(name)
                
                item = QListWidgetItem(name)
                item.setSizeHint(self.item_size)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)

                icon = QIcon()
                icon.addPixmap(pixmap, QIcon.Selected)

                item.setIcon(icon)
                self.icon_list_wgt.addItem(item)

            i += 1
        
        self.name_list_wgt.setCurrentRow(0)
        self.icon_list_wgt.setCurrentRow(0)

        text = self.name_list_wgt.item(0).text()
        self.path_le.setText("QStyle.SP_{}".format(text))

    def refresh_icon_list_wgt(self):
        icon_list_wgt_width = self.icon_list_wgt.size().width() - self.scrl_bar_width - 1

        count = int(icon_list_wgt_width / self.item_width)
        spacing = icon_list_wgt_width - self.item_width * count

        add = float(spacing) / count

        if icon_list_wgt_width > (self.item_width * self.icon_list_wgt.count()):
            add = 0

        self.icon_list_wgt.setGridSize(QSize(self.item_width + add, self.item_height))

        if add % 2:
            add -= 1

        self.style_sheet["add"] = str(add/2)

        self.icon_list_wgt.setStyleSheet(
            QtIconBrowser.ICON_LIST_WGT_STYLE_SHEET % self.style_sheet
        )

        self.scroll_to_selected_index(self.icon_list_wgt)

    def scroll_to_selected_index(self, list_wgt):
        if list_wgt.selectedIndexes():
            index = list_wgt.selectedIndexes()[0]
            list_wgt.scrollTo(index, QAbstractItemView.PositionAtCenter)

    def resizeEvent(self, event):
        self.refresh_icon_list_wgt()
    
    def showEvent(self, event):
        self.name_list_wgt.setFocus()
        self.resize(850, 522)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    qt_icon_browser = QtIconBrowser()
    qt_icon_browser.show()
    sys.exit(app.exec_())