# -*- coding: utf-8 -*-
from models import *


class Connector:
    def __init__(self, user='root'):
        mysql_db.connect()
        try:
            User.create_table()
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
                User.get_or_create(
                    uid=int(id),
                    username=(user['name'] + ' ' + user['surname']).encode('utf-8'),
                    age=user['age'],
                    friends_count=user['friends'],
                    photos_count=photo,
                    sex=user['sex'],
                )
