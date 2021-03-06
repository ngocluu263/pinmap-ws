from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/pinmap.db'
db = SQLAlchemy(app)


class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    rating = db.Column(db.Float(1))
    description = db.Column(db.Text)
    lat = db.Column(db.Float(6))
    lng = db.Column(db.Float(6))
    photo = db.Column(db.Text)
    date = db.Column(db.Integer)
    googleplus_id = db.Column(db.Text)

    def __init__(self, title, rating, description, lat, lng, photo, date, googleplus_id):
        self.title = title
        self.rating = rating
        self.description = description
        self.lat = lat
        self.lng = lng
        self.photo = photo
        self.date = date
        self.googleplus_id = googleplus_id

    # Avoid unwanted fields when serialize
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route('/insert', methods=['GET'])
def insert():
    # Empty db
    Pin.query.delete()
    # Example data
    pin = Pin('August 2014 in Tallinn', 5.0, 'I spent one month in the capital of Estonia working in a hostel as a volunteer. Unforgetable experience!',
              59.431898, 24.740681, 'http://156.35.95.75:8080/1429481944.jpg', 1408116466, '904972304704039106999')
    pin2 = Pin('4 days in London', 4.0, 'Visiting the capital of UK. You never get bored of London <3',
               51.5286416, -0.1015987, 'http://156.35.95.75:8080/1429483267.jpg', 1411658866, '904972304704039106999')
    pin3 = Pin('My weekend in Moscow', 4.5, 'Visiting the capital of Russia. Amazing buildings and culture.',
               55.749792, 37.6324949, 'http://156.35.95.75:8080/1429483251.jpg', 1411658866, '904972304704039106999')
    pin4 = Pin('NYC Rules! Winter 2013', 5.0, 'Undoubtedly the most stunning city I have ever been.',
               40.7033127, -73.979681, 'http://156.35.95.75:8080/1429483235.jpg', 1411658866, '904972304704039106999')
    pin5 = Pin('January in Budapest', 4.9, 'Visiting my friend. Incredible atmosphere every night!',
               47.4812134, 19.1303031, 'http://156.35.95.75:8080/1429482727.jpg', 1411658866, '904972304704039106999')
    db.session.add(pin)
    db.session.add(pin2)
    db.session.add(pin3)
    db.session.add(pin4)
    db.session.add(pin5)
    db.session.commit()
    return 'Inserted: ' + json.dumps(pin.as_dict()) + json.dumps(pin2.as_dict()) + json.dumps(pin3.as_dict()) + json.dumps(pin4.as_dict()) + json.dumps(pin5.as_dict())

@app.route('/pins/<user_google_id>', methods=['GET'])
def get_all_pins(user_google_id):
    pins = Pin.query.filter_by(googleplus_id=user_google_id).all()
    return json.dumps([pin.as_dict() for pin in pins])

@app.route('/pin/<pin_id>', methods=['GET'])
def get_pin(pin_id):
    pin = Pin.query.filter_by(id=pin_id).first()
    return json.dumps(pin.as_dict()) if pin is not None else '404'

@app.route('/pin', methods=['POST'])
def create_pin():
    data = request.data
    data_json = data.decode(encoding='UTF-8')
    data_dict = json.loads(data_json)
    pin = Pin(data_dict['title'], data_dict['rating'], data_dict['description'],
              data_dict['lat'], data_dict['lng'], data_dict['photo'],
              data_dict['date'], data_dict['googleplus_id'], )
    db.session.add(pin)
    db.session.commit()
    print('Created pin: ' + data_json)
    return '200'

@app.route('/pin/<pin_id>', methods=['DELETE'])
def delete_pin(pin_id):
    pin = Pin.query.filter_by(id=pin_id).first()
    if pin is not None:
        db.session.delete(pin)
        db.session.commit()
        print('Deleted pin ' + json.dumps(pin.as_dict()))
        return '200'
    else:
        return '404'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
    db.create_all()