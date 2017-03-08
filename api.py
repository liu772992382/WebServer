#!/usr/bin/env python
#coding=utf8

import os
import hashlib
import json
import requests
from flask import Flask, request, render_template, redirect,make_response, flash, session , g ,url_for, jsonify
from datetime import datetime
from model import *
import time

app = Flask(__name__)

def hashimage(upfile):
    fname = upfile.filename
    a = fname[:fname.rfind('.')].encode('utf8') + str(time.time())
    ha=hashlib.md5()
    ha.update(a)
    c = str(ha.hexdigest()) + fname[fname.rfind('.'):]
    upfile.save(os.path.join(UPLOAD_FOLDER, c))
    return c

#登陆验证及获取时间函数
#-------------------------------------------------------------------------------
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect('/shanyi/login')
        return func(*args, **kwargs)
    return wrapper

def get_time():
	return time.strftime("%Y-%m-%d %X", time.localtime())


@app.route('/shanyi/ap/activities/<int:aid>', methods=['GET'])
def get_activity(aid):
    task = filter(lambda t: t['id'] == aid, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})
