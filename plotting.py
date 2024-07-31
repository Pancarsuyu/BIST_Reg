import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os
import datetime

# TODO drive api

def download_dollar_data():
    """Downloads stock data, updating it if necessary."""
    last_update = get_last_update_date("TRY=X")
    if last_update is None or last_update < datetime.date.today():
        update_stock_data("TRY=X")
    data = pd.read_csv(get_data_path("TRY=X"), index_col=0, parse_dates=True)
    data.rename(columns={"Adj Close": "Fiyat"}, inplace=True)  # Rename column

    return data

def get_data_path(stock_symbol, extension="csv"):
    """Returns the path to the data file (CSV or TXT) for the given stock symbol."""
    data_folder = "stock_data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    return os.path.join(data_folder, f"{stock_symbol}.{extension}")

def get_last_update_date(stock_symbol):
    """Retrieves the last update date for the given stock from the .txt file."""
    update_file_path = get_data_path(stock_symbol, extension="txt")
    try:
        with open(update_file_path, 'r') as f:
            last_update_str = f.read().strip()
        return datetime.datetime.strptime(last_update_str, '%Y-%m-%d').date()
    except FileNotFoundError:
        return None

def update_stock_data(stock_symbol):
    """Downloads and updates the stock data from Yahoo Finance."""
    data = yf.download(stock_symbol, start="2020-07-27", interval="1d")["Adj Close"]
    data = pd.DataFrame(data)
    data_path = get_data_path(stock_symbol)  # CSV path
    update_file_path = get_data_path(stock_symbol, extension="txt")  # TXT path

    data.to_csv(data_path, header=True, index=True)  # Save CSV data
    with open(update_file_path, 'w') as f:
        f.write(str(datetime.date.today()))  # Write update date to .txt

def download_data(selected_stock):
    """Downloads stock data, updating it if necessary."""
    last_update = get_last_update_date(selected_stock)
    if last_update is None or last_update < datetime.date.today():
        update_stock_data(selected_stock)
    data = pd.read_csv(get_data_path(selected_stock), index_col=0, parse_dates=True)
    data.rename(columns={"Adj Close": "Fiyat"}, inplace=True)  # Rename column

    return data

def calculate_trend(data):
    """Calculate the polynomial trend line for the stock data"""
    print(data.columns)
    x = np.arange(len(data["Adj Close"]))
    y = data["Adj Close"]
    katsayı = np.polyfit(x, y, 2)
    polfonk = np.poly1d(katsayı)
    trend = polfonk(x)
    r2 = r2_score(y, trend)
    hata = y - trend
    ss = np.std(hata)
    return x, y, trend, r2, ss


def calculate_dollar_trend(data, dollar_data):
    """Calculate the polynomial trend line for the stock data"""
    print(dollar_data.columns)
    x = np.arange(len(data["Adj Close"]))
    dollar_data = dollar_data.reindex(data.index, method='ffill')
    y = data["Adj Close"]/dollar_data["Adj Close"]
    katsayı = np.polyfit(x, y, 2)
    polfonk = np.poly1d(katsayı)
    trend = polfonk(x)
    r2 = r2_score(y, trend)
    hata = y - trend
    ss = np.std(hata)
    return x, y, trend, r2, ss


def plot_stock_data(selected_stock, selected_model, data, trend, r2, ss):
    """Generate the stock price plot"""
    figure = Figure()
    canvas = FigureCanvas(figure)
    ax = figure.add_subplot(111)
    
    ax.plot(data.index, data["Fiyat"], "b.", label="Hisse")
    ax.plot(data.index, trend, "r-", label="Trend")
    ax.fill_between(data.index, trend - ss, trend + ss, color="navy", alpha=0.3, label="±1 Standart Sapma")
    ax.fill_between(data.index, trend - 2 * ss, trend + 2 * ss, color="darkred", alpha=0.3, label="±2 Standart Sapma")
    ax.fill_between(data.index, trend - 3 * ss, trend + 3 * ss, color="gray", alpha=0.3, label="±3 Standart Sapma")
    ax.set_title(f"Hisse Polinomal Regresyon (R-Kare: {r2:.2f})")
    ax.legend(loc="upper left")
    
    canvas.draw()
    return canvas, figure

download_dollar_data()