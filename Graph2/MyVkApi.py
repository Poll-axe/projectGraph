from json import JSONDecodeError
import time
import requests

"""
примеры id
122541914
336081407
186553202
440350634
346219128
Cсылка для получения ключа доступа
https://oauth.vk.com/authorize?client_id=6498822&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52

"""


# https://oauth.vk.com/authorize?client_id=6498822&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52

# if __name__ == '__main__':

class MyVkApi:

    def __init__(self):
        self.parametrs = {
            'access_token': '3363af857c4ec2be479ed05d5752beeab0d049e80da95f22bee4f36157ca4d388d95d288920e0be18107c',
            # 'user_id': 1,
            'v': 5.78}
        self.catalog = {}
        self.friends_dikt = {}
        self.working_id = 0

    def update_catalog(self, res):
        """

        :param res: ответ от сервера
        :return: словарь с ключем id, именем и фамилией
        """
        d = {}
        if 'error' in res.json().keys():
            print("error")
            print(res.json()['error']['error_msg'])
            if res.json()['error']['error_msg'] == 'Too many requests per second':
                time.sleep(1)
        if 'response' in res.json().keys():
            r = res.json()
            d = self.get_dict_info(r)
            self.catalog.update(d)
        return d

    def get_dict_info(self, r):
        """

        :param r: ответ сервера на запрос в формате json
        :return: словарь по id и информацией по нему
        """
        d = {}
        for dic in r['response']:
            d[dic['id']] = dic['last_name'], dic['first_name'], dic['sex']
        return d

    # test function
    def user_get1(self, user_id):
        """

        :param user_id: id пользователя vk
        :return: словарь с ключем id, именем и фамилией
        """
        d = {}
        url2 = 'https://api.vk.com/method/users.get'

        if user_id in self.catalog:
            d[user_id] = self.catalog[user_id]
            return d

        g = {'user_ids': user_id, 'fields': 'sex'}    # параметры запроса
        res = requests.get(url2, params={**self.parametrs, **g})
        # если ошибка, повторяем запрос
        if 'error' in res.json().keys():
            if res.json()['error']['error_msg'] == 'Too many requests per second':
                time.sleep(0.3)
                res = requests.get(url2, params={**self.parametrs, **g})

        d.update(self.update_catalog(res))
        return d

    # test function
    def users_get(self, user_ids):
        """

        :param user_ids: список из id пользователей vk
        :return: словарь с ключем id, именем и фамилией
        """

        d = {}
        url2 = 'https://api.vk.com/method/users.get'
        p = {}
        # убираем id по которым уже есть информация
        for i in tuple(user_ids):
            if i in self.catalog:
                p[i] = self.catalog[i]
        u = user_ids.copy()
        for t in p.keys():
            u.remove(t)

        # защита от JSONDecodeError, ограничение на длинну запроса
        for i in range(len(u) // 250 + 1):
            # подан список, делаем из него строку с id, разделённую запятыми
            user_ids_str = (','.join(map(str, u[i * 250:(i + 1) * 250])))
            g = {'user_ids': user_ids_str, 'fields': 'sex'}
            res = requests.get(url2, params={**self.parametrs, **g})
            if 'error' in res.json().keys():
                if res.json()['error']['error_msg'] == 'Too many requests per second':
                    time.sleep(0.3)
                    res = requests.get(url2, params={**self.parametrs, **g})
            k = self.update_catalog(res)
            d.update(k)
        d.update(p)
        return d

    # не забыть очистить
    def user_get(self, user_ids):
        """

        :param user_ids: id пользователя VK или список из id
        :return: словарь с ключем id, именем и фамилией
        """

        d = {}
        url2 = 'https://api.vk.com/method/users.get'
        if type(user_ids) == int or (type(user_ids) == list and len(user_ids) == 1):
            if type(user_ids) == list:
                user_ids = int(user_ids[0])
            if user_ids in self.catalog:
                d[user_ids] = self.catalog[user_ids]
                return d
            g = {'user_ids': user_ids, 'fields': 'sex'}
            res = requests.get(url2, params={**self.parametrs, **g})
            if 'error' in res.json().keys():
                if res.json()['error']['error_msg'] == 'Too many requests per second':
                    time.sleep(0.3)
                    res = requests.get(url2, params={**self.parametrs, **g})
            d.update(self.update_catalog(res))
            return d

        p = {}

        # если подан список, делаем из него строку с id, разделённую запятыми
        if len(user_ids) > 1:
            for i in tuple(user_ids):
                if i in self.catalog:
                    p[i] = self.catalog[i]
            u = user_ids.copy()
            for t in p.keys():
                u.remove(t)

            # защита от JSONDecodeError
            for i in range(len(u) // 250 + 1):
                user_ids_str = (','.join(map(str, u[i * 250:(i + 1) * 250])))
                g = {'user_ids': user_ids_str, 'fields': 'sex'}
                res = requests.get(url2, params={**self.parametrs, **g})
                if 'error' in res.json().keys():
                    if res.json()['error']['error_msg'] == 'Too many requests per second':
                        time.sleep(0.3)
                        res = requests.get(url2, params={**self.parametrs, **g})
                k = self.update_catalog(res)
                d.update(k)
        d.update(p)
        return d

    def get_friends(self, user_id):
        """

        :param user_id: id пользователя VK
        :return: множество id друзей
        """
        url = 'https://api.vk.com/method/friends.get'
        res = self.user_get1(user_id)
        if user_id in res:
            res = res[user_id]  # зачем это было нужно???
        self.catalog[user_id] = res
        idset = set()
        self.parametrs['user_id'] = user_id
        ans = requests.get(url, self.parametrs).json()
        if 'response' in ans.keys():
            idset = ans['response']['items']
        self.users_get(list(idset))
        return idset

    def cross_friends(self, user_id1, user_id2):
        """

        :param user_id1: id пользователя VK
        :param user_id2: id пользователя VK
        :return: список, состоящий из id общих друзей
        """
        url = 'https://api.vk.com/method/friends.getMutual'
        par = {'source_uid': user_id1, 'target_uid': user_id2}

        res = requests.get(url, params={**par, **self.parametrs})
        if 'error' in res.json():
            return []

        self.catalog.update(self.user_get(res.json()['response']))
        return res.json()['response']

    def do_request_cross_friend(self, user_id1, tg_uids):
        """

        :param user_id1: id пользователя VK
        :param tg_uids: список id пользователей с которыми производится проверка на общих друзей
        :return: ответ на запрос в виде словаря
        """
        url = 'https://api.vk.com/method/friends.getMutual'
        s = str(tg_uids)
        # s = tg_uids.__str__()
        s = s.replace(' ', '').replace('[', '').replace(']', '')
        par = {'source_uid': user_id1, 'target_uids': s}
        res = requests.get(url, params={**par, **self.parametrs})
        return res.json()

    def crossing_friends_count(self, user_id1, user_ids):
        """

        :param user_id1: id пользователя VK
        :param user_ids: список id пользователей с которыми производится проверка на общих друзей
        :return: словарь, где ключ это количество общих друзей, а значение - список ид с таким колличеством
        """
        step = 10
        d = {0: []}
        lst_err = []
        for_chek = []
        ite = len(user_ids) // step
        for i in range(ite + 1):
            ans = self.do_request_cross_friend(user_id1, user_ids[i * step:(i + 1) * step])
            if 'error' in ans:
                lst_err.extend(user_ids[i * step:(i + 1) * step])
                continue
            ans = ans['response']
            for_chek.clear()
            for usr in ans:
                for_chek.append(usr['id'])
                if usr['common_count'] in d.keys():
                    g = d[usr['common_count']]
                    g.append(usr['id'])
                    # d[usr['common_count']].append(usr['id'])
                else:
                    d[usr['common_count']] = ([usr['id']])
            self.catalog.update(self.user_get(for_chek))
            print('Обработано ', step * (i + 1))
        while step != 1:
            step = step // 2
            ite = len(lst_err) // step
            for i in range(ite, -1, -1):
                x = lst_err[i * step:(i + 1) * step]
                ans = self.do_request_cross_friend(user_id1, x)
                if 'error' not in ans:
                    p = x
                    for y in p:
                        lst_err.remove(y)
                    ans = ans['response']
                    for_chek.clear()
                    for usr in ans:
                        for_chek.append(usr['id'])
                        if usr['common_count'] in d.keys():
                            g = d[usr['common_count']]
                            g.append(usr['id'])
                            # d[usr['common_count']].append(usr['id'])
                        else:
                            d[usr['common_count']] = ([usr['id']])

                    self.catalog.update(self.user_get(for_chek))
                else:
                    continue
        return d

    def friends_friends(self, kort):
        """

        :param kort: принимает кортеж из id, для которых нужно получить списки друзей
        :return: словарь, где каждому принятому id соответствует список его друзей
        """
        url = 'https://api.vk.com/method/execute.get25frends'
        kort = tuple(kort)
        d = {}
        s = kort.__str__()
        s = s.replace(' ', '').replace('(', '').replace(')', '')
        res = requests.get(url, params={'korteg': s, 'access_token': self.parametrs['access_token'], 'v': 5.90})
        ans = res.json()
        r = ans['response']
        for i in range(len(kort)):
            if r[i] != False:
                d[kort[i]] = r[i]['items']
            else:
                d[kort[i]] = []
        return d

    def get_friends_friends(self, user_id):
        """

        :param user_id: id пользователя
        :return: словарь с ключами id и значениями списков друзей
        """
        friends = tuple(self.get_friends(user_id=user_id))
        d = {}

        ite = len(friends) // 25
        for i in range(ite + 1):
            y = self.friends_friends(friends[25 * i:25 * (i + 1) - i])
            # [self.user_get(y[_id]) for _id in y.keys()]
            d.update(y)
            print('Обработано ', 25 * (i + 1))
        return d

    def graph_builder1(self, graph):
        for ids in self.friends_dikt.keys():
            for friends in self.friends_dikt[ids]:
                for t in self.friends_dikt.keys():
                    if ids != t:
                        if friends == t:
                            # if friends in self.friends_dikt[t]:
                            if ids in self.catalog:
                                if t in self.catalog:
                                    graph.add_node(self.catalog[ids][0] + '\n' + self.catalog[ids][1])
                                    graph.add_node(self.catalog[t][0] + '\n' + self.catalog[t][1])
                                    graph.add_edge(self.catalog[ids][0] + '\n' + self.catalog[ids][1],
                                                   self.catalog[t][0] + '\n' + self.catalog[t][1])
        return graph

    def graph_builder2(self, graf):
        for ids in self.friends_dikt.keys():
            for friends in self.friends_dikt[ids]:
                for t in self.friends_dikt.keys():
                    if friends in self.friends_dikt[t]:
                        if t in self.catalog:
                            if friends in self.catalog:
                                graf.add_node(self.catalog[friends][0] + '\n' + self.catalog[friends][1])
                                graf.add_node(self.catalog[t][0] + '\n' + self.catalog[t][1])
                                graf.add_edge(self.catalog[friends][0] + '\n' + self.catalog[friends][1],
                                              self.catalog[t][0] + '\n' + self.catalog[t][1])
                            break
        return graf

    def remuve_nodes_with_1edge(self, graf):
        remuve = []
        for nodes in graf.degree:
            if nodes[1] == 1 or nodes[1] == 0:
                remuve += [nodes[0]]
        graf.remove_nodes_from(remuve)
        return graf
