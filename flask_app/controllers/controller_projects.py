from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
import re
from flask_app import app
from flask_app.models.user import User
from flask_app.models.project import Project
from flask_app.models.progress import Progress
bcrypt = Bcrypt(app)


#New Project
@app.route('/new/project')
def new_project():
    return render_template('project_create.html')

#Create Project
@app.route('/create/project', methods=['POST'])
def create_project():
    if 'user_id' not in session:
        return redirect ('/')

    if not Project.validate_project(request.form):
        return redirect ('/new/project')

    form_data = {
        'date_created': request.form['date_created'],
        'title': request.form['title'],
        'description': request.form['description'],
        'technologies_used': request.form['technologies_used'],
        'benefits': request.form ['benefits'],
        'status': request.form ['status'],
        'user_id': session['user_id'],
    }

    Project.save_project(form_data)
    return redirect('/dashboard')


#Display Project
@app.route('/project/<int:project_id>')
def display(project_id):
    data = {
        'id': project_id
    }
    project = Project.get_one_project(data)
    progress = Progress.get_all_progress_entries(data)
    user = User.get_one_user({'id':session['user_id']})
    session ['project_id'] = project_id
    print(project)
    print(progress)
    print(user)
    return render_template('project_display.html', project=project, progress=progress, user=user)








