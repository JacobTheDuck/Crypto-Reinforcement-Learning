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

    def bollinger_bands(self):
        sma = data['Close'].rolling
        # std = prices.rolling(rate).std()
        # bollinger_up = sma + std * 2 # Calculate top band
        # bollinger_down = sma - std * 2 # Calculate bottom band
        #return bollinger_up, bollinger_down

    
    def create_figure(self):
        #Create figure
        figure = go.Figure()

        # Create the candle sticks
        figure.add_trace(go.Candlestick(x=self.data.index,
                        open=self.data['Open'],
                        high=self.data['High'],
                        low=self.data['Low'],
                        close=self.data['Close'], name = 'market data'))

        #Add Moving average on the graph
        # figure.add_trace(go.Scatter(x=self.data.index, y= self.data['MA20'],line=dict(color='blue', width=1.5), name = 'Long Term MA'))
        # figure.add_trace(go.Scatter(x=self.data.index, y= self.data['MA5'],line=dict(color='orange', width=1.5), name = 'Short Term MA'))

        #Updating X axis and graph
        # X-Axes
        figure.update_xaxes(
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

        # Present figure
        figure.show()


if __name__ == '__main__':
    data = Market_Data('BTC-USD', '8d', '90m')

    data.create_figure()