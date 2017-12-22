# -*- coding: utf-8 -*-
from vk import VkParser
from config import config
import db_connector
import threading


def chunks(array, n):
    for i in range(0, len(array), n):
        yield array[i:i + n]


def worker(parser, connector, ids):
    print 'thread started!'
    connector.add_users(parser.get_personal_info(custom_ids=ids), parser.get_user_photos(count=True, custom_ids=ids))
    connector.add_groups(parser.get_user_subscriptions(custom_ids=ids))
    print 'thread done!'


if __name__ == '__main__':
    group_ids = ['spmi1773', 'podslushano_gornii', 'mining__anon', 'mjkvdsnfivritevnwin', 'podgon_pogon',
                 'studenthelp89046411462', 'za4etka_spb']  # mining_abiturs

    parser = VkParser(config['login'], config['password'], range(52962950, 52962952))

    members = parser.get_group_members(group_ids)
    connector = db_connector.Connector(user='vk')

    if len(members) > 1000:
        members = chunks(members, 1000)
        for member in members:
            t = threading.Thread(target=worker, args=(parser, connector, member))
            t.start()
    else:
        parser.ids = members
        connector.add_users(parser.get_personal_info(), parser.get_user_photos(count=True))
        connector.add_groups(parser.get_user_subscriptions())







        # print parser.get_personal_info()

        # subs = parser.get_user_subscriptions()
        # print subs

        # parser = VkParser(config.py['login'], config.py['password'], ages)
        # stat = parser.get_user_stat()
        # urls = open('url', 'ab')
        # photos_count = parser.get_user_photos(count=True)
        # comments_count = parser.get_user_comments(count=True)
        # for id, count in photos_count.items():
        #     if (count > 20) and (id in comments_count) and (comments_count[id] > 20):
        #         urls.write('https://vk.com/id' + str(id) + '\n')
        # urls.close()
