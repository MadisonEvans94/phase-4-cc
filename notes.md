<!-- TODO: models.py -->
<!-- [x] make necessary imports -->

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

<!-- [x] build all the Classes in models and add __tablename__ properties -->
<!--
side note: be sure to use proper notation for the items that require USDC time:
example:
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())
 -->
<!-- [x] include SerializerMixin wrapper to each class -->
<!-- [x] add backrefs where needed -->
<!-- ex: hero_powers = db.relationship('HeroPower', backref = 'hero') -->
<!-- [x] add the association proxies -->
<!-- example:

    ... in the case of the Hero Class ...
    powers = association_proxy('hero_powers', 'power'),

    where heroe_powers is not the name of a table, but rather the name of the relationship ...

    hero_powers = db.relationship('HeroPower', backref = 'hero')
 -->
<!-- [x] set serialize_rules that exclude the CURRENT instance of the class  -->
<!--

class Hero(db.Model, SerializerMixin):
    # ...
    serialize_rules = ('-hero_powers.power',)


class HeroPower(db.Model, SerializerMixin):
    # ...
    serialize_rules = ('-hero', '-power',)


class Power(db.Model, SerializerMixin):
    # ...
    serialize_rules = ('-hero_powers.hero',)

 -->
<!-- ex:
... within the HeroPowers class ...
hero = db.Column(db.Integer, db.ForeignKey('heroes.id'))
power = db.Column(db.Integer, db.ForeignKey('powers.id'))
serialize_rules = ('-power.hero_powers', '-hero.hero_powers')

... within the Heroes class ..
hero_powers = db.relationship('HeroPowers', backref = 'hero')
powers = association_proxy('hero_powers', 'power')
serialize_rules = ('-powers.hero', '-hero_powers.hero')

-->
<!-- [ ] add validations -->
<!--

class Power(db.Model, SerializerMixin):
   ...

    @validates('description')
    def validates_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("Strength must have a length")
        return description
 -->
<!-- TODO: app.py -->
<!-- [ ] upgrade and migrate -->
<!--
flask db upgrade (synonymous to makemgirations)
flask db migrate (synonymous to migrate)
 -->
<!-- [ ] make necessary imports -->

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, <!-- also include any other models here -->

<!-- [ ] make sure initial boiler plate code is in place -->

app = Flask(**name**)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

if **name** == '**main**':
app.run(port=5555, debug=True)

<!-- [ ] GET (all) example -->
<!--
class Hero(Resource):
    def get(self):
        heroes = Hero.query.all()
        heroes_dict = [hero.to_dict() for hero in heroes]
        response = make_response(
            jsonify(heroes_dict),
            200
        )
        return response
-->
<!-- [ ] PUT example -->
<!--

class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()
        if (heroes):
            heroes_dict = [hero.to_dict() for hero in heroes]
            return make_response(heroes_dict, 200)
        else:
            return make_response("no heroes found", 404)

    def put(self):
        try:
            new_hero = Hero(
                name=request.get_json()['name'],
                super_name=request.get_json()['super_name']
            )
            db.session.add(new_hero)
            db.session.commit()
            return_hero = Hero.query.filter_by(
                id=new_hero.id).first().to_dict()
            return make_response(return_hero, 201)
        except ValueError:
            return make_response("value don't workkkk", 404)

 -->
