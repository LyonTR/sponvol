# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


builtin_list = list


db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


# [START model]
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
        return "<Volunteer(title='%s', author=%s)" % (self.title, self.author)
# [END model]


# [START list]
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Volunteer.query
             .order_by(Volunteer.title)
             .limit(limit)
             .offset(cursor))
    volunteer = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(volunteer) == limit else None
    return (volunteer, next_page)
# [END list]


# [START read]
def read(id):
    result = Volunteer.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read]


# [START create]
def create(data):
    volunteer = Volunteer(**data)
    db.session.add(volunteer)
    db.session.commit()
    return from_sql(volunteer)
# [END create]


# [START update]
def update(data, id):
    volunteer = Volunteer.query.get(id)
    for k, v in data.items():
        setattr(volunteer, k, v)
    db.session.commit()
    return from_sql(volunteer)
# [END update]


def delete(id):
    Volunteer.query.filter_by(id=id).delete()
    db.session.commit()


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
