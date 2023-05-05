import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 윈도우 설정
        self.setWindowTitle("Process Scheduling Simulator")
        self.setGeometry(100, 100, 1200, 700)

        # main_label
        main_label = QLabel("Process Scheduling Simulator", self)
        main_label.setFont(QFont('',30))
        main_label.resize(400, 40)
        main_label.move(439, 30)

        # Team_label
        team_label = QLabel("오예스 Team v1.0.0", self)
        team_label.resize(150,30)
        team_label.setFont(QFont('',15))
        team_label.move(439,70)

        # logo_label
        logo_label = QLabel(self)
        pixmap = QPixmap("koreatech_logo.png")
        logo_label.setPixmap(pixmap)
        logo_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

        # process 입력받기
        # process_name_label = QLabel("Process Name:",self)
        # process_name_edit = QLineEdit(self)
        # process_arrival_time_label = QLabel("Arrival Time:",self)
        # process_arrival_time_edit = QLineEdit(self)
        # add_button = QPushButton("Add Process",self)
        # add_button.clicked.connect(self.add_process)
        #
        # process_layout = QVBoxLayout()
        # process_layout.addWidget(process_name_label)
        # process_layout.addWidget(process_name_edit)
        # process_layout.addWidget(process_arrival_time_label)
        # process_layout.addWidget(process_arrival_time_edit)
        #
        # process_layout.setGeometry(100, 100, 200)
        # self.setLayout(process_layout)

    def add_process(self):  # 프로세스 추가해주는 버튼
        print('프로세스를 추가합니다')


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
