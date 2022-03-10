import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication

baseUIClass, baseUIWidget = uic.loadUiType("chess.ui")
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent = None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.load_data()
        self.setup_board()

        self.squares = [self.pushButton_1,
        self.pushButton_2,
        self.pushButton_3,
        self.pushButton_4,
        self.pushButton_5,
        self.pushButton_6,
        ]

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

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Logic()
    #ui.showMaximized()
    ui.show()
    sys.exit(app.exec_())

main()
