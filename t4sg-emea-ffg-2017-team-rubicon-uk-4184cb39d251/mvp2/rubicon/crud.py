# Copyright 2018 Rubicon UK
#
import io
import sys

import pandas as pd
from flask import Blueprint, current_app, redirect, render_template, request, \
    session, url_for, jsonify, make_response

from rubicon import get_model, oauth2, storage

crud = Blueprint('crud', __name__)


def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)
    return public_url


@crud.route("/")
def index():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    spolunteers, next_page_token = get_model().list(table="Spolunteer", cursor=token)

    return render_template(
        "index.html",
        spolunteers=spolunteers,
        next_page_token=next_page_token)


# [START profile]
@crud.route("/profile")
def profile():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    if 'profile' in session:
        spolunteers, next_page_token = get_model().list_by_user(
            table="Spolunteer",
            user_id=session['profile']['id'],
            cursor=token)

        return render_template(
            "profile.html",
            spolunteers=spolunteers,
            next_page_token=next_page_token)

    return render_template("profile.html")
# [END profile]

# [START reception]
@crud.route("/reception", methods=['GET'])
@oauth2.required
def reception():
    operation = request.args.get('operation')
    spolunteers = get_model().list_by_operation(
        table="Spolunteer",
        operation=operation)

    return render_template(
        "reception.html",
        spolunteers=spolunteers,
        operation=operation,
        request=request)
# [END reception]

# [START guidance]
@crud.route("/guidance")
@oauth2.required
def guidance():
    operation = request.args.get('operation')
    spolunteers = get_model().list_by_operation(
        table="Spolunteer",
        operation=operation)

    return render_template(
        "guidance.html",
        spolunteers=spolunteers,
        operation=operation,
        request=request)
# [END guidance]

# [START training]
@crud.route("/training")
@oauth2.required
def training():
    operation = request.args.get('operation')
    spolunteers = get_model().list_by_operation(
        table="Spolunteer",
        operation=operation)

    return render_template(
        "training.html",
        spolunteers=spolunteers,
        operation=operation,
        request=request)
# [END training]

# [START holding]
@crud.route("/holding")
@oauth2.required
def holding():
    operation = request.args.get('operation')
    spolunteers = get_model().list_by_operation(
        table="Spolunteer",
        operation=operation)

    return render_template(
        "holding.html",
        spolunteers=spolunteers,
        operation=operation,
        request=request)
# [END holding]

# [START status]
@crud.route("/status")
@oauth2.required
def status():
    operation = request.args.get('operation')
    spolunteers = get_model().list_by_operation(
        table="Spolunteer",
        operation=operation)

    return render_template(
        "status.html",
        spolunteers=spolunteers,
        operation=operation,
        request=request)
# [END status]

# [START admin]
@crud.route("/admin")
@oauth2.required
def admin():
    email = session['profile']['emails'][0]['value']
    if get_model().role(email) != 'admin':
        return 'Access Denied'
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    spolunteers, next_page_token = get_model().list(table="Spolunteer", cursor=token)
    interest, next_page_token = get_model().list(table="Interest", cursor=token)
    return render_template(
        "admin.html",
        spolunteers=spolunteers,
        interest=interest,
        next_page_token=next_page_token,
        request=request)
# [END admin]

# [START statistics]
@crud.route("/statistics")
@oauth2.required
def statistics():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    spolunteers, next_page_token = get_model().list(table='Spolunteer', cursor=token)

    return render_template(
        "statistics.html",
        spolunteers=spolunteers,
        next_page_token=next_page_token,
        request=request)
# [END statistics]

# [START list]
@crud.route("/list")
@oauth2.required
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    spolunteers, next_page_token = get_model().list(table='Spolunteer', cursor=token)

    return render_template(
        "list.html",
        spolunteers=spolunteers,
        next_page_token=next_page_token)
# [END list]

# [START add]
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If an image was uploaded, update the data to point to the new image.
#       image_url = upload_image_file(request.files.get('image'))

#        if image_url:
#            data['imageUrl'] = image_url

        # If the user is logged in, associate their profile with the new spolunteer.
        if 'profile' in session:
            data['createdBy'] = session['profile']['displayName']
            data['createdById'] = session['profile']['id']

        spolunteer = get_model().create(data)
        print('hello there', file=sys.stderr)
        return redirect(url_for('.index', id=spolunteer['id']))

    return render_template("form.html", action="Add", spolunteer={})
# [END add]

@crud.route('/user/<id>', methods=['GET', 'PATCH'])
def view(id):
    spolunteer = get_model().read(table='Spolunteer', id=id)
    if request.method == 'PATCH':
        data = request.form.to_dict(flat=True)
        for key, value in data.items():
            spolunteer[key]=value
            spolunteer = get_model().update('Spolunteer', spolunteer, id)

        return jsonify(spolunteer)
    #    return render_template("view.html", spolunteer=spolunteer)

    #return render_template("view.html", spolunteer=spolunteer)
    return jsonify(spolunteer)

@crud.route('/admin/add')
@oauth2.required
def adminadd():
    data = {}
    if 'profile' in session:
        data['createdBy'] = session['profile']['displayName']
        data['createdById'] = session['profile']['id']

    data['createdAt'] = 'now'
    data['firstname'] = ''
    spolunteer = get_model().create('Spolunteer', data)
    print(spolunteer, file=sys.stderr)
    #return render_template("admin.html", action="List", spolunteer={})
    return redirect(url_for('.admin'))

