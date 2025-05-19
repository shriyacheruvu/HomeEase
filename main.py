from flask import Flask, render_template,url_for 
from flask_sqlalchemy import SQLAlchemy
from applications.config import Config
from applications.database import db
from applications.models import User, Role, UserRole


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

        admin = Role.query.filter_by(name='admin').first()
        if not admin:
            admin = Role(name = 'admin')
            db.session.add(admin)

        servicer = Role.query.filter_by(name='servicer').first()
        if not servicer:
            servicer = Role(name = 'servicer')
            db.session.add(servicer)

        customer = Role.query.filter_by(name='customer').first()
        if not customer:
            customer = Role(name = 'customer')
            db.session.add(customer)

        admin_user = User.query.filter_by(email='admin@homeease.com').first()
        if not admin_user:
            admin_user = User(name='me',
                               email='admin@homeease.com',
                              password='admin',
                              address='admin address',
                              state='telangana',
                              pincode='500072',
                              phone='1234567890',
                              roles = [admin])
            db.session.add(admin_user)
        
        db.session.commit()
        
    return app

app = create_app()
from applications.routes import *

if __name__ == '__main__':
    app.run(debug=True)
