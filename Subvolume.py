import hashlib
import re
from subprocess import Popen, PIPE, STDOUT
import lz4


class Subvolume():
    def __init__(self):
        self.matchSubvolume = re.compile("^ID (\d+) gen (\d+) top level (\d+) path (.+)$")

    def listSubvolumes(self):
        list = []
        p = Popen("btrfs subvolume list . | sort", shell=True, stdout=PIPE, stderr=STDOUT)

        for line in p.stdout.readlines():
            match = self.matchSubvolume.match(line)

            if match is None:
                continue

            list.append(match.group(4))

        return list

    def read(self, subvolume):
            hex = hashlib.sha1(subvolume).hexdigest()
            file = ".btrfs/" + hex + ".lz4"

            with open(file, "r") as fd:
                compressed = fd.read()
                decompressed = lz4.decompress(compressed)
                return decompressed.split('\n')