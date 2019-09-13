import datetime
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required, current_user
import flask_admin as admin
from sqlalchemy.exc import IntegrityError

from dash import models as model
from dash.forms import (CompanyForm, ProjectForm, UserRequestForm)

user_bp = Blueprint('user_bp', __name__, url_prefix='/user', template_folder="templates/user")
project_bp = Blueprint('project_bp', __name__, url_prefix='/project', template_folder="templates/project")
company_bp = Blueprint('company_bp', __name__, url_prefix='/company', template_folder="templates/company")
request_bp = Blueprint('request_bp', __name__, url_prefix='/request', template_folder="templates/request")


@user_bp.route('/index', methods=('GET', 'POST'))
@login_required
def user_profile():

    return render_template('user/index.html')


@request_bp.route('/index', methods=('GET', 'POST'))
@login_required
def index_request():
    requests = model.UserRequest.query.filter_by(user_id=current_user.id).all()
    return render_template('request/index.html', requests=requests)


@request_bp.route('/view/<int:id>', methods=('GET', 'POST'))
@login_required
def view_request(id):
    request = model.UserRequest.query.filter_by(id=id).first()
    return render_template('request/view.html', request=request)


@request_bp.route('/add', methods=('GET', 'POST'))
@login_required
def add_request():
    user_request = model.UserRequest()
    form = UserRequestForm(obj=user_request)
    if request.method == 'POST':
        if form.validate():
            form.populate_obj(request)
            user_request.date = datetime.datetime.now()
            user_request.user_id = current_user.id
            user_request.status = 0
            model.db.session.add(user_request)
            model.db.session.commit()

            flash('Request created.')
            return redirect(url_for("request_bp.index"))

    return render_template('request/add.html', form=form)


@company_bp.route('/index')
@login_required
def index_company():
    company = model.Company.query.filter_by(id=current_user.company_id).first()
    service_agreements = model.ServiceAgreement.query.filter_by(company_id=current_user.company_id).all()
    return render_template('company/index.html', company=company, service_agreements=service_agreements)


@company_bp.route('/add', methods=('GET', 'POST'))
@login_required
def add_company():
    company = model.Company()
    form = CompanyForm(obj=company)
    if request.method == 'POST':
        if form.validate():
            form.populate_obj(company)
            model.db.session.add(company)
            try:
                model.db.session.commit()
            except IntegrityError as err:
                model.db.session.rollback()
                if "Duplicate entry" in str(err):
                    # Generate request
                    flash('Company already exists.')
                    return redirect(url_for("index"))

            flash('Company created successfully.')
            return redirect(url_for("company_bp.index"))

    return render_template('company/add.html', form=form)


@project_bp.route('/index', methods=('GET', 'POST'))
@login_required
def index_project():
    projects = model.Project.query.filter_by(company_id=current_user.company_id).all()
    return render_template('project/list.html', projects=projects)


@project_bp.route('/<int:id>', methods=('GET', 'POST'))
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
