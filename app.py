import sys # for command line arguments
import os
# from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QLabel, QFileDialog
# from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt  # Import Qt for alignment


app = QApplication(sys.argv)

class App_Window(QMainWindow):
    def __init__(self):
        super().__init__()
 
        self.setWindowTitle("My App") # set the title
        self.setStyleSheet("background-color: #FEFBEA;") 
 
        # setting  the geometry of window
        self.setGeometry(0, 0, 1000, 600)
 
        self.show()
        self.front_pageUI()

    def front_pageUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        label = QLabel("Open a main directory", self)
        label.setStyleSheet("color: black;")
        label.setFont(QFont("Helvetica", 23))

        open_button = QPushButton('Open directory', self)
        open_button.setFixedSize(200, 50)
        open_button.clicked.connect(self.open_dir_button)
        open_button.setStyleSheet("color: black;") 

        front_page = QVBoxLayout()
        front_page.addWidget(label, alignment=Qt.AlignCenter)
        front_page.addWidget(open_button, alignment=Qt.AlignCenter)
        central_widget.setLayout(front_page)
    
    def open_dir_button(self):
        directory = QFileDialog.getExistingDirectory(self)  # Open dialog
        if directory:
            print(f"Selected directory: {directory}")  # Print selected directory path
        else:
            print(f"Error: no directory selected")  # Print selected directory path
    
    def display_images(self, directory):
        for filename in os.listdir(directory):
            #     if ".jpg" | ".png" in file_name:
            # chat gpt:
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):  # You can also display folders if you want
                self.central_widget.addItem(filename)
            # end here
    
if __name__ == '__main__':
    window = App_Window() # window
    app.exec() # event loop