import os
import pandas as pd
import random 
from flask import flash, request, redirect, url_for, render_template
from flaskproject.forms import RegistrationForm, LoginForm
from flaskproject.models import User
from flaskproject import app,db, bcrypt
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask_login import login_user, current_user, logout_user, login_required



####################################################################
products_prob = pd.read_csv("./products_prob.csv")

def recommend(prod, n):
    #Now lets select a hypothetical basket of goods (one or more products) that a customer has already purchased or
    #shown an interest for by clicking on an add or something, and then suggest him relative ones
    #basket = ['HOME BUILDING BLOCK WORD']
    basket=prod
    #Also select the number of relevant items to suggest
    no_of_suggestions = n
    all_of_basket = products_prob[basket]
    all_of_basket = all_of_basket.sort_values( ascending=False)
    suggestions_to_customer = list(all_of_basket.index[:no_of_suggestions])
    #print(products_prob)
    #print(all_of_basket)
    print('You may also consider buying:', suggestions_to_customer)
    output=[]
    for i in suggestions_to_customer:
        output.append(products_prob.loc[i,'Unnamed: 0'])
    return (output)
####################################################################

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/index', methods=['GET', 'POST'])
def home():
    return render_template("./index.html")
    
@app.route('/product/<product>', methods=['GET', 'POST'])
def predict(product):
     l=recommend(product, 10)
     s = set()
     while(len(s)!=5):
        s.add(random.randrange(0,10,1))
        
     d = [l[i] for i in s]
     return '#'.join(d)



@app.route('/about')
@app.route('/index/about')
def about():
    return render_template("./about.html")
    
@app.route('/register',methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template("./register.html",title="register",form = form)


@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("./login.html",title="login",form = form)


@app.route('/logout')
@app.route('/index/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

