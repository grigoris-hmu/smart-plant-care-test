from flask_wtf import FlaskForm
from flask_babel import _
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

class loginForm(FlaskForm):
 
    email = StringField(label=_('Email'),
                           validators=[DataRequired(message=_('This field cannot be empty.')), 
                                       Email(message=_('Please enter a valid email address'))])

    password = StringField(label=_('Password'),
                           validators=[DataRequired(message=_('This field cannot be empty.'))])
    
    remember_me = BooleanField(label=_('Remember me'))

    submit = SubmitField(_('Login'))