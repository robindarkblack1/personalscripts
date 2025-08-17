import requests
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask.helpers import flash
from util.functions import tcolor,timetaken
from flask_login import login_required,login_user,current_user
from util.db import db, Todo , User , Webpage
from util.db import User as UserInfo
from util.forms import RegisterForm,LoginForm
from config import config
from util.auth import oauth
todo = Blueprint('todo', __name__)



def get_quote_of_the_day():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        response.raise_for_status()
        quote_data = response.json()[0]
        return f'"{quote_data["q"]}" - {quote_data["a"]}'
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quote: {e}")
        return "Could not fetch a quote at this time."

try:
    @todo.route('/dashboard',methods=['POST','GET'])
    @login_required 
    def dashboard():
        page = Webpage.query.filter_by(slug='dashboard').first()
        if not page:
            page = Webpage(title='Dashboard',slug='dashboard',content='This is the dashboard page')
            db.session.add(page)
            db.session.commit()
        data = Todo.query.filter_by(user_id=current_user.id).all()
        quote = get_quote_of_the_day()
        return render_template('dashboard.html', todo=data,page=page, quote=quote)

    def add_task(tit,desc):
        new_task =Todo(title=tit,description=desc,user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()

    @todo.route('/submit',methods=['POST'])
    def submit():
        if request.method == 'POST':
            title = request.form.get('title')
            desc = request.form.get('description')
            add_task(title,desc)
            flash('Entry sucessfully','success')
            return redirect(url_for("todo.dashboard"))

    @todo.route('/delete/<int:id>', methods=['POST','GET'])
    @login_required
    def delete(id):
        us = Todo.query.get_or_404(id)
        db.session.delete(us)
        db.session.commit()
        flash('Delete sucessfully','success')
        return redirect(url_for("todo.dashboard"))

    @todo.route("/update/<int:id>", methods=["GET","POST"])
    @login_required
    def update(id):
        if request.method == "POST":
            record = Todo.query.get_or_404(id)
            record.title = request.form.get('title')
            record.description = request.form.get('description')
            db.session.commit()
            flash('Update sucessfully','success')
            return redirect(url_for("todo.dashboard"))
        
        record = Todo.query.get_or_404(id)
        return render_template('update.html',record=record)

    @todo.route('/signup',methods=['POST','GET'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            name = form.username.data
            email = form.email.data
            password = form.password.data
            new_user = User(name=name,email=email,password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created sucessfully','success')
            return redirect(url_for('todo.login'))
        return render_template('signup.html',form=form)

    @todo.route('/login',methods=['POST','GET'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user and user.password == password:
                login_user(user)
                flash('Login sucessfully','success')
                return redirect(url_for('todo.dashboard'))
            else:
                flash('Invalid email or password','danger')
                return redirect(url_for('todo.login'))
        return render_template('login.html',form=form)


    @todo.route('/google_login')
    def glogin():
        redirect_uri = url_for('todo.google_authorize', _external=True)
        return oauth.google.authorize_redirect(redirect_uri)


    @todo.route('/google_authorize')
    def google_authorize():
        token = oauth.google.authorize_access_token()

        # ✅ Directly get the 'id_token'
        id_token = token.get('id_token')
        if not id_token:
            flash('Login failed: No ID token received.', 'danger')
            return redirect(url_for('todo.login'))

        try:
            # ✅ FIX: Pass 'nonce' from the token when parsing
            user_info = oauth.google.parse_id_token(token, nonce=token.get('nonce', ''))
        except Exception as e:
            flash(f'Login failed: {str(e)}', 'danger')
            return redirect(url_for('todo.login'))

        # ✅ Ensure user exists in DB
        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            user = User(name=user_info['name'], email=user_info['email'], password=None)
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash('Login successful!', 'success')
        return redirect(url_for('todo.dashboard'))

    @todo.route('/reset-password', methods=['GET', 'POST'])
    def reset_password():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            try:
             user = UserInfo.query.filter_by(email=email).first()
             user.password = password
             db.session.commit()
             flash('Password reset successfully!', 'success')
             return render_template('user/reset_password.html')  
            except Exception as e:
                flash('User Does Not Exist', 'danger')
                db.session.rollback()
                return redirect('/reset-password') 
        return render_template('user/reset_password.html')

    @todo.route('/logout')
    @login_required
    def logout():
        session.clear()
        return redirect(url_for('login'))
except Exception as e:
    print(f'{tcolor.RED}Error inside todo routes: {e}{tcolor.RESET}')