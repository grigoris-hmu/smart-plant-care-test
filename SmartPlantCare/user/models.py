from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from .. import login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    profile_image = db.Column(db.String(30), nullable=False, default='default_profile_image.png')
    password = db.Column(db.String(15), nullable=False)
    crops = db.relationship('Crop', backref='author', lazy=True)

    def __repr__(self):
        return f"{self.username}:{self.email}"
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))