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
    """Archives the static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    output = f"versions/web_static_{time}.tgz"
    try:
        print(f"Packing web_static to {output}")
        local(f"tar -cvzf {output} web_static")
        size = os.stat(output).st_size
        print(f"web_static packed: {output} -> {size} Bytes")
    except Exception:
        output = None
    return output
