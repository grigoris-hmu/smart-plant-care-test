#from flask_wtf import FlaskForm
#from flask_wtf.file import FileField, FileAllowed
#from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
#from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional
#from ..models import User
#from flask_login import current_user

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Optional
from flask_login import current_user
from flask_babel import _
from datetime import datetime as dt
from ..models import User

current_year = dt.now().year

### Custom Validation function outside the form class ###
def maxImageSize(max_size=2):
    max_bytes = max_size * 1024 * 1024
    def _check_file_size(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(_('The size of the image cannot exceed {max_size} MB').format(max_size=max_size))

    return _check_file_size


### Validation function outside the form class ###
def validate_email(form, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError(_('This email already exists!'))

class accountUpdateForm(FlaskForm):
    username = StringField(label=_('Username'),
                           validators=[DataRequired(message=_('This field cannot be empty.')),
                                       Length(min=3, max=15, message=_('This field must be between 3 and 15 characters'))])

    email = StringField(label=_('Email'),
                           validators=[DataRequired(message=_('This field cannot be empty.')), 
                                       Email(message=_('Please enter a valid email address'))])

    ## Αρχείο Εικόνας, με επιτρεπόμενους τύπους εικόνων τα 'jpg', 'jpeg', 'png', και μέγιστο μέγεθος αρχείου εικόνας τα 2 MBytes, ΜΗ υποχρεωτικό πεδίο
    profile_image = FileField(_('Crop image'), validators=[Optional(strip_whitespace=True),
                                                           FileAllowed([ 'jpg', 'jpeg', 'png' ],
                                                            _('Only jpg, jpeg and png image files are allowed!')),
                                                           maxImageSize(max_size=2)])
   
    submit = SubmitField(_('Submit'))

    ## Validator για έλεγχο ύπαρξης του user στη βάση
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(_('This username already exists!'))      

    ## Validator για έλεγχο ύπαρξης του email στη βάση
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(_('This email already exists!'))