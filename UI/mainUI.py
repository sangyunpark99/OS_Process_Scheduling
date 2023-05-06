import sys
from Scheduling_algorithm.hrrn import hrrn_algorithm
from PyQt5.QtWidgets import QApplication, QLabel, QComboBox, QLineEdit, QGridLayout, QWidget, QPushButton
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QGraphicsView, QGraphicsScene


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Create labels
        self.ecore = None
        self.pcore = None
        self.processes = None
        self.algorithm_type = None
        self.p_core_num = None
        self.time_quantum = None
        self.total_processor = None
        self.arrival_time = None
        self.burst_time = None
        type_label = QLabel("Type:")
        time_quantum_label = QLabel("Time Quantum:")
        total_processor_label = QLabel("Total Processor:")
        p_core_label = QLabel("P-Core No.:")

        # Create input widgets
        self.type_combo = QComboBox()
        self.type_combo.addItem("FCFS")
        self.type_combo.addItem("RR")
        self.type_combo.addItem("SPN")
        self.type_combo.addItem("SRTN")
        self.type_combo.addItem("HRRN")
        self.type_combo.addItem("CUSTOM")
        self.time_quantum_input = QLineEdit()
        self.total_processor_input = QLineEdit()
        self.p_core_combo = QComboBox()
        self.p_core_combo.addItem("1")
        self.p_core_combo.addItem("2")
        self.p_core_combo.addItem("3")
        self.p_core_combo.addItem("4")

        # Create consumption labels
        consumption_label = QLabel("Consumption")
        p_core_consumption_label = QLabel("p-core:")
        e_core_consumption_label = QLabel("e-core:")
        total_consumption_label = QLabel("total:")
        p_core_consumption_output = QLabel()
        e_core_consumption_output = QLabel()
        total_consumption_output = QLabel()

        # Create grid layout and add widgets
        layout = QGridLayout()
        layout.addWidget(type_label, 0, 0)
        layout.addWidget(self.type_combo, 0, 1)
        layout.addWidget(time_quantum_label, 1, 0)
        layout.addWidget(self.time_quantum_input, 1, 1)
        layout.addWidget(total_processor_label, 2, 0)
        layout.addWidget(self.total_processor_input, 2, 1)
        layout.addWidget(p_core_label, 3, 0)
        layout.addWidget(self.p_core_combo, 3, 1)
        layout.addWidget(consumption_label, 4, 0)
        layout.addWidget(p_core_consumption_label, 5, 0)
        layout.addWidget(e_core_consumption_label, 5, 1)
        layout.addWidget(total_consumption_label, 4, 1)
        layout.addWidget(p_core_consumption_output, 5, 1)
        layout.addWidget(e_core_consumption_output, 5, 3)
        layout.addWidget(total_consumption_output, 5, 3)
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle("My Application")
        self.setGeometry(100, 100, 1200, 800)

        # Add table widget
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(15)
        self.table_widget.setColumnCount(2)
        self.table_widget.setFixedSize(405, 587)
        layout.addWidget(self.table_widget, 6, 0, 1, 4)

        # Set column names
        column_names = ['Arrival Time', 'Burst Time']
        for index, name in enumerate(column_names):
            self.table_widget.setHorizontalHeaderItem(index, QTableWidgetItem(name))

        # Set row names
        row_names = [f"     P{i + 1}     " for i in range(self.table_widget.rowCount())]
        for index, name in enumerate(row_names):
            self.table_widget.setVerticalHeaderItem(index, QTableWidgetItem(name))

        # Adjust the height of the horizontal header
        horizontal_header = self.table_widget.horizontalHeader()
        horizontal_header.setDefaultSectionSize(158)  # Adjust the height of the header

        # Create sub-layout for the Gantt chart and additional table
        sub_layout = QGridLayout()

        # Add additional table widget
        self.additional_table_widget = QTableWidget()
        self.additional_table_widget.setRowCount(15)
        self.additional_table_widget.setColumnCount(5)
        self.additional_table_widget.setFixedSize(900, 395)  # Adjust the size of the additional table widget
        sub_layout.addWidget(self.additional_table_widget, 0, 0)

        # Set row names
        for i in range(self.additional_table_widget.rowCount()):
            self.additional_table_widget.setVerticalHeaderItem(i, QTableWidgetItem(f"   P{i + 1}   "))

        # Set column names
        column_names = ['AT', 'BT', 'WT', 'TT', 'NTT']
        for index, name in enumerate(column_names):
            self.additional_table_widget.setHorizontalHeaderItem(index, QTableWidgetItem(name))

        # Adjust the height of the horizontal header
        horizontal_header = self.additional_table_widget.horizontalHeader()
        horizontal_header.setDefaultSectionSize(162)  # Adjust the height of the header

        # Add Gantt chart widget
        gantt_chart_view = QGraphicsView()
        gantt_chart_view.setFixedSize(900, 395)  # Adjust the size of the Gantt chart widget
        gantt_chart_scene = QGraphicsScene()
        gantt_chart_view.setScene(gantt_chart_scene)
        sub_layout.addWidget(gantt_chart_view, 1, 0)

        # Add sub-layout to the main layout
        layout.addLayout(sub_layout, 0, 4, 7, 1)

        # Add the "Run FCFS" button
        self.run_button = QPushButton("Run")
        layout.addWidget(self.run_button, 5, 2)

        self.run_button.clicked.connect(lambda: self.button_event())

        # Set layout to the window
        self.setLayout(layout)

    def button_event(self):
        self.algorithm_type = self.type_combo.currentText()  # 알고리즘 종류
        self.time_quantum = self.time_quantum_input.text()  # 타임 퀀텀
        self.total_processor = self.total_processor_input.text()  # 전체 프로세서 갯수
        self.pcore = self.p_core_combo.currentText()  # pcore 갯수
        self.ecore = int(self.total_processor) - int(self.pcore)  # ecore 갯수

        self.arrival_time = [int(self.table_widget.item(i, 0).text()) for i in range(self.table_widget.rowCount()) if
                             self.table_widget.item(i, 0) and self.table_widget.item(i, 0).text()]  # 도착시간
        self.burst_time = [int(self.table_widget.item(i, 1).text()) for i in range(self.table_widget.rowCount()) if
                           self.table_widget.item(i, 1) and self.table_widget.item(i, 1).text()]  # 실행 시간

        self.processes = len(self.arrival_time)

        self.startAlgorithm()

    def startAlgorithm(self):
        if self.algorithm_type == 'HRRN':
            self.waiting_times, self.turnaround_times, self.normalized_turnaround_times, self.core_consumption = hrrn_algorithm(
                int(self.processes), int(self.pcore), int(self.ecore), self.arrival_time, self.burst_time)

        if self.algorithm_type == "FCFS":
            print('여기다가 알고리즘 넣어 준혁')

        self.input_table_value()

    def input_table_value(self): # 표에 값 그리기
        for i in range(self.processes):
            for j in range(5):
                if j == 0:  # arrival_time
                    self.additional_table_widget.setItem(i, j, QTableWidgetItem(str(self.arrival_time[i])))
                elif j == 1:  # burst_time
                    self.additional_table_widget.setItem(i, j, QTableWidgetItem(str(self.burst_time[i])))
                elif j == 2:  # waiting_time
                    self.additional_table_widget.setItem(i, j, QTableWidgetItem(str(self.waiting_times[i])))
                elif j == 3:
                    self.additional_table_widget.setItem(i, j, QTableWidgetItem(str(self.turnaround_times[i])))
                elif j == 4:
                    self.additional_table_widget.setItem(i, j,
                                                         QTableWidgetItem(str(round(self.normalized_turnaround_times[i],2))))


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
