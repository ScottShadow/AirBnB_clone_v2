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
    Packs the "web_static" directory into a .tgz archive and returns the
    path of the created archive. If the packing process fails, returns None.
    """

    # Create the "versions" directory if it doesn't exist
    local("mkdir -p versions")

    # Get the current date and time and format it as a string
    date = datetime.now().strftime("%Y%m%d%H%M%S")

    # Construct the path for the archive file
    arch_file_path = f"versions/web_static_{date}.tgz"

    # Pack the "web_static" directory into a .tgz archive and save it to the
    # specified path
    t_gzip = local(f"tar -cvzf {arch_file_path} web_static")

    # If the packing process succeeded, return the path of the created
    # archive, otherwise return None
    if t_gzip.succeeded:
        return arch_file_path
    else:
        return None


def do_deploy(archive_path):
    """
    Deploys a new version of the web application to the web servers.

    Args:
        archive_path (str): Path to the archive file containing the new version.

    Returns:
        bool: True if the deployment was successful, False otherwise.
    """

    # Check if the archive file exists
    if os.path.exists(archive_path):

        # Extract the archive file name without the full path
        file_arch = archive_path[9:]

        # Construct the path for the new version of the application
        new_ver = "/data/web_static/releases/" + file_arch[:-4]

        # Construct the path for the temporary location of the archive file
        file_arch = "/tmp/" + file_arch

        # Transfer the archive file to the remote servers
        put(archive_path, "/tmp/")

        # Create the directory for the new version of the application
        run(f"sudo mkdir -p {new_ver}")

        # Extract the contents of the archive file to the new version directory
        run(f"sudo tar -xzf {file_arch} -C {new_ver}/")

        # Remove the temporary archive file
        run(f"sudo rm {file_arch}")

        # Move the contents of the web_static directory to the new version directory
        run(f"sudo mv {new_ver}/web_static/* {new_ver}")

        # Remove the web_static directory
        run(f"sudo rm -rf {new_ver}/web_static")

        # Remove the current version of the application
        run("sudo rm -rf /data/web_static/current")

        # Create a symbolic link to the new version of the application
        run(f"sudo ln -s {new_ver} /data/web_static/current")

        print("New version deployed!")

        # Return True to indicate successful deployment
        return True

    # Return False if the archive file does not exist
    return False
