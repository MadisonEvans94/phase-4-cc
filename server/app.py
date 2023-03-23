#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

class Restaurants(Resource): 
    def get(self): 
        restaurants = Restaurant.query.all()
        if(restaurants): 
            restaurants_dict = [restaurant.to_dict() for restaurant in restaurants]      
            return make_response(restaurants_dict, 200)
        else: 
            return make_response("no restaurants found in db", 404)
            
class RestaurantsById(Resource): 
    def get(self,id): 
        restaurant = Restaurant.query.filter_by(id=id).first()
        if(restaurant):    
            return make_response(restaurant.to_dict(), 200)
        else: 
            return make_response("This restaurant id doesn't exist", 404)
    
class Pizzas(Resource): 
    def get(self): 
        pizzas = Pizza.query.all()
        if(pizzas): 
            pizzas_dict = [pizza.to_dict() for pizza in pizzas]      
            return make_response(pizzas_dict, 200)
        else: 
            return make_response("no pizzas", 404)
        
class PizzasById(Resource): 
    def get(self,id): 
        pizza = Pizza.query.filter_by(id=id).first()
        if(pizza):    
            return make_response(pizza.to_dict(), 200)
        else: 
            return make_response("This pizza id doesn't exist", 404)
    
# TODO: connect resources 
api.add_resource(Pizzas, "/pizzas")
api.add_resource(PizzasById, "/pizzas/<int:id>")
api.add_resource(Restaurants, '/restaurants')
api.add_resource(RestaurantsById, '/restaurants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
