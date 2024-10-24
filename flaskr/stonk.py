from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
import yfinance as yf
import matplotlib.pyplot as plt
import os

bp = Blueprint('stonk', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM posts p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('stonk/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('stonk.index'))

    return render_template('stonk/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('stonk/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


#
# ##### BELOW IS PREVIOUS CODE ####
# @app.route('/stock', methods=['POST'])
# def stock():
#     symbol = request.form['symbol'].upper()
#     stock_data = fetch_stock_data(symbol)
#
#     if stock_data:
#         return render_template('stock.html', stock=stock_data, symbol=symbol)
#     else:
#         return render_template('error.html', symbol=symbol)
#
#
# def fetch_stock_data(symbol):
#     try:
#         stock = yf.Ticker(symbol)
#         stock_info = stock.info
#
#         hist = stock.history(period='1mo')
#         plot_stock_chart(symbol, hist['Close'])
#
#         return {
#             'Open': stock_info['open'],
#             'High': stock_info['dayHigh'],
#             'Low': stock_info['dayLow'],
#             'Close': stock_info['close'],
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
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
