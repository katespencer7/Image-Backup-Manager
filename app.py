import sys # for command line arguments
import os
import glob
import json
import hashlib
import shutil # for copy

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt  # Import Qt for alignment
from PIL import Image, ImageQt, ImageOps # pillow

app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont(os.path.abspath("assets/centurygothic.ttf"))
font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
app.setFont(QFont(font_family))

class Buttons:
    def __init__(self, app_window, json_settings, checker):
        self.app = app_window
        self.json_set = json_settings
        self.hash_check = checker

        self.style = """QPushButton {
                              background-color : #e2e2e2;
                              color: #424242;
                              border-radius: 10px;
                              }
                          QPushButton:hover {
                              background-color: #dadada;
                              }"""
        
        self.false_style = """QPushButton {
                              background-color : #f1f1f1;
                              color: #424242;
                              border-radius: 10px;
                              }"""
            
        # button functionality
    def open_dir(self):
        directory = QFileDialog.getExistingDirectory(self.app)  # open dialog
        if directory:
            self.app.active_dir = directory
            self.app.image_display_pageUI()
        else:
            print(f"Error: no directory selected")

    def backup(self, flag):
        directory = QFileDialog.getExistingDirectory(self.app)  # open dialog
        if directory:
            if flag == 1:
                self.app.backup_dir1 = directory
            
            elif flag == 2:
                self.app.backup_dir2 = directory

            elif flag == 3:
                self.app.backup_dir3 = directory
            
        if (self.app.backup_dir1 != None) & (self.app.backup_dir2 != None) & (self.app.backup_dir3 != None):
            self.app.backup_now_button.setStyleSheet(self.style)
            self.app.backup_now_button.setEnabled(True) # enable

    
    def back_to_page(self, pagefn):
        pagefn()
    
    def select_all(self, bool):
        for checkbox, img in self.app.checked:
            checkbox.setChecked(bool)
    
    def store_hash(self):
        for checkbox, img in self.app.checked:
            if checkbox.isChecked():
                self.json_set.send_to_json(img)
        self.app.copy_files()

    def backup_now(self):
        if (self.app.backup_dir1 != None) & (self.app.backup_dir2 != None) & (self.app.backup_dir3 != None):
            self.store_hash()



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

        self.style = """
                        QMessageBox {
                              background-color: white;
                              }
                        QLabel {
                              color: #424242;
                              font-family: Helvetica;
                              text-align: center;
                              }
                        QPushButton {
                              background-color : #f1f1f1;
                              color: #424242;
                              border-radius: 10px;
                              padding: 5px 10px
                              }
                        QPushButton:hover {
                              background-color: #E9E9E9;
                              }
                          """
        

    def check_authenticity(self):
        self.incorrect_hashes = [] # base case
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
                    img_file = os.path.basename(img)
                    self.incorrect_hashes.append(img_file)
        
        self.popup() # results
        

    def popup(self):
        window = QMessageBox()
        window.setWindowTitle("Check Results")
        window.setStandardButtons(QMessageBox.Ok)
        window.setStyleSheet(self.style)
        
        if self.incorrect_hashes == []:
            window.setText("Files have not been edited")
        else:
            all_hashes = "The files that have been edited are:\n\n"
            for name in self.incorrect_hashes:
                all_hashes += name + "\n"
            window.setText(all_hashes)
        
        window.exec_()



class Add_Del:
    def __init__(self, app_window):
        self.app = app_window

    def add(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self.app,
        "Select image files to add", "", "Image Files (*.jpg *.jpeg *.png *.JPG *.JPEG *.PNG)")

        for filen in file_paths:
            dest_path = os.path.join(self.app.active_dir, os.path.basename(filen))
            if not os.path.exists(dest_path):
                shutil.copy2(filen, self.app.active_dir)
        
        self.app.image_display_pageUI() # refresh page with new pics

    def delete(self):
        trash = os.path.join(os.getcwd(), "trash")
        os.makedirs(trash, exist_ok=True)


        for checkbox, img in self.app.checked:
            if checkbox.isChecked():
                if os.path.exists(img): 
                    shutil.move(img, trash) # move to trash directory
        
        self.app.image_display_pageUI()



