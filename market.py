from investorAgent import *
from broker import *
from IndexHandler import *
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class Market():
    def __init__(self, fear_greed_index_path, sp500_index_path, list_of_investors: list[InvestorAgent]):
        self.index_handler = IndexHandler(fear_greed_index_path, sp500_index_path)
        self.broker = Broker(list_of_investors)
        self.last_date = self.index_handler.sp500_data['Date'][0]
        self.current_date = self.index_handler.sp500_data['Date'][0]
        assert self.current_date == self.index_handler.fgi_data['datetime'][0]
        self.current_index_price = self.index_handler.sp500_data['Open'][0]
        self.yesterday_index_price = self.index_handler.sp500_data['Open'][0]#they are the same for the first day, does not since all agents start with no money invested
        self.portfolio_values_over_time = {investor.name: [investor.get_total_value()] for investor in list_of_investors}

    def string_to_date(self, dateStr: str) -> datetime:
        return datetime.strptime(dateStr, '%Y-%m-%d')
    
    def date_to_string(self, date: datetime) -> str:
        return date.strftime('%Y-%m-%d')
    
    def get_next_date(self) -> str:
        current_date = self.current_date
        while current_date is None:
            self.last_date += timedelta(days=1)
            df = self.index_handler.sp500_data["Date"][self.index_handler.sp500_data["Date"] == self.last_date]
            if df.empty:
                continue
            current_date = self.last_date
        #current_date = self.string_to_date(self.current_date)
        current_date += timedelta(days=1)
        #current_dateStr = self.date_to_string(current_date)
        if current_date in self.index_handler.sp500_data['Date'].values:
            return current_date
        return None
        
    def update_market(self):
        sentiment = self.index_handler.get_fear_and_greed_index(self.current_date)
        self.current_index_price = self.index_handler.get_sp500_index(self.current_date)
        geometric_index_change = self.current_index_price / self.yesterday_index_price
        self.yesterday_index_price = self.current_index_price
        self.broker.update_portfolios(geometric_index_change, sentiment)

    def run_simulation(self):
        day = 1
        while self.last_date < self.index_handler.latestDate:
            if day % 100 == 1:
                print(f"Day {day} of simulation and investor {investors[0].name} has {investors[0].get_total_value()} money.")
            if self.current_date is not None and self.current_date.weekday() == 1:
                self.last_date = self.current_date
                self.update_market()
                self.portfolio_values_over_time = {investor.name: self.portfolio_values_over_time[investor.name] + [investor.get_total_value()] for investor in self.broker.investors}
            self.current_date = self.get_next_date()
            day += 1
        return self.broker.investors
    

if __name__ == "__main__":
    investors = [ FullUntilFearInvestor(1.0),ReversedRebalancingInvestor(1.0), PrudentInvestor(1.0), RebalancingInvestor(1.0), ConstantInvestor(1.0), FullyInvestedInvestor(1.0), HypeInvestor(1.0)]
    market = Market('fear_and_greed_data.csv', 'sp500_data.csv', investors)
    investors = market.run_simulation()
    for investor in investors:
        print(f"{investor.name} has {investor.get_total_value()} in their account after date {market.last_date}.")
        plt.plot(market.portfolio_values_over_time[investor.name], label=investor.name)
    plt.legend()
    plt.show()
   

