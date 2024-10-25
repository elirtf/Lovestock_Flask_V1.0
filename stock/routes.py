from flask import Blueprint, render_template, request, redirect, url_for
import yfinance as yf
import plotly.graph_objs as go
from models import db, User
from flask_login import current_user, login_required


bp = Blueprint('stock', __name__)

DEFAULT_STOCKS = ['AAPL', 'TSLA', 'AMZN', 'GOOGL', 'SBUX', 'MSFT', 'NFLX', 'FB']


### Home route for displaying default stocks & watchlist *if logged in* ###
@bp.route('/')
@login_required
def index():
    sort_by = request.args.get('sort_by', 'Name')
    stock_data = []

    for symbol in DEFAULT_STOCKS:
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period='1d')
        stock_data.append({
            'symbol': symbol,
            'price': stock_info['Close'][0],
            'change': stock_info['Close'][0] - stock_info['Open'][0],
        })

    if sort_by == 'Price':
        stock_data.sort(key=lambda x: x['price'], reverse=True)
    elif sort_by == 'Change':
        stock_data.sort(key=lambda x: x['change'], reverse=True)
    else:
        stock_data.sort(key=lambda x: x['symbol'])

    return render_template('stock/index.html', stocks=stock_data)


@bp.route('/add_to_watchlist', methods=['POST'])
@login_required
def add_to_watchlist():
    symbol = request.form['symbol']
    if symbol not in current_user.watchlist:
        current_user.watchlist.append(symbol)
        db.session.commit()
    return redirect(url_for('stock.index'))

@bp.route('/remove_from_watchlist', methods=['POST'])
@login_required
def remove_from_watchlist():
    symbol = request.form['symbol']
    if symbol in current_user.watchlist:
        current_user.watchlist.remove(symbol)
        db.session.commit()
    return redirect(url_for('stock.index'))

@bp.route('/stock/<symbol>')
@login_required
def stock(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period='1mo')

    # Generate Plotly chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name=symbol))
    chart_html = fig.to_html(full_html=False)

    stock_data = {
        'symbol': symbol,
        'price': hist['Close'][-1],
        'change': hist['Close'][-1] - hist['Open'][0]
    }

    return render_template('stock.html', stock_data=stock_data, chart_html=chart_html)


# # Function: Fetch stock data using yfinance #
# def fetch_stock_data(symbol, time_period='1mo'):
#     try:
#         stock = yf.Ticker(symbol)
#         stock_info = stock.info
#
#         hist = stock.history(period=time_period)
#         plot_stock_chart(symbol, hist['Close']) # Plots and saves chart
#
#         return {
#             'Open': stock_info['open'],
#             'High': stock_info['dayHigh'],
#             'Low': stock_info['dayLow'],
#             'Close': stock_info['regularMarketPrice'],
#             'Vol': stock_info['volume'],
#             'Mkt Cap': stock_info['marketCap'],
#             'P/E': stock_info.get('forwardPE', 'N/A'),
#             'EPS': stock_info.get('trailingEps', 'N/A'),
#             'Beta': stock_info.get('beta', 'N/A'),
#             'Div Yield': stock_info.get('dividendYield', 'N/A'),
#             '52 Wk High': stock_info['fiftyTwoWeekHigh'],
#             '52 Wk Low': stock_info['fiftyTwoWeekLow'],
#         }
#     except Exception as e:
#         print(f'Error fetching data for {symbol}: {e}')
#         return None
#
# # Function: Plot the chart & save to static folder #
# def plot_stock_chart(symbol, data):
#     plt.figure(figsize=(10, 5))
#     plt.plot(data, color='green')
#     plt.title(f'{symbol} Stock Price - Last Month')
#     plt.xlabel('Date')
#     plt.ylabel('Price')
#
#     chart_path = f'static/{symbol}_chart.png'
#     plt.savefig(chart_path)
#     plt.close()