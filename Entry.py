import hashlib
import re


class Entry:
    def __init__(self, string):
        matchAllocation = re.compile("^inode (\d+) file offset (\d+) len (\d+) disk start (\d+) offset (\d+) gen (\d+) flags (\w+) (.*)$")
        match = matchAllocation.match(string)

        self.inode = match.group(1)
        self.offset = match.group(2)
        self.size = int(match.group(3))
        self.start = match.group(4)
        self.offset2 = match.group(5)
        self.gen = match.group(6)
        self.flags = match.group(7)
        self.path = match.group(8)
        self.sha1 = hashlib.sha1(self.inode + "|" + self.offset + "|" + str(self.size) + "|" + self.start + "|" + self.offset2).hexdigest()
