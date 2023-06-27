#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakery_id = []
    for item in BakedGood.query.all():
        item_dict = {
            'bakery_id': item.bakery_id,
            'created_at': item.created_at,
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'updated_at': item.updated_at,
        }
        bakery_id.append(item_dict)

    response = make_response(
        jsonify(bakery_id),
            200
        )
    
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bk = BakedGood.query.get(id)
    bakery_dict = {
            'bakery_id': bk.bakery_id,
            'created_at': bk.created_at,
            'id': bk.id,
            'name': bk.name,
            'price': bk.price,
            'updated_at': bk.updated_at,
        }
    response = make_response(
        jsonify(bakery_dict),
            200
        )

    response.headers['Content-Type'] = 'application/json'
    return response
    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.asc()).all()
    
    baked_goods_list = []
    for baked_good in baked_goods:
        baked_good_dict = {
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'bakery_id': baked_good.bakery_id,
            'created_at': baked_good.created_at,
            'updated_at': baked_good.updated_at
        }
        baked_goods_list.append(baked_good_dict)
    
    response = make_response(
        jsonify(baked_goods_list),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response

    
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    baked_good_dict = {
        'id': most_expensive.id,
        'name': most_expensive.name,
        'price': most_expensive.price,
        'bakery_id': most_expensive.bakery_id,
        'created_at': most_expensive.created_at,
        'updated_at': most_expensive.updated_at
    }
    
    response = make_response(
        jsonify(baked_good_dict),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)