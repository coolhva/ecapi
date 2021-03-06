"""Email.Cloud IOC Management

This application allows you to manage the Indicator of Compromise feature of
Email.Cloud through a webapplication. Register a user, enter API credentials,
log in and you are ready to start the app.

Author: henk.vanachterberg@broadcom.com
"""
from app import create_app, db
from app.models import User

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
