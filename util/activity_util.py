#!/usr/bin/env python
#coding=utf8

import sys
sys.path.append("..")
from model import *

def get_activity(*args):
    tmp = {'status':False, 'data':[]}
    try:
        for i in args:
            tmp['data'].append(session.query(Activity).filter_by(aid=i).first().get_dict())
        tmp['status'] = True
        return tmp
    except:
        return tmp

def create_activity(**kwargs):
    tmp_activity = Activity()
    tmp_activity.init_activity(**kwargs)
    try:
        session.add(tmp_activity)
        session.commit()
        return True
    except:
        return False

def update_activity(**kwargs):
    tmp = {'status':False}
    tmp_activity = session.query(Activity).filter_by(aid=kwargs['aid']).first()
    if tmp_activity != None:
        try:
            tmp_activity.init_activity(**kwargs)
            session.commit()
            tmp['status'] = True
            return tmp
        except:
            tmp['info'] = 'error'
            return tmp

def delete_user(aid):
    # try:
    delete_activities = session.query(Activity).filter_by(aid=aid).all()
    try:
        for i in delete_activities:
            session.delete(i)
        session.commit()
        return True
    except:
        return False
