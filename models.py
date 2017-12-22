# -*- coding: <encoding name> -*-
from peewee import *

mysql_db = MySQLDatabase('vk', user='vk', password='qwerty', charset='utf8mb4')


class MySQLModel(Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = mysql_db


class User(MySQLModel):
    uid = PrimaryKeyField()
    username = CharField(max_length=200, default='')
    age = IntegerField(default=0)
    friends_count = IntegerField(default=0)
    photos_count = IntegerField(default=0)
    sex = CharField(max_length=6, default='')
    university = CharField(max_length=200, default='')
    career = CharField(max_length=200, default='')


class Group(MySQLModel):
    gid = PrimaryKeyField()


class Subscribtions(MySQLModel):
    user = ForeignKeyField(User)
    group = ForeignKeyField(Group)
