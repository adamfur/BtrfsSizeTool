class Lookup():
    def __init__(self):
        self.index = {}

    def add(self, wordId, path):
        if wordId not in self.index:
            self.index[wordId] = []

        self.index[wordId].append(path)

    def search(self, wordId):
        if wordId in self.index:
            for path in self.index[wordId]:
                print "search result: ", path
