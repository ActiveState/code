# Automated Stock Market Trading Simulation
# FB - 20140515
import random

initialMoneyOwned = 1000.0
initialStocksOwned = 0.1
initialStockPrice = 10000.0
tradingDays = 1000
tp = 5.0 # buy/sell percentage threshold of the investor
maxVolatilityPercent = 5.0 # of the stock
numTrials = 1000

initialInvestment = initialMoneyOwned + initialStocksOwned * initialStockPrice

def SimulateTrading(moneyOwned, stocksOwned, stockPrice, days):
    stockBuySellPrice = stockPrice
    
    for day in range(days):
        volatility = random.random() * stockPrice * maxVolatilityPercent / 100.0 
        stockPrice += (random.random() * 2.0 - 1.0) * volatility

        # trading
        if stocksOwned > 0.0:
            if stockPrice >= stockBuySellPrice * (100.0 + tp) / 100.0:
                # sell
                moneyOwned += stocksOwned * stockPrice
                stocksOwned = 0.0
                stockBuySellPrice = stockPrice

        if moneyOwned > 0.0:
            if stockPrice <= stockBuySellPrice * (100.0 - tp) / 100.0:
                # buy
                stocksOwned += moneyOwned / stockPrice
                moneyOwned = 0.0
                stockBuySellPrice = stockPrice

    return (moneyOwned, stocksOwned, stockPrice)

numWins = 0
numLosses = 0
totalWins = 0.0
totalLosses = 0.0
for i in range(numTrials):
    (moneyOwned, stocksOwned, stockPrice) = \
    SimulateTrading(initialMoneyOwned, initialStocksOwned, initialStockPrice, tradingDays)

    finalReturn = moneyOwned + stocksOwned * stockPrice - initialInvestment

    if finalReturn > 0.0:
        numWins += 1
        totalWins += finalReturn
    elif finalReturn < 0.0:
        numLosses += 1
        totalLosses += finalReturn

print "Initial Investment = " + str(initialInvestment) 
print "Trading Days       = " + str(tradingDays) 
print "Number of Trials   = " + str(numTrials)
print "Number of Wins     = " + str(numWins)
print "Average Win Amt    = " + str(totalWins / numWins)
print "Number of Losses   = " + str(numLosses)
print "Average Loss Amt   = " + str(abs(totalLosses / numLosses))
