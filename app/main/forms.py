from flask import request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError, DataRequired
from app.models import User, Domain

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    clientnet_user = StringField('ClientNet Username', validators=[DataRequired()])
    clientnet_password = PasswordField('ClientNet Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class DomainForm(FlaskForm):
    domainname = StringField('Domain', validators=[DataRequired()])
    submit = SubmitField('Add domain')

    def validate_domainname(self, domainname):
        domain = Domain.query.filter_by(domainname=self.domainname.data, user_id = current_user.id).first()
        if domain is not None:
            raise ValidationError('Domainname already in use')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class IOCForm(FlaskForm):
    
    submit = SubmitField('Add')