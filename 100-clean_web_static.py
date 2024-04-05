#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import *

env.hosts = ["54.85.131.209", "100.25.163.221"]


def do_clean(number=0):
    """
    Function to clean out-of-date archives.

    Args:
        number (int): Number of archives to clean. Defaults to 0.
    """

    # Convert number to int and set to 1 if 0
    number = 1 if int(number) == 0 else int(number)

    # Sort archives and remove specified number
    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]

    # Change local directory and remove archives
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    # Change remote directory and remove archives
    with cd("/data/web_static/releases"):
        # Get list of archives and filter for web_static_
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        # Remove specified number of archives
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
