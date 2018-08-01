from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rubicon.db'

db = SQLAlchemy(app)

class Volunteer(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    known_as = db.Column(db.String(255))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(4096))
    email_address = db.Column(db.String(255))\
    mobile_phone_number = db.Column(db.String(255))
    alternative_phone_number = db.Column(db.String(255))
    street_address  = db.Column(db.String(255))
    town_city = db.Column(db.String(255))
    postcode = db.Column(db.String(255))
    emergency_contact = db.Column(db.String(255))
    outdoor_work = db.Column(db.String(255))
    indoor_work = db.Column(db.String(255))
    interests = db.Column(db.String(255))
    signed_in = db.Column(db.String(255))
    spolunteer_number = db.Column(db.Integer)
    workforce_holding = db.Column(db.String(255))
    induction = db.Column(db.Boolean, unique=False, default=False)
    training_and_awareness = db.Column(db.String(255))
    ops_vrc = db.Column(db.String(255))
    comments = db.Column(db.String(255))
    status = db.Column(db.String(255))
    strike_team = db.Column(db.String(255))
    location = db.Column(db.String(255))

    def __repr__(self):
        return "<Volunteer {}".format(self.id)