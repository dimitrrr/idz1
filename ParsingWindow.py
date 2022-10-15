from PyQt6.QtWidgets import *
from ParsingFunctions import *
from Analyzer import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class ParsingWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IDZ #1")
        self.resize(1024, 768)

        self.layout_main = QFormLayout()
        self.widget_rb = QWidget()
        self.widget_text = QWidget()
        self.widget_file = QWidget()
        self.widget_url = QWidget()
        self.widget_result = QWidget()
        self.textarea = QTextEdit()
        self.input_url = QLineEdit()

        self.create_basic_layout()

        self.content = ''
        self.analyzer = None
        self.result_layout = None

    def create_basic_layout(self):
        self.create_rb_layout()
        self.create_content_layout()

        self.setLayout(self.layout_main)

    def create_rb_layout(self):
        rb_layout = QHBoxLayout()

        rb_text = QRadioButton("Text")
        rb_text.setChecked(True)
        rb_text.toggled.connect(lambda: self.btnstate(rb_text))
        rb_layout.addWidget(rb_text)

        rb_file = QRadioButton("File")
        rb_file.toggled.connect(lambda: self.btnstate(rb_file))
        rb_layout.addWidget(rb_file)

        rb_url = QRadioButton("URL")
        rb_url.toggled.connect(lambda: self.btnstate(rb_url))
        rb_layout.addWidget(rb_url)

        self.widget_rb.setLayout(rb_layout)
        self.layout_main.addWidget(self.widget_rb)

    def create_content_layout(self):
        layout_text = QVBoxLayout()
        layout_file = QVBoxLayout()
        layout_url = QVBoxLayout()

        analyze_btn_text = QPushButton('Analyze text')
        analyze_btn_text.clicked.connect(self.click_text)
        analyze_btn_file = QPushButton('Analyze selected file')
        analyze_btn_file.clicked.connect(self.click_file)
        analyze_btn_url = QPushButton('Analyze site')
        analyze_btn_url.clicked.connect(self.click_url)

        layout_text.addWidget(self.textarea)
        layout_text.addWidget(analyze_btn_text)
        layout_file.addWidget(analyze_btn_file)
        layout_url.addWidget(self.input_url)
        layout_url.addWidget(analyze_btn_url)

        self.widget_text.setLayout(layout_text)
        self.layout_main.addWidget(self.widget_text)

        self.widget_file.setLayout(layout_file)
        self.layout_main.addWidget(self.widget_file)
        self.widget_file.hide()

        self.widget_url.setLayout(layout_url)
        self.layout_main.addWidget(self.widget_url)
        self.widget_url.hide()

    def btnstate(self, b):
        if b.text() == 'Text':
            if b.isChecked():
                self.widget_text.show()
                self.widget_url.hide()
                self.widget_file.hide()
            else:
                self.widget_text.hide()
        elif b.text() == 'URL':
            if b.isChecked():
                self.widget_text.hide()
                self.widget_url.show()
                self.widget_file.hide()
            else:
                self.widget_url.hide()
        elif b.text() == 'File':
            if b.isChecked():
                self.widget_text.hide()
                self.widget_url.hide()
                self.widget_file.show()
            else:
                self.widget_file.hide()

    def click_text(self):
        self.content = self.textarea.toPlainText()
        self.print_analysis_result()

    def click_url(self):
        url = self.input_url.text()
        self.content = parse_url(url)
        self.print_analysis_result()

    def click_file(self):
        filter_extensions = "Text Files (*.txt);; Word Files (*.docx)"
        filename = QFileDialog.getOpenFileName(self, 'Open file', None, filter_extensions)

        if filename[0]:
            data = parse_file(filename[0])
            self.content = data
            self.print_analysis_result()

    def print_analysis_result(self):
        self.analyzer = Analyzer(self.content)

        self.widget_text.hide()
        self.widget_url.hide()
        self.widget_file.hide()
        self.widget_rb.hide()

        self.result_layout = QVBoxLayout()
        hello_text = QLabel("<h1>Results</h1>")
        self.result_layout.addWidget(hello_text)

        layout_buttons = QHBoxLayout()
        back_btn = QPushButton('Back to main')
        back_btn.clicked.connect(self.back_to_main)
        save_btn = QPushButton('Export')
        save_btn.clicked.connect(self.file_save)
        layout_buttons.addWidget(back_btn)
        layout_buttons.addWidget(save_btn)
        widget_buttons = QWidget()
        widget_buttons.setLayout(layout_buttons)

        self.result_layout.addWidget(hello_text)
        self.result_layout.addWidget(widget_buttons)

        layout_tables = QHBoxLayout()

        stats_text = QLabel("<h5>Stats / most common words</h5>")
        self.result_layout.addWidget(stats_text)
        table_stats = self.create_table_widget()
        layout_tables.addWidget(table_stats)
        table_common = self.create_common_words_table_widget()
        layout_tables.addWidget(table_common)
        widget_tables = QWidget()
        widget_tables.setLayout(layout_tables)
        self.result_layout.addWidget(widget_tables)

        plots_text = QLabel("<h5>Plots</h5>")
        self.result_layout.addWidget(plots_text)

        self.add_plot()

        self.widget_result.setLayout(self.result_layout)
        self.layout_main.addWidget(self.widget_result)

    def create_table_widget(self):
        data = self.analyzer.get_table_stats_data()

        table = QTableWidget()

        if data:
            table.setRowCount(len(data))
            table.setColumnCount(len(data[0]))

            for i in range(len(data)):
                for j in range(len(data[0])):
                    item = QTableWidgetItem(str(data[i][j]))
                    table.setItem(i, j, item)

            table.setSortingEnabled(True)
            table.setHorizontalHeaderLabels(['Property', 'Value'])
            table.setMaximumWidth(table.horizontalHeader().length() + 50)
            table.setMaximumHeight(500)

        return table

    def create_common_words_table_widget(self):
        data = self.analyzer.get_words_frequency()

        table = QTableWidget()

        if data:
            table.setRowCount(len(data))
            table.setColumnCount(2)

            row = 0
            for key, value in data:
                item_key = QTableWidgetItem(str(key))
                table.setItem(row, 0, item_key)
                item_value = QTableWidgetItem(str(value))
                table.setItem(row, 1, item_value)
                row = row + 1

            table.setSortingEnabled(True)
            table.setHorizontalHeaderLabels(['Word', 'Frequency'])
            table.setMaximumWidth(table.horizontalHeader().length() + 50)
            table.setMaximumHeight(500)

        return table

    def add_plot(self):
        most_common = self.analyzer.get_words_frequency()
        keys = [m[0] for m in most_common]
        values = [m[1] for m in most_common]
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(keys, values)
        self.result_layout.addWidget(sc)

    def back_to_main(self):
        self.widget_result.hide()
        self.widget_text.show()
        self.widget_rb.show()

    def file_save(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Word Files (*.docx)")
        stats = self.analyzer.get_table_stats_data()
        common = self.analyzer.get_words_frequency()
        save_file(filename, stats, common)

