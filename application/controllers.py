from flask import Flask, render_template, redirect, request, url_for, abort
from flask import current_app as app
from flask_security import auth_required, login_required, verify_password, hash_password, roles_required, current_user
from datetime import datetime
from .models import Customer, db, Professional, Service, ServiceRequest, User

datastore = app.security.datastore

@app.route('/logout')
def logout():
     return redirect(url_for('login'))
#     return render_template('ServiceRequest.html')


@app.route('/userlogin', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = datastore.find_user(email = email)
        # this_user = User.query.filter_by(email = email).first() # or .all()
        if user:
            if verify_password(password, user.password):
                if user.roles[0].name == "admin":
                    return redirect('/admin')
                elif user.roles[0].name == "professional":
                    # this_user = Professional.query.filter_by(email = email).first()
                    return redirect(f'/professional/{user.id}')
                else:
                    return redirect(f'/user/{user.id}') 
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
        this_user = datastore.find_user(email = email)
        if this_user:
            return "user already exists with this email!"
        else:
            user = datastore.create_user(email=email, password=hash_password(pwd))
            datastore.add_role_to_user(user, 'customer')  # Add role separately
            db.session.commit()
            new_user = Customer( user_id=user.id, address=address, pincode=pincode, fullname= fullname)
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
        user = datastore.find_user(email = email)
        if user:
            return "user already exists with this email!"
        else:
            user = datastore.create_user(email=email, password=hash_password(pwd), active= False)
            datastore.add_role_to_user(user, 'professional')  # Add role separately
            db.session.commit()
            new_user = Professional( user_id=user.id, address=address, pincode=pincode, fullname= fullname, service_id=service)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/userlogin')

    return render_template('professional-reg.html', service=service)



@app.route('/admin', methods=['GET','POST'])
# @auth_required("token")
# @roles_required("admin")
def admin():
    # admin=User.query.filter_by(role="admin").first()
    professionals = Professional.query.all()
    services = Service.query.all()
    service_request= ServiceRequest.query.all()
    return render_template('a_dash.html', professionals= professionals, services= services, service_request=service_request)

@app.route('/user/<int:id>', methods=['GET','POST'])
def customer(id):
   user=Customer.query.filter_by(user_id=id).first()
   services=Service.query.all()
   service_request=ServiceRequest.query.filter_by(customer_id=id)
   return render_template('c_dash.html',user=user, services=services, service_request=service_request)


@app.route('/professional/<int:id>', methods=['GET','POST'])
# @roles_required("professional")
def professional(id):
    user=Professional.query.filter_by(user_id=id).first()
    services=ServiceRequest.query.filter_by(professional_id=id)
    if user.user.is_blocked or not user.user.active:
        return abort(403)
    service_request=ServiceRequest.query.filter_by(professional_id=id)
    return render_template('p_dash.html',user=user, services=services, service_request=service_request)


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
    user=Customer.query.filter_by(user_id=user_id).first()
    return render_template('service.html', service=service, professionals=professionals, user=user)



@app.route('/service_request/<int:user_id>/<int:professional_id>', methods=['GET'])
def service_request(user_id, professional_id):
    # ServiceRequest=ServiceRequest.query.filter_by(id=id).first()
    professional=Professional.query.filter_by(user_id=professional_id).first()
    service=Service.query.get(professional.service_id)
    user=Customer.query.filter_by(user_id=user_id).first()
    new_service_request = ServiceRequest(service_name=service.name, customer_name=user.fullname, professional_name=professional.fullname ,service_id=professional.service_id, customer_id=user.user_id, professional_id=professional.user_id,date_of_request=datetime.now() )
    db.session.add(new_service_request)
    db.session.commit()
    return redirect(url_for('customer', id=user_id))


def raw(text): # text = ServiceRequest One
    split_list = text.split() #----> list ['ServiceRequest', 'One']
    src_word = ''
    for word in split_list:
        src_word += word.lower()
    return src_word

@app.route('/search_req/<id>')
def req_search(id):
    srch_word = request.args.get('result')
    srch_word = "%"+srch_word.title()+"%"
    srch_prof = "%"+srch_word.title()+"%"
    r_service_name = ServiceRequest.query.filter(ServiceRequest.customer_id==id,ServiceRequest.service_name.like(srch_word)).all()
    r_prof_name = ServiceRequest.query.filter(ServiceRequest.customer_id==id,ServiceRequest.professional_name.like(srch_prof)).all()
    search_results = r_service_name + r_prof_name
    return render_template('search_req.html', service_request=search_results, user_id=id)

@app.route('/search_service/<id>')
def service_search(id):
    srch_word = request.args.get('result')
    srch_word = "%"+srch_word.title()+"%"
    # srch_prof = "%"+srch_word.title()+"%"
    r_service_name = Service.query.filter(Service.name.like(srch_word)).all()
    # r_prof_name = ServiceRequest.query.filter(ServiceRequest.customer_id==id,ServiceRequest.professional_name.like(srch_prof)).all()
    search_results = r_service_name 
    return render_template('search_service.html', services=search_results, user_id=id)

@app.route('/search_professional')
def prof_search():
    srch_word = request.args.get('result')
    srch_word = "%"+srch_word.title()+"%"
    srch_prof = "%"+srch_word.title()+"%"
    r_prof_name = Professional.query.filter(Professional.fullname.like(srch_prof)).all()
    search_results = r_prof_name
    return render_template('search_professionals.html', professionals=search_results)

@app.route('/accept_req/<id>')
def accept_req(id):
    req= ServiceRequest.query.get(id)
    param = request.args.get('param')
    if param == 'Accept':
        req.status = "accepted"
        db.session.commit()
        return redirect(url_for('professional', id=req.professional_id))
    if param == 'Reject':
        req.status = "rejected"
        db.session.commit()
        return redirect(url_for('professional', id=req.professional_id))

    return render_template('accept_req.html', req_id=id)

@app.route('/user_action/<int:id>')
def user_action(id):
    user=User.query.get(id)
    param = request.args.get('param')
    if param == 'Approve':
        user.active = True
        db.session.commit()
        return redirect(url_for('admin'))
    if param == 'Block':
        user.is_blocked = True
        db.session.commit()
        return redirect(url_for('admin'))
    if param == 'Unblock':
        user.is_blocked = False
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('user_action.html', user=user)

@app.route('/service_remarks/<int:request_id>', methods=['GET', 'POST'])
def service_remarks(request_id):
    req= ServiceRequest.query.get(request_id)
    if request.method == 'POST':
        # rating_value = request.form.get('rating')
        # remarks = request.form.get('remarks')
        
        # # Assuming you have `Professional` and `ServiceRequest` models
        # professional_id = request.form.get('professional_id')  # ID passed as hidden input
        
        # # Save the rating and remarks in the Rating model
        # rating = Rating(rating=float(rating_value), professional_id=professional_id)
        # db.session.add(rating)
        
        # # Update average rating for professional
        # professional = Professional.query.get(professional_id)
        # ratings = [r.rating for r in professional.ratings]
        # professional.average_rating = sum(ratings) / len(ratings) if ratings else rating_value
        # db.session.commit()


        req.status = "closed"
        req.date_of_completion = datetime.now()
        db.session.commit()
        return redirect(url_for('customer', id=req.customer_id))  # Redirect to home or any other page

    # Render the template with pre-filled data for GET request
    
    return render_template('service_remarks.html', service_req= req)

@app.route('/profile/<int:id>', methods=['GET','POST'])
def profile(id):
    user=User.query.get(id)
    if request.method=="POST":
        email= request.form.get('email')
        password = request.form.get('password')
        
        if email !='':
            user.email= email
        if password != '':
            user.password= password

        if user.roles[0].name == "professional":
            pincode = request.form.get('pincode')
            if pincode != '':
                user.professional.pincode= pincode
            db.session.commit()
            return redirect(f'/professional/{user.id}')

        if user.roles[0].name == "customer":
            pincode = request.form.get('pincode')
            if pincode != '':
                user.customer.pincode= pincode
            db.session.commit()
            return redirect(f'/user/{user.id}') 

    return render_template('profile.html',user=user)

@app.route("/summary/<int:user_id>")
def graph(user_id):
    # Query the database for the given customer_id
    data = (
        db.session.query(ServiceRequest.status, db.func.count(ServiceRequest.id))
        .filter((ServiceRequest.customer_id == user_id) | (ServiceRequest.professional_id == user_id))  # Filter for either customer or professional
        .group_by(ServiceRequest.status)
        .all()
    )
    
    # Prepare data for the chart
    labels = [row[0] for row in data]  # Statuses (e.g., "requested", "completed")
    values = [row[1] for row in data]  # Count of requests for each status

    return render_template("summary.html", labels=labels, values=values)


@app.route("/summary")
def summery():
    # Query the database for the given customer_id
    data = (
        db.session.query(ServiceRequest.status, db.func.count(ServiceRequest.id))  
        .group_by(ServiceRequest.status)
        .all()
    )
    
    # Prepare data for the chart
    labels = [row[0] for row in data]  # Statuses (e.g., "requested", "completed")
    values = [row[1] for row in data]  # Count of requests for each status

    return render_template("summary.html", labels=labels, values=values)