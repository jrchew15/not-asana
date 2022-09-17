## Get all tasks of current user
from app.forms.task_form import TaskForm
from ..models.models import db, Workspace, Project, Task
from ..models import db
from flask import Blueprint, redirect
from flask_login import login_required, current_user

task_routes = Blueprint('task', __name__, url_prefix='/api/tasks')

@task_routes.route('')
def get_all_tasks():
    tasks = Task.query.all()
    response = [task.to_dict() for task in tasks]
    return {"tasks": response}

@task_routes.route('/<int:id>')
@login_required
def edit_task(id):
    task = Task.query.get(id)
    if task is None:
        return {"message":"Task couldn't be found", "statusCode":404}

    form = TaskForm()
    if form.validate_on_submit():
        data = form.data

        task.user_id = data["userId"]
        task.project_id=data['projectId']
        task.name=data['name']
        task.due_date=data['dueDate']
        task.description=data['description']

        db.session.commit()
        return task.to_dict()

    return {"message":"Bad Data", "statusCode": 400}

@task_routes.route('/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.get(id)
    if task is None:
        return {"message":"Task couldn't be found", "statusCode":404}

    if task.user_id is not current_user.id:
        return {"message":"Unauthorized", "statusCode": 304}

    db.session.delete(task)
    db.session.commit()
    return {
            "message": "Successfully deleted",
             "statusCode": 200
        }
