import sys # for command line arguments
import os
import glob
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt  # Import Qt for alignment


app = QApplication(sys.argv)

class Buttons:
    def __init__(self, app_window):
        self.app = app_window

        self.style = """QPushButton {
                              background-color : #f1f1f1;
                              color: #424242;
                              border-radius: 10px;
                              }
                          QPushButton:hover {
                              background-color: #E9E9E9;
                              }"""
        
        self.backup_flag = 0
    
        # button functionality
    def open_dir(self):
        directory = QFileDialog.getExistingDirectory(self.app)  # open dialog
        if directory:
            self.app.active_dir = directory
            self.app.directory_screen_pageUI(directory)
        else:
            print(f"Error: no directory selected")

    def backup(self):
        directory = QFileDialog.getExistingDirectory(self.app)  # open dialog
        if directory:
              self.backup_flag += 1
              print(f"Selected backup: {directory}")
        else:
            print(f"Error: no backup selected")
    
    def next_button(self):
        if self.backup_flag != 3:
            error_txt = QLabel("Error! Please select three locations.", self.app)
            print("Error!!")
        else:
            self.app.image_display_pageUI()



class App_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button = Buttons(self)
 
        self.setWindowTitle("Image Backup Manager") 
        self.setStyleSheet("background-color: white;")
        self.font_color = "color: #424242;"
        
        # for future use:
        self.backuptype = 1
        self.active_dir = None
 
        self.setGeometry(0, 0, 1000, 750)
 
        self.show()
        self.front_pageUI()

    # opening page
    def front_pageUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # title
        label = QLabel("Open a main directory", self)
        label.setStyleSheet(self.font_color)
        label.setFont(QFont("Helvetica", 23))

        # open directory button
        open_button = QPushButton('Open main directory', self)
        open_button.setFixedSize(200, 50)
        open_button.clicked.connect(self.button.open_dir)
        open_button.setStyleSheet(self.button.style)
        # layout
        front_page = QVBoxLayout()
        front_page.addWidget(label, alignment=Qt.AlignCenter)
        front_page.addWidget(open_button, alignment=Qt.AlignCenter)
        
        central_widget.setLayout(front_page)
    

    # setting 2 & 1 directories
    def directory_screen_pageUI(self, directory):
        directory_widget = QWidget()
        self.setCentralWidget(directory_widget)
        
        screen = QLabel(f"Selected directory: {directory}", self)
        screen.setStyleSheet(self.font_color)

        dir_page = QVBoxLayout()
        dir_page.addWidget(screen, alignment=Qt.AlignCenter)

        backone_button = QPushButton('Set backup 1 directory', self)
        backtwo_button = QPushButton('Set backup 2 directory', self)
        cloud_button = QPushButton('Set cloud backup location', self)

        all_buttons = [backone_button, backtwo_button, cloud_button]

        for button in all_buttons:
            button.setFixedSize(200, 50)
            button.clicked.connect(self.button.backup)
            button.setStyleSheet(self.button.style)
            dir_page.addWidget(button, alignment=Qt.AlignCenter)

        directory_widget.setLayout(dir_page)
        
        next_button = QPushButton('Next', self)
        next_button.setFixedSize(200, 50)
        next_button.setStyleSheet(self.button.style)
        next_button.clicked.connect(self.button.next_button)

        dir_page.addWidget(next_button, alignment=Qt.AlignCenter)
    

    # image scroll through GUI
    def image_display_pageUI(self):
        display_widget = QWidget()
        self.setCentralWidget(display_widget)

        title = QLabel(f"Selected directory: {self.active_dir}", self)
        title.setStyleSheet(self.font_color)

        display_page = QVBoxLayout()
        display_page.addWidget(title, alignment=Qt.AlignCenter)
        display_widget.setLayout(display_page)

        # image display information
        extentions = ["*.jpg", "*.png", "*.jpeg", "*.JFIF"]
        files = []

        for extension in extentions:
          files.extend(glob.glob(os.path.join(self.active_dir, extension))) #fixme
        
        # # scroll utilization
        scroll = QScrollArea()
        display_page.addWidget(scroll)

        # grid for photos
        img_display = QWidget()
        grid = QGridLayout()
        img_display.setLayout(grid)
        scroll.setWidget(img_display)
        columns = 4
        pic_size = 175

        index = 0
        for img in files:
            label = QLabel()
            pixmap = QPixmap(img)
            pixmap = pixmap.scaled(pic_size, pic_size)
            label.setPixmap(pixmap)
            label.setFixedSize(pic_size, pic_size)

            row = index // columns
            column = index % columns
            grid.addWidget(label, row, column)

            index += 1


        # display_page.setWidget(scroll)



    
    # def display_images(self, directory):
    #     for filename in os.listdir(directory):
    #         #     if ".jpg" | ".png" in file_name:
    #         # chat gpt:
    #         filepath = os.path.join(directory, filename)
    #         if os.path.isfile(filepath):  # You can also display folders if you want
    #             self.central_widget.addItem(filename)
    #         # end here


if __name__ == '__main__':
    window = App_Window() # window
    app.exec() # event loop