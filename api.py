#!/usr/bin/env python
#coding=utf8

import os
import hashlib
import json
from flask import Flask, request, render_template, redirect,make_response, abort, \
                session , g ,url_for, jsonify, make_response
from datetime import datetime
from model import *
import time
from flask_httpauth import HTTPBasicAuth
from collections import OrderedDict
from utils.moment_util import *
from utils.user_util import *
from utils.activity_util import *
from werkzeug import secure_filename


app = Flask(__name__)
auth = HTTPBasicAuth()

@app.teardown_request
def shutdown_session(exception=None):
    session.close()

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

def hashimage(fname):
    a = fname[:fname.rfind('.')].encode('utf8') + str(time.time())
    ha=hashlib.md5()
    ha.update(a)
    c = str(ha.hexdigest()) + fname[fname.rfind('.'):]
    upfile.save(os.path.join(UPLOAD_FOLDER, c))
    return c

tmp = {}

def get_time():
	return time.strftime("%Y-%m-%d %X", time.localtime())

#--------------------用户接口---------------------

@app.route('/shanyi/wx/user/get/<string:openId>', methods=["GET"])
def user_get(openId):
    return jsonify(get_user(openId))
    #返回值

@app.route('/shanyi/wx/user/get', methods=['GET'])
@app.route('/shanyi/wx/user/get/', methods=['GET'])
def user_get_all():
    return jsonify(get_all_user())

@app.route('/shanyi/wx/user/exist/<openId>', methods=['GET'])
def user_exist(openId):
    return jsonify(if_user_exist(openId))

@app.route('/shanyi/wx/user/create', methods = ['POST'])
def user_create():
    return jsonify(create_user(**request.form.to_dict()))

@app.route('/shanyi/wx/user/update', methods = ['POST'])
def user_update():
    return jsonify(update_user(**request.form.to_dict()))

@app.route('/shanyi/wx/user/delete/<int:openId>', methods = ['GET'])
def user_delete(openId):
    return jsonify(delete_user(openId))

@app.route('/shanyi/wx/user/login', methods = ['POST'])
def user_login():
    tmp_info = request.form.to_dict()
    if not if_user_exist(tmp_info['openId'])['status']:
        return jsonify(create_user(**tmp_info))
    else:
        return jsonify(login_user(tmp_info['openId']))

@app.route('/shanyi/wx/user/corp/get/<int:uid>', methods = ['GET'])
def corp_get(uid):
    return jsonify(get_corporation(uid))

@app.route('/shanyi/wx/user/corp/get_all', methods = ['GET'])
def corp_get_all():
    return jsonify(get_all_corporation())


#--------------------活动接口---------------------
@app.route('/shanyi/wx/activity/get_all', methods = ['GET'])
def activity_get_all():
    tmp_activities = get_all_activities()
    for i in tmp_activities['data']:
        i['thumbs'] = len(get_participants(i['aid'])['data'])
    return jsonify(tmp_activities)

@app.route('/shanyi/wx/activity/get/<int:aid>', methods = ['GET'])
def activity_get(aid):
    return jsonify(get_activity(aid))

@app.route('/shanyi/wx/activity/create', methods = ['POST'])
def activity_create():
    return jsonify(create_activity(**request.form.to_dict()))

@app.route('/shanyi/wx/activity/update', methods = ['POST'])
def activity_update():
    return jsonify(update_activity(**request.form.to_dict()))

@app.route('/shanyi/wx/activity/delete/<int:aid>', methods = ['GET'])
def activity_delete(aid):
    return jsonify(delete_activity(aid))

@app.route('/shanyi/wx/activity/participant/get/<int:aid>', methods = ['GET'])
def activity_participant_get(aid):
    return jsonify(get_participants(aid))

@app.route('/shanyi/wx/activity/participant/add', methods = ['POST'])
def activity_participant_add():
    req_uid = request.form.get('uid')
    req_aid = request.form.get('aid')
    return jsonify(add_participant(req_uid, req_aid))

@app.route('/shanyi/wx/activity/participant/delete', methods = ['POST'])
def activity_participant_delete():
    req_uid = request.form.get('uid')
    req_aid = request.form.get('aid')
    return jsonify(delete_participant(req_uid, req_aid))


#--------------------动态接口---------------------

@app.route('/shanyi/wx/moment/get_all', methods=['GET'])
def moment_getAll():
    return jsonify(get_all_moment())

@app.route('/shanyi/wx/moment/get/<int:mid>', methods=['GET'])
def moment_getById(mid):
    return jsonify(get_moment(mid))

@app.route('/shanyi/wx/moment/create', methods=['POST'])
def moment_create():
    return jsonify(create_moment(**request.form.to_dict()))

@app.route('/shanyi/wx/moment/delete/<int:mid>', methods=['GET'])
def moment_delete(mid):
    return jsonify(delete_moment(mid))

@app.route('/shanyi/wx/moment/get_likes/<int:mid>', methods=['GET'])
def moment_getLikes(mid):
    return jsonify(get_likes(mid))

@app.route('/shanyi/wx/moment/like', methods=['POST'])
def moment_like():
    req_mid = request.form.get('mid')
    req_uid = request.form.get('uid')
    return jsonify(like_moment(req_mid, req_uid))

@app.route('/shanyi/wx/moment/cancel_like', methods=['POST'])
def moment_cancel_like():
    req_mid = request.form.get('mid')
    req_uid = request.form.get('uid')
    return jsonify(cancel_like(req_mid, req_uid))

@app.route('/shanyi/wx/moment/create_comment', methods = ['POST'])
def moment_create_comment():
    req_mid = request.form.get('mid')
    req_uid = request.form.get('uid')
    req_content = request.form.get('content')
    return jsonify(create_comment(req_mid, req_uid, req_content))

@app.route('/shanyi/wx/moment/comments/<int:mid>', methods = ['GET'])
def moment_comments(mid):
    return jsonify(get_comments(mid))

@app.route('/shanyi/wx/moment/add_image', methods = ['POST'])#待测试
def moment_add_image():
    file0 = request.files['file']
    req_mid = request.form.get('mid')
    if file0 and allowed_file(file0.filename):
        filename = hashimage(secure_filename(file0.filename))
        file0.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify(req_mid, filename)
    else:
        return jsonify({'status':False})

@app.route('/shanyi/wx/moment/images/<int:mid>', methods = ['GET'])
def moment_get_images(mid):
    return jsonify(get_images(mid))





if __name__ == '__main__':
    app.run(debug=True, port=HOST_PORT)
