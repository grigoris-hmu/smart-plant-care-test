from .. import db
from ..user.models import User
#from werkzeug.security import generate_password_hash, check_password_hash
#from .. import login
#from flask_login import UserMixin
#from ..models import Todo

#from SmartPlantCare import db
from datetime import datetime

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True) ## δήλωση id καλλιέργειας, πρωτεύον κλειδί
    title = db.Column(db.String(50), nullable=True)
    plot = db.Column(db.Text(), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    release_year = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) ## δήλωση ID του χρήστη που αποθήκευσε την ταινία, ForeignKey στο πεδίο id του πίνακα user, υποχρεωτικό πεδίο

    def __repr__(self):
        return f"{self.id}:{self.name}:{self.crop_area}"
