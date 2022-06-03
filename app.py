import pdb
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Inventory %r>' % self.name


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['product_name']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        new_product = Inventory(name=name, description=description, price=price, quantity=quantity)

        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your product'
    else:
        products = Inventory.query.order_by(Inventory.date_created).all()
        return render_template("index.html", products=products)
    

@app.route('/delete/<int:id>')
def delete(id):
    product_to_delete = Inventory.query.get_or_404(id)

    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that product'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    product = Inventory.query.get_or_404(id)

    if request.method == 'POST':
        product.name = request.form['product_name']
        product.description = request.form['description']
        product.price = request.form['price']
        product.quantity = request.form['quantity']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your product'
    else:
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

