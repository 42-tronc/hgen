#!/usr/bin/env python3

from configparser import ConfigParser
from enum import IntEnum
from sys import argv


class Version(IntEnum):
    Major = 0
    Minor = 1
    Patch = 2


def version_up(file: ConfigParser, update: Version):
    ver = [int(v) for v in file["metadata"]["version"].split(".")]
    ver[update] += 1
    for i in range(2, update, -1):
        ver[i] = 0
    return ".".join(str(v) for v in ver)


if __name__ == "__main__":
    # Determine the version component to update (Major, Minor, or Patch)
    to_update = Version[argv[1]] if len(argv[1:]) else Version.Patch

    # Read the setup.cfg file
    file = ConfigParser()
    file.read("setup.cfg")

    # Generate the new version
    new_ver = version_up(file, to_update)

    # Print the new version to STDOUT
    print(new_ver)

    # Update the version in the setup.cfg file
    file.set("metadata", "version", new_ver)
    file.write(open("setup.cfg", "w"))
