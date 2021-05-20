# Project

Clone this repository to yput project directory


# Pyenv and Pipenv

* install and configure [pyenv](https://github.com/pyenv/pyenv)
* change directory to project's
* install Python 3.9.1 version and activate in project directory:

        pyenv install 3.9.1
        pyenv local 3.9.1

* install `pipenv`:

        pyenv exec python -m pip install pipenv

* create `.venv` subdirectory in project directory
* install required apps:

        pipenv install


# Creating gunicorn systemd units

Socket unit

    systemctl edit myfin-gunicorn.socket --full --force

Simple template for unit:

    [Unit]
    Description=MyFin Gunicorn Socket
    
    [Socket]
    ListenStream=/run/myfin-gunicorn.sock
    
    [Install]
    WantedBy=sockets.target

Service unit

    systemctl edit myfin-gunicorn.service --full --force

Simple template for unit:

    [Unit]
    Description=MyFin Gunicorn Daemon
    Requires=myfin-gunicorn.socket
    After=network.target
    
    [Service]
    User=user
    Group=group
    WorkingDirectory=/path/to/myfin
    ExecStart=/path/to/myfin/.venv/bin/gunicorn \
              --pythonpath /path/to/.pyenv/versions/3.9.1 \
              --access-logfile /path/to/myfin/logs/access.log \
              --error-logfile /path/to/myfin/logs/error.log \
              --workers 2 \
              --bind unix:/run/myfin-gunicorn.sock \
              base.wsgi:application
    
    [Install]
    WantedBy=multi-user.target

Starting units

    systemctl start myfin-gunicorn.socket
    systemctl enable myfin-gunicorn.socket
    
    systemctl start myfin-gunicorn
    systemctl enable myfin-gunicorn

Check status and journal

    systemctl status myfin-gunicorn
    journalctl -u myfin-gunicorn

# Configure nginx as proxy to gunicorn

Simple config for nginx

    server {
        listen 80;
        server_name server_domain_or_IP;
    
        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /path/to/myfin/public/;
        }
    
        location / {
            include proxy_params;
            proxy_pass http://unix:/run/myfin-gunicorn.sock;
        }
    }
