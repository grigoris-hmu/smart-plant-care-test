from SmartPlantCare import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    profile_image = db.Column(db.String(30), nullable=False, default='default_profile_image.png')
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"{self.username}:{self.email}"


class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True) ## δήλωση id καλλιέργειας, πρωτεύον κλειδί
    name = db.Column(db.String(50), nullable=False) ## δήλωση ονόματος καλλιέργειας (50 χαρακτήρες), υποχρεωτικό πεδίο
    location = db.Column(db.String(50), nullable=False) ## δήλωση τοποθεσίας καλλιέργειας (50 χαρακτήρες), υποχρεωτικό πεδίο
    location_longitude = db.Column(db.String(50), nullable=False) ## δήλωση longitude τοποθεσίας καλλιέργειας (50 χαρακτήρες), υποχρεωτικό πεδίο
    location_latitude = db.Column(db.String(50), nullable=False) ## δήλωση latitude τοποθεσίας καλλιέργειας (50 χαρακτήρες), υποχρεωτικό πεδίο
    prefecture = db.Column(db.Integer, nullable=False, default=1) ## δήλωση νομού που βρίσκεται η καλλιέργεια, υποχρεωτικό πεδίο
    area = db.Column(db.Integer, nullable=False, default=1) ## δήλωση περιοχής που βρίσκεται η καλλιέργεια, υποχρεωτικό πεδίο
    crop_area = db.Column(db.Float, nullable=False) ## δήλωση έκτασης καλλιέργειας, υποχρεωτικό πεδίο
    crop_type = db.Column(db.Integer, nullable=False, default=1) ## δήλωση Eείους Καλλιέργειας, υποχρεωτικό πεδίο
    soil_type = db.Column(db.Integer, nullable=False, default=1) ## δήλωση τύπου εδάφους, υποχρεωτικό πεδίο
    image = db.Column(db.String(40), nullable=True, default='default_crop_image.png') ## δήλωση ονόματος εικόνας καλλιέργειας (40 χαρακτήρες) με προεπιλεγμένο τίτλο:'default_movie_image.png', ΜΗ υποχρεωτικό πεδίο


    def __repr__(self):
        return f"{self.id}:{self.name}:{self.location}"