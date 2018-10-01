import unittest
import MyVkApi


class MyTestCase(unittest.TestCase):

    def test_user_get(self):
        a = MyVkApi.MyVkApi()
        d = MyVkApi.MyVkApi.user_get(a, 336081407)
        d1 = {336081407: ('Иванов', 'Вася', 2)}
        self.assertEquals(d, d1)
        user_id = [1, 2]
        d = MyVkApi.MyVkApi.user_get(a, user_id)
        d1 = {1: ('Дуров', 'Павел', 2), 2: ('Владимирова', 'Александра', 1)}
        self.assertEquals(d, d1)

    def test_get_friends(self):
        a = MyVkApi.MyVkApi()
        d1 = MyVkApi.MyVkApi.get_friends(a, 223825695)
        self.assertTrue(len(d1) > 0)

    def test_cross_friends(self):
        a = MyVkApi.MyVkApi()
        d1 = set(MyVkApi.MyVkApi.get_friends(a, 223825695))
        d2 = set(a.cross_friends(223825695, 223825695))
        self.assertEquals(d1, d2)

    def test_friends_friends(self):
        a = MyVkApi.MyVkApi()
        d1 = {336081407: [15860009, 26583568, 27351517, 30483369, 36460000, 45276016, 50583650, 51667445, 51714957, 53916162,
              56043335, 56474669, 59309871, 59868883, 62656556, 62768021, 66548870, 66658851, 88568320, 93003281,
              94514005, 96396064, 98991106, 102196535, 103327974, 113637487, 119510973, 124441401, 138343937, 139679594,
              145255384, 157372144, 157759248, 158750146, 159454475, 160822336, 161995527, 163321475, 173689313,
              186553202, 196077418, 199249171, 200054378, 209544378, 223825695, 226651728, 228989271, 237330522,
              238519081, 250432564, 315123739, 335927520, 345690684, 345790749, 346219128, 366872651, 374655218,
              374835491, 383749787, 389074537, 449682809, 450690121],
              66307177: [12281379, 30483369, 49757170, 50583650, 51714957, 53754488, 55274555, 56474669, 62201865, 62768021,
              64397370, 66295961, 66350027, 67553019, 72411553, 75369361, 80031463, 80716258, 81591417, 87624999,
              93003281, 95921923, 96396064, 98991106, 102196535, 103327974, 110406565, 113637487, 114648210, 119510973,
              121028846, 124441401, 139148475, 139674145, 145255384, 150397827, 151861950, 157750137, 159697592,
              163992789, 167978035, 174355943, 175475634, 178561826, 187887482, 196738351, 202561956, 211512594,
              217631916, 229333932, 238519081, 251607593, 271849809, 308198902, 315123739, 321498489, 326388708,
              346219128, 380490423, 383875424, 389074537, 449682809, 481417215]}
        d2 = a.friends_friends([336081407, 66307177])
        self.assertEquals(d1, d2)


if __name__ == '__main__':
    unittest.main()
