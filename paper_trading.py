class PaperAccount:
    def __init__(self, balance=10000):
        self.balance=float(balance)
        self.trades=[]

    def record(self, trade):
        self.trades.append(trade)
