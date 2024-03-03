from investorAgent import *

class Broker():
    def __init__(self, listOfInvestors: list[InvestorAgent]):
        self.investors = listOfInvestors
 
    def updatePortfolios(self, geometricIndexChange: float, sentiment: str):
        for investor in self.investors:
            investor.updateMarketValue(geometricIndexChange)
            investment = investor.takeAction(sentiment)
            #Make sure that agent does not overdraft their accounts
            if investment > investor.cash:
                investment = investor.cash
            if investment < -investor.investedMoney:
                investment = -investor.investedMoney
            investor.cash -= investment
            investor.investedMoney += investment
