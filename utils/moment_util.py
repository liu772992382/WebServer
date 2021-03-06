#!/usr/bin/env python
#coding=utf8

import sys
sys.path.append("..")
from model import *

def owner_get(uid):
    tmp = {'status':False, 'data':[]}
    try:
        moments = session.query(Moment).filter_by(uid=uid).order_by(Moment.mid.desc()).all()
        for i in moments:
            tmp['data'].append(i.get_dict())
        tmp['status'] = True
    except:
        pass
    finally:
        return tmp

def get_moment(*args):
    tmp = {'status':False, 'data':[]}
    try:
        for i in args:
            tmp['data'].append(session.query(Moment).filter_by(mid=i).first().get_dict())
        tmp['status'] = True
    except:
        pass
    finally:
        return tmp

def get_all_moment(num=4, offset = 0):
    tmp = {'status':False, 'data':[]}
    try:
        moments = session.query(Moment).order_by(Moment.mid.desc()).limit(num).offset(offset).all()
        for i in moments:
            tmp['data'].append(i.get_dict())
        tmp['status'] = True
    except Exception, e:
        logging.info(Exception, e)
    finally:
        return tmp

def create_moment(**kwargs):#返回数据存在bug
    tmp = {'status':False}
    tmp_moment = Moment()
    tmp_moment.init_moment(**kwargs)
    if not tmp_moment.aid:
        tmp_moment.aid = 1
    tmp_moment.time = get_time()
    try:
        session.add(tmp_moment)
        session.commit()
        tmp['data'] = tmp_moment.mid
        tmp['status'] = True
        return tmp
    except Exception, e:
        logging.info(Exception, e)
        return tmp

def search_moment(sdata):
    tmp = {'status': False, 'data': []}
    try:
        tmp_moments = session.query(Moment).filter(Moment.content.like('%'+sdata+'%')).order_by(Moment.mid.desc()).all()
        for i in tmp_moments:
            tmp['data'].append(i.get_dict())
        tmp_users = session.query(User).filter(User.nickName.like('%'+sdata+'%')).all()
        for i in tmp_users:
            tmp_moments = session.query(Moment).filter(Moment.uid==i.uid).order_by(Moment.mid.desc()).all()
            for j in tmp_moments:
                tmp['data'].append(j.get_dict())
        tmp['status'] = True
        return tmp
    except:
        return tmp





# def update_moment(**kwargs):
#     tmp = {'status':False}
#     tmp_moment = session.query(Moment).filter_by(mid=kwargs['mid']).first()
#     if tmp_moment != None:
#         try:
#             tmp_moment.init_moment(**kwargs)
#             session.commit()
#             tmp['status'] = True
#             return tmp
#         except:
#             tmp['info'] = 'error'
#             return tmp
#
#     else:
#         tmp['info'] = 'No such openId user'
#         return tmp

def delete_moment(mid):
    tmp = {'status':False}
    delete_moments = session.query(Moment).filter_by(mid=mid).all()
    try:
        for i in delete_moments:
            session.delete(i)
        session.commit()
        tmp['status'] = True
        return tmp
    except:
        return tmp


def get_like_status(mid, uid):
    tmp = {'status':False}
    tmp_like = session.query(MomentLike).filter_by(mid=mid).filter_by(uid=uid).first()
    if tmp_like !=None:
        tmp['status'] = True
        tmp['data'] = tmp_like
        return tmp
    else:
        return tmp

def get_likes(mid):
    tmp = {'status':False, 'data':[]}
    tmp_likes = session.query(MomentLike).filter_by(mid=mid).all()
    try:
        for i in tmp_likes:
            tmp['data'].append(i.uid)
        tmp['status'] = True
        return tmp
    except Exception, e:
        logging.info(Exception, e)
        return tmp


def like_moment(mid, uid):
    tmp = {'status':False}
    if not get_like_status(mid, uid)['status']:
        mlike = MomentLike()
        mlike.mid = mid
        mlike.uid = uid
        mlike.time = get_time()
        try:
            session.add(mlike)
            session.commit()
            tmp['status'] = True
            return tmp
        except:
            return tmp
    else:
        tmp['info'] = '你已经赞过这条动态'
        return tmp


def cancel_like(mid, uid):
    tmp = {'status':False}
    tmp_like = get_like_status(mid, uid)
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

def create_comment(mid, uid, content):
    tmp = {'status':False}
    tmp_comment = MomentComment()
    tmp_comment.mid = mid
    tmp_comment.uid = uid
    tmp_comment.content = content
    tmp_comment.time = get_time()
    try:
        session.add(tmp_comment)
        session.commit()
        tmp['status'] = True
        return tmp
    except:
        return tmp

def get_comments(mid):
    tmp = {'status':False, 'data':[]}
    tmp_comments = session.query(MomentComment).filter_by(mid=mid).order_by(MomentComment.cmid.desc()).all()
    if tmp_comments != []:
        for i in tmp_comments:
            tmp['data'].append(i.get_dict())
        tmp['status'] = True
        return tmp

    else:
        tmp['info'] = 'no comment'
        return tmp

def add_image(mid, md5):
    tmp = {'status':False}
    tmp_image = MomentImage()
    tmp_image.mid = mid
    tmp_image.md5 = md5
    try:
        session.add(tmp_image)
        session.commit()
        tmp['status'] = True
        return tmp
    except:
        return tmp

def get_images(mid):
    tmp = {'status':False, 'data':[]}
    tmp_images = session.query(MomentImage).filter_by(mid=mid).all()
    if tmp_images != []:
        for i in tmp_images:
            tmp['data'].append(i.get_dict())
        tmp['status'] = True
        return tmp
    else:
        tmp['info'] = 'no image'
        return tmp
