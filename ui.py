import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Qt5Agg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import numpy as np
from sklearn.metrics import r2_score
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton, QHBoxLayout, QLabel, QTabWidget
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
from plotting import download_data, calculate_trend, plot_stock_data

class MyWindow(QMainWindow):
    def __init__(self):
        """Initialize the main window and its widgets"""
        super(MyWindow, self).__init__()
        self.initUI()
    
    def initUI(self):
        """Set up the user interface"""
        self.setWindowTitle("Pala Capital")
        self.setGeometry(0, 0, 1920, 1080)

        # Set the application icon
        self.setWindowIcon(QtGui.QIcon("icon-copy.png"))  # Update with the correct path to your emoji file

        # Set the background color
        self.setStyleSheet("background-color: #f0f8ff;")  # Light relaxing color for the main window

        # Central widget to hold all other widgets
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        # Main layout to split the window into left and right sections
        main_layout = QHBoxLayout(self.central_widget)
        
        # Left layout for buttons and controls
        left_layout = QVBoxLayout()
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setStyleSheet("background-color: #d1e7dd;")  # Different color for the menu background
        main_layout.addWidget(left_widget, 1)  # Adjust the stretch factor to control the size
        
        # Right layout for charts
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout, 3)  # Adjust the stretch factor to control the size
        
        # Add a label for stock prediction
        self.label = QtWidgets.QLabel("Stock Prediction")
        left_layout.addWidget(self.label)
        
        # Button to trigger plot generation
        self.b1 = QtWidgets.QPushButton("Click Me")
        self.b1.clicked.connect(self.button_clicked)
        left_layout.addWidget(self.b1)
        
        # ComboBox for selecting stock symbols
        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["EREGL.IS", "SASA.IS", "TKFEN.IS", "SISE.IS", "ENKAI.IS", "DOHOL.IS", "THYAO.IS", "EKGYO.IS", "PETKM.IS"])
        left_layout.addWidget(QLabel("Stock Prediction"))
        left_layout.addWidget(self.comboBox)
        
        # Buttons for selecting models
        self.model1_button = QPushButton("Model 1")
        self.model2_button = QPushButton("Model 2")
        self.model1_button.setCheckable(True)
        self.model2_button.setCheckable(True)
        
        self.model1_button.clicked.connect(self.on_button_clicked)
        self.model2_button.clicked.connect(self.on_button_clicked)
        
        # Layout to hold model selection buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.model1_button)
        button_layout.addWidget(self.model2_button)
        
        left_layout.addWidget(QLabel("Model:"))
        left_layout.addLayout(button_layout)
        
        # Button to show current selection
        self.show_selection_button = QPushButton("Seçimleri Göster")
        self.show_selection_button.clicked.connect(self.show_selection)
        left_layout.addWidget(self.show_selection_button)
        
        # Tab widget to hold multiple charts
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        right_layout.addWidget(self.tab_widget)
    
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
