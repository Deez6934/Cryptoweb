from flask import Flask, render_template, jsonify, request
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from flask_caching import Cache

app = Flask(__name__)

# Function to generate candlestick chart with Plotly
def create_candlestick_chart(ticker, period, interval):
    data = yf.download(ticker + "-USD", period=period, interval=interval)
    
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name=ticker
    )])

    # Customizing the chart
    fig.update_layout(
        title=f'{ticker} Price - {period}, Interval: {interval}',
        yaxis_title='Price (USD)',
        xaxis_title='Date',
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        hovermode='x'
    )

    return pio.to_json(fig)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Configure cache
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 60})

# API to get the chart data
@app.route('/chart', methods=['GET'])
def get_chart():
    ticker = request.args.get('ticker', default='BTC')
    period = request.args.get('period', default='1d')
    interval = request.args.get('interval', default='15m')

    # Get historical chart data
    chart_json = create_candlestick_chart(ticker, period, interval)

    # Fetch the most recent price
    data = yf.Ticker(ticker + "-USD")
    price = data.history(period="1d")['Close'][0]

    response = {
        'chart': chart_json,
        'price': round(price, 6)  # Format the price to 2 decimal places
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
