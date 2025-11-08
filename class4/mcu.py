class gpio:
    def __init__(self):
        self._D0 = 16
        self._D1 = 5
        self._D2 = 4
        self._D3 = 0
        self._D4 = 2
        self._D5 = 14
        self._D6 = 12
        self._D7 = 13
        self._D8 = 15
        self._SDD3 = 10
        self._SDD2 = 9

    @property
    def D0(self):
        return self._D0

    @property
    def D1(self):
        return self._D1

    @property
    def D2(self):
        return self._D2

    @property
    def D3(self):
        return self._D3

    @property
    def D4(self):
        return self._D4

    @property
    def D5(self):
        return self._D5

    @property
    def D6(self):
        return self._D6

    @property
    def D7(self):
        return self._D7

    @property
    def D8(self):
        return self._D8

    @property
    def SDD3(self):
        return self._SDD3

    @property
    def SDD2(self):
        return self._SDD2
