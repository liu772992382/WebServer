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

app = Flask(__name__)
auth = HTTPBasicAuth()
api = Api(app)

# parser = reqparse.RequestParser()
# parser.add_argument('rate', type=int, help='Rate to charge for this resource')
# args = parser.parse_args()

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(aid):
    if aid not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(aid))

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)


# Todo
#   show a single todo item and lets you delete them
class ActivityApi(Resource):
    def get(self, aid):
        abort_if_todo_doesnt_exist(aid)
        return TODOS[aid]

    def delete(self, aid):
        abort_if_todo_doesnt_exist(aid)
        del TODOS[aid]
        return '', 204

    def put(self, aid):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[aid] = task
        return task, 201


# TodoList
#   shows a list of all todos, and lets you POST to add new tasks
class ActivityList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        aid = int(max(TODOS.keys()).lstrip('todo')) + 1
        aid = 'todo%i' % aid
        TODOS[aid] = {'task': args['task']}
        return TODOS[aid], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


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

# class UserApi(Resource):
#     def get(self, uid):
#         return {uid: tmp[uid]}
#
#     def put(self, uid):
#         tmp[uid] = request.form['data']
#         return {uid: tmp[uid]}
#
# api.add_resource(UserApi, '/shanyi/user/<string:uid>')



if __name__ == '__main__':
    app.run(debug=True, port=HOST_PORT)
