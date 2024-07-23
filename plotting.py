import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def download_data(selected_stock):
    """Download stock data from Yahoo Finance"""
    data = yf.download(selected_stock, start="2020-07-27", interval="1d")["Adj Close"]
    return pd.DataFrame(data)

def calculate_trend(data):
    """Calculate the polynomial trend line for the stock data"""
    data.rename(columns={"Adj Close": "Fiyat"}, inplace=True)
    x = np.arange(len(data["Fiyat"]))
    y = data["Fiyat"]
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
