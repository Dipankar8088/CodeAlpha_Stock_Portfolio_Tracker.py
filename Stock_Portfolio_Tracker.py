import yfinance as yf
import pandas as pd

class Stock:
    def __init__(self, ticker, shares, purchase_price):
        self.ticker = ticker
        self.shares = shares
        self.purchase_price = purchase_price

    def current_price(self):
        try:
            stock_data = yf.Ticker(self.ticker)
            # Get the last available closing price
            current_price = stock_data.history(period="1d")['Close'].iloc[-1]
            return current_price
        except Exception as e:
            print(f"Error fetching price for {self.ticker}: {e}")
            return None

    def current_value(self):
        price = self.current_price()
        if price is not None:
            return self.shares * price
        return 0

    def profit_loss(self):
        price = self.current_price()
        if price is not None:
            return (price - self.purchase_price) * self.shares
        return 0

class Portfolio:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, ticker, shares, purchase_price):
        if ticker in self.stocks:
            self.stocks[ticker].shares += shares
        else:
            self.stocks[ticker] = Stock(ticker, shares, purchase_price)
        print(f"Added {shares} shares of {ticker} at ${purchase_price:.2f} each.")

    def remove_stock(self, ticker, shares):
        if ticker in self.stocks:
            if self.stocks[ticker].shares >= shares:
                self.stocks[ticker].shares -= shares
                if self.stocks[ticker].shares == 0:
                    del self.stocks[ticker]
                print(f"Removed {shares} shares of {ticker}.")
            else:
                print("Not enough shares to remove.")
        else:
            print(f"Stock {ticker} not found in portfolio.")

    def total_value(self):
        total = sum(stock.current_value() for stock in self.stocks.values())
        return total

    def display_portfolio(self):
        if not self.stocks:
            print("Your portfolio is empty.")
        else:
            print("\nCurrent Portfolio:")
            for stock in self.stocks.values():
                current_price = stock.current_price()
                if current_price is not None:
                    total_value = stock.current_value()
                    profit_loss = stock.profit_loss()
                    print(f"{stock.ticker}: {stock.shares} shares, "
                          f"Current Price: ${current_price:.2f}, "
                          f"Total Value: ${total_value:.2f}, "
                          f"Profit/Loss: ${profit_loss:.2f}")
            print(f"Total Portfolio Value: ${self.total_value():.2f}\n")

def main():
    portfolio = Portfolio()
    while True:
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Display Portfolio")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            ticker = input("Enter stock ticker: ").upper()
            shares = int(input("Enter number of shares: "))
            purchase_price = float(input("Enter purchase price per share: "))
            portfolio.add_stock(ticker, shares, purchase_price)
        elif choice == '2':
            ticker = input("Enter stock ticker to remove: ").upper()
            shares = int(input("Enter number of shares to remove: "))
            portfolio.remove_stock(ticker, shares)
        elif choice == '3':
            portfolio.display_portfolio()
        elif choice == '4':
            print("Exiting the portfolio tracker.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
