# -*- coding: utf-8 -*-
from models import *


class Connector:
    def __init__(self, user='root'):
        mysql_db.connect()
        try:
            User.create_table()
            Group.create_table()
            Subscribtions.create_table()
        except:
            pass

    def __del__(self):
        print "Connector closed"

    def add_users(self, users, photos=None, music=None):
        for id, user in users.iteritems():
            print id
            if (len(user['name']) * len(user['surname'])):
                photo = 0
                if id in photos:
                    photo = photos[id]
                try:
                    User.get_or_create(
                        uid=int(id),
                        username=(user['name'] + ' ' + user['surname']).encode('utf-8'),
                        age=user['age'],
                        friends_count=user['friends'],
                        photos_count=photo,
                        sex=user['sex'],
                        university=user['university'],
                        occupation=user['occupation'],
                    )
                except:
                    print 'error adding uid' + str(id)
        print 'ended writing users to database'

    def add_groups(self, data):
        print 'started writing groups to database'
        for user, groups in data.iteritems():
            for group in groups:
                Group.get_or_create(
                    gid=int(group)
                )
                us = User.get_or_create(uid=int(user))
                if type(us) == tuple:
                    us = us[0]
                Subscribtions.get_or_create(
                    user=us,
                    group=Group.get(gid=int(group))
                )
        print 'ended writing groups to database'
