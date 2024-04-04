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
    """generates a .tgz archive from the contents of the web_static folder"""
    local("mkdir -p versions")
    local("tar -cvzf versions/web_static_$(date '+%Y%m%d%H%M%S').tgz web_static")

    return "versions/web_static_$(date '+%Y%m%d%H%M%S').tgz"
