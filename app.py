from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sarees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Saree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    sarees = Saree.query.all()
    return render_template('index.html', sarees=sarees)

@app.route('/saree/<int:id>')
def saree_detail(id):
    saree = Saree.query.get_or_404(id)
    return render_template('detail.html', saree=saree)

@app.route('/add', methods=['GET', 'POST'])
def add_saree():
    if request.method == 'POST':
        new_saree = Saree(
            name=request.form['name'],
            description=request.form['description'],
            price=float(request.form['price']),
            image_url=request.form['image_url'],
            category=request.form['category']
        )
        db.session.add(new_saree)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_saree.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000) 