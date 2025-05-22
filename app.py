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
            # self.app.image_display_pageUI()
        else:
            print(f"Error: no directory selected")

    def backup(self, flag):
        directory = QFileDialog.getExistingDirectory(self.app)  # open dialog
        if directory:
            if flag == 1:
                self.backup_flag += 1
                self.app.backup_dir1 = directory
            
            elif flag == 2:
                self.backup_flag += 1
                self.app.backup_dir2 = directory

            elif flag == 3:
                self.backup_flag += 1
                self.app.backup_dir3 = directory
            
            print(f"Selected backup: {directory}")
        else:
            print(f"Error: no backup selected")
    
    def next(self):
        if self.backup_flag < 3:
            print("Error!!")
            return False
        else:
            self.app.image_display_pageUI()
            return True
    
    def back_to_page(self, pagefn):
        pagefn()
    
    def select_all(self, bool):
        for checkbox, img in self.app.checked:
            checkbox.setChecked(bool);



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
        self.setMinimumSize(1000, 700)

        # storage
        self.active_dir = None
        self.backup_dir1 = None
        self.backup_dir2 = None
        self.backup_dir3 = None
        self.img_files = []

        # checkboxes
        self.checked = []
  
        self.show()
        self.front_pageUI()


    def front_pageUI(self):
        '''opening page'''

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


    def directory_screen_pageUI(self, directory):
        '''set backups 2 & 1'''

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
            button.setStyleSheet(self.button.style)
            dir_page.addWidget(button, alignment=Qt.AlignCenter)

        backone_button.clicked.connect(lambda: self.button.backup(1))
        backtwo_button.clicked.connect(lambda: self.button.backup(2))
        cloud_button.clicked.connect(lambda: self.button.backup(3))

        directory_widget.setLayout(dir_page)
        
        next = QPushButton('Next', self)
        next.setFixedSize(200, 50)
        next.setStyleSheet(self.button.style)
        next.clicked.connect(self.button.next)
        # print(all_backups)
        # if  all_backups == True:
        #     self.app.image_display_pageUI()
        # else:
        #     error = QLabel("Error! Please select three locations.", self)
        #     dir_page.addWidget(error)
        
        back_button = QPushButton('Back', self)
        back_button.setFixedSize(200, 50)
        back_button.setStyleSheet(self.button.style)
        back_button.clicked.connect(lambda: self.button.back_to_page(self.front_pageUI))

        # place the buttons next to each other
        utils = QHBoxLayout()
        utils.addWidget(back_button)
        utils.addWidget(next)
        utils.setSpacing(5)
        utils.setAlignment(Qt.AlignCenter)
        dir_page.addLayout(utils)
        # dir_page.addWidget(back_button, alignment=Qt.AlignCenter)
        

    def image_display_pageUI(self):
        '''image scroll through GUI'''
        self.checked = [] # base case

        display_widget = QWidget()
        self.setCentralWidget(display_widget)

        title = QLabel(f"Selected directory: {self.active_dir}", self)
        title.setStyleSheet(self.font_color)

        display_page = QVBoxLayout()
        display_page.addWidget(title, alignment=Qt.AlignCenter)
        display_widget.setLayout(display_page)

        # buttons
        select_all_button = QPushButton('Select all', self)
        select_all_button.setFixedSize(100, 25)
        select_all_button.clicked.connect(lambda: self.button.select_all(True))
        select_all_button.setStyleSheet(self.button.style)

        deselect_all_button = QPushButton('Deselect all', self)
        deselect_all_button.setFixedSize(100, 25)
        deselect_all_button.clicked.connect(lambda: self.button.select_all(False))
        deselect_all_button.setStyleSheet(self.button.style)

        # place the buttons next to each other
        utils = QHBoxLayout()
        utils.addWidget(select_all_button)
        utils.addWidget(deselect_all_button)
        utils.setSpacing(5)
        utils.setAlignment(Qt.AlignRight)
        display_page.addLayout(utils)

        # image display information
        extentions = ["*.jpg", "*.png", "*.jpeg", "*.JPG", "*.PNG", "*.JPEG"]
        files = []

        for extension in extentions:
          files.extend(glob.glob(os.path.join(self.active_dir, extension))) #FIXME
        
        files = sorted(files, key=os.path.getctime, reverse=True) # most recent at the top
        self.img_files = files # store in class

        # # scroll utilization
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        display_page.addWidget(scroll)

        # back button
        back_button = QPushButton('Back', self)
        back_button.setFixedSize(200, 50)
        back_button.setStyleSheet(self.button.style)
        back_button.clicked.connect(lambda: self.button.back_to_page(lambda: self.directory_screen_pageUI(self.active_dir)))
        # display_page.addWidget(back_button)

        # backup now button #FIXME does nothing
        backup_button = QPushButton('Backup Now', self)
        backup_button.setFixedSize(200, 50)
        backup_button.setStyleSheet(self.button.style)

        # place the buttons next to each other
        butils = QHBoxLayout()
        butils.addWidget(back_button)
        butils.addWidget(backup_button)
        butils.setSpacing(10)
        display_page.addLayout(butils)

        # grid for photos
        img_display = QWidget()
        grid = QGridLayout()
        grid.setSpacing(7)
        grid.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        img_display.setLayout(grid)
        scroll.setWidget(img_display)
        columns = 5
        pic_size = 175

        for index, img in enumerate(files):
            widget = QWidget()
            widget.setFixedSize(pic_size, pic_size)
            label = QLabel(widget)

            image = Image.open(img)
            image = ImageOps.exif_transpose(image)  # make sure rotation works
            
            qt_image = ImageQt.ImageQt(self._crop_img(image))      
            pixmap = QPixmap.fromImage(qt_image)
            pixmap = pixmap.scaled(pic_size, pic_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            label.setPixmap(pixmap)
            label.setFixedSize(pic_size, pic_size)
            label.setAlignment(Qt.AlignCenter)

            checkbox = QCheckBox(widget)
            checkbox.move(5,5)
            checkbox.setStyleSheet("QCheckBox {background: transparent;}")
            self.checked.append((checkbox, img)) # add all to self for future ref

            row = index // columns
            column = index % columns
            grid.addWidget(widget, row, column)


    def _crop_img(self, image):
        '''crop image to be square'''

        width, height = image.size 
        side = min(width, height)
        left = (width - side) // 2
        top = (height - side) // 2
            
        cropped = image.crop((left, top, left + side, top + side))
        cropped = cropped.resize((side, side), Image.LANCZOS)
        return cropped


if __name__ == '__main__':
    window = App_Window() # window
    app.exec() # event loop