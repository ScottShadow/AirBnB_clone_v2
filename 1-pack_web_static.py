#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack.
"""
import os
from datetime import datetime
from fabric.api import local, runs_once


@runs_once
def do_pack():
    """
    Packs the static files of the web_static folder into a .tgz archive.

    Returns:
        str or None: The path of the created archive, or None if the packing
        process fails.
    """
    # Check if the 'versions' directory exists, create it if not.
    if not os.path.isdir("versions"):
        os.mkdir("versions")

    # Get the current date and time and format it as a string.
    time = datetime.now().strftime("%Y%m%d%H%M%S")

    # Construct the path for the archive file.
    output = f"versions/web_static_{time}.tgz"

    try:
        # Print the path of the archive being created.
        print(f"Packing web_static to {output}")

        # Use the 'tar' command to create the archive.
        local(f"tar -cvzf {output} web_static")

        # Get the size of the created archive.
        size = os.stat(output).st_size

        # Print the size of the created archive.
        print(f"web_static packed: {output} -> {size} Bytes")

    except Exception:
        # If the packing process fails, set the output to None.
        output = None

    # Return the path of the created archive or None.
    return output
