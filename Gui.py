import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QDesktopWidget, QGraphicsScene, QGraphicsItem, QGraphicsView, QHBoxLayout, QGraphicsRectItem
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap
from PyQt5.QtCore import Qt

baseUIClass, baseUIWidget = uic.loadUiType("newchess.ui")

class Logic(baseUIClass, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.setup_table()
        self.setup_board()
        self.setWindowIcon(QtGui.QIcon('assets/images/simple/icon.png'))
        self.resize(1500, 1000)
        self.center()
     
        # self.setCentralWidget(Board())

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
    
    def setup_board(self):
        self.label.setPixmap(QtGui.QPixmap('assets/images/simple/Board.png'))

    def center(self):
        rect = self.frameGeometry()
        user = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(user)
        self.move(rect.topLeft())

class Board(QGraphicsView):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.scene = QGraphicsScene(0, 0, 100, 100)
        # pixmap = QPixmap('assets/images/simple/Board.png')
        # self.scene.addPixmap(pixmap)
        # self.setScene(self.scene)
        length = 20
        for i in range(8):
            for n in range(8):
                rect = QGraphicsRectItem(20 * i, 20 * n, length, length)
                self.scene.addItem(rect)
        self.setScene(self.scene)

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

    ui = Logic()
    # board = Board(ui)
    ui.show()
    #ui.showMaximized()
    
    sys.exit(app.exec_())
