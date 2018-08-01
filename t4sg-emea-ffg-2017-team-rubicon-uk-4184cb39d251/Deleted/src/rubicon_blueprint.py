import os
from flask import Blueprint, current_app, redirect, render_template, request, \
    session, url_for
import sqldb

basedir = os.path.abspath(os.path.dirname(__file__))


crud = Blueprint('crud', __name__)


class Config:
    SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'rubicon.db')
    SQLALCHEMY_TRACK_MODIFICATION = False

@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    spolunteers, next_page_token = sqldb.list(cursor=token)

    return render_template(
        "list.html",
        spolunteers=spolunteers,
        next_page_token=next_page_token)

# # [START list_mine]
# @crud.route("/mine")
# def list_mine():
#     token = request.args.get('page_token', None)
#     if token:
#         token = token.encode('utf-8')
#
#     spolunteers, next_page_token = sqldb.list_by_user(
#         user_id=session['profile']['id'],
#         cursor=token)
#
#     return render_template(
#         "list.html",
#         spolunteers=spolunteers,
#         next_page_token=next_page_token)
# # [END list_mine]

#
# @crud.route('/<id>')
# def view(id):
#     spolunteer = sqldb.read(id)
#     return render_template("view.html", spolunteer=spolunteer)
#
#
# # [START add]
# @crud.route('/add', methods=['GET', 'POST'])
# def add():
#     if request.method == 'POST':
#         data = request.form.to_dict(flat=True)
#
#         # If an image was uploaded, update the data to point to the new image.
# #       image_url = upload_image_file(request.files.get('image'))
#
# #        if image_url:
# #            data['imageUrl'] = image_url
#
#         # If the user is logged in, associate their profile with the new spolunteer.
#         if 'profile' in session:
#             data['createdBy'] = session['profile']['displayName']
#             data['createdById'] = session['profile']['id']
#
#         spolunteer = sqldb.create(data)
#
#         return redirect(url_for('.view', id=spolunteer['id']))
#
#     return render_template("form.html", action="Add", spolunteer={})
# # [END add]
#
#
# @crud.route('/<id>/edit', methods=['GET', 'POST'])
# def edit(id):
#     spolunteer = sqldb.read(id)
#
#     if request.method == 'POST':
#         data = request.form.to_dict(flat=True)
#
# #        image_url = upload_image_file(request.files.get('image'))
#
# #        if image_url:
# #            data['imageUrl'] = image_url
#
#         spolunteer = sqldb.update(data, id)
#
#         return redirect(url_for('.view', id=spolunteer['id']))
#
#     return render_template("form.html", action="Edit", spolunteer=spolunteer)
#
#
# @crud.route('/<id>/delete')
# def delete(id):
#     sqldb.delete(id)
#     return redirect(url_for('.list'))
