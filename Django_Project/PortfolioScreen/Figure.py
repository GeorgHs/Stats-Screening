from builtins import property


class Figure():

    def __init__(self, figurenameValue, figurevalueValue, figureidValue):
        self._figurename = figurenameValue
        self._figurevalue = figurevalueValue
        self._figureid = figureidValue

    @property
    def figurename(self):
        return '{}'.format(self._figurename)

    @figurename.setter
    def figurename(self, value):
        self._figurename = value

    @figurename.deleter
    def figurename(self):
        self.figurename = None


    @property
    def figurevalue(self):
        return '{}'.format(self._figurevalue)

    @figurevalue.setter
    def figurevalue(self, value):
        self._figurevalue = value



    # figureid
    @property
    def figureid(self):
        return '{}'.format(self._figureid)

    @figureid.setter
    def figureid(self, value):
        self._figureid = value

    @figureid.deleter
    def figureid(self):
        self._figureid = None