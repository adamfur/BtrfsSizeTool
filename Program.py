#!/usr/bin/python
import hashlib
import sys
import re
import lz4
from Entry import Entry
from Index import Index
from Subvolume import Subvolume


def aggregateArgv(start):
    result = []

    for x in range(start, len(sys.argv)):
        result.append(sys.argv[x])

    return result

class Program:
    def __init__(self):
        self.index = Index()
        self.folder = ".btrfs"
        self.matchAllocation = re.compile("^inode (\d+) file offset (\d+) len (\d+) disk start (\d+) offset (\d+) gen (\d+) flags (\w+) (.*)$")
        self.subvolume = Subvolume()

    def start(self):
        self.index.create()
        self.index.scan()

    def logic(self, list):
        print list
        sum = 0
        lookup = {}
        for item in list:
            hex = hashlib.sha1(item).hexdigest()
            file = self.folder + "/" + hex + ".lz4"

            print "processing: " + file
            with open(file, "r") as fd:
                compressed = fd.read()
                decompressed = lz4.decompress(compressed)
                lines = decompressed.split('\n')

                for line in lines:
                    file = Entry(line)

                    if file.sha1 in lookup:
                        continue

                    lookup[file.sha1] = True
                    sum += file.size

        print "Accumulated size is: ", self.printSize(sum)

    def remove(self, list):
        omega, crap = self.buildLookup(self.subvolume.listSubvolumes())
        exclude, files = self.buildLookup(list)
        result = self.blabla(omega, exclude, files)

        print "Accumulated freed size is: ", self.printSize(result)
        #print "Files to remove: ", result

    def blabla(self, omega, exclude, files):
        sum = 0

        for key in exclude:
            if omega[key] == exclude[key]:
                sum += files[key].size
                pass

        return sum

    def buildLookup(self, subvolumes):
        lookup = {}
        files = {}

        for subvolume in subvolumes:
            print "* " + subvolume
            hex = hashlib.sha1(subvolume).hexdigest()
            file = self.folder + "/" + hex + ".lz4"

            with open(file, "r") as fd:
                compressed = fd.read()
                decompressed = lz4.decompress(compressed)
                lines = decompressed.split('\n')

                for line in lines:
                    entry = Entry(line)
                    files[entry.sha1] = entry

                    if entry.sha1 in lookup:
                        lookup[entry.sha1] += 1
                    else:
                        lookup[entry.sha1] = 1

        return lookup, files

    def printSize(self, size):
        kb = 1024
        mb = kb*kb
        gb = kb*mb
        resolution = 3

        if (size >= gb):
            return str(round(size / float(gb), resolution)) + " gb"
        elif (size >= mb):
            return str(round(size / float(mb), resolution)) + " mb"
        elif (size >= kb):
            return str(round(size / float(kb), resolution)) + " kb"

        return str(size) + " b"

program = Program()

program.start()

print "-------------------------------------------------------------------------"

if len(sys.argv) > 1:
    if sys.argv[1] == "consume":
        program.logic(aggregateArgv(2))
    elif sys.argv[1] == "remove":
        program.remove(aggregateArgv(2))