# -*- coding: utf-8 -*-
import vk_api
import re
import shutil
import requests
import os


class VkParser:
    def __init__(self, login, password, start=52962734, stop=52962735):
        vk_session = vk_api.VkApi(login, password)
        try:
            vk_session.auth()
        except vk_api.AuthError as error_msg:
            print error_msg
        self.vk = vk_session.get_api()
        self.start = start
        self.stop = stop

    def __save_photo(self, data, filename):
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(data.raw, out_file)

    def get_personal_info(self):
        ids = []
        result = {}
        for id in xrange(self.start, self.stop + 1):
            ids.append(id)
        friendsRequest = self.vk.users.get(user_ids=ids, fields=[u'counters'])
        info = self.vk.users.get(user_ids=ids, fields=[u'followers_count', u'bdate'])
        for i in xrange(len(info)):
            result[info[i]['id']] = {}
            result[info[i]['id']]['name'] = info[i][u'first_name']
            result[info[i]['id']]['sirname'] = info[i][u'last_name']
            bdate = None
            result[info[i]['id']]['age'] = None
            result[info[i]['id']]['friends'] = None
            if u'counters' in friendsRequest[i]:
                result[info[i]['id']]['friends'] = friendsRequest[i][u'counters'][u'friends']
            if u'bdate' in info[i]:
                bdate = info[i][u'bdate']
                result[info[i]['id']]['age'] = re.findall(r'[0-9]{4}', bdate)
                if type(result[info[i]['id']]['age']) is list:
                    result[info[i]['id']]['age'] = 2017 - int(result[info[i]['id']]['age'][0])
        return result

    def get_user_photos(self, id):
        photos = self.vk.photos.getAll(owner_id=id)
        if int(photos[u'count']) > 0:
            if not os.path.exists(str(id)):
                os.makedirs(str(id))
            for i in xrange(len(photos[u'items'])):
                resp = ''
                for key, val in photos[u'items'][i].iteritems():
                    if (key.find(u'photo') > -1):
                        url = val
                        resp = requests.get(url, stream=True)
                self.__save_photo(resp, str(id) + '/' + str(i) + '.jpg')

    def get_user_comments(self, id, count):
        comments = self.vk.photos.getAllComments(owner_id=id, count=count)
        if int(comments[u'count']) > 0:
            for item in comments[u'items']:
                if item[u'from_id'] == id:
                    with open(str(id) + '/comments', 'ab') as out_file:
                        out_file.write('\r\n' + item[u'text'].encode('utf-8') + '\r\n')


if __name__ == '__main__':
    parser = VkParser('', '', 52962734, 52962735)
    print parser.get_personal_info()
    parser.get_user_photos(52962735)
    parser.get_user_comments(52962735, 100)
    # 17721869
    # 52962735
