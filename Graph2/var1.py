import MyVkApi as api
import networkx
import time


# if __name__ == '__main__':

class Getter:
    vk = api.MyVkApi()

    @staticmethod
    def print_menu():
        print()
        print('1. Информация по id')
        print('2. Получить список друзей')
        print('3. получить общих друзей')
        print('4. Вывести список известных личностей')
        print('5. построение графа')
        print('6. друзья друзей')
        print('0. Выход')
        print()

    def get_user(self):
        """

        :return: печатает информацию по запрошенному id
        """
        try:
            i = input(" 1 или несколько?\n")
            if i == '1':
                user_id = int(input('введите id\n'))
            else:
                user_id = [int(m) for m in
                           input('Введите id через пробел (допускается запятая)\n').replace(',', '').split()]
        except ValueError:
            print('введено не число')
            return

        user = api.MyVkApi.users_get(self.vk, user_ids=user_id)
        [print(i, ' ', user[i]) for i in user]
        if len(user) > 0:
            return True
        else:
            return False

    def get_user_friends(self):
        """

        :return: множество id друзей
        """
        ids = set()
        try:
            user_id = int(input('введите id\n'))
            self.vk.working_id = user_id
        except ValueError:
            print('введено не число')
            return ids
        ids = api.MyVkApi.get_friends(self.vk, user_id=user_id)
        users = api.MyVkApi.users_get(self.vk, ids)
        for i in users:
            print(i, users[i])
        print(ids)
        return ids

    def print_catalog(self):
        """

        :return: выводит на экран каталог с известными иненами с id
        """

        sorted(self.vk.catalog)
        with open('base2.txt', 'a') as f:
            for user_id, name in self.vk.catalog.items():
                f.write(str(str(user_id) + ' ' + str(name) + '\n'))
        [print(user_id, ' ', name) for user_id, name in self.vk.catalog.items()]
        print('в базе содержится ', len(self.vk.catalog))

    def cross_friends(self):
        """

        :return: список общих друзей
        """
        s = set()
        try:
            user_id1 = int(input('введите id1\n'))
            user_id2 = int(input('введите id2\n'))
        except ValueError:
            print('введено не число')
            return s

        crossset = api.MyVkApi.cross_friends(self.vk, user_id1=user_id1, user_id2=user_id2)
        print('общих друзей ', len(crossset))
        [print(i) for i in crossset]
        return crossset

    def get_friends_friends(self, user_id):
        """

        :param user_id: id пользователя
        :return: словарь с ключами id и значениями списков друзей
        """
        friends = tuple(api.MyVkApi.get_friends(self.vk, user_id=user_id))
        d = {}

        ite = len(friends) // 25
        for i in range(ite):
            y = api.MyVkApi.friends_friends(self.vk, friends[25 * i:25 * (i + 1) - i])
            [api.MyVkApi.users_get(self.vk, y[_id]) for _id in y.keys()]
            d.update(y)
            print('Обработано ', 25 * (i + 1))
        y = api.MyVkApi.friends_friends(self.vk, friends[25 * ite:])
        [api.MyVkApi.users_get(self.vk, y[_id]) for _id in y.keys()]
        d.update(y)
        return d

    def friends_friends(self):
        """

        :return: составляет словарь с информацией о друзьях с ключем по id
        """
        try:
            user_id = int(input('введите id\n'))
        except ValueError:
            print('введено не число')
            return
        self.vk.working_id = user_id
        self.vk.friends_dikt.update(Getter.get_friends_friends(self, user_id))

    def build_graf(self):
        """
        рисует граф по результатам работы функции friends_friends
        """
        graf = networkx.Graph()

        for ids in self.vk.friends_dikt.keys():
            for friends in self.vk.friends_dikt[ids]:
                for t in self.vk.friends_dikt.keys():
                    if friends == t:
                        if ids in self.vk.catalog:
                            if t in self.vk.catalog:
                                graf.add_node(self.vk.catalog[ids][0] + '\n' + self.vk.catalog[ids][1])
                                graf.add_node(self.vk.catalog[t][0] + '\n' + self.vk.catalog[t][1])
                                graf.add_edge(self.vk.catalog[ids][0] + '\n' + self.vk.catalog[ids][1],
                                              self.vk.catalog[t][0] + '\n' + self.vk.catalog[t][1])

        print(graf.size())

        # удаление вершин с одним ребром
        # remuve = []
        # for nodes in graf.degree:
        #     if nodes[1] == 1:
        #         remuve += [nodes[0]]
        # print(len(graf.nodes()))
        # graf.remove_nodes_from(remuve)
        # print(len(graf.nodes()))

        graf = self.vk.remuve_nodes_with_1edge(graf)

        networkx.draw(graf, with_labels=True, pos=networkx.spring_layout(graf), node_size=500, node_color='r',
                      edge_color='g', node_shape='o')
        import pylab as plt
        # fig, axes = plt.subplots(ncols=1, nrows=1, dpi=100, facecolor='white', edgecolor='lightblue')
        # plt.show()
        plt.gcf().set_size_inches(50, 50)
        plt.savefig(str(self.vk.catalog[self.vk.working_id]) + '1' + '.png')
        plt.close()


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////694767
if __name__ == '__main__':
    actions = {1: Getter.get_user, 2: Getter.get_user_friends, 3: Getter.cross_friends, 4: Getter.print_catalog,
               5: Getter.build_graf, 6: Getter.friends_friends, }
    sesion = Getter()
    while True:
        Getter.print_menu()
        try:
            n = int(input())
        except ValueError:
            print('Введите число')
        else:
            if n == 0:
                break
            if n in actions.keys():
                func = actions[n]
                func(sesion)
            else:
                print('данного пункта нет в меню')
