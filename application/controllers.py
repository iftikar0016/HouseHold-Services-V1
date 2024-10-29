from flask import Flask, render_template, redirect, request, url_for
from flask import current_app as app
from datetime import datetime
from .models import * 


@app.route('/userlogin', methods=['GET','POST'])
def user_login():
    if request.method=='POST':
        email = request.form.get("email")
        pas = request.form.get("password")
        this_user = User.query.filter_by(email = email).first() # or .all()
        if this_user:
            if this_user.password == pas:
                if this_user.role == "admin":
                    return redirect('/admin')
                else:
                    return redirect(f'/user/{this_user.id}') 
            else:
                return "incorrect Password"
        else:
            return "user does not exist!"
    return render_template('login.html')

@app.route('/prof_login', methods=['GET','POST'])
def prof_login():
    if request.method=='POST':
        email = request.form.get("email")
        pas = request.form.get("password")
        this_user = Professional.query.filter_by(email = email).first() # or .all()
        if this_user:
            if this_user.password == pas:
                return redirect(f'/professional/{this_user.id}') 
            else:
                return "incorrect Password"
        else:
            return "user does not exist!"
    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def customer_reg():
    if request.method == 'POST':
        email = request.form.get("email")
        pwd = request.form.get("password")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        fullname=request.form.get("fullname")
        this_user = User.query.filter_by(email = email).first()
        if this_user:
            return "user already exists with this email!"
        else:
            new_user = User(email = email, password = pwd, address=address, pincode=pincode, fullname= fullname)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/userlogin')

    return render_template('customer-reg.html')


@app.route('/prof_register', methods=['GET','POST'])
def professional_reg():
    service=Service.query.all()
    if request.method == 'POST':
        email = request.form.get("email")
        pwd = request.form.get("password")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        fullname=request.form.get("fullname")
        service=request.form.get("service")
        this_user = Professional.query.filter_by(email = email).first()
        if this_user:
            return "user already exists with this email!"
        else:
            new_user = Professional(email = email, password = pwd, address=address, pincode=pincode, fullname= fullname, service_id=service)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/userlogin')

    return render_template('professional-reg.html', service=service)



@app.route('/admin', methods=['GET','POST'])
def admin():
    admin=User.query.filter_by(role="admin").first()
    professionals = Professional.query.all()
    services = Service.query.all()
    service_request= ServiceRequest.query.all()
    return render_template('a_dash.html', professionals= professionals, services= services, service_request=service_request)

@app.route('/user/<int:id>', methods=['GET','POST'])
def user(id):
   user=User.query.get(id)
   services=Service.query.all()
   service_request=ServiceRequest.query.filter_by(customer_id=id)
   return render_template('c_dash.html',user=user, services=services, service_request=service_request)


@app.route('/professional/<int:id>', methods=['GET','POST'])
def professional(id):
   user=Professional.query.get(id)
   services=ServiceRequest.query.filter_by(professional_id=id)
   return render_template('p_dash.html',user=user, services=services)


@app.route('/add_service', methods=['GET','POST'])
def addService():
    if request.method=="POST":
        ServiceName= request.form.get('service_name')
        BasePrice = request.form.get('base_price')
        description = request.form.get('description')
        new_service = Service( name= ServiceName , price= BasePrice, description=description )
        db.session.add(new_service)
        db.session.commit()
        return redirect('/admin')
    return render_template('AddService.html')

@app.route('/editservice/<int:id>', methods=['GET','POST'])
def editService(id):
    service=Service.query.filter_by(id=id).first()
    if request.method=="POST":
        ServiceName= request.form.get('service_name')
        BasePrice = request.form.get('base_price')
        description = request.form.get('description')
        if description !='':
            service.description= description
        if ServiceName != '':
            service.name = ServiceName
        if BasePrice != '':
            service.price= BasePrice
        db.session.commit()
        return redirect('/admin')

    return render_template('EditService.html',service=service)

@app.route('/service/<int:id>/<int:user_id>', methods=['GET','POST'])
def service(id, user_id):
    service=Service.query.filter_by(id=id).first()
    professionals=Professional.query.filter_by(service_id=id).all()
    user=User.query.get(user_id)
    return render_template('service.html', service=service, professionals=professionals, user=user)



@app.route('/service_request/<int:user_id>/<int:professional_id>', methods=['GET'])
def service_request(user_id, professional_id):
    # ServiceRequest=ServiceRequest.query.filter_by(id=id).first()
    professional=Professional.query.get(professional_id)
    user=User.query.get(user_id)
    new_service_request = ServiceRequest( service_id=professional.service_id, customer_id=user.id, professional_id=professional.id )
    db.session.add(new_service_request)
    db.session.commit()
    return redirect(url_for('user', id=user_id))