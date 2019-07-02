#!/usr/bin/env python3

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import dictionary_core.english as english

import sys

appctxt = None

def main():
    global appctxt
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

    # TODO: load_window

    # loading
    english.parse()
    main_window = MainWindow()
    
    # TODO: connect to click event on load_window
    main_window.show()

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Input/Search box (type == QLineEdit)
        # defined in make_input_box
        self.search_box = None

        # Output boxes (type == QPlainTextEdit)
        # defined in make_output_box
        self.english_box = None
        self.hindi_box = None

        qss_src = appctxt.get_resource('styles/main_style.qss')
        with open(qss_src) as qss_file:
            qss = qss_file.read()
        self.setStyleSheet(qss)

        self.initUI()

        # Debug phase only
        self.search_box.setText('sky')
        self.go()

    def initUI(self):
        header = self.make_header()
        input_box = self.make_input_box()
        output_box = self.make_output_box()
        footer = self.make_footer()
        
        layout = QVBoxLayout()
        layout.addWidget(header)
        layout.addWidget(input_box)
        layout.addWidget(output_box)
        layout.addWidget(footer)

        window = QWidget()
        window.setObjectName('main_window')
        window.setLayout(layout)

        self.setWindowTitle('Word Book')
        self.resize(600, 600)
        self.move(0,0) # TODO: remove this
        self.setCentralWidget(window)

    def make_header(self):
        left_img_src = appctxt.get_resource('images/f4t_logo.png')
        left_img = QPixmap(left_img_src).scaledToHeight(64, Qt.SmoothTransformation)
        left_label = QLabel()
        left_label.setObjectName('left_img')
        left_label.setPixmap(left_img)

        right_img_src = appctxt.get_resource('images/nss_logo.png')
        right_img = QPixmap(right_img_src).scaledToHeight(64, Qt.SmoothTransformation)
        right_label = QLabel()
        right_label.setObjectName('right_img')
        right_label.setPixmap(right_img)

        layout = QHBoxLayout()
        layout.addWidget(left_label)
        layout.addWidget(right_label)
        
        header = QWidget()
        header.setLayout(layout)
        return header

    def make_input_box(self):
        label = QLabel('Type a word: ')
        self.search_box = QLineEdit()
        button = QPushButton('Search')
        button.setFocusPolicy(Qt.StrongFocus)
        
        self.search_box.returnPressed.connect(self.go)
        button.clicked.connect(self.go)
        # emit clicked signal when enter is pressed with focus
        button.setAutoDefault(True)

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.search_box)
        layout.addWidget(button)

        input_box = QWidget()
        input_box.setLayout(layout)
        return input_box

    def make_output_box(self):
        self.english_box = QPlainTextEdit()
        self.english_box.setReadOnly(True)

        self.hindi_box = QPlainTextEdit()
        self.hindi_box.setReadOnly(True)
        
        tabs = QTabWidget()
        tabs.addTab(self.english_box, 'English')
        tabs.addTab(self.hindi_box, 'Hindi')

        layout = QHBoxLayout()
        layout.addWidget(tabs)

        output_box = QWidget()
        output_box.setLayout(layout)
        return output_box

    def make_footer(self):
        label = QLabel('Designed and developed by NSS IITD in collaboration with F4TF.')
        label.setObjectName('footer') # for qss id selector

        layout = QVBoxLayout()
        layout.addWidget(label)

        footer = QWidget()
        footer.setLayout(layout)
        return footer

    # Respond to click of Search button by filling output boxes
    def go(self):
        word = self.search_box.text()
        # all words in data must be in lower case
        # TODO: hindi data
        word = word.strip().lower()

        self.english_box.clear()
        self.english_box.appendHtml(english.define(word))
        self.english_box.appendPlainText(english.define(word))
        self.english_box.verticalScrollBar().triggerAction(QScrollBar.SliderToMinimum)

if __name__ == '__main__':
    main()

