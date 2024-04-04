#!/usr/bin/env bash
# configures a new Ubuntu machine

# Install nginx on web-01 server
apt-get -y update
apt-get -y install nginx

# Create directories if they do not exist
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

printf %s "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html
# Delete the symbolic link if it exists
if [ -L "/data/web_static/current" ]; then
    rm /data/web_static/current
fi

# Create the symbolic link /data/web_static/current linked to /data/web_static/releases/test/
ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

#setup nginx server block
printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    location /redirect_me {
        return 301 https://www.youtube.com/channel/UCvo9gk4s8yS-X_OV-FvKi1Q
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" > /etc/nginx/sites-available/default
#restart nginx
service nginx restart