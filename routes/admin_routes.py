from flask import Blueprint, abort, render_template,request,session,flash,redirect,url_for
from util.db import db, Todo,Webpage,ActivityLog
from util.db import User as UserInfo


from datetime import datetime
from sqlalchemy.exc import IntegrityError
import os

admin_routes = Blueprint('admin_routes', __name__)


#variables
COOKIES_FILE_PATH = 'parts/cookies.txt'


#functions for activity logs 

def log_activity(action):
    user_email = session.get('email', 'Unknown')
    activity = ActivityLog(user_email=user_email, action=action)
    db.session.add(activity)
    db.session.commit()

@admin_routes.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'email' in session and 'role' in session:
        if session.get('role') != 'user': 
            return redirect('/admin_dashboard')
        else: 
            flash('Access denied. You do not have admin privileges.', 'error')
            return redirect('/')
    
    # Handle POST method for login form submission
    if request.method == 'POST':
        adminemail = request.form.get('email') 
        adminpass = request.form.get('password')
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        if adminemail and adminpass:
            admin = UserInfo.query.filter_by(email=adminemail).first()
            if admin and admin.password == adminpass:
                # Store user details in session
                session['email'] = admin.email
                session['name'] = admin.name
                session['role'] = admin.role
                if admin.role != 'user':
                    # log_activity(f'{admin.email} logged in as {admin.role}' )
                    return redirect('/admin_dashboard')
                else:
                    # log_activity(f'{admin.email} tried to login {admin.role}' )
                    flash('You do not have admin privileges.', 'error')
                    return redirect('/')
            else:
                flash('Invalid login credentials. Please try again.', 'error')
                # error = 'Invalid login credentials. Please try again.'
        else:
            # error = 'Enter both email and password to login.'
         return render_template('admin/login.html')

    # Render login page for GET request
    return render_template('admin/login.html')



@admin_routes.route('/admin_dashboard')
def admin_dashboard():
    # Check if user is an admin or editor, restrict access otherwise
    if session.get('role') in ['admin', 'editor', 'viewer']:
        role=session.get('role')
        recent_activities = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(10).all()
        return render_template('admin/admin_dashboard.html',role=role,recent_activities=recent_activities)
    else:
        flash('You are not authorized to access this page.', 'error')
        return redirect('/admin')


@admin_routes.route('/admin/records')
# @login_required  # This decorator ensures only logged-in users can access this route
def show_records():
  if session.get('role') in ['admin', 'editor','viewer']:  # Additional check for admin access
    records = UserInfo.query.all()  # Fetch all user records
    user = UserInfo.query.filter_by(email=session.get('email')).first()
    # log_activity(f'{session.get('email')} viewed records' )
    return render_template("admin/records.html", records=records , user=user)
  return redirect('/admin')  # Redirect to admin login if not admin

@admin_routes.route('/admin/delete/<int:sno>')
def delete(sno):
    if session.get('role') in ['admin', 'editor']:
        user = UserInfo.query.get(sno)
        db.session.delete(user)
        db.session.commit()
        # log_activity(f'{session.get('email')} deleted {user.email}' )
        flash('User deleted successfully!', 'success')
        return redirect('/admin/records')
    
@admin_routes.route('/admin/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if session.get('role') in ['admin', 'editor']:
        if request.method == 'POST':
            user = UserInfo.query.get(sno)
            user.name = request.form['name']
            user.email = request.form['email']
            user.password = request.form['password']
            db.session.commit()
            # log_activity(f'{session.get('email')} updated {user.email}' )
            flash('User updated successfully!', 'success')
            return redirect('/admin/records')
        user = UserInfo.query.get(sno)
        return render_template('admin/updatedb.html', user=user)

@admin_routes.route('/admin/add', methods=['GET', 'POST'])
def add_user():
    if session.get('role') in ['admin', 'editor']:
      if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        date_created = datetime.now()

        # Check if any required field is missing
        if not name or not email or not password:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('show_records'))

        # Create a new UserInfo object
        new_user = UserInfo(name=name, email=email, password=password, role=role)

        try:
            # Add the user to the database
            db.session.add(new_user)
            db.session.commit()
            # log_activity(f'{session.get('email')} added {email}' )
            flash('User added successfully!', 'success')
            return redirect(url_for('show_records'))
        except IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                flash(f"Error: Email '{email}' is already registered.", 'error')
            else:
                flash('Error adding user. Please try again.', 'error')
            db.session.rollback()  # Rollback in case of an error
           
            return redirect(url_for('show_records'))

    # Render the form if the request method is GET
    return render_template('admin/add_user.html')

@admin_routes.route('/logout_admin')
def logout():
    # log_activity(f'{session.get('email')} logged out' )
    session.pop('email', None)
    return redirect('/admin')

@admin_routes.route('/admin/update_cookies', methods=['GET', 'POST'])
def update_cookies():
    # Check if the user is an admin (adjust logic based on your app's auth system)
    if not session.get('role') in ['admin', 'editor']:
        return abort(403)  # Forbidden

    if request.method == 'POST':
        # Check if a file is uploaded
        if 'cookies_file' not in request.files or request.files['cookies_file'].filename == '':
            flash("No file selected!", "error")
            return redirect(url_for('admin_routes.update_cookies'))

        file = request.files['cookies_file']

        # Remove the old cookies file if it exists
        if os.path.exists(COOKIES_FILE_PATH):
            os.remove(COOKIES_FILE_PATH)

        # Save the new cookies file
        file.save(COOKIES_FILE_PATH)
        # log_activity(f'{session.get('email')} updated cookies' )
        flash("Cookies updated successfully!", "success")
        return redirect(url_for('admin_routes.update_cookies'))

    return render_template('admin/update_cookies.html')

@admin_routes.route("/admin/edit/<slug>", methods=["GET","POST"])
def admin_page(slug):
    page = Webpage.query.filter_by(slug=slug).first_or_404()
    if request.method == "POST":
        title = request.form.get("title")
        page.title = title
        db.session.commit()
        flash("Page updated successfully!", "success")
        return render_template('admin/pages/content.html', page=page)

    return render_template('admin/pages/content.html',page=page)

@admin_routes.route("/admin/edit", methods=["GET"])
def admin_edit():
    pages = Webpage.query.all()
    return render_template('admin/pages/edit.html', pages=pages)

@admin_routes.route("/admin/webpage/add", methods=["GET","POST"])
def admin_webpage():
    if request.method == "POST":
        title = request.form.get("title")
        slug = request.form.get("slug")
        content = request.form.get("content")
        page = Webpage(title=title,slug=slug,content=content)
        try:
            db.session.add(page)
            db.session.commit()
            flash("Page added successfully!", "success")
            return redirect(url_for('admin_routes.admin_edit'))
        except:
            flash("Error adding page. Please try again.", "error")
            db.session.rollback()
            return redirect(url_for('admin_routes.admin_webpage'))
    return render_template('admin/pages/add_pages.html')