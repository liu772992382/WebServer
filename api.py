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
from test_qiniu import *
import random


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

@app.route('/shanyi/wx/api/uptoken', methods = ['POST'])
def uptoken():
    keys = request.form
    tmp_token = {}
    for i in keys:
        tmp_token[keys[i]] = q.upload_token(bucket_name, keys[i][9:], 7200)
    print tmp_token
    return jsonify(tmp_token)


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
    tmp_activity = get_activity(aid)
    tmp_uid = tmp_activity['data'][0]['organizer']
    tmp_activity['data'][0]['organizerInfo'] = session.query(Corporation).filter_by(uid=tmp_uid).first().get_dict()
    return jsonify(tmp_activity)

@app.route('/shanyi/wx/activity/create', methods = ['POST'])
def activity_create():
    return jsonify(create_activity(**request.form.to_dict()))

@app.route('/shanyi/wx/activity/weburl/<string:openId>', methods = ['GET'])
def weburl(openId):
    tmp_user = session.query(User).filter(User.openId==openId).first()
    if tmp_user:
        tmp_acts = session.query(Activity).filter(Activity.organizer==tmp_user.uid).all()
        actData = []
        for i in tmp_acts:
            actData.append(i.get_dict())
        return render_template('Adminuser.html', userInfo = tmp_user.get_dict(), actData = actData)
    else:
        return jsonify({'status': False, 'info': 'no such user'})

@app.route('/shanyi/wx/activity/create_web', methods = ['POST'])
def activity_create_web():
    image = request.files['file']
    if image and allowed_file(image.filename):
        filename=secure_filename(image.filename)
        image.save(os.path.join('./',filename))
        key = str(random.randrange(100,1000000))+filename
        token = q.upload_token(bucket_name, key, 3600)
        ret, info = put_file(token, key, './'+filename)
        tmp = request.form.to_dict()
        tmp['cover'] = QINIUURL + ret.get('key')
        tmp_info = create_activity(**tmp)
        tmp_info = '发布成功' if tmp_info['status'] else '发布失败'
        return tmp_info
    else:
        return jsonify({'status': False, 'info': 'invalid file'})

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
    req_aid = request.form.get('aid')
    req_uid = session.query(User).filter_by(openId=request.form.get('openId')).first().uid
    print req_aid, req_uid
    return jsonify(add_participant(req_uid, req_aid))

@app.route('/shanyi/wx/activity/participant/delete', methods = ['POST'])
def activity_participant_delete():
    req_uid = request.form.get('uid')
    req_aid = request.form.get('aid')
    return jsonify(delete_participant(req_uid, req_aid))

@app.route('/shanyi/wx/activity/myrecently/<string:openId>', methods = ['GET'])
def activity_myrecently(openId):
    print openId
    tmp = {'status': True, 'data': ''}
    tmp_uid = get_uid(openId)['data']
    tmp_acts = session.query(Participant).filter_by(uid=tmp_uid).all()
    for i in tmp_acts:
        tmp['data'] += session.query(Activity).filter_by(aid=i.aid).first().name
        tmp['data'] += ' '
    return jsonify(tmp)


#--------------------动态接口---------------------
@app.route('/shanyi/wx/moment/owner_get/<string:openId>', methods=['GET'])
def moment_owner_get(openId):
    tmp_uid = get_uid(openId)['data']
    tmp_moments = owner_get(tmp_uid)
    # print tmp_moments
    tmp_moments['userInfo'] = session.query(User).filter_by(uid=tmp_uid).first().get_dict()
    for i in tmp_moments['data']:
        i['images'] = get_images(i['mid'])['data']
        i['likeAmount'] = len(get_likes(i['mid'])['data'])
        i['commentAmount'] = len(get_comments(i['mid'])['data'])
    return jsonify(tmp_moments)


@app.route('/shanyi/wx/moment/get_all', methods=['GET'])
def moment_getAll():
    tmp_moments = get_all_moment()
    # print tmp_moments
    for i in tmp_moments['data']:
        i['userInfo'] = session.query(User).filter_by(uid=i['uid']).first().get_dict()
        i['images'] = get_images(i['mid'])['data']
        i['likeAmount'] = len(get_likes(i['mid'])['data'])
        i['commentAmount'] = len(get_comments(i['mid'])['data'])
    return jsonify(tmp_moments)

