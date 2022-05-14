class Langexceldata:
    KEY = 'Key'
    def __init__(self):
        self._headerwidthws = []
        self._header = dict()

    def getheader(self):
        return self._header

    def setheader(self, plangs):
        self._header = dict()
        self._header[1] = self.KEY
        for idx, l in enumerate(plangs, start=2):
            self._header[idx] = l
        self._header[len(plangs) + 2] = 'Description'
        self._header[len(plangs) + 3] = 'Comments'

    def setheaderwidth(self,pdimensions:list):
        self._headerwidthws = pdimensions

    def getheaderwidth(self):
        return self._headerwidthws

    def getheader(self):
        return self._header

    def setheader(self, plangs):
        self._header = dict()
        self._header[1] = self.KEY
        for idx, l in enumerate(plangs, start=2):
            self._header[idx] = l
        else:
            self._header[len(plangs) + 2] = 'Description'
            self._header[len(plangs) + 3] = 'Comments'

    def getheaderlist(self):
        retval = [self._header[k] for k in sorted(self._header.keys())]
        return retval

    def analyzeheader(self, prow):
        if not (self.KEY in prow and len(prow) > 1):
            raise AssertionError("***** Header must contain 'Key' and at least one language-code")
        self._header = dict()
        for idx, title in enumerate(prow, start=1):
            self._header[idx] = title

    def keyrow(self):
        for i, v in self._header.items():
            if v == self.KEY:
                return i

    @staticmethod
    def strislang(l: str) -> bool:
        return l.lower() in SUPPORTEDLANGUAGES.keys()
