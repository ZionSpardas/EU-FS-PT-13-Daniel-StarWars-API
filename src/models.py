from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
 

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    eye_color = db.Column(db.String(80), unique=False, nullable=False)
    hair_color = db.Column(db.String(80), unique=False, nullable=False)
    # user = db.relationship("User", secondary="Favorite_Character")
    

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "eye color": self.eye_color,
            "hair color": self.hair_color,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)
    terrain = db.Column(db.String(80), unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
   # user = db.relationship("User", secondary="Favorite_Planet")

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "diameter": self.diameter,
            # do not serialize the password, its a security breach
        }
    
class Favorite_Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id =db.Column(db.Integer, db.ForeignKey('planets.id'))
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    planets = db.relationship(Planets)
    #user = db.relationship(User, backref=db.backref("Favorite_Planet", cascade="all"))
    #planets = db.relationship(Planets, backref=db.backref("Favorite_Planet", cascade="all"))

    
    def __repr__(self):
        return '<FavPlanet %r>' % self.favplanet

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "user_id": self.user_id
            # do not serialize the password, its a security breach
        }

class Favorite_Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    people_id =db.Column(db.Integer, db.ForeignKey('people.id'))
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    people = db.relationship(People)
    
    
    def __repr__(self):
        return '<FavPeople %r>' % self.favpeople

    def serialize(self):
        return {
            "id": self.id,
            "peopleid": self.people_id,
            "userid": self.user_id
            # do not serialize the password, its a security breach
        }