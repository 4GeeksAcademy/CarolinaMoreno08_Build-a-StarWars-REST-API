"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, People, Planets, Favorites_People, Favorites_Planets
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



@app.route('/users/', methods=['GET'])
def get_users():
    all_users = Users.query.all()
    results = list(map(lambda elements: elements.serialize(), all_users))
    return jsonify(results), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    received_user_id = request.json.get('id')
    results = Favorites_People.query.filter_by(user_id = received_user_id).all()
    people_favorites_serialized = list(map(lambda element: element.serialize(), results))
    results_2 = Favorites_Planets.query.filter_by(user_id = received_user_id).all()
    planets_favorites_serialized = list(map(lambda element: element.serialize(), results_2))

    return jsonify({'planets_favorites': planets_favorites_serialized,'people_favorites': people_favorites_serialized}), 200


@app.route('/people', methods=['GET'])
def get_all_people():
    all_people = People.query.all()
    results = list(map(lambda elements: elements.serialize(), all_people))
    return jsonify(results), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    one_people = People.query.filter_by(id = people_id).first()
    return jsonify(one_people.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets = Planets.query.all()
    results = list(map(lambda elements: elements.serialize(), all_planets))
    return jsonify(results), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    one_planet = Planets.query.filter_by(id = planet_id).first()
    return jsonify(one_planet.serialize()), 200



# @app.route('/planet/<int:planet_id>', methods=['POST'])
# def add_favorite_planet(planet_id):
#     add_planet = Planets(name= request.get_json()["name"], climate= request.get_json()["climate"], diameter= request.get_json()["diameter"])
#     db.session.add(new_planet)
#     db.session.commit()
#     response_body = {
#         "msg": "Add new planet to favorites"
#     }
#     return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
        try:
            user_id = request.args.get('user_id')
            existing_favorite = Favorites_Planets.query.filter_by(user_id=user_id, planet_id=planet_id).first()            
            if existing_favorite:
                return jsonify({"message": "Is already a favorite planet of the user"}), 400            
            planet = Planets.query.get(planet_id)
            if not planet:
                return jsonify({"message": "Planet does not exist"}), 404            
            new_favorite = Favorites_Planets(user_id=user_id, planet_id=planet_id)
            db.session.add(new_favorite)
            db.session.commit()
            return jsonify({"message": "Planet set as favorite"}), 200
        except Exception as e:
            print(str(e))
            return jsonify({"message": "Server error"}), 500
        


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_people(people_id):
        try:
            user_id = request.args.get('user_id')
            existing_favorite = Favorites_People.query.filter_by(user_id=user_id, people_id=people_id).first()            
            if existing_favorite:
                return jsonify({"message": "Is already a favorite people of the user"}), 400            
            people = People.query.get(people_id)
            if not people:
                return jsonify({"message": "People does not exist"}), 404            
            new_favorite = Favorites_People(user_id=user_id, people_id=people_id)
            db.session.add(new_favorite)
            db.session.commit()
            return jsonify({"message": "People set as favorite"}), 200
        except Exception as e:
            print(str(e))
            return jsonify({"message": "Server error"}), 500
        




       
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_one_fav_planet(planet_id):

    # user_id = request.json.get('user_id')  # Obtener user_id del cuerpo de la solicitud
    # print (planet_id, user_id)
    # return jsonify({"msg": "Fav Planet deleted successfully"}), 200
    
    try:
        user_id = request.json.get('user_id')  # Obtener user_id del cuerpo de la solicitud
        print (planet_id, user_id)
        existing_favorite = Favorites_Planets.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if existing_favorite:
            db.session.delete(existing_favorite)  # Eliminar la fila existente
            db.session.commit()
            return jsonify({"msg": "Fav Planet deleted successfully"}), 200
        planet = Planets.query.get(planet_id)
        if not planet:
            return jsonify({"message": "Fav Planet does not exist"}), 404
    except Exception as e:
        db.session.rollback()  # Revertir cualquier cambio en la base de datos
        print(str(e))
        return jsonify({"message": "Server error"}), 500
    
    
        
        # delete_fav_planet = Favorites_Planets.query.get(planet_id)

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_one_fav_people(people_id):

    # user_id = request.json.get('user_id')  # Obtener user_id del cuerpo de la solicitud
    # print (planet_id, user_id)
    # return jsonify({"msg": "Fav Planet deleted successfully"}), 200
    
    try:
        user_id = request.json.get('user_id')  # Obtener user_id del cuerpo de la solicitud
        existing_favorite = Favorites_People.query.filter_by(user_id=user_id, people_id=people_id).first()
        if existing_favorite:
            db.session.delete(existing_favorite)  # Eliminar la fila existente
            db.session.commit()
            return jsonify({"msg": "Fav People deleted successfully"}), 200
        people = People.query.get(people_id)
        if not people:
            return jsonify({"message": "Fav People does not exist"}), 404
    except Exception as e:
        db.session.rollback()  # Revertir cualquier cambio en la base de datos
        print(str(e))
        return jsonify({"message": "Server error"}), 500
       







# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
