# -*- coding: utf-8 -*-
from vk import VkParser
from config import config
import db_connector

if __name__ == '__main__':
    group_ids = ['spmi1773', 'mining_abiturs']

    parser = VkParser(config['login'], config['password'], range(52962950, 52962962))

    members = parser.get_group_members(group_ids)

    connector = db_connector.Connector(user='vk')
    connector.add_users(parser.get_personal_info(), parser.get_user_photos(count=True))

    #print parser.get_personal_info()

    #subs = parser.get_user_subscriptions()
    #print subs

    # parser = VkParser(config['login'], config['password'], ages)
    # stat = parser.get_user_stat()
    # urls = open('url', 'ab')
    # photos_count = parser.get_user_photos(count=True)
    # comments_count = parser.get_user_comments(count=True)
    # for id, count in photos_count.items():
    #     if (count > 20) and (id in comments_count) and (comments_count[id] > 20):
    #         urls.write('https://vk.com/id' + str(id) + '\n')
    # urls.close()