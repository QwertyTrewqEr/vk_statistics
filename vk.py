# -*- coding: utf-8 -*-
import vk_api
import re
import shutil
import requests
import os


class VkParser:
    def __init__(self, login, password, ids):
        self.vk_session = vk_api.VkApi(login=login, password=password)#, app_id=6305442, api_version='5.69')
        try:
            self.vk_session.auth()
        except vk_api.AuthError as error_msg:
            print error_msg
        self.vk = self.vk_session.get_api()
        self.ids = ids

    def __del__(self):
        print ("destructor called")

    def __save_photo(self, data, filename):
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(data.raw, out_file)

    # This method returns ids with given ages
    def get_checked_by_age(self, age_start, age_end):
        checked = {}
        with vk_api.VkRequestsPool(self.vk_session) as pool:
            resp = pool.method_one_param(
                'users.get',
                key='user_ids',
                values=self.ids,
                default_values={'fields': 'bdate'}
            )
        for id, data in resp.result.items():
            if u'bdate' in data[0]:
                bdate = data[0][u'bdate']
                checked[id] = re.findall(r'[0-9]{4}', bdate)
                if (type(checked[id]) is list) and (len(checked[id]) > 0):
                    checked[id] = 2017 - int(checked[id][0])
        return [k for k, v in checked.items() if (v >= age_start) and (v <= age_end)]

    def get_personal_info(self):
        ids = self.ids
        result = {}
        friendsRequest = self.vk.users.get(user_ids=str(ids), fields=[u'counters'])
        info = self.vk.users.get(user_ids='52962951', fields=[u"sex", u"bdate", u"city", u"country"])#,
                                                            # u'home_town', u'domain', u'has_mobile',
                                                            # u'education', u'universities',
                                                            # u'schools', u'status', u'last_seen',
                                                            # u'followers_count', u'common_count', u'occupation',
                                                            # u'relation', u'personal', u'connections',
                                                            # u'music', u'books', u'games',
                                                            # u'career']))
        for i in range(len(info)):
            result[info[i]['id']] = {}
            result[info[i]['id']]['name'] = info[i][u'first_name']
            result[info[i]['id']]['surname'] = info[i][u'last_name']
            result[info[i]['id']]['sex'] = 'None'
            result[info[i]['id']]['age'] = 0
            result[info[i]['id']]['friends'] = 0
            if u'counters' in friendsRequest[i]:
                result[info[i]['id']]['friends'] = friendsRequest[i][u'counters'][u'friends']
            if u'bdate' in info[i]:
                bdate = info[i][u'bdate']
                result[info[i]['id']]['age'] = re.findall(r'[0-9]{4}', bdate)
                if type(result[info[i]['id']]['age']) is list:
                    result[info[i]['id']]['age'] = 2017 - int(result[info[i]['id']]['age'][0])
            if info[i][u'sex'] == 1:
                result[info[i]['id']]['sex'] = 'female'
            elif info[i][u'sex'] == 2:
                result[info[i]['id']]['sex'] = 'male'
            else:
                result[info[i]['id']]['sex'] = 'None'

        return result

    # if count=True, method returns photos count
    def get_user_photos(self, count=False):
        # self.vk.photos.getAll(owner_id=id)
        result = {}
        with vk_api.VkRequestsPool(self.vk_session) as pool:
            resp = pool.method_one_param(
                'photos.getAll',
                key='owner_id',
                values=self.ids
            )
        for id, photos in resp.result.iteritems():
            counter = 0
            if int(photos[u'count']) > 0:
                if count:
                    counter += int(photos[u'count'])
                    result[id] = counter
                    continue
                if not os.path.exists(str(id)):
                    os.makedirs(str(id))
                for i in xrange(len(photos[u'items'])):
                    resp = ''
                    for key, val in photos[u'items'][i].iteritems():
                        if (key.find(u'photo') > -1):
                            url = val
                            resp = requests.get(url, stream=True)
                    self.__save_photo(resp, str(id) + '/' + str(i) + '.jpg')
        if count:
            return result

    def get_user_comments(self, count=False):
        result = {}
        with vk_api.VkRequestsPool(self.vk_session) as pool:
            resp = pool.method_one_param(
                'photos.getAllComments',
                key='owner_id',
                values=self.ids
            )
        for id, comments in resp.result.iteritems():
            counter = 0
            if int(comments[u'count']) > 0:
                if count:
                    counter += int(comments[u'count'])
                    result[id] = counter
                    continue
                for item in comments[u'items']:
                    if item[u'from_id'] == id:
                        with open(str(id) + '/comments', 'ab') as out_file:
                            out_file.write('\r\n' + item[u'text'].encode('utf-8') + '\r\n')
        if count:
            return result

    def get_user_stat(self):
        friends = {}
        with vk_api.VkRequestsPool(self.vk_session) as pool:
            friends = pool.method_one_param(
                'friends.get',  # Метод
                key='user_id',  # Изменяющийся параметр
                values=self.ids,
                default_values={'fields': 'photo'}
            )
        return friends.result

    def get_user_subscriptions(self):
        subscriptions = {}
        with vk_api.VkRequestsPool(self.vk_session) as pool:
            resp = pool.method_one_param(
                'users.getSubscriptions',
                key='user_id',  # Изменяющийся параметр
                values=self.ids
            )
        for id, sub in resp.result.iteritems():
            if int(sub[u'groups'][u'count']) > 0:
                subscriptions[id] = sub[u'groups'][u'items']
        return subscriptions
