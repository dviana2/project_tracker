from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
import re
from flask_app import app
from flask_app.models.user import User
from flask_app.models.project import Project
from flask_app.models.progress import Progress
bcrypt = Bcrypt(app)

#New Progress Entry
@app.route('/new/progress')
def new_progress_entry():
    return render_template('progress_create.html')

#Create Progress Entry
@app.route ('/create/progress', methods= ['POST'])
def create_entry():
    if 'user_id' not in session:
        return redirect ('/')

    form_data = {
        'date_created': request.form ['date_created'],
        'logged_progress': request.form ['logged_progress'],
        'project_id': session ['project_id']
    }
    project_id = session ['project_id']
    Progress.save_progress(form_data)
    return redirect (f'/project/{project_id}')

#Update Progress Entry
@app.route('/update/progress/<int:progress_id>')
def update_progress(progress_id):
    data = {
        "id":progress_id
    }
    progress=Progress.get_one_progress_entry(data)
    return render_template('progress_update.html', progress=progress)

#Process Update of Progress Entry
@app.route('/process/progress/<int:progress_id>', methods=["POST"])
def process_progress_update(progress_id):
    # if not Progress.validate_progress(request.form):
    #     return redirect (f'/update/progress/{progress_id}')

    data = {
        "id": progress_id,
        "date_created": request.form['date_created'],
        "logged_progress": request.form ['logged_progress'],
        'project_id': session ['project_id']
    }
    project_id = session ['project_id']
    Progress.update_progress_entry(data)
    return redirect (f'/project/{project_id}')

#Destroy Progress Entry
@app.route('/destroy/progress/<int:progress_id>')
def destroy(progress_id):
    data = {
        "id": progress_id,
        'project_id': session ['project_id']
    }
    project_id = session ['project_id']
    Progress.destroy_progress_entry(data)
    return redirect(f'/project/{project_id}')

