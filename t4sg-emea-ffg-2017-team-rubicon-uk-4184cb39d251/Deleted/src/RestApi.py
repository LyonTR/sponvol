import json

import httplib2
from flask import current_app, Flask, redirect, request, session, url_for
import sqldb
from oauth2client.contrib.flask_util import UserOAuth2
from rubicon_blueprint import crud

app = Flask(__name__)
app.register_blueprint(crud, url_prefix='/volunteer')
oauth2 = UserOAuth2()

# [START request_user_info]
def _request_user_info(credentials):
    """
    Makes an HTTP request to the Google+ API to retrieve the user's basic
    profile information, including full name and photo, and stores it in the
    Flask session.
    """
    http = httplib2.Http()
    credentials.authorize(http)
    resp, content = http.request(
        'https://www.googleapis.com/plus/v1/people/me')

    if resp.status != 200:
        current_app.logger.error(
            "Error while obtaining user profile: \n%s: %s", resp, content)
        return None
    session['profile'] = json.loads(content.decode('utf-8'))

# [END request_user_info]

@app.route('/logout')
def logout():
    # Delete the user's profile and the credentials stored by oauth2.
    del session['profile']
    session.modified = True
    oauth2.storage.delete()
    return redirect(request.referrer or '/')

# applications.
@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


@app.route("/")
def index():
    return redirect(url_for('crud.list'))


if __name__ == '__main__':
    with app.app_context():
        model = sqldb
        model.init_app(app)
    app.run(threaded=True, debug=True)