import sys # for command line arguments
import os
import glob
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
        self.button_style = """QPushButton {
                              background-color : #f1f1f1;
                              color: #424242;
                              border-radius: 10px;
                              }
                          QPushButton:hover {
                              background-color: #E9E9E9;
                              }"""
        # for future use:
        self.backuptype = 1
        self.active_dir = None
 
        self.setGeometry(0, 0, 1000, 700)
 
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
        open_button.setStyleSheet(self.button_style)
        # layout
        front_page = QVBoxLayout()
        front_page.addWidget(label, alignment=Qt.AlignCenter)
        front_page.addWidget(open_button, alignment=Qt.AlignCenter)
        
        central_widget.setLayout(front_page)
    
    def open_dir_button(self):
        directory = QFileDialog.getExistingDirectory(self)  # Open dialog
        if directory:
            if self.backuptype == 1:
              print(f"Selected directory: {directory}")  # Print selected directory path
              self.active_dir = directory
              self.directory_screen_pageUI(directory)
            elif self.backuptype == 2:
              print(f"Selected backup: {directory}")
        else:
            print(f"Error: no directory selected")  # Print selected directory path

    def directory_screen_pageUI(self, directory):
        directory_widget = QWidget()
        self.setCentralWidget(directory_widget)
        
        screen = QLabel(f"Selected directory: {directory}", self)
        screen.setStyleSheet("color: #424242;")

        dir_page = QVBoxLayout()
        dir_page.addWidget(screen, alignment=Qt.AlignCenter)

        backone_button = QPushButton('Set backup 1 directory', self)
        backtwo_button = QPushButton('Set backup 2 directory', self)
        cloud_button = QPushButton('Set cloud backup location', self)

        all_buttons = [backone_button, backtwo_button, cloud_button]

        for button in all_buttons:
            self.backuptype = 2
            print(self.backuptype)
            button.setFixedSize(200, 50)
            button.clicked.connect(self.open_dir_button)
            button.setStyleSheet(self.button_style)
            dir_page.addWidget(button, alignment=Qt.AlignCenter)

        directory_widget.setLayout(dir_page)
        
        next_button = QPushButton('Next', self)
        next_button.setFixedSize(200, 50)
        next_button.setStyleSheet(self.button_style)
        next_button.clicked.connect(self.image_display_pageUI)

        dir_page.addWidget(next_button, alignment=Qt.AlignCenter)
    
    def image_display_pageUI(self):
        print(f"{self.active_dir}")
        display_widget = QWidget()
        self.setCentralWidget(display_widget)

        title = QLabel(f"Selected directory: {self.active_dir}", self)
        title.setStyleSheet("color: #424242;")

        display_page = QVBoxLayout()
        display_page.addWidget(title, alignment=Qt.AlignCenter)
        display_widget.setLayout(display_page)

        # image display information
        extentions = ["*.jpg", "*.png", "*.jpeg", "*.JFIF"]
        files = []

        for extension in extentions:
          files.extend(glob.glob(os.path.join(self.active_dir, extension))) #fixme
          print(f'{files}')

        # scroll utilization
        scroll = QScrollArea()
        display_page.addWidget(scroll)

        for img in files:
            pixmap = QPixmap(img)
            scroll.setWidget(img)

        display_page.setWidget(scroll)



    
    # def display_images(self, directory):
    #     for filename in os.listdir(directory):
    #         #     if ".jpg" | ".png" in file_name:
    #         # chat gpt:
    #         filepath = os.path.join(directory, filename)
    #         if os.path.isfile(filepath):  # You can also display folders if you want
    #             self.central_widget.addItem(filename)
    #         # end here
    
    ''' To use in the future for choosing more directories'''

    # def open_backup(self):
    #     directory = QFileDialog.getExistingDirectory(self)  # Open dialog
    #     if directory:
    #         print(f"Selected backup: {directory}")  # Print selected directory path
    #     else:
    #         print(f"Error: no directory selected")  # Print selected directory path
    
    # def open_backup_two(self):
    #     directory = QFileDialog.getExistingDirectory(self)  # Open dialog
    #     if directory:
    #         print(f"Selected backup: {directory}")  # Print selected directory path
    #     else:
    #         print(f"Error: no directory selected")  # Print selected directory path
    
    # def open_cloud_backup(self):
    #     directory = QFileDialog.getExistingDirectory(self)  # Open dialog
    #     if directory:
    #         print(f"Selected cloud location: {directory}")  # Print selected directory path
    #     else:
    #         print(f"Error: no directory selected")  # Print selected directory path


if __name__ == '__main__':
    window = App_Window() # window
    app.exec() # event loop