from .database import db

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'))
    date_of_request = db.Column(db.String())
    date_of_completion = db.Column(db.DateTime)
    status = db.Column(db.String(25), default="requested")
    remarks = db.Column(db.String(250))

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(), nullable=False )
    password= db.Column(db.String(), nullable=False)
    role=db.Column(db.String(30), nullable=False, default="customer")
    fullname= db.Column(db.String(80))
    address= db.Column(db.String(200))
    pincode=db.Column(db.Integer)

class Professional(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(), nullable=False )
    password= db.Column(db.String(), nullable=False)
    role=db.Column(db.String(30), nullable=False, default="professional")
    fullname= db.Column(db.String(80))
    address= db.Column(db.String(200))
    pincode=db.Column(db.Integer)
    phone_no=db.Column(db.Integer)
    
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(250))
    time_required = db.Column(db.Integer)


db.create_all()