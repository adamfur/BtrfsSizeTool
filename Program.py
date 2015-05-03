#!/usr/bin/python
import hashlib
import sys
import re
from Entry import Entry
from Index import Index


class Program:
    def __init__(self):
        self.index = Index()
        self.folder = ".btrfs"
        self.matchAllocation = re.compile("^inode (\d+) file offset (\d+) len (\d+) disk start (\d+) offset (\d+) gen (\d+) flags (\w+) (.*)$")

    def start(self):
        self.index.create()
        self.index.scan()

    def logic(self, list):
        print list
        sum = 0
        lookup = {}
        for item in list:
            hex = hashlib.sha1(item).hexdigest()
            file = self.folder + "/" + hex

            print "processing: " + file
            with open(file, "r") as f:
                for line in f:
                    file = Entry(line)

                    if file.sha1 in lookup:
                        continue

                    lookup[file.sha1] = True
                    sum += file.size

        print "Accumulated size is: ", self.printSize(sum)

    def printSize(self, size):
        kb = 1024
        mb = kb*kb
        gb = kb*mb

        if (size >= gb):
            return str(round(size / float(gb), 2)) + " gb"
        elif (size >= mb):
            return str(round(size / float(mb), 2)) + " mb"
        elif (size >= kb):
            return str(round(size / float(kb), 2)) + " kb"

        return size



program = Program()

program.start()

print "-------------------------------------------------------------------------"
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

if len(sys.argv) > 1:
    if sys.argv[1] == "consume":
        list = []
        for x in range(2, len(sys.argv)):
            list.append(sys.argv[x])

        program.logic(list)