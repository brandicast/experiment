from lib.abstract import mathematic


class increment (mathematic):

    def getName(self):
        return __name__

    def apply(self, number):
        return number + 1
