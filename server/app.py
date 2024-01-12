#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

# Route to create a new baked good
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    name = data.get('name')
    price = float(data.get('price'))  # Convert price to float
    # Create a new baked good in the database
    new_baked_good = BakedGood(name=name, price=price)
    db.session.add(new_baked_good)
    db.session.commit()
    # Return the newly created baked good as JSON
    return jsonify(new_baked_good.to_dict()), 201  # 201 Created status code

# Route to update the name of a bakery
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery_name(id):
    data = request.form
    new_name = data.get('name')
    # Find the bakery by its ID
    bakery = Bakery.query.get(id)
    if bakery is None:
        return jsonify({'error': 'Bakery not found'}), 404
    # Update the bakery's name if a new name is provided
    if new_name:
        bakery.name = new_name
        db.session.commit()
    # Return the updated bakery as JSON
    return jsonify(bakery.to_dict())

# Route to delete a baked good by its ID
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    # Find the baked good by its ID
    baked_good = BakedGood.query.get(id)
    if baked_good is None:
        return jsonify({'error': 'Baked good not found'}), 404
    # Delete the baked good from the database
    db.session.delete(baked_good)
    db.session.commit()
    # Return a success message
    return jsonify({'message': 'Baked good deleted'})

# Rest of your routes (bakeries, bakery_by_id, baked_goods_by_price, most_expensive_baked_good) remain unchanged

if __name__ == '__main__':
    app.run(port=5555, debug=True)