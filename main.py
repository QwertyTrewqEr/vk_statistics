# -*- coding: utf-8 -*-
from vk import VkParser
from config import config

if __name__ == '__main__':
    parser = VkParser(config['login'], config['password'], range(52962945, 52962947))
    #print parser.get_personal_info()

    subs = parser.get_user_subscriptions()
    print subs

    # parser = VkParser(config['login'], config['password'], ages)
    # stat = parser.get_user_stat()
    # urls = open('url', 'ab')
    # photos_count = parser.get_user_photos(count=True)
    # comments_count = parser.get_user_comments(count=True)
    # for id, count in photos_count.items():
    #     if (count > 20) and (id in comments_count) and (comments_count[id] > 20):
    #         urls.write('https://vk.com/id' + str(id) + '\n')
    # urls.close()