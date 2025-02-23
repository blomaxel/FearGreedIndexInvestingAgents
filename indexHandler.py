from investorAgent import *
from broker import *
import pandas as pd
class IndexHandler():
    def __init__(self, fear_greed_index_path, sp500_index_path):
        self.fgi_data = pd.read_csv(fear_greed_index_path, parse_dates=['datetime'])
        self.sp500_data = pd.read_csv(sp500_index_path, parse_dates=['Date'])
        self.latestDate = min(self.fgi_data['datetime'].max() ,self.sp500_data['Date'].max())
    def get_fear_and_greed_index(self, date)-> str:
        df = self.fgi_data[self.fgi_data['datetime'] == date]['rating']
        if df.empty:
            return None
        return df.values[0]

    def get_sp500_index(self, date)-> float:
        df = self.sp500_data[self.sp500_data['Date'] == date]['Open']
        if df.empty:
            return None
        return df.values[0]

        