from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites_people = db.relationship('Favorites_People', backref='users', lazy=True)
    favorites_planets = db.relationship('Favorites_Planets', backref='users', lazy=True)

    def __repr__(self):
        return '<Users %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    birth_year= db.Column(db.String(80), unique=False, nullable=False)
    eye_color = db.Column(db.String(20), unique=False, nullable=True)
    favorites_people = db.relationship('Favorites_People', backref='people', lazy=True)

    def __repr__(self):
        return '<Name %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate= db.Column(db.String(80), unique=False, nullable=False)
    diameter = db.Column(db.Integer(), unique=False, nullable=False)
    favorites_planets = db.relationship('Favorites_Planets', backref='planets', lazy=True)

    def __repr__(self):
        return '<Name %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            # do not serialize the password, its a security breach
        }
    

class Favorites_People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'),
        nullable=False)
    

    def __repr__(self):
        return '<Favorites_People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "user_id": self.user_id,
            # do not serialize the password, its a security breach
        }
    

class Favorites_Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'),
        nullable=False)
    

    def __repr__(self):
        return '<Favorites_Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "user_id": self.user_id,
            # do not serialize the password, its a security breach
        }







