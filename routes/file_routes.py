import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from util.db import db, File

file_routes = Blueprint('file_routes', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@file_routes.route('/files')
@login_required
def files():
    user_files = File.query.filter_by(user_id=current_user.id).all()
    print(f"Found {len(user_files)} files for user {current_user.id}")
    return render_template('files.html', files=user_files)

@file_routes.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('file_routes.files'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('file_routes.files'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + '_' + filename

        # Ensure the upload folder exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file.save(os.path.join(upload_folder, unique_filename))

        new_file = File(
            filename=filename,
            unique_filename=unique_filename,
            user_id=current_user.id
        )
        db.session.add(new_file)
        db.session.commit()
        flash('File successfully uploaded', 'success')
        return redirect(url_for('file_routes.files'))
    else:
        flash('File type not allowed', 'danger')
        return redirect(url_for('file_routes.files'))

@file_routes.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    file_to_download = File.query.get_or_404(file_id)
    if file_to_download.user_id != current_user.id:
        flash('You do not have permission to download this file.', 'danger')
        return redirect(url_for('file_routes.files'))

    upload_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, file_to_download.unique_filename, as_attachment=True)

@file_routes.route('/delete_file/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    file_to_delete = File.query.get_or_404(file_id)
    if file_to_delete.user_id != current_user.id:
        flash('You do not have permission to delete this file.', 'danger')
        return redirect(url_for('file_routes.files'))

    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.remove(os.path.join(upload_folder, file_to_delete.unique_filename))

    db.session.delete(file_to_delete)
    db.session.commit()
    flash('File successfully deleted', 'success')
    return redirect(url_for('file_routes.files'))
