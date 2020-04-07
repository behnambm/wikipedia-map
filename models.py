from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwdhash = db.Column(db.String(94), nullable=False)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname  = lastname
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

class Place():
    def address_to_latlong(self, address):
        key = '45c0c172c62bfd'
        url = 'https://eu1.locationiq.com/v1/search.php'  # europe server | provided by locationiq.com
        param = {
            'key': key,
            'q': address,
            'format':'json'
        }
        req = requests.get(url, params=param)
        data = json.loads(req.text)
        try:
            lat = float(data[0].get('lat'))
            lon = float(data[0].get('lon'))
            return (lat, lon)
        except (TypeError, KeyError):
            return False

    def get_wiki_path(self, title):
        url = 'https://en.wikipedia.org/wiki/' + str(title.replace(' ', '_'))
        req = requests.get(url)
        return url 

    def get_walking_time(self, distance):
        return int(distance // 80)

    def query(self, address, radius=5000):
        geocode = self.address_to_latlong(address)
        if geocode:
            lat, lng = geocode
            url = 'https://en.wikipedia.org/w/api.php'
            param = {
                'action': 'query',
                'list': 'geosearch',
                'gsradius': str(radius),
                'gscoord': str(lat) + '|' + str(lng),
                # 'gslimit': '20',
                'format': 'json'
            }
            req = requests.get(url, params=param)
            data = json.loads(req.text)
            places = []
            for place in data['query']['geosearch']:
                title = place.get('title') 
                dist = place.get('dist')
                lat = place.get('lat')
                lng = place.get('lon')
                wiki_path = self.get_wiki_path(title)
                walking_time = self.get_walking_time(dist)  # per minute
                tmp = {
                    'name': title,
                    'lat': lat,
                    'lng': lng,
                    'time': walking_time,
                    'url': wiki_path
                }
                places.append(tmp)
            return places

