import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

class Market_Data():

    def __init__(self, ticker, period, interval):
        
        self.ticker = ticker
        self.period = period
        self.interval = interval

        # Get the data set
        self.data = yf.download(tickers=ticker, period=period, interval=interval)

        #Create figure
        self.figure = go.Figure()


    # Print the table
    def print_data(self):
        print(self.data)


    def bollinger_bands(self):
        # 20 day sma
        self.data['20SMA'] = self.data['Close'].rolling(20).mean()
        std = self.data['20SMA'].rolling(10).std()

        sma = self.data['20SMA']

        # Calculate Bands
        bollinger_uppper = sma + std * 2
        bollinger_lower = sma - std * 2 

        # Set the bands in the table
        self.data['BollingerU'] = bollinger_uppper
        self.data['BollingerL'] = bollinger_lower

        #Add Bollinger on the graph
        self.figure.add_trace(go.Scatter(x=self.data.index, y= self.data['BollingerU'], line=dict(color='blue', width=1.5), name = 'Upper Bollinger'))
        self.figure.add_trace(go.Scatter(x=self.data.index, y= self.data['BollingerL'], line=dict(color='orange', width=1.5), name = 'Lower Bollinger'))

    # MACD
    def macd(self):

        exp1 = self.data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = self.data['Close'].ewm(span=26, adjust=False).mean()

        macd = exp1-exp2
        exp3 = macd.ewm(span=9, adjust=False).mean()

        self.data['MACD'] = macd

        self.figure.add_trace(go.Scatter(x=self.data.index, y= exp3, line=dict(color='green', width=1.5), name = 'EXPMACD'))
        self.figure.add_trace(go.Scatter(x=self.data.index, y= self.data['MACD'], line=dict(color='purple', width=1.5), name = 'MACD'))




    def rsi(self, periods=14, simple=True):
        
        closing_delta = self.data['Close'].diff()

        # Get upper and lower bands
        up = closing_delta.clip(lower=0)
        down = -1 * closing_delta.clip(upper=0)

        if simple == False:
            # Exponential moving average
            moving_average_up = up.ewm(com = periods - 1, min_periods = periods).mean()
            moving_average_down = down.ewm(com = periods - 1, min_periods = periods).mean()
        else:
            # Simple moving average
            moving_average_up = up.rolling(window = periods).mean()
            moving_average_down = down.rolling(window = periods).mean()
        
        rsi = moving_average_up / moving_average_down
        rsi = 100 - (100/(1 + rsi))

        self.data['RSI'] = rsi

        self.figure.add_trace(go.Scatter(x=self.data.index, y= self.data['RSI'], line=dict(color='purple', width=1.5), name = 'RSI'))

    
    def create_figure(self):

        # Create the candle sticks
        self.figure.add_trace(go.Candlestick(x=self.data.index,
                        open=self.data['Open'],
                        high=self.data['High'],
                        low=self.data['Low'],
                        close=self.data['Close'], name = 'market data'))


        #Updating X axis and graph
        # X-Axes
        self.figure.update_xaxes(
            # This creates a range slider
            rangeslider_visible=True,
            rangeselector=dict(

                # These are buttons that can be used to break down the graph

                buttons=list([
                    dict(count=3, label="3d", step="day", stepmode="backward"),
                    dict(count=5, label="5d", step="day", stepmode="backward"),
                    dict(count=7, label="WTD", step="day", stepmode="todate"),
                    dict(step="all")
                ])
            )
        )


    def show_figure(self):
        # Present figure
        self.figure.show()

    
    def get_table_values(self):
        return self.data



if __name__ == '__main__':
    data = Market_Data('BTC-USD', '8d', '90m')

    data.bollinger_bands()
    # data.rsi(simple=False)
    data.macd()

    data.create_figure()
    data.show_figure()

    

    print(data.get_table_values())