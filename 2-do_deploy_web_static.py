#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from datetime import datetime
from fabric.api import *
import os

env.hosts = ["54.85.131.209", "100.25.163.221"]
env.user = "ubuntu"


def do_pack():
    """
        return the archive path
    """

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    arch_file_path = f"versions/web_static_{date}.tgz"
    t_gzip = local(f"tar -cvzf {arch_file_path} web_static")

    if t_gzip.succeeded:
        return arch_file_path
    else:
        return None


def do_deploy(archive_path):
    """
        Distribute archive.
    """
    print("Deploying archive: {}".format(archive_path))
    if os.path.exists(archive_path):
        print(f"Archive exists{archive_path}, continuing with deployment...")
        archived_file = archive_path[9:]
        print("Archived file: {}".format(archived_file))
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        print("Newest version: {}".format(newest_version))
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        print("Uploaded archive to tmp/")
        run("sudo mkdir -p {}".format(newest_version))
        print("Created newest version directory: {}".format(newest_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             newest_version))
        print("Extracted archive contents to: {}".format(newest_version))
        run("sudo rm {}".format(archived_file))
        print("Removed archive from tmp/")
        run("sudo mv {}/web_static/* {}".format(newest_version,
                                                newest_version))
        print("Moved contents of web_static to latest version")
        run("sudo rm -rf {}/web_static".format(newest_version))
        print("Removed empty web_static directory")
        run("sudo rm -rf /data/web_static/current")
        print("Removed current symlink")
        run("sudo ln -s {} /data/web_static/current".format(newest_version))
        print("Created symlink to latest version")

        print("New version deployed!")
        return True

    print("Archive does not exist, aborting deployment.")
    return False
