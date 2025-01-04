#from flask_wtf.file import FileField, FileAllowed
#from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
#from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional
#from flask_login import current_user
#from datetime import datetime as dt
from flask_wtf import FlaskForm
from flask_babel import _
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from ..models import User

### Validation function outside the form class ###
def validate_email(form, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError(_('This email already exists!'))
    

class signupForm(FlaskForm):
    username = StringField(label=_('Username'),
                           validators=[DataRequired(message=_('This field cannot be empty.')),
                                       Length(min=3, max=15, message=_('This field must be between 3 and 15 characters'))])

    email = StringField(label=_('Email'),
                           validators=[DataRequired(message=_('This field cannot be empty.')), 
                                       Email(message=_('Please enter a valid email address')), validate_email])

    password = StringField(label=_('Password'),
                           validators=[DataRequired(message=_('This field cannot be empty.')),
                                       Length(min=3, max=15, message=_('This field must be between 3 and 15 characters'))])
    
    password2 = StringField(label=_('Confirm password'),
                           validators=[DataRequired(message=_('This field cannot be empty.')),
                                       Length(min=3, max=15, message=_('This field must be between 3 and 15 characters')),
                                       EqualTo('password', message=_('The two password fields must be the same'))])
    
    submit = SubmitField(_('Signup'))


    ## Validator για έλεγχο ύπαρξης του user στη βάση
    def validate_username(self, username):
      user = User.query.filter_by(username=username.data).first()
      if user:
         raise ValidationError(_('This email already exists!'))