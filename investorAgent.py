class InvestorAgent:
    def __init__(self, cash = 1, investedMoney = 0.0):
        self.cash = cash
        self.investedMoney = investedMoney
        self.defaultInvestment = 0.01
        self.defaultWithdrawal = 0.01
        self.name = "InvestorAgent"
    
    def takeAction(self, sentiment: str) -> float:
        #Sentiment will be one of the following: "extreme fear", "fear", "neutral", "greed", "extreme greed"
        #Returns: The proportion of cash to invest
        pass
    
    def getTotalValue(self) -> float:
        return self.cash + self.investedMoney
    
    def updateMarketValue(self, geometricIndexChange: float):
        self.investedMoney = self.investedMoney * geometricIndexChange

class ConstantInvestor (InvestorAgent):
    def __init__(self, cash = 1.0):
        super().__init__(cash)
        self.name = "Constant Investor"
    def takeAction(self, sentiment):
        return self.defaultInvestment * self.cash
    
class FullyInvestedInvestor (InvestorAgent):
    def __init__(self, cash = 1.0):
        super().__init__(cash)
        self.defaultInvestment = 1.0
        self.name = "Fully Invested Investor"
    def takeAction(self, sentiment):
        return self.cash

class PrudentInvestor (InvestorAgent):
    def __init__(self, cash = 1.0):
        super().__init__(cash)
        self.name = "Prudent Investor"

    def takeAction(self, sentiment):
        if sentiment == "extreme fear":
            return self.defaultInvestment * self.cash * 5
        elif sentiment == "fear":
            return self.defaultInvestment * 2  * self.cash
        elif sentiment == "neutral":
            return 0.0
        elif sentiment == "greed":
            return -self.defaultWithdrawal  * self.investedMoney
        elif sentiment == "extreme greed":
            return -self.defaultWithdrawal * 2  * self.investedMoney


class RebalancingInvestor (InvestorAgent):
    def __init__(self, cash = 1.0):
        super().__init__(cash)
        self.name = "Rebalancing Investor"
    def takeAction(self, sentiment):
        if sentiment == "extreme fear":
            return 0.9 * self.getTotalValue()  - self.investedMoney
        elif sentiment == "fear":
            return 0.75 * self.getTotalValue()  - self.investedMoney
        elif sentiment == "neutral":
            return 0.60 * self.getTotalValue()  - self.investedMoney
        elif sentiment == "greed":
            return 0.40 * self.getTotalValue()  - self.investedMoney
        elif sentiment == "extreme greed":
            return 0.20 * self.getTotalValue()  - self.investedMoney

class HypeInvestor (InvestorAgent):
    def __init__(self, cash = 1.0):
        super().__init__(cash)
        self.name = "Hype Investor"

    def takeAction(self, sentiment):
        if sentiment == "extreme fear":
            return 0
        elif sentiment == "fear":
            return 0
        elif sentiment == "neutral":
            return 0.0
        elif sentiment == "greed":
            return self.defaultInvestment *2* self.cash
        elif sentiment == "extreme greed":
            return self.defaultInvestment * 5  * self.cash