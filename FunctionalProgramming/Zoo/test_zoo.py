import zoo
import animal


def test_listen():
    lion = animal.init_lion()
    tiger = animal.init_tiger()
    wolf = animal.init_wolf()
    my_zoo = zoo.Zoo([lion, tiger, wolf])
    zoo.listen(my_zoo)
