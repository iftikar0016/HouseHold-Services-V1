from flask import Flask, render_template, redirect, request
from flask import current_app as app
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


@app.route('/user/<int:id>', methods=['GET','POST'])
def user(id):
   user=User.query.get(id)
   return render_template('c_dash.html',user=user)