"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from sqlalchemy import and_
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorite_Character, Favorite_Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False


db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



@app.route('/people', methods=['GET'])
def handle_people():
    people = People.query.all()
    # https://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
    return jsonify([p.serialize() for p in people]), 200

@app.route('/people/<int:person_id>', methods=['PUT', 'GET'])
def handle_person(person_id):
    # Potential reference : https://stackoverflow.com/questions/54472696/failed-to-decode-json-object-expecting-value-line-1-column-1-char-0
    if request.method == 'GET':
        person = People.query.get(person_id)
        return jsonify(person.serialize()), 200
    
    if request.method == 'PUT':
        person = People.query.get(person_id)
        body = request.get_json()
        person.username = body.username
        db.session.commit()
        return jsonify(person.serialize()), 200
    
    return "Invalid Method", 404


@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = Planets.query.all()
    return jsonify([p.serialize() for p in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET', 'PUT'])
def handle_planet(planets_id):
     if request.method == 'GET':
        planet = Planets.query.get(planets_id)
        return jsonify(planet.serialize()), 200
     
     if request.method == 'PUT':
        planet = Planets.query.get(planets_id)
        body = request.get_json()
        planet.name = body.name
        db.session.commit()
        return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def handle_users():
    users = User.query.all()
    return jsonify([p.serialize() for p in users]), 200

@app.route('/users/favoritesplanet/<int:user_id>', methods=['GET'])
def handle_favorites_planet(user_id):
    favplan = Favorite_Planet.query.filter_by(user_id = user_id).all()  
    return jsonify([p.serialize() for p in favplan]), 200
    
@app.route('/users/favoritescharacter/<int:user_id>', methods=['GET'])
def handle_favorites_character(user_id):
    favchar = Favorite_Character.query.filter_by(user_id = user_id).all()
    return jsonify([p.serialize() for p in favchar]), 200


@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    existing_favorite = Favorite_Planet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        return "Planet is already in favorites", 400  
    new_favorite = Favorite_Planet(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    favplan = Favorite_Planet.query.filter_by(user_id = user_id).all() 
    return jsonify([p.serialize() for p in favplan]), 200

@app.route('/favorite/<int:user_id>/character/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    existing_favorite = Favorite_Character.query.filter_by(user_id=user_id, people_id=character_id).first()
    if existing_favorite:
        return "Character is already in favorites", 400  
    new_favorite = Favorite_Character(user_id=user_id, people_id=character_id)
    db.session.add(new_favorite)
    db.session.commit()
    favchar = Favorite_Character.query.filter_by(user_id = user_id).all() 
    return jsonify([p.serialize() for p in favchar]), 200

@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id,planet_id):
    session = db.session
    condition = and_(Favorite_Planet.planet_id == planet_id, Favorite_Planet.user_id == user_id)
    session.query(Favorite_Planet).filter(condition).delete()
    session.commit()
    favplan = Favorite_Planet.query.filter_by(user_id = user_id).all()   
    return jsonify([p.serialize() for p in favplan]), 200
 
@app.route('/favorite/<int:user_id>/people/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id,character_id):
    session = db.session
    condition = and_(Favorite_Character.people_id == character_id, Favorite_Character.user_id == user_id)
    session.query(Favorite_Character).filter(condition).delete()
    session.commit()
    favchar = Favorite_Character.query.filter_by(user_id = user_id).all()   
    return jsonify([p.serialize() for p in favchar]), 200
 
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
