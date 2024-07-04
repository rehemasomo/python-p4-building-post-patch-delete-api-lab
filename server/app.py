#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
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

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    bakery_id = int(data['bakery_id'])
    bakery = Bakery.query.get(bakery_id)
    if not bakery:
        return jsonify({"message": "Bakery not found"}), 404
    
    new_baked_good = BakedGood(
        name=data['name'],
        price=float(data['price']),
        bakery_id=bakery_id
    )
    db.session.add(new_baked_good)
    db.session.commit()
    
    return jsonify(new_baked_good.to_dict()), 201

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        return jsonify({"message": "Bakery not found"}), 404
    
    data = request.form
    if 'name' in data:
        bakery.name = data['name']
    
    db.session.commit()
    
    return jsonify(bakery.to_dict()), 200

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if not baked_good:
        return jsonify({"message": "Baked good not found"}), 404
    
    db.session.delete(baked_good)
    db.session.commit()
    
    return jsonify({"message": "Baked good deleted successfully"}), 200

if __name__ == '__main__':
    app.run(port=5558, debug=True)

    