class App_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # include other classes
        self.hash = JSON_Settings(self)
        self.check_hash = Check_Hash(self, self.hash)
        self.button = Buttons(self, self.hash, self.check_hash)
        self.add_del = Add_Del(self)
 
        # app visual settings
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
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

        # # title
        logo = QLabel()
        pixmap = QPixmap("assets/logo.png")
        pixmap = pixmap.scaled(662, 132, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)

        # open directory button
        open_button = QPushButton('Open main directory', self)
        open_button.setFixedSize(300, 75)
        open_button.clicked.connect(self.button.open_dir)
        open_button.setStyleSheet(self.button.style + "QPushButton{font-size: 18px;}")
        
        # check hash button
        authenticity_button = QPushButton('Verify hash', self)
        authenticity_button.setFixedSize(300, 75)
        authenticity_button.setStyleSheet(self.button.style)
        authenticity_button.clicked.connect(self.check_hash.check_authenticity)
        authenticity_button.setStyleSheet(self.button.style + "QPushButton{font-size: 18px;}")

        buttons = QHBoxLayout()
        buttons.addWidget(authenticity_button)
        buttons.addWidget(open_button)
        buttons.setSpacing(45)
        buttons.setAlignment(Qt.AlignCenter)

        # layout
        front_page = QVBoxLayout()
        front_page.addWidget(logo, alignment=Qt.AlignCenter)
        front_page.addLayout(buttons)

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
        
        self.backup_now_button = QPushButton('Backup Now', self)
        self.backup_now_button.setFixedSize(200, 50)
        self.backup_now_button.setStyleSheet(self.button.false_style)
        self.backup_now_button.setEnabled(False) # disable
        self.backup_now_button.clicked.connect(lambda: self.button.backup_now())

        back_button = QPushButton('Back', self)
        back_button.setFixedSize(200, 50)
        back_button.setStyleSheet(self.button.style)
        back_button.clicked.connect(lambda: self.button.back_to_page(self.image_display_pageUI))

        bottom_utils = QHBoxLayout()
        bottom_utils.addWidget(back_button)
        bottom_utils.addWidget(self.backup_now_button)
        bottom_utils.setSpacing(30)
        bottom_utils.setAlignment(Qt.AlignCenter)
        dir_page.addLayout(bottom_utils)
        
        directory_widget.setLayout(dir_page)
        self.set_page(directory_widget)
        

    def image_display_pageUI(self):
        '''image scroll through GUI'''
        self.checked = [] # base case

        display_widget = QWidget()
        title = QLabel(f"Selected directory: {self.active_dir}", self)
        title.setStyleSheet(self.font_color)

        display_page = QVBoxLayout()
        display_page.addWidget(title, alignment=Qt.AlignCenter)
        display_widget.setLayout(display_page)

        utils = self._top_bar_buttons()
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

        # backup now button
        backup_button = QPushButton('Choose Backup Directories', self)
        backup_button.setFixedSize(200, 50)
        backup_button.setStyleSheet(self.button.style)
        backup_button.clicked.connect(lambda: self.directory_screen_pageUI(self.active_dir))

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

            # calculate grid
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
    

    def _top_bar_buttons(self):
        '''buttons for image_display_pageUI, makes function shorter'''
        # add/delete buttons
        add_button = QPushButton('Add +', self)
        add_button.setFixedSize(100, 25)
        add_button.clicked.connect(self.add_del.add)
        add_button.setStyleSheet(self.button.style)

        delete_button = QPushButton('Delete -', self)
        delete_button.setFixedSize(100, 25)
        delete_button.clicked.connect(self.add_del.delete)
        delete_button.setStyleSheet(self.button.style)

        adutils = QHBoxLayout()
        adutils.addWidget(add_button)
        adutils.addWidget(delete_button)
        adutils.setSpacing(5)
        adutils.setAlignment(Qt.AlignLeft)

        # select/deselect buttons
        select_all_button = QPushButton('Select all', self)
        select_all_button.setFixedSize(100, 25)
        select_all_button.clicked.connect(lambda: self.button.select_all(True))
        select_all_button.setStyleSheet(self.button.style)

        deselect_all_button = QPushButton('Deselect all', self)
        deselect_all_button.setFixedSize(100, 25)
        deselect_all_button.clicked.connect(lambda: self.button.select_all(False))
        deselect_all_button.setStyleSheet(self.button.style)

        sdutils = QHBoxLayout()
        sdutils.addWidget(select_all_button)
        sdutils.addWidget(deselect_all_button)
        sdutils.setSpacing(5)
        sdutils.setAlignment(Qt.AlignRight)

        # combine all buttons
        utils = QHBoxLayout()
        utils.addLayout(adutils)
        utils.addStretch()  
        utils.addLayout(sdutils)   
        return utils


    def copy_files(self):
        '''copy files to respective backups'''

        total_files = 0
        backup_files = 0
        for checkbox, img in self.checked:
            img_file = os.path.basename(img)
            one = os.path.join(self.backup_dir1, img_file)
            two = os.path.join(self.backup_dir2, img_file)
            three = os.path.join(self.backup_dir3, img_file)
            
            if checkbox.isChecked():
                total_files += 1
                
                if not os.path.exists(one):
                    shutil.copy2(img, one)
                
                if not os.path.exists(two): 
                    shutil.copy2(img, two)
                
                if not os.path.exists(three): 
                    shutil.copy2(img, three)
                
                if os.path.exists(one) & os.path.exists(two) & os.path.exists(three):
                    backup_files += 1
        
        window = QMessageBox()
        window.setStandardButtons(QMessageBox.Ok)
        window.setStyleSheet(self.check_hash.style)
        if backup_files == total_files:
            window.setText("All files have been sucessfully backed up")
        else:
            window.setText("Error in backing up, try again")
        window.exec_()


if __name__ == '__main__':
    window = App_Window() # window
    app.exec() # event loop