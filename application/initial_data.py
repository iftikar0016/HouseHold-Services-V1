from flask import current_app as app
from application.models import db, Customer, Professional, Service
from flask_security import SQLAlchemyUserDatastore, hash_password

with app.app_context():
    db.create_all()

    userdatastore : SQLAlchemyUserDatastore = app.security.datastore
    first_service = Service( name= "Plumbing" , price= "100", description="First Service of this platform is Plumbing" )
    

    admin_role = userdatastore.find_or_create_role(name='admin', description='superuser')
    customer_role = userdatastore.find_or_create_role(name='customer', description='general customer')
    professional_role = userdatastore.find_or_create_role(name='professional', description='service professional')
    db.session.commit()

    # Create admin user
    if not userdatastore.find_user(email='admin@email'):
        user = userdatastore.create_user(email='admin@email', password=hash_password('pass'))
        userdatastore.add_role_to_user(user, admin_role)  # Added role separately
        db.session.commit()

    # Create customer user
    if not userdatastore.find_user(email='customer1@email'):
        user = userdatastore.create_user(email='customer1@email', password=hash_password('pass'))
        userdatastore.add_role_to_user(user, customer_role)  
        db.session.commit()
        
        # Create and add customer profile
        customer1 = Customer(user_id=user.id, fullname="customer1")
        db.session.add(customer1)
        db.session.commit()

    # Create professional user
    if not userdatastore.find_user(email='professional1@email'):
        user = userdatastore.create_user(email='professional1@email', password=hash_password('pass'))
        userdatastore.add_role_to_user(user, professional_role)
        db.session.add(first_service)  
        db.session.commit()
        
        # Create and add professional profile
        professional1 = Professional(user_id=user.id,fullname="professional1", service_id=first_service.id)
        db.session.add(professional1)
        db.session.commit()
    # db.session.commit()