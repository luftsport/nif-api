
class Clubs:
    def __init__(self, clubs):

        if clubs is None:
            self.value = []

        elif 'int' in clubs:
            self.value = clubs['int']

        else:
            self.value = []


