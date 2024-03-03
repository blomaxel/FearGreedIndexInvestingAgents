from investorAgent import *
from broker import *
from indexHandler import *
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class Market():
    def __init__(self, fearGreedIndexPath, sp500IndexPath, listOfInvestors: list[InvestorAgent]):
        self.indexHandler = IndexHandler(fearGreedIndexPath, sp500IndexPath)
        self.broker = Broker(listOfInvestors)
        self.lastDate = self.indexHandler.sp500Data['Date'][0]
        self.currentDate = self.indexHandler.sp500Data['Date'][0]
        assert self.currentDate == self.indexHandler.fgiData['datetime'][0]
        self.currentIndexPrice = self.indexHandler.sp500Data['Open'][0]
        self.yesterdayIndexPrice = self.indexHandler.sp500Data['Open'][0]#they are the same for the first day, does not since all agents start with no money invested
        self.portfolioValuesOverTime = {investor.name: [investor.getTotalValue()] for investor in listOfInvestors}

    def strToDate(self, dateStr: str) -> datetime:
        return datetime.strptime(dateStr, '%Y-%m-%d')
    
    def dateToStr(self, date: datetime) -> str:
        return date.strftime('%Y-%m-%d')
    
    def getNextDate(self) -> str:
        currentDate = self.currentDate
        while currentDate is None:
            self.lastDate += timedelta(days=1)
            df = self.indexHandler.sp500Data["Date"][self.indexHandler.sp500Data["Date"] == self.lastDate]
            if df.empty:
                continue
            currentDate = self.lastDate
        #currentDate = self.strToDate(self.currentDate)
        currentDate += timedelta(days=1)
        #currentDateStr = self.dateToStr(currentDate)
        if currentDate in self.indexHandler.sp500Data['Date'].values:
            return currentDate
        return None
        
    def updateMarket(self):
        sentiment = self.indexHandler.getFGI(self.currentDate)
        self.currentIndexPrice = self.indexHandler.getSP500Index(self.currentDate)
        geometricIndexChange = self.currentIndexPrice / self.yesterdayIndexPrice
        self.yesterdayIndexPrice = self.currentIndexPrice
        self.broker.updatePortfolios(geometricIndexChange, sentiment)

    def runSimulation(self):
        day = 1
        while self.lastDate < self.indexHandler.latestDate:
            if day % 100 == 1:
                print(f"Day {day} of simulation and investor {investors[0].name} has {investors[0].getTotalValue()} money.")
            if self.currentDate is not None and self.currentDate.weekday() == 1:
                self.lastDate = self.currentDate
                self.updateMarket()
                self.portfolioValuesOverTime = {investor.name: self.portfolioValuesOverTime[investor.name] + [investor.getTotalValue()] for investor in self.broker.investors}
            self.currentDate = self.getNextDate()
            day += 1
        return self.broker.investors
    

if __name__ == "__main__":
    investors = [PrudentInvestor(1.0), RebalancingInvestor(1.0), ConstantInvestor(1.0), FullyInvestedInvestor(1.0), HypeInvestor(1.0)]
    market = Market('fear_and_greed_data.csv', 'sp500_data.csv', investors)
    investors = market.runSimulation()
    for investor in investors:
        print(f"{investor.name} has {investor.getTotalValue()} in their account after date {market.lastDate}.")
        plt.plot(market.portfolioValuesOverTime[investor.name], label=investor.name)
    plt.legend()
    plt.show()
   

