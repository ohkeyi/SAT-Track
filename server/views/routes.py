from flask import request, current_app, render_template, jsonify, redirect, session, url_for, g
import json
from server.views import bp

# app routes
@bp.route('/', methods=['GET'])
def index():
    # user_id = session.get('user_id')
    # if user_id is None:
    #     g.user = None
    #     return redirect(url_for('auth.login'))
    return render_template('index.html', title = "Index")

@bp.route('/test_error_log', methods=['GET', 'POST'])
def test_error_log():
    try:
        x = 1 / 0
    except Exception as e:
        current_app.logger.error('[Calculating error] x = 1 / 0')
    return 'testErrorLog'

@bp.route('/version', methods=['GET', 'POST'])
def version():
    # test version auto-update
    return 'test version 0.0.01'

@bp.route('/search_satellite', methods=['GET', 'POST'])
def search_satellite():
    """
    1. Get satellite id from frontend.
    2. Check if satellite information has already been in database.
    3. Fetch satellite information (id, location, ...) from external website.
    4. Send satellite information to slave-computer.
    5. Get satellite signal from slave-computer.
    6. Return satellite signal to user.
    """
    if request.method == 'GET':
        return 'GET method'

    if request.method == 'POST':
        try:
            satellite_id = request.form['id']

            from server.controllers import satellite_tracking
            data = satellite_tracking(satellite_id)

            return jsonify({
                'code': '001',
                'data': data
            })
        except:
            return 'got no id'

    return 'None'


@bp.route('/register', methods=('GET', 'POST'))
def register():
    return render_template('register.html', title="Register")


@bp.route('/login', methods=('GET', 'POST'))
def login():
    return render_template('login.html', title="Login")

# log recording api request
@bp.before_request
def before_app_request():
    api_name = request.url
    user_ip = request.remote_addr
    try:
        user_name = request.remote_user
    except Exception as e:
        user_name = e
    try:
        # receive frontend data
        request_data = json.loads(request.get_data())
    except Exception as e:
        request_data = request.form.to_dict()
    current_app.logger.info('{"api_name":"%s", "user_ip":"%s", "user_name":"%s"}'
                            % (api_name, user_ip, user_name))

# log report api response
@bp.after_request
def after_app_request(response):
    api_name = request.url
    user_ip = request.remote_addr
    try:
        user_name = request.remote_user
    except Exception as e:
        user_name = e
    response_data = response.json
    if str(response.status_code).startswith('4') or str(response.status_code).startswith('5') :
         current_app.logger.info('{"api_name": "%s", "user_ip": "%s", "user_name": "%s", "status_code":"%s"}' %(api_name, user_ip, user_name, response.status_code))
    else:
        current_app.logger.info('{"api_name": "%s", "user_ip": "%s", "user_name": "%s", "status_code":"%s"}' % (
        api_name, user_ip, user_name, response.status_code))
    return response
