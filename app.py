import sys # for command line arguments
import os
import glob
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt  # Import Qt for alignment
from PIL import Image, ImageQt, ImageOps # pillow

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
        
        self.backup_flag = 0 #FIXME
    
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
              self.app.backup_dirs.append(directory)
              print(f"Selected backup: {directory}")
        else:
            print(f"Error: no backup selected")
    
    def next_button(self):
        if self.backup_flag < 3:
            print("Error!!")
            return False
        else:
            self.app.image_display_pageUI()
            return True
    
    def back_front_page(self):
        self.app.front_pageUI()


class DB_Settings:
    def __init__(self, app_window):
        self.app = app_window


class App_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # include other classes
        self.button = Buttons(self)
        self.db = DB_Settings(self)
 
        # app visual settings
        self.setWindowTitle("Image Backup Manager") 
        self.setStyleSheet("background-color: white;")
        self.font_color = "color: #424242;"
        self.setGeometry(0, 0, 1000, 650)

        # store directories
        self.active_dir = None
        self.backup_dirs = []
  
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
        # print(all_backups)
        # if  all_backups == True:
        #     self.app.image_display_pageUI()
        # else:
        #     error = QLabel("Error! Please select three locations.", self)
        #     dir_page.addWidget(error)
        
        back_button = QPushButton('Back', self)
        back_button.setFixedSize(200, 50)
        back_button.setStyleSheet(self.button.style)
        back_button.clicked.connect(self.button.back_front_page)

        # place the buttons next to each other
        utils = QHBoxLayout()
        utils.addWidget(back_button)
        utils.addWidget(next_button)
        utils.setSpacing(5)
        utils.setAlignment(Qt.AlignCenter)
        dir_page.addLayout(utils)
        # dir_page.addWidget(back_button, alignment=Qt.AlignCenter)
        

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
        extentions = ["*.jpg", "*.png", "*.jpeg", "*.JPG", "*.PNG", "*.JPEG"]
        files = []

        for extension in extentions:
          files.extend(glob.glob(os.path.join(self.active_dir, extension))) #FIXME
        
        # # scroll utilization
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        display_page.addWidget(scroll)

        # grid for photos
        img_display = QWidget()
        grid = QGridLayout()
        grid.setSpacing(7)
        grid.setAlignment(Qt.AlignTop)
        img_display.setLayout(grid)
        scroll.setWidget(img_display)
        columns = 5
        pic_size = 175

        for index, img in enumerate(files):
            label = QLabel()

            image = Image.open(img)
            image = ImageOps.exif_transpose(image)  # make sure rotation works
            
            width, height = image.size
            side = max(width, height)
            image = image.resize((side, side), Image.LANCZOS)

            qt_image = ImageQt.ImageQt(image)      
            pixmap = QPixmap.fromImage(qt_image)
            pixmap = pixmap.scaled(pic_size, pic_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            label.setPixmap(pixmap)
            label.setFixedSize(pic_size, pic_size)
            label.setAlignment(Qt.AlignCenter)

            row = index // columns
            column = index % columns
            grid.addWidget(label, row, column)


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