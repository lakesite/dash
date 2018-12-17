import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required
import flask_admin as admin

from dash import models as model
from dash.forms import (ProjectForm)

bp = Blueprint('project', __name__, url_prefix='/project', template_folder="templates/project")


@bp.route('/index', methods=('GET', 'POST'))
@login_required
def project_list():
    projects = model.Project.query.all()

    return render_template('project/list.html', projects=projects)


@bp.route('/<int:id>', methods=('GET', 'POST'))
@login_required
def edit_project(id):
    query = model.db.session.query(model.Project).filter(
        model.Project.id == id
    )
    project = query.first()

    if project:
        form = ProjectForm(formdata=request.form, obj=project)

        if request.method == 'POST' and form.validate():
            project.save_changes(form)
            return redirect(url_for('.edit_project', id=id))

        return render_template('project/single.html', form=form)

    else:
        return 'Error loading #{id}'.format(id=id)
