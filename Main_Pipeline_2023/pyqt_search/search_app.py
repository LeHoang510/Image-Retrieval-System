from PyQt5.QtWidgets import QApplication
import sys
import os
import csv
import json
import webbrowser

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QHBoxLayout, QComboBox, QTabWidget, QPushButton, QFrame
from PyQt5.QtWidgets import QMenu, QAction, QToolBar, QFileDialog, QMessageBox, QInputDialog
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QTabBar
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import pandas as pd
import pyperclip
import json

# Class App
class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        # Create a central widget to hold the layout
        self.setWindowTitle("Searching app")
        self.window = QWidget()

        # Set center zone
        self.setCentralWidget(self.window)

        self.mainLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()

        self.left_layout_init()
        self.right_layout_init()

        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)
        self.window.setLayout(self.mainLayout)

        self.showMaximized()
        self.show()

    def left_layout_init(self):
        # Create the first line with labels and line edits
        self.form = QHBoxLayout()
        # Add other widgets or layouts here
        self.label_l = QLabel("L")
        self.label_v = QLabel("V")
        self.label_index = QLabel("index")


        self.input_l = QLineEdit()
        self.input_v = QLineEdit()
        self.input_index = QLineEdit()

        self.left_button = QPushButton("Left")
        self.left_button.clicked.connect(self.change_id_left)
        self.left_button.setShortcut(Qt.Key_Left)
        self.right_button = QPushButton("Right")
        self.right_button.clicked.connect(self.change_id_right)
        self.right_button.setShortcut(Qt.Key_Right)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.get_result)
        self.search_button.setShortcut("Return")

        self.label_output = QLabel("Result")
        self.result = QLineEdit()

        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_value)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_value)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_to_tab)

        self.form.addWidget(self.label_l)
        self.form.addWidget(self.input_l)
        self.form.addWidget(self.label_v)
        self.form.addWidget(self.input_v)
        self.form.addWidget(self.label_index)
        self.form.addWidget(self.input_index)

        self.input_l.setFixedWidth(100)
        self.input_v.setFixedWidth(100)
        self.input_index.setFixedWidth(100)

        self.form.addWidget(self.left_button)
        self.form.addWidget(self.right_button)

        self.form.addWidget(self.search_button)
        self.form.addWidget(self.label_output)

        self.result.setFixedWidth(300)

        self.form.addWidget(self.result)
        self.form.addWidget(self.copy_button)
        self.form.addWidget(self.convert_button)
        self.form.addWidget(self.add_button)

        self.youtube_layout = QHBoxLayout()

        self.label_youtube = QLabel("Youtube link")
        self.input_youtube = QLineEdit()
        self.search_youtube = QPushButton("Go")
        self.search_youtube.clicked.connect(self.search_link)

        self.youtube_layout.addWidget(self.label_youtube)
        self.youtube_layout.addWidget(self.input_youtube)
        self.youtube_layout.addWidget(self.search_youtube)

        self.image_layout = QVBoxLayout()

        self.image_display = QLabel()

        self.rows = []
        for i in range(3):
            row_layout = QHBoxLayout()
            self.rows.append(row_layout)
            for j in range(3):
                if i == 1 and j == 1:
                    layout = QVBoxLayout()
                    self.border_frame = QFrame()
                    #border_frame.setStyleSheet("background-color: red;")
                    layout.addWidget(self.image_display)
                    self.border_frame.setLayout(layout)
                    row_layout.addWidget(self.border_frame)
                else:
                    label = QLabel()
                    row_layout.addWidget(label)
            self.image_layout.addLayout(row_layout)


        self.leftLayout.addLayout(self.form)
        self.leftLayout.addLayout(self.youtube_layout)
        self.leftLayout.addLayout(self.image_layout)

    def get_result(self):
        try:
            l = int(self.input_l.text())
            v = int(self.input_v.text())
            id = int(self.input_index.text())

            value_l = str(l).zfill(2)
            value_v = str(v).zfill(3)

            print('before set image')

            # set image
            self.set_image(value_l, value_v, id)

            print('AFTER set image')

            # get path
            csv_path = f'map_frame_id/MapKeyframe_L{value_l}/L{value_l}_V{value_v}.csv'
            json_path = f'dataset/New_Metadata/L{value_l}_V{value_v}.json'
            # csv
            
            print('before set path')
            
            
            if not os.path.exists(csv_path) or not os.path.exists(json_path):
                self.result.setText("CSV/json file does not exist.")
                return
            
            print('before read csv')
            
            
            df = pd.read_csv(csv_path)
            df.set_index('n', inplace=True)
            
            print('after read csv')
            
            try:
                output = df.at[id, 'frame_idx']
                pts_time = df.at[id, 'pts_time']
            except KeyError:
                print('except key error')
                output = None
            if output is None:
                self.result.setText("Id not found")
            else:
                self.result.setText(f"L{value_l}_V{value_v},{output}")
            #json

            with open(json_path, 'r',  encoding="utf8") as json_file:
                json_data = json.load(json_file)

                
            watch_url = json_data.get('watch_url', '')

            minutes = int(pts_time // 60)  # Get the whole minutes
            seconds = int(pts_time % 60)   # Get the remaining seconds

            link = f"{watch_url}&t={minutes}m{seconds}s"
            self.input_youtube.setText(link)
        except ValueError as e:
            self.image_display.setText("Invalid input. Please enter valid numbers.")
            print(e)
    def set_image(self, value_l: str, value_v: str, value_index: int):
        value_index_1 = str(value_index).zfill(4)
        value_index_2 = str(value_index).zfill(3)

        chosen_image_path = ""
        image_path_1 = f'dataset/Keyframes_L{value_l}/keyframes/L{value_l}_V{value_v}/{value_index_1}.jpg'
        image_path_2 = f'dataset/Keyframes_L{value_l}/keyframes/L{value_l}_V{value_v}/{value_index_2}.jpg'

        if os.path.exists(image_path_1):
            chosen_image_path = image_path_1
        elif os.path.exists(image_path_2):
            chosen_image_path = image_path_2
        else:
            self.border_frame.setStyleSheet("")
            self.image_display.setText("Image path not exist")
        file_paths = self.generate_file_paths(chosen_image_path, num_images=9)
        current_id = 0
        for i in range(3):
            row = self.rows[i]
            for j in range(3):
                if i == 1 and j == 1:
                    # set image
                    pixmap = QPixmap(chosen_image_path)
                    pixmap = pixmap.scaledToWidth(500)
                    if not pixmap.isNull():
                        self.border_frame.setStyleSheet("background-color: red;")
                        self.image_display.setPixmap(pixmap)
                else:
                    if not os.path.exists(file_paths[current_id]):
                        row.itemAt(j).widget().setText("Image path not exist")
                    else:
                        pixmap = QPixmap(file_paths[current_id])
                        pixmap = pixmap.scaledToWidth(500)
                        row.itemAt(j).widget().setPixmap(pixmap)
                current_id +=1



    def generate_file_paths(self, input_path, num_images=9):
        path_parts = input_path.split('/')
        base_path = '/'.join(path_parts[:-1]) + '/'  # Extract the base path
        file_name = path_parts[-1]  # Extract the file name

        file_number = int(file_name.split('.')[0])  # Extract the numeric part of the file name
        file_extension = file_name.split('.')[1]  # Extract the file extension

        substring = input_path.split('/')[-1].split('.')[0]
        length = len(substring)

        file_paths = []

        for i in range(file_number - num_images // 2, file_number + num_images // 2 + 1):
            new_file_name = f"{str(i).zfill(length)}.{file_extension}"
            new_path = f"{base_path}{new_file_name}"
            file_paths.append(new_path)

        return file_paths
    def change_id_left(self):
        val = int(self.input_index.text())
        if val == 1 or val == '':
            return
        val -= 1
        self.input_index.setText(str(val))
        self.get_result()
    def change_id_right(self):
        val = int(self.input_index.text())
        if val == '':
            return
        val += 1
        self.input_index.setText(str(val))
        self.get_result()
    def copy_value(self):
        pyperclip.copy(self.result.text())
    def convert_value(self):
        path, frame = self.result.text().split(',')
        value_l, value_v = path.split('_')
        csv_path = f'map_frame_id/MapKeyframe_{value_l}/{path}.csv'

        value_l = value_l.lstrip('L')
        value_v = value_v.lstrip('V')

        if not os.path.exists(csv_path):
            self.image_display.setText("CSV file does not exist.")
            return
        df = pd.read_csv(csv_path)
        df.set_index('frame_idx', inplace=True)
        try:
            value_index = int(df.at[int(frame), 'n'])
        except KeyError:
            value_index = None
        if value_index is None:
            self.image_display.setText("Id not found")
        else:
            self.set_image(value_l, value_v, value_index)
            value_l=value_l.lstrip('0')
            value_v = value_v.lstrip('0')
            self.input_l.setText(value_l)
            self.input_v.setText(value_v)
            self.input_index.setText(str(value_index))
            self.get_result()
    def add_to_tab(self):
        current_tab_index = self.tabs_widget.currentIndex()

        if current_tab_index >= 0:
            input_text = self.result.text()
            submit_edit = self.tabs_widget.currentWidget().findChild(QTextEdit, "submit")
            result_edit = self.tabs_widget.currentWidget().findChild(QTextEdit, "result")

            if submit_edit:
                submit_edit.append(input_text)
            if result_edit:
                path, frame = self.result.text().split(',')
                str = f'{path}/{self.input_index.text().zfill(4)}'
                result_edit.append(str)
    def search_link(self):
        webbrowser.open(self.input_youtube.text())

    def right_layout_init(self):
        self.tab_menu_layout = QHBoxLayout()
        self.add_tab_button = QPushButton("Add Tab")
        self.delete_tab_button = QPushButton("Delete Tab")
        self.tab_menu_layout.addWidget(self.add_tab_button)
        self.tab_menu_layout.addWidget(self.delete_tab_button)


        self.submit_button = QPushButton("Submit")
        self.tab_menu_layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.save_csv)

        self.tabs_widget = QTabWidget()

        self.rightLayout.addLayout(self.tab_menu_layout)
        self.rightLayout.addWidget(self.tabs_widget)

        # Connect the Create Tab button to create new tabs
        self.add_tab_button.clicked.connect(self.create_tab)
        self.delete_tab_button.clicked.connect(self.delete_tab)

        self.tabs_widget.tabBarDoubleClicked.connect(self.edit_tab_name)

    def create_tab(self):
        new_tab = QWidget()
        self.tabs_widget.addTab(new_tab, "Click to edit name")

        tab_layout = QVBoxLayout()

        submit_text = QTextEdit()
        submit_text.setObjectName("submit")  # Set a unique object name
        result_text = QTextEdit()
        result_text.setObjectName("result")  # Set a unique object name

        tab_layout.addWidget(submit_text)
        tab_layout.addWidget(result_text)

        new_tab.setLayout(tab_layout)
    def edit_tab_name(self):
        current_tab_index = self.tabs_widget.currentIndex()
        current_name = self.tabs_widget.tabText(current_tab_index)
        new_name, ok = QInputDialog.getText(self, "Edit Tab Name", "Enter new tab name:", text=current_name)
        if ok and new_name:
            self.tabs_widget.setTabText(current_tab_index, new_name)
    def delete_tab(self):
        current_tab_index = self.tabs_widget.currentIndex()
        if current_tab_index >= 0:
            self.tabs_widget.removeTab(current_tab_index)
    def save_csv(self):
        current_tab_index = self.tabs_widget.currentIndex()
        current_name = self.tabs_widget.tabText(current_tab_index)
        current_tab = self.tabs_widget.widget(current_tab_index)
        text_edit = current_tab.findChild(QTextEdit).toPlainText()
        if not text_edit:
            self.show_warning("Text is empty", "Please enter some text before saving.")
            return
        save_dir = "pyqt_search/csv/"

        os.makedirs(save_dir, exist_ok=True)
        file_name = os.path.join(save_dir, f"{current_name}.csv")
        try:
            lines = text_edit.split('\n')
            rows = [line.split(',') for line in lines]
            # Write the rows to the CSV file
            with open(file_name, "w", newline='', encoding="utf8") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(rows)
            self.show_message("File Saved", f"File has been saved to '{file_name}'")
        except Exception as e:
            self.show_warning("Error Saving File", str(e))

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.addButton(QMessageBox.Ok)
        msg_box.exec_()
    def show_warning(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.addButton(QMessageBox.Ok)
        msg_box.exec_()

if __name__ == "__main__":
    # os.environ["QT_QPA_PLATFORM"] = "xcb"
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
