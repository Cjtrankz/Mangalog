from flask import render_template, redirect, request, session
from flask_app import app, bcrypt
from flask_app.models import model_login, model_manga

@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/backlog')
    return render_template('index.html')

# @app.route('/dashboard')
# def dashboard():
#     # if 'uuid' not in session:
#     #     return redirect('/')
#     # context = {
#     #     'user':model_login.User.get_one({'id':session['uuid']}),
#     #     'backlog':model_manga.Manga.get_all_mangas({'id':session['uuid']})
#     # }
#     # # test
#     # return render_template('dashboard.html', **context)
#     return redirect('/backlog')

@app.route('/user/create', methods=['post'])
def user_create():
    is_valid = model_login.User.validator_registration(request.form)
    if not is_valid:
        return redirect('/')

    pw = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        **request.form,
        'password':pw
    }

    user_id = model_login.User.create(data)
    session['uuid'] = user_id
    return redirect('/')

@app.route('/user/login', methods=['post'])
def user_login():
    is_valid = model_login.User.validate_login(request.form)
    if is_valid:
        return redirect('/backlog')
    return redirect('/')


@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')