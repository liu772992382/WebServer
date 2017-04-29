#!/usr/bin/env python
#coding=utf8

import sys
sys.path.append("..")
from model import *

def get_activity(args):
    tmp = {'status':False}

    try:
        # for i in args:
        tmp['data'] = copy.deepcopy(session.query(Activity).filter_by(aid=args).first().get_dict())
        tmp['status'] = True
        return tmp
    except Exception, e:
        # print Exception, e
        return tmp

def create_activity(**kwargs):
    tmp = {'status':False}
    tmp_activity = Activity()
    tmp_activity.createTime = get_time()
    tmp_activity.init_activity(**kwargs)
    try:
        session.add(tmp_activity)
        session.commit()
        # print tmp_activity.aid
        tmp['status'] = True
        tmp['data'] = tmp_activity.aid
        return tmp
    except Exception, e:
        logging.info(Exception, e)
        return tmp

def get_all_activities():
    tmp = {'status':False, 'data':[]}
    tmp_activities = session.query(Activity).order_by(Activity.aid.desc()).all()
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
            tmp['info'] = '报名失败：无此用户或活动'
            return tmp
    else:
        tmp['info'] = '报名失败：你已经报过名了'
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
    tmp_participants = session.query(Participant).filter_by(aid=aid).order_by(Participant.pid.desc()).all()
    if tmp_participants != []:
        for i in tmp_participants:
            tmp['data'].append(i.get_dict())
        tmp['status'] = True
        return tmp
    else:
        tmp['info'] = 'no participants'
        return tmp


def activity_get_like_status(aid, uid):
    tmp = {'status':False}
    tmp_like = session.query(ActivityLike).filter_by(aid=aid).filter_by(uid=uid).first()
    if tmp_like !=None:
        tmp['status'] = True
        tmp['data'] = tmp_like
        return tmp
    else:
        return tmp

def activity_get_likes(aid):
    tmp = {'status':False, 'data':[]}
    tmp_likes = session.query(ActivityLike).filter_by(aid=aid).all()
    try:
        for i in tmp_likes:
            tmp['data'].append(i.uid)
        tmp['status'] = True
        return tmp
    except Exception, e:
        logging.info(Exception, e)
        return tmp


def like_activity(aid, uid):
    tmp = {'status':False}
    if not activity_get_like_status(aid, uid)['status']:
        alike = ActivityLike()
        alike.aid = aid
        alike.uid = uid
        alike.time = get_time()
        try:
            session.add(alike)
            session.commit()
            tmp['status'] = True
            return tmp
        except:
            return tmp
    else:
        tmp['info'] = '你已经赞过这条活动'
        return tmp


def activity_cancel_like(aid, uid):
    tmp = {'status':False}
    tmp_like = activity_get_like_status(aid, uid)
    if tmp_like['status']:
        try:
            session.delete(tmp_like['data'])
            session.commit()
            tmp['status'] = True
            return tmp
        except:
            return tmp
    else:
        tmp['info'] = 'no such like'
        return tmp



if __name__ == '__main__':
    create_activity(**{'name':'善意', 'organizer':'asdf'})
    tmp_acts = get_all_activities()
    for i in tmp_acts['data']:
        print i
