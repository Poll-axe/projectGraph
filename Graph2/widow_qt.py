import sys
import datetime

import networkx
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

import design
import MyVkApi as api


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.vk = api.MyVkApi()
        self.runbut.clicked.connect(self.btn_clk)
        self.pushButton.clicked.connect(self.clear)

    #     //////////////////////////////////////////////////////////
    #     self.figure = plt.figure()
    #     # this is the Canvas Widget that displays the `figure`
    #     # it takes the `figure` instance as a parameter to __init__
    #     self.canvas = FigureCanvas(self.figure)
    #     layout = QVBoxLayout()
    #     layout.addWidget(self.canvas)
    #     self.setLayout(layout)
    #     //////////////////////////////////////////////////////////

    def clear(self):
        self.textEdit_2.clear()
        self.vk.friends_dikt.clear()

    def btn_clk(self):
        """
        Обрабатывает нажатие кнопки и выполняет соответствующий пункт меню
        :return:
        """
        if self.menu1.isChecked():
            t = self.textEdit.toPlainText()
            try:
                user_id = [int(m) for m in t.replace(',', ' ').split()]
            except ValueError:
                self.textEdit.setText('введено не число')
                return
            user = api.MyVkApi.users_get(self.vk, user_ids=user_id)
            [self.textEdit_2.append(str('\n' + str(i) + ' ' + str(user[i]))) for i in user]

        if self.menu2.isChecked():
            t = self.textEdit.toPlainText()
            try:
                user_id = int(t)
                self.vk.working_id = user_id
            except ValueError:
                self.textEdit.setText('введено не число')
            else:
                ids = api.MyVkApi.get_friends(self.vk, user_id=user_id)
                users = api.MyVkApi.users_get(self.vk, ids)
                [self.textEdit_2.append(str(str(i) + ' ' + str(users[i]))) for i in users]
                self.textEdit_2.append(str('всего друзей ' + str(len(users))))

        if self.menu3.isChecked():
            t = self.textEdit.toPlainText()
            try:
                users = [int(i) for i in (t.split('\n'))]
                user_id1 = users[0]
                user_id2 = users[1]
            except ValueError:
                self.textEdit.setText('введено не число')
            else:
                crossset = api.MyVkApi.cross_friends(self.vk, user_id1=user_id1, user_id2=user_id2)

                self.textEdit_2.append('общих друзей ' + str(len(crossset)))
                for i in crossset:
                    s = str(self.vk.catalog[i])
                    self.textEdit_2.append(str(i) + ' ' + s)

        if self.menu4.isChecked():
            sorted(self.vk.catalog)
            with open('base.txt', 'a') as f:
                for user_id, name in self.vk.catalog.items():
                    try:
                        f.write(str(str(user_id) + ' ' + str(name) + '\n'))
                    except:
                        print(str(str(user_id) + ' ' + str(name) + '\n'))
            self.textEdit_2.append('записано в файл base.txt')
            [self.textEdit_2.append(str(str(user_id) + ' ' + str(name))) for user_id, name in self.vk.catalog.items()]
            self.textEdit_2.append(str('в базе содержится ' + str(len(self.vk.catalog))))

        if self.menu5.isChecked():
            graf = networkx.Graph()
            graf = self.vk.graph_builder1(graf)
            # graf = self.vk.remuve_nodes_with_1edge(graf)
            networkx.draw(graf, with_labels=True, pos=networkx.spring_layout(graf), node_size=500, node_color='r',
                          edge_color='g', node_shape='o')
            fig = plt.gcf()
            plt.gcf().set_size_inches(50, 50)
            now = datetime.datetime.now()
            g = (now.strftime("%d-%m-%y %I-%M"))
            print(g)
            plt.savefig(str(self.vk.catalog[self.vk.working_id]) + g + '.png')
            plt.close()
            self.textEdit_2.append('Граф по первому алгоритму построен')

            # graf = networkx.Graph()
            # graf = self.vk.graph_builder2(graf)
            # graf = self.vk.remuve_nodes_with_1edge(graf)
            # networkx.draw(graf, with_labels=True, pos=networkx.spring_layout(graf), node_size=500, node_color='r',
            #               edge_color='g', node_shape='o')
            # fig = plt.gcf()
            # plt.gcf().set_size_inches(50, 50)
            # plt.savefig(str(self.vk.catalog[self.vk.working_id]) + '2' + '.png')
            # plt.close()
            # self.textEdit_2.append('Граф по второму алгоритму построен')

        if self.menu6.isChecked():
            t = self.textEdit.toPlainText()
            try:
                user_id = int(t)
            except ValueError:
                self.textEdit.setText('введено не число')
            else:
                self.vk.working_id = user_id
                y = self.vk.get_friends_friends(user_id)
                self.vk.friends_dikt.update(y)
                self.textEdit_2.append('Готово')

        if self.menu7.isChecked():
            t = self.textEdit.toPlainText()
            try:
                user_id = int(t)
            except ValueError:
                self.textEdit.setText('введено не число')
            else:
                ids = self.vk.get_friends(user_id)
                d = self.vk.crossing_friends_count(user_id, ids)
                keys = sorted(d, reverse=True)
                for i in keys:
                    for j in d[i]:
                        fio = str(self.vk.catalog[j])
                        self.textEdit_2.append(str(str(i) + ' ' + str(j) + fio))
                self.textEdit_2.append('Готово')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
