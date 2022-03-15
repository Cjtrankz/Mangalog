from flask import render_template, redirect, request, session
from flask_app import app, bcrypt
from flask_app.models import model_manga, model_login


@app.route('/user/account')
def show_account():
    context = {
        'results':model_login.User.get_one({'id':session['uuid']}),
        # 'mag_data':model_magazine.Magazine.get_user_mags({'id':session['uuid']})
    }
    return render_template('account.html', **context)

@app.route('/user/account/process', methods=['post'])
def update_account():
    if not session:
        return redirect('/')
    is_valid = model_manga.Manga.validator_user_update(request.form)
    if is_valid == True:
        data = {
            **request.form,
            'id':session['uuid']
        }
        model_login.User.update_one(data)
    return redirect('/user/account')



@app.route('/backlog')
def show_backlog():
    #test
    context = {
        'user':model_login.User.get_one({'id':session['uuid']}),
        'backlog':model_manga.Manga.get_all_mangas({'id':session['uuid']})
    }
    return render_template('backlog.html', **context)


@app.route('/search')
def search_manga():
    context = {
        'user':model_login.User.get_one({'id':session['uuid']})
    }
    return render_template('search.html', **context)

@app.route('/follow/process', methods=['post'])
def follow_manga():
    data = {
        **request.form,
        'user_id':session['uuid']
    }
    print(data)
    is_valid = model_manga.Manga.validate_follow(data)
    if(is_valid == True):
        model_manga.Manga.follow(data)
    return redirect('/search')

@app.route('/chapters/<int:id>/<int:chId>/process', methods=['post'])
def update_ch_read(id, chId):
    
    data = {
        **request.form,
        'user_id':session['uuid'],
        'id':chId
    }
    model_manga.Manga.update_num_ch_read(data)
    return redirect('/backlog')

@app.route('/unfollow/<int:id>/<int:chId>/process')
def unfollow(id, chId):
    data = {
        'user_id':id,
        'id':chId
    }
    model_manga.Manga.unfollow(data)
    return redirect('/backlog')

@app.route('/info/*')
def show_manga(dex_id):
    context = {
        'dex_id':dex_id
    }
    return render_template('info.html', **context)

# @app.route('/info/<int:id>/process', methods=['post'])
# def show_manga():
#     data = {
#         **request.form,
#         'user_id':session['uuid']
#     }
#     model_manga.Manga.follow(data)
#     return render_template('info.html')

# @app.route('/delete/<int:id>')
# def delete_sighting(id):
#     check = model_manga.Manga.get_one({'id':id})
#     if session['uuid'] != check.user_id:
#         return redirect('/')
#     model_manga.Manga.delete_one({'id':id})
#     return redirect('/user/account')


# @app.route('/new')
# def new_sight():
#     if not session:
#         return redirect('/')
#     context = {
#     'user':model_login.User.get_one({'id':session['uuid']})
#     }
#     return render_template('add_magazine.html', **context)

# @app.route('/new/process', methods=['post'])
# def process_sight():
#     if not session:
#         return redirect('/')
#     data = {
#         **request.form
#         }
#     data['user_id'] = session['uuid']
#     is_valid = model_magazine.Magazine.validator_mag(data)
#     if is_valid == True:
#         model_magazine.Magazine.create(data)
#         return redirect('/dashboard')
#     return redirect('/new')