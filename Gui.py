import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import (QDialog, QApplication, QDesktopWidget, QGraphicsScene, QGraphicsItem, QGraphicsView, 
QHBoxLayout, QGraphicsRectItem, QWidget, QGraphicsPixmapItem, QGridLayout, QGraphicsGridLayout)
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap, QPainter
from PyQt5.QtCore import Qt

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu.ui', self)
        self.setup_table()
        self.setWindowIcon(QtGui.QIcon('assets/images/simple/icon.png'))
        self.resize(1500, 1000)
        self.center()
        self.board = Board()

        self.layout_container = QGridLayout()
        self.layout_container.addWidget(self.board, 0, 0)
        self.layout_container.addWidget(self.tableWidget, 0, 1)
        self.layout_container.addWidget(self.resetButton, 1, 1)
        # self.layout_container.setSpacing(0)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout_container)
        self.setCentralWidget(self.central_widget)

    def setup_table(self):
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setFixedSize(500, 840)
        self.load_data()

    def load_data(self):
        log = [{'move': 1, 'white': 'e2e4', 'black': 'e7e5'}]
        row = 0
        self.tableWidget.setRowCount(len(log))
        for move in log:

            # Must convert any ints to strings
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(move['white']))
            row += 1
    
        self.label.setPixmap(QtGui.QPixmap('assets/images/simple/Board.png'))

    def center(self):
        rect = self.frameGeometry()
        user = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(user)
        self.move(rect.topLeft())

class Board(QGraphicsView):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.scene = QGraphicsScene()
        self.length = 68
        self.setup_board()
        self.setup_squares()
        self.setScene(self.scene)
        for item in self.scene.items():
            pass
    def setup_board(self):
        pixmap = QPixmap('assets/images/simple/Board.png').scaled(560, 560, Qt.IgnoreAspectRatio)
        pixItem = QGraphicsPixmapItem(pixmap)
        pixItem.setPos(-7, -7)
        self.scene.addItem(pixItem)
        
    def setup_squares(self):
        
        for i in range(8):
            for n in range(8):
                rect = QGraphicsRectItem(self.length * i, self.length * n, self.length, self.length)
                self.scene.addItem(rect)
                self.scene.addEllipse(self.length * i, self.length * n, self.length, self.length)
                pixmap = QPixmap('assets/images/simple/Piece=Bishop, Side=Black.png').scaled(self.length, self.length, Qt.IgnoreAspectRatio)
                pixItem = QGraphicsPixmapItem(pixmap)
                pixItem.setPos(self.length * i, self.length * n)
                self.scene.addItem(pixItem)
                pixItem.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

    def pos_to_coord(self, x, y):
        x = x // self.length
        y = y // self.length

        x = 'abcdefgh'[x]
        y = '12345678'[y]
        pos = x + y
        return pos


                
def dark_palette():
    # Returns a QPalette object with a dark style! 
    # Shamelessly stolen

    dark_palette = QPalette()

    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)

    return dark_palette

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    app.setStyle('Fusion')
    app.setPalette(dark_palette())

    ui = MainWindow()
    ui.show()
    
    # b = Board()
    # b.show()
    sys.exit(app.exec_())
