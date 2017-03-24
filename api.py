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
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from utils.moment_util import *

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

def hashimage(upfile):
    fname = upfile.filename
    a = fname[:fname.rfind('.')].encode('utf8') + str(time.time())
    ha=hashlib.md5()
    ha.update(a)
    c = str(ha.hexdigest()) + fname[fname.rfind('.'):]
    upfile.save(os.path.join(UPLOAD_FOLDER, c))
    return c

tmp = {}

def get_time():
	return time.strftime("%Y-%m-%d %X", time.localtime())


@app.route('/shanyi/wx/user/get/<string:open_id>', methods=["GET"])
def user_get(open_id):
    tmp = get_user(*[open_id])

@app.route('/shanyi/wx/moment/get_all', methods=['GET'])
def moment_getAll():
    return jsonify(get_all_moment())

@app.route('/shanyi/wx/moment/<int:mid>', methods=['GET'])
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
    pass





if __name__ == '__main__':
    app.run(debug=True, port=HOST_PORT)
