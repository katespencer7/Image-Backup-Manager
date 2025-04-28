import sys # for command line arguments
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt  # Import Qt for alignment


app = QApplication(sys.argv)

class App_Window(QMainWindow):
    def __init__(self):
        super().__init__()
 
        self.setWindowTitle("My App") # set the title
 
        # setting  the geometry of window
        self.setGeometry(0, 0, 500, 300)
 
        self.show()
        self.front_pageUI()

    def front_pageUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        label = QLabel("Open a main directory", self)

        open_button = QPushButton('Open directory', self)
        open_button.setFixedSize(200, 50)
        open_button.clicked.connect(self.button_click)

        front_page = QVBoxLayout()
        front_page.addWidget(label, alignment=Qt.AlignCenter)
        front_page.addWidget(open_button, alignment=Qt.AlignCenter)
        central_widget.setLayout(front_page)
    
    def button_click(self):
        directory = QFileDialog.getExistingDirectory(self)  # Open dialog
        if directory:
            print(f"Selected directory: {directory}")  # Print selected directory path
        else:
            print(f"Error: no directory selected")  # Print selected directory path
    
if __name__ == '__main__':
    window = App_Window() # window
    app.exec() # event loop