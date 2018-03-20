class Enemy:
    life = 3

    def attack(self):
        print('ouch!')
        self.life -= 1

    def check_life(self):
        if self.life <= 0:
            print('I am dead')
        else:
            print(str(self.life) + " life left")


enemy1 = Enemy()
enemy2 = Enemy()

enemy1.attack()
enemy1.attack()
enemy1.check_life()
enemy2.check_life()


class Tuna:

    def __init__(self):
        print('I am tuna')

    def swim(self):
        print('I am swimming')


flipper = Tuna()
flipper.swim()


if __name__ == '__main__':
    pass
