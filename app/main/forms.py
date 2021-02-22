from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import (StringField, SubmitField, PasswordField,
                     SelectField, HiddenField, RadioField)
from wtforms.validators import ValidationError, DataRequired
from app.models import User, Domain


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    clientnet_user = StringField('ClientNet Username',
                                 validators=[DataRequired()])
    clientnet_password = PasswordField('ClientNet Password',
                                       validators=[DataRequired()])
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
        domain = Domain.query.filter_by(domainname=self.domainname.data,
                                        user_id=current_user.id).first()
        if domain is not None:
            raise ValidationError('Domainname already in use')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class IOCForm(FlaskForm):
    iocBlackListId = HiddenField()
    domain = SelectField('Domain', default='global',
                         validators=[DataRequired()])
    iocType = SelectField('Type',
                          choices=[('attachmentname', 'Attachment name'),
                                   ('md5attachment', 'Attachment MD5'),
                                   ('sha2attachment', 'Attachment SHA2'),
                                   ('bodysenderdomain', 'Body Sender Domain'),
                                   ('bodysenderemail', 'Body Sender Email'),
                                   ('bodysendertopleveldomain',
                                    'Body Sender TLD'),
                                   ('envelopesenderdomain',
                                    'Envelope sender domain'),
                                   ('envelopesenderemail',
                                    'Envelope sender email '),
                                   ('envelopesendertopleveldomain',
                                    'Envelope sender TLD'),
                                   ('senderipaddress', 'Sender IP Address'),
                                   ('senderiprange', 'Sender IP Range'),
                                   ('recipientdomain', 'Recipient Domain'),
                                   ('recipientemail', 'Recipient Email'),
                                   ('subject', 'Subject'),
                                   ('url', 'URL')
                                   ],
                          default='subject',
                          validators=[DataRequired()])
    iocValue = StringField('Value', validators=[DataRequired()],
                           render_kw={"placeholder": "IOC Value"})
    description = StringField('Description', validators=[DataRequired()],
                              render_kw={"placeholder": "Description"})
    emailDirection = SelectField('Email direction',
                                 choices=[('I', 'Inbound'),
                                          ('O', 'Outbound'),
                                          ('B', 'Both')],
                                 default='B',
                                 validators=[DataRequired()])
    remediationAction = SelectField('Remediation action',
                                    choices=[('B', 'Block and Delete'),
                                             ('Q', 'Quarantine'),
                                             ('M', 'Redirect'),
                                             ('T', 'Tag subject'),
                                             ('H', 'Append header')],
                                    default='B', validators=[DataRequired()])
    submit = SubmitField('Add')

    def __init__(self, *args, **kwargs):
        super(IOCForm, self).__init__(*args, **kwargs)
        d = [('global', 'Global')]
        for domain in current_user.domains:
            d.append((domain.domainname, domain.domainname))
        self.domain.choices = d


class BulkIOCForm(FlaskForm):
    domain = SelectField('Domain', default='global',
                         validators=[DataRequired()])
    action = SelectField('Action',
                         choices=[('MERGE', 'Merge'),
                                  ('REPLACE', 'Replace'),
                                  ('IOC', 'Individual IOC\'s')],
                         default='merge', validators=[DataRequired()])
    fileType = RadioField('Filetype',
                          choices=[
                              ('csv', 'Comma Seperated Value (CSV)'),
                              ('json', 'JavaScript Object Notation (JSON)')],
                          validators=[DataRequired()], default='csv')
    iocFile = FileField('IOC file', validators=[FileRequired()])
    submit = SubmitField('Upload')

    def __init__(self, *args, **kwargs):
        super(BulkIOCForm, self).__init__(*args, **kwargs)
        d = [('global', 'Global')]
        for domain in current_user.domains:
            d.append((domain.domainname, domain.domainname))
        self.domain.choices = d
