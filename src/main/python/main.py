#!/usr/bin/env python3

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys

appctxt = None

def main():
    global appctxt
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    gui = MainWindow()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        qss_src = appctxt.get_resource('main_style.qss')
        with open(qss_src) as qss_file:
            qss = qss_file.read()
        self.setStyleSheet(qss)

        self.initUI()

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
        self.setCentralWidget(window)
        self.show()

    def make_header(self):
        left_img_src = appctxt.get_resource('f4t_logo.png')
        left_img = QPixmap(left_img_src).scaledToHeight(64, Qt.SmoothTransformation)
        left_label = QLabel()
        left_label.setObjectName('left_img')
        left_label.setPixmap(left_img)

        right_img_src = appctxt.get_resource('nss_logo.png')
        right_img = QPixmap(right_img_src).scaledToHeight(64, Qt.SmoothTransformation)
        right_label = QLabel()
        right_label.setObjectName('right_img')
        right_label.setPixmap(right_img)

        layout = QHBoxLayout()
        layout.addWidget(left_label) #, alignment = Qt.AlignLeft)
        layout.addWidget(right_label) #, alignment = Qt.AlignRight)
        
        header = QWidget()
        header.setLayout(layout)
        return header

    def make_input_box(self):
        label = QLabel('Type a word: ')
        box = QLineEdit()
        button = QPushButton('Search')

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(box)
        layout.addWidget(button)

        input_box = QWidget()
        input_box.setLayout(layout)
        return input_box

    def make_output_box(self):
        english_box = QPlainTextEdit()
        english_box.setReadOnly(True)

        hindi_box = QPlainTextEdit()
        hindi_box.setReadOnly(True)
        
        tabs = QTabWidget()
        tabs.addTab(english_box, 'English')
        tabs.addTab(hindi_box, 'Hindi')

        layout = QHBoxLayout()
        layout.addWidget(tabs)

        output_box = QWidget()
        output_box.setLayout(layout)
        return output_box

    def make_footer(self):
        label = QLabel('Designed and developed by NSS IITD in collaboration with F4TF.')
        label.setObjectName('footer') # for qss id selector

        layout = QVBoxLayout()
        layout.addWidget(label) #, alignment = Qt.AlignCenter)

        footer = QWidget()
        footer.setLayout(layout)
        return footer

if __name__ == '__main__':
    main()

