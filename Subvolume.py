import re
from subprocess import Popen, PIPE, STDOUT


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


