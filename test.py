
class Word:

    def __init__(self, cls):
        self._cls = cls

    def hello(self):
        print('Hello, Victor!')


@Word
class Sign:
    pass


a = Sign
print(a.hello())
