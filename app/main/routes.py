import json
from flask import (render_template, flash, redirect, url_for, request,
                   jsonify, current_app, abort)
from flask.helpers import make_response
from flask_login import current_user, login_required
from app import db
from app.main.forms import DomainForm, EditProfileForm, IOCForm, BulkIOCForm
from app.models import Domain
from app.main import bp
from app.main import iocapi
from app.main.iocapi import FileType, IOC


@bp.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('favicon.ico')


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
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
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.clientnet_user.data = current_user.clientnet_user
        form.clientnet_password.data = current_user.clientnet_password
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/domains', methods=['GET', 'POST'])
@login_required
def domains():
    form = DomainForm()
    if form.validate_on_submit():
        domain = Domain(domainname=form.domainname.data,
                        user_id=current_user.id)
        db.session.add(domain)
        db.session.commit()
        flash('Domain has been added.', 'success')
        return redirect(url_for('main.domains'))
    return render_template('domains.html', title='Domains', form=form)


@bp.route('/domain/<domainname>/remove', methods=['GET'])
@login_required
def delete_domain(domainname):
    domain = Domain.query.filter_by(domainname=domainname,
                                    user_id=current_user.id).first_or_404()
    db.session.delete(domain)
    db.session.commit()
    flash('Domain has been removed.', 'success')
    return redirect(url_for('main.domains'))


@bp.route('/ioc', methods=['GET', 'POST'])
@login_required
def ioc():
    form = IOCForm()
    if form.validate_on_submit():
        ioc = IOC(iocBlackListId=form.iocBlackListId.data,
                  iocDomain=form.domain.data,
                  iocType=form.iocType.data, iocValue=form.iocValue.data,
                  description=form.description.data,
                  emailDirection=form.emailDirection.data,
                  remediationAction=form.remediationAction.data)
        if (ioc.iocBlackListId):
            ioc_result = iocapi.UpdateIOC(ioc, 'U')
            if ioc_result.status_code == 200:
                flash('IOC has been updated.', 'success')
            else:
                flash('ERROR ' + str(ioc_result.status_code) + ': '
                      + ioc_result.error_message, 'danger')
                return render_template('ioc.html', title='IOC', form=form)
        else:
            ioc_result = iocapi.UpdateIOC(ioc, 'A')
            if ioc_result.status_code == 200:
                flash('IOC has been added.', 'success')
            else:
                flash('ERROR ' + str(ioc_result.status_code) + ': '
                      + ioc_result.error_message, 'danger')
                return render_template('ioc.html', title='IOC', form=form)
        return redirect(url_for('main.ioc'))
    return render_template('ioc.html', title='IOC', form=form)


@bp.route('/ioc/bulk', methods=['GET', 'POST'])
@login_required
def bulk_ioc():
    form = BulkIOCForm()
    if form.validate_on_submit():
        fileType = None
        iocs = None
        if form.fileType.data == 'csv':
            iocs = form.iocFile.data.stream.read()
            fileType = iocapi.FileType.csv
        if form.fileType.data == 'json':
            fileType = iocapi.FileType.json
            try:
                iocs = json.loads(form.iocFile.data.stream.read())
            except Exception:
                flash('Unable to parse JSON data', 'danger')
                return redirect(url_for('main.bulk_ioc'))
        ioc_result = iocapi.BulkUpdateIOC(form.domain.data, fileType, iocs,
                                          form.action.data)
        if ioc_result.status_code == 200:
            flash('Bulk upload successful.')
            return redirect(url_for('main.ioc'))
        return render_template('bulk_ioc.html', title='IOC Bulk upload',
                               ioc_result=ioc_result)
    return render_template('bulk_ioc.html', title='IOC Bulk upload', form=form)


@bp.route('/ioc/download/<domainname>', methods=['POST'])
@login_required
def ioc_download(domainname):
    if not domainname == 'global':
        Domain.query.filter_by(domainname=domainname,
                               user_id=current_user.id).first_or_404()
    ioc_result = iocapi.DownloadIOC(domainname)
    return jsonify({'html': ioc_result.html,
                    'status_code': ioc_result.status_code,
                    'error_message': ioc_result.error_message})


@bp.route('/ioc/export/<filetype>/<domainname>', methods=['GET'])
@login_required
def ioc_export(filetype, domainname):
    if filetype not in ['csv', 'json']:
        abort(404)

    if not domainname == 'global':
        Domain.query.filter_by(domainname=domainname,
                               user_id=current_user.id).first_or_404()

    if filetype == 'json':
        content = iocapi.ExportIOC(FileType.json, domainname)
        response = make_response(jsonify(content))
        response.headers['Content-Type'] = 'application/json'
        response.headers['Content-Disposition'] = 'attachment; filename=ioc_' \
                                                  + domainname + '.json'
        return response

    if filetype == 'csv':
        content = iocapi.ExportIOC(FileType.csv, domainname)
        response = make_response(content)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=ioc_' \
                                                  + domainname + '.csv'
        return response


@bp.route('/ioc/renew/<domainname>', methods=['GET'])
@login_required
def ioc_renew(domainname):
    if not domainname == 'global':
        Domain.query.filter_by(domainname=domainname,
                               user_id=current_user.id).first_or_404()

    if iocapi.RenewIOC(domainname):
        flash('IOC\'s have been renewed for ' + domainname + '.')
        return redirect(url_for('main.ioc'))
    else:
        flash('Error occured while renewing IOC\'s for ' + domainname + '.',
              'danger')
        return redirect(url_for('main.ioc'))


@bp.route('/ioc/delete', methods=['POST'])
@login_required
def ioc_delete():
    ioc = IOC(**request.json)
    ioc_result = iocapi.UpdateIOC(ioc, 'D')
    return jsonify({'html': ioc_result.html,
                    'status_code': ioc_result.status_code,
                    'error_message': ioc_result.error_message})
