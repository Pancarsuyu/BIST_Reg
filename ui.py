import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import numpy as np
from sklearn.metrics import r2_score
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton, QHBoxLayout, QLabel, QTabWidget, QGroupBox, QFormLayout, QLineEdit
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtCore import Qt
from plotting import download_data, calculate_trend, plot_stock_data

matplotlib.use('Qt5Agg')

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Pala Capital")
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowIcon(QtGui.QIcon("icon-copy.png")) 

        # Central Widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        main_layout = QHBoxLayout(self.central_widget)

        # --- Left Panel ---
        left_panel = QGroupBox("Stock Analysis Tools") 
        left_panel.setStyleSheet("background-color: #c0c0c0;")  
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        main_layout.addWidget(left_panel, 1)

        # --- Stock Prediction Section ---
        prediction_section = QGroupBox("Stock Prediction")
        prediction_layout = QFormLayout()
        prediction_section.setLayout(prediction_layout)
        left_layout.addWidget(prediction_section)

        # Stock Selection
        self.comboBox = QComboBox(self)
        stock_list = ["EREGL.IS", "SASA.IS", "TKFEN.IS", "SISE.IS", "ENKAI.IS",
                      "DOHOL.IS", "THYAO.IS", "EKGYO.IS", "PETKM.IS", "VESTL.IS", 
                      "PRKME.IS", "ALARK.IS"]
        self.comboBox.addItems(stock_list)
        prediction_layout.addRow("Select Stock:", self.comboBox)

        # Model Selection
        model_layout = QHBoxLayout()
        self.model1_button = QPushButton("Polynomial Regression")
        self.model2_button = QPushButton("Another Model") 
        self.model1_button.setCheckable(True)
        self.model2_button.setCheckable(True)
        self.model1_button.clicked.connect(self.on_button_clicked)
        self.model2_button.clicked.connect(self.on_button_clicked)
        model_layout.addWidget(self.model1_button)
        model_layout.addWidget(self.model2_button)
        prediction_layout.addRow("Select Model:", model_layout)

        # --- Add "Run Analysis" button INSIDE the prediction group box ---
        self.run_analysis_button = QPushButton("Run Analysis")
        self.run_analysis_button.clicked.connect(self.plot_graph)
        self.run_analysis_button.setStyleSheet("background-color: #4CAF50; color: white")  
        prediction_layout.addRow(self.run_analysis_button)  # Add to prediction_layout

        # --- Other Tools (Placeholder) ---
        other_tools_section = QGroupBox("More Tools (Coming Soon)")
        other_tools_layout = QVBoxLayout()
        other_tools_section.setLayout(other_tools_layout)
        left_layout.addWidget(other_tools_section)

        # --- Data Section ---
        data_section = QGroupBox("Data")
        data_layout = QFormLayout()  # Use QFormLayout for better alignment
        data_section.setLayout(data_layout)
        left_layout.addWidget(data_section)

        # Data Source Selection
        self.data_source_combo = QComboBox(self)
        self.data_source_combo.addItems(["Local Files", "SQL Database"])
        self.data_source_combo.currentIndexChanged.connect(self.update_data_source_visibility)
        data_layout.addRow("Data Source:", self.data_source_combo)

        # Update Button
        self.update_data_button = QPushButton("Update")
        self.update_data_button.clicked.connect(self.update_data)  # Connect to a function
        data_layout.addRow(self.update_data_button)

        # --- Add spacing before SQL details ---
        data_layout.addRow(QLabel(""))  # Add an empty label for spacing

        # --- SQL Connection Details (Initially Hidden) ---
        self.sql_details_group = QGroupBox("SQL Connection Details")
        self.sql_details_layout = QFormLayout()
        self.sql_details_group.setLayout(self.sql_details_layout)
        data_layout.addRow(self.sql_details_group)
        self.sql_details_group.hide()  # Hide initially

        # TODO: CONNECT THE SQL, MAKE NECESSARY CHANGES IN PLOTTING.PY
        # SQL Connection Fields
        self.host_edit = QLineEdit()
        self.sql_details_layout.addRow("Host:", self.host_edit)
        self.database_edit = QLineEdit()
        self.sql_details_layout.addRow("Database:", self.database_edit)
        self.username_edit = QLineEdit()
        self.sql_details_layout.addRow("Username:", self.username_edit)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password) # Hide password input
        self.sql_details_layout.addRow("Password:", self.password_edit)

        # --- Add spacing between widgets ---
        left_layout.addSpacing(20)
        prediction_layout.setVerticalSpacing(15)

        # --- Styling ---
        self.setStyleSheet("background-color: lightgrey;") 
        font = QFont()
        font.setPointSize(12) 
        self.setFont(font)

        # --- Right Panel (Chart Area) ---
        right_widget = QWidget() 
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)  

        main_layout.addWidget(right_widget, 3)  
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        right_layout.addWidget(self.tab_widget)

    def update_data_source_visibility(self):
        """Show/hide SQL details based on selected data source."""
        if self.data_source_combo.currentText() == "SQL Database":
            self.sql_details_group.show()
        else:
            self.sql_details_group.hide()

    def update_data(self):
        """Handle data update based on selected source."""
        source = self.data_source_combo.currentText()
        if source == "Local Files":
            print("Updating from local files...")
            # Add your logic for updating from local files
        elif source == "SQL Database":
            print("Updating from SQL database...")
            # Add your logic for updating from the database
            host = self.host_edit.text()
            database = self.database_edit.text()
            username = self.username_edit.text()
            password = self.password_edit.text()
            # Use these variables to connect to the database

    def button_clicked(self):
        """Handle button click event to generate the plot"""
        self.label.setText("Button clicked")
        print("Button clicked")
        self.update()
        self.plot_graph()
    
    def on_button_clicked(self):
        """Handle model selection button click events"""
        sender = self.sender()
        if sender == self.model1_button:
            self.model2_button.setChecked(False)
        elif sender == self.model2_button:
            self.model1_button.setChecked(False)
        self.update_button_colors()
        
    def update_button_colors(self):
        """Update the colors of the model selection buttons based on selection"""
        selected_color = QColor(0, 255, 0)
        default_color = QColor(255, 255, 255)
        
        palette = self.model1_button.palette()
        if self.model1_button.isChecked():
            palette.setColor(QPalette.Button, selected_color)
        else:
            palette.setColor(QPalette.Button, default_color)
        self.model1_button.setPalette(palette)
        self.model1_button.setAutoFillBackground(True)
        
        palette = self.model2_button.palette()
        if self.model2_button.isChecked():
            palette.setColor(QPalette.Button, selected_color)
        else:
            palette.setColor(QPalette.Button, default_color)
        self.model2_button.setPalette(palette)
        self.model2_button.setAutoFillBackground(True)

    def show_selection(self):
        """Display the current selection of stock and model"""
        selected_stock = self.comboBox.currentText()
        selected_model = "Model 1" if self.model1_button.isChecked() else "Model 2" if self.model2_button.isChecked() else "Hiçbiri"
        print(f"Seçilen Hisse: {selected_stock}, Seçilen Model: {selected_model}")
        return selected_stock, selected_model

    def plot_graph(self):
        """Generate and display the stock price chart in a new tab"""
        selected_stock, selected_model = self.show_selection()
        
        data = download_data(selected_stock)
        x, y, trend, r2, ss = calculate_trend(data)
        
        # Create a new figure and canvas for the plot
        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        
        # Plot the stock data and trend line
        ax.plot(data.index, y, "b.", label="Hisse")
        ax.plot(data.index, trend, "r-", label="Trend")
        ax.fill_between(data.index, trend - ss, trend + ss, color="navy", alpha=0.3, label="±1 Standart Sapma")
        ax.fill_between(data.index, trend - 2 * ss, trend + 2 * ss, color="darkred", alpha=0.3, label="±2 Standart Sapma")
        ax.fill_between(data.index, trend - 3 * ss, trend + 3 * ss, color="gray", alpha=0.3, label="±3 Standart Sapma")
        ax.set_title(f"Hisse Polinomal Regresyon (R-Kare: {r2:.2f})")
        ax.legend(loc="upper left")
        
        # Add navigation toolbar for interactivity
        toolbar = NavigationToolbar(canvas, self)
        
        # Create a widget to hold both canvas and toolbar
        tab_widget = QWidget()
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(toolbar)
        tab_layout.addWidget(canvas)
        tab_widget.setLayout(tab_layout)
        
        # Add the plot to a new tab
        tab_name = f"{selected_stock} - {selected_model}"
        self.tab_widget.addTab(tab_widget, tab_name)
        self.tab_widget.setCurrentWidget(tab_widget)
        
    def close_tab(self, index):
        """Close the tab at the specified index"""
        self.tab_widget.removeTab(index)
