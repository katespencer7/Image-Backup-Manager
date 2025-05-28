import sys # for command line arguments
import os
import glob
import json
import hashlib

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt  # Import Qt for alignment
from PIL import Image, ImageQt, ImageOps # pillow

app = QApplication(sys.argv)

class Buttons:
    def __init__(self, app_window, json_settings, checker):
        self.app = app_window
        self.json_set = json_settings
        self.hash_check = checker

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
            # self.app.directory_screen_pageUI(directory)
            self.app.image_display_pageUI()
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
            checkbox.setChecked(bool)
    
    def store_hash(self, checklist):
        for checkbox, img in self.app.checked:
            if checkbox.isChecked():
                self.json_set.send_to_json(img)
    
    # def check_hash(self):
    #     for checkbox, img in self.app.checked:
    #         if checkbox.isChecked():
    #             self.json_set.check_authenticity(img)



class JSON_Settings:
    def __init__(self, app_window):
        self.app = app_window
        self.button = Buttons


    def compute_hash(self, path):
        with open(path, "rb") as file:
            return hashlib.sha256(file.read()).hexdigest()
    

    def send_to_json(self, path):
        hash = self.compute_hash(path)
        
        new_data = {
            "name": path,
            "hash": hash
        }

        with open("sha256.json", "r+") as json_file:
            existing_data = json.load(json_file)
            
            alr_added = any(entry["name"] == path for entry in existing_data["backups"])
            if not alr_added: # prevent duplicates
                existing_data["backups"].append(new_data)
                json_file.seek(0)
                json.dump(existing_data, json_file, indent=4)



class Check_Hash:
    def __init__(self, app_window, json_settings):
        self.app = app_window
        self.file = json_settings

        self.active_dir = None
        self.incorrect_hashes = []
        
    def check_authenticity(self):
        self.active_dir = QFileDialog.getExistingDirectory(self.app)  # open dialog
        
        extentions = ["*.jpg", "*.png", "*.jpeg", "*.JPG", "*.PNG", "*.JPEG"]
        files = []
        for extension in extentions:
          files.extend(glob.glob(os.path.join(self.active_dir, extension)))

        with open("sha256.json", "r") as json_file:
            data = json.load(json_file)
            hashes = [entry["hash"] for entry in data["backups"]]
            names = [entry["name"] for entry in data["backups"]]

        for index, img in enumerate(files):
            val = self.file.compute_hash(img)
            if img not in names:
                continue
            else:
                if val not in hashes:
                    self.incorrect_hashes.append(img)
        
        self.popup() # results
        
    def popup(self):
        window = QMessageBox()
        window.setWindowTitle("Check Results")
        window.setStandardButtons(QMessageBox.Ok)
        
        if self.incorrect_hashes == []:
            window.setText("Files have not been edited")
        else:
            all_hashes = "The files that have been edited are:\n"
            for name in self.incorrect_hashes:
                # name = self.get_path(val)
                # print(name)
                all_hashes += name + "\n"
            window.setText(all_hashes)
        
        window.exec_()



class App_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # include other classes
        self.hash = JSON_Settings(self)
        self.check_hash = Check_Hash(self, self.hash)
        self.button = Buttons(self, self.hash, self.check_hash)


        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
 
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


    def set_page(self, widget):
        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)


    def front_pageUI(self):
        '''opening page'''

        central_widget = QWidget()

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

        authenticity_button = QPushButton('Verify hash', self)
        authenticity_button.setFixedSize(200, 50)
        authenticity_button.setStyleSheet(self.button.style)
        authenticity_button.clicked.connect(self.check_hash.check_authenticity)
        front_page.addWidget(authenticity_button, alignment=Qt.AlignCenter)

        central_widget.setLayout(front_page)
        self.set_page(central_widget)


    def directory_screen_pageUI(self, directory):
        '''set backups 2 & 1'''

        directory_widget = QWidget()        
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
        
        backup_now_button = QPushButton('Backup Now', self)
        backup_now_button.setFixedSize(200, 50)
        backup_now_button.setStyleSheet(self.button.style)
        backup_now_button.clicked.connect(lambda: self.button.store_hash(self.checked))
        
        back_button = QPushButton('Back', self)
        back_button.setFixedSize(200, 50)
        back_button.setStyleSheet(self.button.style)
        back_button.clicked.connect(lambda: self.button.back_to_page(self.image_display_pageUI))

        # place the buttons next to each other
        # side_utils = QHBoxLayout()
        # side_utils.addWidget(backone_button)
        # side_utils.addWidget(backtwo_button)
        # side_utils.addWidget(cloud_button)


        bottom_utils = QHBoxLayout()
        bottom_utils.addWidget(back_button)
        bottom_utils.addWidget(backup_now_button)
        bottom_utils.setSpacing(10)
        bottom_utils.setAlignment(Qt.AlignCenter)
        dir_page.addLayout(bottom_utils)
        
        directory_widget.setLayout(dir_page)
        self.set_page(directory_widget)

        # dir_page.addWidget(back_button, alignment=Qt.AlignCenter)
        

    def image_display_pageUI(self):
        '''image scroll through GUI'''
        self.checked = [] # base case

        display_widget = QWidget()
        # self.setCentralWidget(display_widget)

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
          files.extend(glob.glob(os.path.join(self.active_dir, extension)))
        
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
        back_button.clicked.connect(lambda: self.button.back_to_page(lambda: self.front_pageUI()))
        # display_page.addWidget(back_button)

        # backup now button
        backup_button = QPushButton('Choose Backup Directories', self)
        backup_button.setFixedSize(200, 50)
        backup_button.setStyleSheet(self.button.style)
        backup_button.clicked.connect(lambda: self.directory_screen_pageUI(self.active_dir))

        # authenticity_button = QPushButton('Verify hash', self)
        # authenticity_button.setFixedSize(200, 50)
        # authenticity_button.setStyleSheet(self.button.style)
        # authenticity_button.clicked.connect(lambda: self.button.check_hash())

        # place the buttons next to each other
        butils = QHBoxLayout()
        butils.addWidget(back_button)
        butils.addWidget(backup_button)
        # butils.addWidget(authenticity_button)
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
        self.set_page(display_widget)


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