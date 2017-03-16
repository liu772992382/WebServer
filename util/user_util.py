#!/usr/bin/env python
#coding=utf8

import sys
sys.path.append("..")
from model import *


def get_user(*args):
    tmp = {'status':False, 'data':[]}
    try:
        for i in args:
            tmp['data'].append(session.query(User).filter_by(openId=i).first().get_dict())
        tmp['status'] = True
        return tmp
    except:
        return tmp

def create_user(**kwargs):
    tmp = {'status':False}
    tmp_user = User()
    tmp_user.init_user(**kwargs)
    try:
        session.add(tmp_user)
        session.commit()
        tmp['status'] = True
        return tmp
    except:
        return tmp

def update_user(**kwargs):
    tmp = {'status':False}
    tmp_user = session.query(User).filter_by(openId=kwargs['openId']).first()
    if tmp_user != None:
        try:
            tmp_user.init_user(**kwargs)
            session.commit()
            tmp['status'] = True
            return tmp
        except:
            tmp['info'] = 'error'
            return tmp


    else:
        tmp['info'] = 'No such openId user'
        return tmp

def delete_user(open_id):
    tmp = {'status':False}
    # try:
    tmp_users = session.query(User).filter_by(openId=open_id).all()
    try:
        for i in tmp_users:
            session.delete(i)
        session.commit()
        tmp['status'] = True
        return tmp
    except:
        return tmp
