class Wordlist():
    def __init__(self):
        self.sequence = 1;
        self.dictionary = {}

    def add(self, word):
        index = self.sequence
        self.sequence += 1

        if (word in self.dictionary):
            return self.dictionary[word]

        self.dictionary[word] = index
        return index