@app.route('/shanyi/wx/moment/get_more/<int:offset>', methods=['GET'])
def moment_getMore(offset):
    tmp_moments = get_all_moment(offset=offset)
    # print tmp_moments
    for i in tmp_moments['data']:
        i['userInfo'] = session.query(User).filter_by(uid=i['uid']).first().get_dict()
        i['images'] = get_images(i['mid'])['data']
        i['likeAmount'] = len(get_likes(i['mid'])['data'])
        i['commentAmount'] = len(get_comments(i['mid'])['data'])
    return jsonify(tmp_moments)

@app.route('/shanyi/wx/moment/get/<int:mid>', methods=['GET'])
def moment_getById(mid):
    tmp_moment = get_moment(mid)['data'][0]
    tmp_moment['userInfo'] = session.query(User).filter_by(uid=tmp_moment['uid']).first().get_dict()
    tmp_moment['images'] = get_images(tmp_moment['mid'])['data']
    tmp_moment['likeAmount'] = len(get_likes(tmp_moment['mid'])['data'])
    tmp_moment['comments'] = get_comments(tmp_moment['mid'])['data']
    for i in tmp_moment['comments']:
        i['userInfo'] = session.query(User).filter_by(uid=i['uid']).first().get_dict()
    tmp_moment['commentAmount'] = len(tmp_moment['comments'])
    return jsonify(tmp_moment)

@app.route('/shanyi/wx/moment/create', methods=['POST'])
def moment_create():
    tmp_moment = request.form.to_dict()
    tmp_moment['uid'] = get_uid(tmp_moment['openId'])['data']
    return jsonify(create_moment(**tmp_moment))

@app.route('/shanyi/wx/moment/delete/<int:mid>', methods=['GET'])
def moment_delete(mid):
    return jsonify(delete_moment(mid))

@app.route('/shanyi/wx/moment/search/<string:sdata>', methods=['GET'])
def moment_search(sdata):
    tmp_moments = search_moment(sdata)
    for i in tmp_moments['data']:
        i['userInfo'] = session.query(User).filter_by(uid=i['uid']).first().get_dict()
        i['images'] = get_images(i['mid'])['data']
        i['likeAmount'] = len(get_likes(i['mid'])['data'])
        i['commentAmount'] = len(get_comments(i['mid'])['data'])
    return jsonify(tmp_moments)

@app.route('/shanyi/wx/moment/get_likes/<int:mid>', methods=['GET'])
def moment_getLikes(mid):
    return jsonify(get_likes(mid))

@app.route('/shanyi/wx/moment/like', methods=['POST'])
def moment_like():
    req_mid = request.form.get('mid')
    req_uid = session.query(User).filter_by(openId=request.form.get('openId')).first().uid
    return jsonify(like_moment(req_mid, req_uid))

@app.route('/shanyi/wx/moment/cancel_like', methods=['POST'])
def moment_cancel_like():
    req_mid = request.form.get('mid')
    req_uid = request.form.get('uid')
    return jsonify(cancel_like(req_mid, req_uid))

@app.route('/shanyi/wx/moment/create_comment', methods = ['POST'])
def moment_create_comment():
    print request.form.get('openId')
    req_uid = session.query(User).filter_by(openId=request.form.get('openId')).first().uid
    req_mid = request.form.get('mid')
    req_content = request.form.get('content')
    return jsonify(create_comment(req_mid, req_uid, req_content))

@app.route('/shanyi/wx/moment/comments/<int:mid>', methods = ['GET'])
def moment_comments(mid):
    return jsonify(get_comments(mid))

@app.route('/shanyi/wx/moment/add_image', methods = ['POST'])#待测试
def moment_add_image():
    tmp_mid = request.form.get('mid')
    tmp_md5 = request.form.get('md5')
    if 'http://' not in tmp_md5:
        tmp_md5 = 'http://oo4l2ezdu.bkt.clouddn.com/' + tmp_md5
    return jsonify(add_image(tmp_mid, tmp_md5))

@app.route('/shanyi/wx/moment/images/<int:mid>', methods = ['GET'])
def moment_get_images(mid):
    return jsonify(get_images(mid))





if __name__ == '__main__':
    app.run(debug=True, port=HOST_PORT, host='0.0.0.0')
