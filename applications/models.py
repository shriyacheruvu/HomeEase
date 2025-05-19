from applications.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Integer, nullable=True)
    
    servicer = db.relationship('Servicer',backref='user_servicer',lazy=True)
    customer = db.relationship('Customer', backref='user_customer',lazy=True)
    roles = db.relationship('Role', secondary='user_role')

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
     
class Servicer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    doc_path = db.Column(db.String(300), nullable=False)       
    ver_doc = db.Column(db.String(25), default=False, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
     
    service =db.relationship('Service', lazy=True)
    
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    description = db.Column(db.String(100), nullable = True)
    base_price=db.Column(db.Integer,nullable=False)

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    servicer_id = db.Column(db.Integer, db.ForeignKey('servicer.id'), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    request_date = db.Column(db.DateTime, nullable=False)
    completion_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False)
       
    service = db.relationship('Service', lazy=True)
    servicer = db.relationship('Servicer', lazy=True )
    customer = db.relationship('Customer', lazy=True)

class NewServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    new_service_name = db.Column(db.String(80), nullable=False)
    new_service_description = db.Column(db.String(255), nullable=True)
    request_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)  

    customer = db.relationship('Customer', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    servicer_id = db.Column(db.Integer, db.ForeignKey('servicer.id'), nullable=False)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(100), nullable=True)  

    customer = db.relationship('Customer', lazy=True)
    servicer = db.relationship('Servicer', lazy=True )


    



