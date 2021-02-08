from datetime import datetime
import time
from flask import render_template, flash, redirect, url_for, request, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import DomainForm, EditProfileForm, EmptyForm
from app.models import User, Domain
from app.main import bp
from app.main import iocapi
from app.main.iocapi import IOC


@bp.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('favicon.ico')

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='Home')

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.clientnet_user = form.clientnet_user.data
        current_user.clientnet_password = form.clientnet_password.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.clientnet_user.data = current_user.clientnet_user
        form.clientnet_password.data = current_user.clientnet_password
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@bp.route('/domains', methods=['GET', 'POST'])
@login_required
def domains():
    form = DomainForm()
    if form.validate_on_submit():
        domain = Domain(domainname=form.domainname.data, user_id=current_user.id)
        db.session.add(domain)
        db.session.commit()
        flash('Domain has been added.')
        return redirect(url_for('main.domains'))
    return render_template('domains.html', title='Domains', form=form)
        
@bp.route('/domain/<domainname>/remove', methods=['GET'])
@login_required
def delete_domain(domainname):
    domain = Domain.query.filter_by(domainname=domainname, user_id = current_user.id).first_or_404()
    db.session.delete(domain)
    db.session.commit()
    flash('Domain has been removed.')
    return redirect(url_for('main.domains'))

@bp.route('/ioc')
@login_required
def ioc():
    return render_template('ioc.html', title='IOC')

@bp.route('/ioc/download/<domainname>', methods=['POST'])
@login_required
def ioc_download(domainname):
    if not domainname == 'global':
        domain = Domain.query.filter_by(domainname=domainname, user_id = current_user.id).first_or_404()
    ioc_result = iocapi.DownloadIOC(domainname)
    return jsonify({'html': ioc_result.html, 
                    'status_code': ioc_result.status_code, 
                    'error_message': ioc_result.error_message })

@bp.route('/ioc/delete', methods=['POST'])
@login_required
def ioc_delete():
    ioc = IOC(**request.json)
    ioc_result = iocapi.DeleteIOC(ioc)
    return jsonify({'html': ioc_result.html, 
                    'status_code': ioc_result.status_code, 
                    'error_message': ioc_result.error_message })