from investorAgent import *

class Broker():
    def __init__(self, list_of_investors: list[InvestorAgent]):
        self.investors = list_of_investors
 
    def update_portfolios(self, geometric_index_change: float, sentiment: str):
        for investor in self.investors:
            investor.update_market_value(geometric_index_change)
            investment = investor.take_action(sentiment)
            #Make sure that agent does not overdraft their accounts
            if investment > investor.cash:
                investment = investor.cash
            if investment < -investor.investedMoney:
                investment = -investor.investedMoney
            investor.cash -= investment
            investor.investedMoney += investment
