from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock_portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

# Define Stock model
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shares = db.Column(db.Integer, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    stocks = Stock.query.all()
    total_value = sum(stock.shares * stock.purchase_price for stock in stocks)
    return render_template('index.html', stocks=stocks, total_value=total_value)

@app.route('/add', methods=['POST'])
def add_stock():
    name = request.form['name']
    shares = int(request.form['shares'])
    purchase_price = float(request.form['purchase_price'])

    new_stock = Stock(name=name, shares=shares, purchase_price=purchase_price)

    db.session.add(new_stock)
    db.session.commit()
    flash('Stock added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_stock(id):
    stock = Stock.query.get_or_404(id)
    db.session.delete(stock)
    db.session.commit()
    flash('Stock deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
