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
 
        self.setWindowTitle("Image Backup Manager") 
        self.setStyleSheet("background-color: white;") 
 
        self.setGeometry(0, 0, 1000, 700)
        # self.setGeometry(0, 0, 500, 300)
 
        self.show()
        self.front_pageUI()

    def front_pageUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # title
        label = QLabel("Open a main directory", self)
        label.setStyleSheet("color: #424242;")
        label.setFont(QFont("Helvetica", 23))

        # open directory button
        open_button = QPushButton('Open main directory', self)
        open_button.setFixedSize(200, 50)
        open_button.clicked.connect(self.open_dir_button)
        open_button.setStyleSheet("""
                                QPushButton {
                                    background-color : #f1f1f1;
                                    color: #424242;
                                    border-radius: 10px;
                                  }
                                QPushButton:hover {
                                  background-color: #E9E9E9;
                                  }
                                """)
        # layout
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
    
    # def display_images(self, directory):
    #     for filename in os.listdir(directory):
    #         #     if ".jpg" | ".png" in file_name:
    #         # chat gpt:
    #         filepath = os.path.join(directory, filename)
    #         if os.path.isfile(filepath):  # You can also display folders if you want
    #             self.central_widget.addItem(filename)
    #         # end here
    
    ''' To use in the future for choosing more directories'''
    def backup_oneUI(self):
        backone_button = QPushButton('Set backup 1 directory', self)
        backone_button.setFixedSize(200, 50)
        backone_button.clicked.connect(self.open_dir_button)
        backone_button.setStyleSheet("""
                                QPushButton {
                                    background-color : #f1f1f1;
                                    color: #424242;
                                    border-radius: 10px;
                                  }
                                QPushButton:hover {
                                  background-color: #E9E9E9;
                                  }
                                """)
    def open_backup_one(self):
        directory = QFileDialog.getExistingDirectory(self)  # Open dialog
        if directory:
            print(f"Selected backup: {directory}")  # Print selected directory path
        else:
            print(f"Error: no directory selected")  # Print selected directory path
        
    def backup_twoUI(self):
        backtwo_button = QPushButton('Set backup 2 directory', self)
        backtwo_button.setFixedSize(200, 50)
        backtwo_button.clicked.connect(self.open_dir_button)
        backtwo_button.setStyleSheet("""
                                QPushButton {
                                    background-color : #f1f1f1;
                                    color: #424242;
                                    border-radius: 10px;
                                  }
                                QPushButton:hover {
                                  background-color: #E9E9E9;
                                  }
                                """)
    
    def open_backup_two(self):
        directory = QFileDialog.getExistingDirectory(self)  # Open dialog
        if directory:
            print(f"Selected backup: {directory}")  # Print selected directory path
        else:
            print(f"Error: no directory selected")  # Print selected directory path
    
    def cloud_backupUI(self):
        cloud_button = QPushButton('Set cloud backup location', self)
        cloud_button.setFixedSize(200, 50)
        cloud_button.clicked.connect(self.open_dir_button)
        cloud_button.setStyleSheet("""
                                QPushButton {
                                    background-color : #f1f1f1;
                                    color: #424242;
                                    border-radius: 10px;
                                  }
                                QPushButton:hover {
                                  background-color: #E9E9E9;
                                  }
                                """)
    
    def open_cloud_backup(self):
        directory = QFileDialog.getExistingDirectory(self)  # Open dialog
        if directory:
            print(f"Selected cloud location: {directory}")  # Print selected directory path
        else:
            print(f"Error: no directory selected")  # Print selected directory path


if __name__ == '__main__':
    window = App_Window() # window
    app.exec() # event loop