from plugins.abstract import mathematic


class substract (mathematic):

    def getName(self):
        return __name__

    def apply(self, number):
        return number - 1
