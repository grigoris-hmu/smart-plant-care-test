from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional, NumberRange
from SmartPlantCare.models import User
from flask_login import current_user

from datetime import datetime as dt

current_year = dt.now().year


''' Custom Validation function outside the form class '''
def maxImageSize(max_size=2):
    max_bytes = max_size * 1024 * 1024
    def _check_file_size(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(f'Το μέγεθος της εικόνας δε μπορεί να υπεβαίνει τα {max_size} MB')

    return _check_file_size


''' Validation function outside the form class '''
def validate_email(form, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError('Αυτό το email υπάρχει ήδη!')



class SignupForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

    email = StringField(label="email",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), 
                                       Email(message="Παρακαλώ εισάγετε ένα σωστό email"), validate_email])

    password = StringField(label="password",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])
    
    password2 = StringField(label="Επιβεβαίωση password",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες"),
                                       EqualTo('password', message='Τα δύο πεδία password πρέπει να είναι τα ίδια')])
    
    submit = SubmitField('Εγγραφή')


    ## Validator για έλεγχο ύπαρξης του user στη βάση
    def validate_username(self, username):
      user = User.query.filter_by(username=username.data).first()
      if user:
         raise ValidationError('Αυτό το username υπάρχει ήδη!')


class AccountUpdateForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

    email = StringField(label="email",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), 
                                       Email(message="Παρακαλώ εισάγετε ένα σωστό email")])

    ## Αρχείο Εικόνας, με επιτρεπόμενους τύπους εικόνων τα 'jpg', 'jpeg', 'png', και μέγιστο μέγεθος αρχείου εικόνας τα 2 MBytes, ΜΗ υποχρεωτικό πεδίο
    profile_image = FileField('Αρχείο Εικόνας', validators=[Optional(strip_whitespace=True),
                                                           FileAllowed([ 'jpg', 'jpeg', 'png' ],
                                                            'Επιτρέπονται μόνο αρχεία εικόνων τύπου jpg, jpeg και png!'),
                                                           maxImageSize(max_size=2)])
   
    submit = SubmitField('Αποστολή')

    ## Validator για έλεγχο ύπαρξης του user στη βάση
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Αυτό το username υπάρχει ήδη!')      

    ## Validator για έλεγχο ύπαρξης του email στη βάση
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Αυτό το email υπάρχει ήδη!')  
        

class LoginForm(FlaskForm):
 
    email = StringField(label="email",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), 
                                       Email(message="Παρακαλώ εισάγετε ένα σωστό email")])

    password = StringField(label="password",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό.")])
    
    remember_me = BooleanField(label="Remember me")

    submit = SubmitField('Είσοδος')


class NewCropForm(FlaskForm):
    ## Όνομα καλλιέργειας, υποχρεωτικό πεδίο κειμένου από 3 έως 50 χαρακτήρες και το αντίστοιχο label και μήνυμα στον validator
    name = StringField(label="Όνομα καλλιέργειας",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=50, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])

    ## τοποθεσίας καλλιέργειας, υποχρεωτικό πεδίο κειμένου από 3 έως 50 χαρακτήρες και το αντίστοιχο label και μήνυμα στον validator
    location = StringField(label="Τοποθεσία καλλιέργειας",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=50, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])
    
    ## Όνομα Καλλιέργειας, υποχρεωτικό πεδίο κειμένου από 3 έως 50 χαρακτήρες και το αντίστοιχο label και μήνυμα στον validator
    location_longitude = StringField(label="Longitude καλλιέργειας",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=50, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])

    ## Όνομα Καλλιέργειας, υποχρεωτικό πεδίο κειμένου από 3 έως 50 χαρακτήρες και το αντίστοιχο label και μήνυμα στον validator
    location_latitude = StringField(label="Latitude καλλιέργειας",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=50, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])        

    prefecture = StringField(label="Νομός που βρίσκεται η καλλιέργεια",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=1, max=2, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])

    area = StringField(label="Περιοχή που βρίσκεται η καλλιέργεια",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=1, max=2, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])

    crop_area = StringField(label="Έκταση που έχει η καλλιέργεια",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=1, max=2, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])

    crop_type = StringField(label="Είδος καλιέργειας",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=1, max=2, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])

    soil_type = StringField(label="Τύπος εδάφους",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=1, max=2, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])

    ## Αρχείο Εικόνας, με επιτρεπόμενους τύπους εικόνων τα 'jpg', 'jpeg', 'png', και μέγιστο μέγεθος αρχείου εικόνας τα 2 MBytes, ΜΗ υποχρεωτικό πεδίο
    image = FileField('Αρχείο Εικόνας', validators=[Optional(strip_whitespace=True),
                                                           FileAllowed([ 'jpg', 'jpeg', 'png' ],
                                                            'Επιτρέπονται μόνο αρχεία εικόνων τύπου jpg, jpeg και png!'),
                                                           maxImageSize(max_size=2)])

    submit = SubmitField(label='Αποστολή')