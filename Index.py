import os
from subprocess import Popen, PIPE, STDOUT
import re
import hashlib
import lz4


class Index():
    def __init__(self):
        self.matchSubvolume = re.compile("^ID (\d+) gen (\d+) top level (\d+) path (.+)$")
        self.matchAllocation = re.compile("^inode (\d+) file offset (\d+) len (\d+) disk start (\d+) offset (\d+) gen (\d+) flags (\w+) (.*)$")
        self.folder = ".btrfs"
        pass

    def create(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def scan(self):
        p = Popen("btrfs subvolume list . | sort", shell=True, stdout=PIPE, stderr=STDOUT)

        for line in p.stdout.readlines():
            match = self.matchSubvolume.match(line)

            if match is None:
                continue

            subvolume = match.group(4)
            self.scanSubvolume(subvolume)

    def scanSubvolume(self, subvolume):
        hex = hashlib.sha1(subvolume).hexdigest()
        file = self.folder + "/" + hex + ".lz4"
        completed = self.folder + "/" + hex  + ".complete"

        print "scaning: " + subvolume + " (" + hex + ")"

        if os.path.exists(completed):
            return

        p = Popen('btrfs subvolume find-new ' + subvolume + ' 0', shell=True, stdout=PIPE, stderr=STDOUT)
        list = []

        for line in p.stdout.readlines():
            match = self.matchAllocation.match(line)

            if match is None:
                continue

            list.append(match.group(0))

        with open(file, "w") as text_file:
            text_file.write(lz4.compress("\n".join(list)))

        open(completed, 'a').close()
