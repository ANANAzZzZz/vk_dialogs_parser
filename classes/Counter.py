class Counter:

    def __init__(self):
        self._value = 0


    def new_value(self):
        self._value += 1
        return self._value


    def get_value(self):
        return self._value