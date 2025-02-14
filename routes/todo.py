from flask import Blueprint, render_template, request, redirect, url_for, session
from flask.helpers import flash
from util.functions import tcolor,timetaken
from flask_login import login_required,login_user,current_user
from util.db import db, Todo , User
from forms import RegisterForm,LoginForm

todo = Blueprint('todo', __name__)
try:
    @todo.route('/dashboard',methods=['POST','GET'])
    @login_required 
    @timetaken
    def dashboard():
        data = Todo.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboard.html', todo=data)

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

    @todo.route('/logout')
    @login_required
    def logout():
        session.clear()
        return redirect(url_for('login'))
except Exception as e:
    print(f'{tcolor.RED}Error inside todo routes: {e}{tcolor.RESET}')