import threading
import time


class Pet:
    def __init__(self):
        self.age = 0

    def plus(self):
        while self.age < 10:
            self.age += 1
            print('___________', self.age)
            time.sleep(1)

    def t(self):
        threading.Thread(target=self.plus).start()


def spam():
    for i in range(10):
        print('spam')
        time.sleep(1)


pet = Pet()
pet.t()
spam()
