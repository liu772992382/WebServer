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
    tmp = {'status':False}
    tmp_activity = Activity()
    tmp_activity.createTime = get_time()
    tmp_activity.init_activity(**kwargs)
    try:
        session.add(tmp_activity)
        session.commit()
        print tmp_activity.aid
        tmp['status'] = True
        tmp['data'] = tmp_activity.aid
        return tmp
    except Exception, e:
        print Exception, e
        return tmp

def get_all_activities():
    tmp = {'status':False, 'data':[]}
    tmp_activities = session.query(Activity).all()
    if tmp_activities != []:
        for i in tmp_activities:
            tmp['data'].append(i.get_dict())
        tmp['status'] = True
        return tmp
    else:
        tmp['info'] = 'no activities'
        return tmp

def update_activity(**kwargs):
    tmp = {'status':False}
    tmp_activity = session.query(Activity).filter_by(aid=kwargs.get('aid')).first()
    if tmp_activity != None:
        try:
            tmp_activity.init_activity(**kwargs)
            session.commit()
            tmp['status'] = True
            return tmp
        except:
            tmp['info'] = 'error'
            return tmp

    else:
        tmp['info'] = 'No such activity'
        return tmp

def delete_activity(aid):
    tmp = {'status':False}
    # try:
    tmp_activities = session.query(Activity).filter_by(aid=aid).all()
    try:
        for i in tmp_activities:
            session.delete(i)
        session.commit()
        tmp['status'] = True
        return tmp
    except:
        return tmp

def get_part_status(uid, aid):
    tmp = {'status':False}
    tmp_participant = session.query(Participant).filter_by(uid=uid).filter_by(aid=aid).first()
    if tmp_participant != None:
        tmp['status'] = True
        tmp['data'] = tmp_participant
        return tmp
    else:
        return tmp


def add_participant(uid, aid):
    tmp = {'status':False}
    if not get_part_status(uid, aid)['status']:
        tmp_participant = Participant()
        tmp_participant.uid = uid
        tmp_participant.aid = aid
        tmp_participant.time = get_time()
        try:
            session.add(tmp_participant)
            session.commit()
            tmp['status'] = True
            return tmp
        except:
            tmp['info'] = 'no such uid or aid'
            return tmp
    else:
        tmp['info'] = 'this participant is existed'
        return tmp

def delete_participant(uid, aid):
    tmp = {'status':False}
    tmp_participant = get_part_status(uid, aid)
    if tmp_participant:
        try:
            session.delete(tmp_participant['data'])
            session.commit()
            tmp['status'] = True
            return tmp
        except:
            return tmp

    else:
        tmp['info'] = 'no such participant'
        return tmp


def get_participants(aid):
    tmp = {'status':False, 'data':[]}
    tmp_participants = session.query(Participant).filter_by(aid=aid).all()
    if tmp_participants != []:
        for i in tmp_participants:
            tmp['data'].append(i.get_dict())
        tmp['status'] = True
        return tmp
    else:
        tmp['info'] = 'no participants'
        return tmp



if __name__ == '__main__':
    create_activity(**{'name':'善意', 'organizer':'asdf'})
    tmp_acts = get_all_activities()
    for i in tmp_acts['data']:
        print i
