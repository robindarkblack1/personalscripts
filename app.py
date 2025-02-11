from flask import Flask,redirect,url_for,render_template,request,flash,session
from db import db, Todo , User
from config import config
from forms import RegisterForm,LoginForm
from flask_login import login_required,LoginManager,login_user,current_user
from datetime import datetime
import pytz,requests
app = Flask(__name__)

app.config.from_object(config)
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).strftime('%I:%M %p').lstrip("0")
    formatted_date = datetime.now(ist).strftime('%a, %b %d %p')

    api_key = 'cea78d1d78e04732a47112844250902'  # Your WeatherAPI key
    location = 'Panipat,Haryana'
    api_url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=no'

    try:
        response = requests.get(api_url)
        weather_data = response.json()
        temperature_c = weather_data['current']['temp_c']
    except Exception as e:
        temperature_c = 'N/A'
        print(f"Error fetching weather data: {e}")

    return render_template('home.html',time=current_time,hometime=formatted_date,temp=temperature_c)

@app.route('/dashboard',methods=['POST','GET'])
@login_required
def dashboard():
    data = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', todo=data)

def add_task(tit,desc):
    new_task =Todo(title=tit,description=desc,user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()

@app.route('/submit',methods=['POST'])
def submit():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('description')
        add_task(title,desc)
        flash('Entry sucessfully','success')
        return redirect(url_for("dashboard"))

@app.route('/delete/<int:id>', methods=['POST','GET'])
def delete(id):
    us = Todo.query.get_or_404(id)
    db.session.delete(us)
    db.session.commit()
    flash('Delete sucessfully','success')
    return redirect(url_for("dashboard"))

@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    if request.method == "POST":
     record = Todo.query.get_or_404(id)
     record.title = request.form.get('title')
     record.description = request.form.get('description')
     db.session.commit()
     flash('Update sucessfully','success')
     return redirect(url_for("dashboard"))
     
    record = Todo.query.get_or_404(id)
    return render_template('update.html',record=record)

@app.route('/signup',methods=['POST','GET'])
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
        return redirect(url_for('login'))
    return render_template('signup.html',form=form)

@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            flash('Login sucessfully','success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password','danger')
            return redirect(url_for('login'))
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)