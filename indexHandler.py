from investorAgent import *
from broker import *
import pandas as pd
class IndexHandler():
    def __init__(self, fearGreedIndexPath, sp500IndexPath):
        self.fgiData = pd.read_csv(fearGreedIndexPath, parse_dates=['datetime'])
        self.sp500Data = pd.read_csv(sp500IndexPath, parse_dates=['Date'])
        self.latestDate = min(self.fgiData['datetime'].max() ,self.sp500Data['Date'].max())
    def getFGI(self, date)-> str:
        df = self.fgiData[self.fgiData['datetime'] == date]['rating']
        if df.empty:
            return None
        return df.values[0]

    def getSP500Index(self, date)-> float:
        df = self.sp500Data[self.sp500Data['Date'] == date]['Open']
        if df.empty:
            return None
        return df.values[0]

        