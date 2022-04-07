# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("My App")

#         button = QPushButton("Press Me!")
#         button.setCheckable(True)
#         button.clicked.connect(self.the_button_was_clicked)
#         button.clicked.connect(self.the_button_was_toggled)

#         self.setCentralWidget(button)

#     def the_button_was_clicked(self):
#         print("Clicked!")

#     def the_button_was_toggled(self, a, l):
#         print("Checked?", a, l)

# app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

# app.exec()

t = {'a': '2'}
for key,value in t.items():
    value = 4
    key = 0
    print(key, value)
    
print(t)

class human():
    def __init__(self):
        pass
h = human()
print(human and None)