@crud.route('/admin/download')
@oauth2.required
def admin_download():
    spolunteers = get_model().download_as_csv(table='Spolunteer')
    si = io.StringIO()
    all_spolunteers = []
    for spolunteer in spolunteers:
        temp_dict = {}
        for item in spolunteer.keys():
            temp_dict[item] = spolunteer[item]
        all_spolunteers.append(temp_dict)
    df = pd.DataFrame(all_spolunteers)
    df.to_csv(si, index=False)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@crud.route('/admin/purge/<table>')
@oauth2.required
def admin_purge(table):
    entries, token = get_model().list(table)
    list_of_key_to_delete = []
    for entry in entries:
        list_of_key_to_delete.append(entry.key)
    get_model().delete_all(list_of_key_to_delete)
    return redirect(url_for('.admin'))

@crud.route('/reception/add')
@oauth2.required
def receptionadd():
    data = {}
    if 'profile' in session:
        data['createdBy'] = session['profile']['displayName']
        data['createdById'] = session['profile']['id']

    data['createdAt'] = 'now'
    data['firstname'] = ''
    spolunteer = get_model().create('Spolunteer', data)
    print(spolunteer, file=sys.stderr)
    return redirect(url_for('.reception'))

# [START register]
@crud.route('/register', methods=['GET', 'POST'])
def register():
    # get interests from the interest table
    interests, next_page_token = get_model().list(table="Interest")

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If an image was uploaded, update the data to point to the new image.
        image_url = upload_image_file(request.files.get('image'))

        if image_url:
            data['imageUrl'] = image_url

        # If the user is logged in, associate their profile with the new spolunteer.
        if 'profile' in session:
            data['createdBy'] = session['profile']['displayName']
            data['createdById'] = session['profile']['id']

        spolunteer = get_model().create('Spolunteer', data)
        print(spolunteer, file=sys.stderr)
        return redirect(url_for('.profile', id=spolunteer['id']))

    return render_template("register.html", action="Add", spolunteer={}, interests=interests)

# [END register]

# [START reception]
@crud.route('/reception2', methods=['GET', 'POST'])
@oauth2.required
def reception2():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If an image was uploaded, update the data to point to the new image.
        image_url = upload_image_file(request.files.get('image'))

        if image_url:
            data['imageUrl'] = image_url

        # If the user is logged in, associate their profile with the new spolunteer.
        if 'profile' in session:
            data['createdBy'] = session['profile']['displayName']
            data['createdById'] = session['profile']['id']

        spolunteer = get_model().create(data)

        return redirect(url_for('.list', id=spolunteer['id']))

    return render_template("reception.html", action="Add", spolunteer={})
# [END reception]

# [START interview]
@crud.route('/interview', methods=['GET', 'POST'])
@oauth2.required
def interview():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If an image was uploaded, update the data to point to the new image.
        image_url = upload_image_file(request.files.get('image'))

        if image_url:
            data['imageUrl'] = image_url

        # If the user is logged in, associate their profile with the new spolunteer.
        if 'profile' in session:
            data['createdBy'] = session['profile']['displayName']
            data['createdById'] = session['profile']['id']

        spolunteer = get_model().create('Spolunteer', data)

        return redirect(url_for('.list', id=spolunteer['id']))

    return render_template("interview.html", action="Add", spolunteer={})
# [END interview]

# [START interests]
@crud.route("/interests", methods=['GET'])
def getInterests():
    interest = get_model().getInterest()
    return jsonify(interest)

@crud.route("/interests", methods=['POST'])
@oauth2.required
def createInterest():
    data = request.form.to_dict(flat=True)
    interest = get_model().createInterest(data)
    return jsonify(interest)

@crud.route('/interests/add')
@oauth2.required
def interestadd():
    data = {}
    if 'profile' in session:
        data['createdBy'] = session['profile']['displayName']
        data['createdById'] = session['profile']['id']

    data['createdAt'] = 'now'
    interest = get_model().create('Interest', data)
    print(interest, file=sys.stderr)
    #return render_template("admin.html", action="List", spolunteer={})
    return redirect(url_for('.admin'))

@crud.route("/interests/<id>", methods=['GET'])
def getInterest(id):
    interest = get_model().getInterest(id)
    return jsonify(interest)

#@crud.route('/interests/<id>', methods=['DELETE'])
#@oauth2.required
#def deleteInterest(id):
#    interests = get_model.deleteInterest(id)
#    return jsonify(interests)
# [END interests]

@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    spolunteer = get_model().read(id)
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

#        image_url = upload_image_file(request.files.get('image'))

#        if image_url:
#            data['imageUrl'] = image_url

        spolunteer = get_model().update('Spolunteer', data, id)
        return redirect(url_for('.list', id=spolunteer['id']))
    return render_template("form.html", action="Edit", spolunteer=spolunteer)


@crud.route('/user/<id>/delete')
@oauth2.required
def delete(id):
    get_model().delete("Spolunteer", id)
    #return redirect(url_for(request.path))
    #return redirect(request.path)
    return redirect(url_for('.admin'))
