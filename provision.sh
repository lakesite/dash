#!/bin/sh

if [ ! -e "/home/vagrant/provisioned" ]
then
    export DEBIAN_FRONTEND=noninteractive
    apt-get update
    apt-get -y upgrade
    apt-get -y install git python3 python3-dev python3-setuptools python3-pip python-virtualenv python-mysqldb mysql-client

    # Mysql install
    echo 'mysql-server mysql-server/root_password password dash' | debconf-set-selections
    echo 'mysql-server mysql-server/root_password_again password dash' | debconf-set-selections
    apt-get install -y mysql-server > /dev/null 2>&1

    # Mysql setup
    mysqladmin -uroot -pdash create dash || exit 1
    mysql -uroot -pdash -Bse "create user 'dash'@'localhost' identified by 'dash';"
    mysql -uroot -pdash -Bse "grant all privileges on \`dash\`.* to 'dash'@'localhost';"
    mysqladmin -uroot -pdash flush-privileges || exit 1

    cat <<'EOF' > /etc/systemd/system/dash.service
    [Unit]
    Description=dash gunicorn daemon
    After=network.target

    [Service]
    User=vagrant
    Group=vagrant
    WorkingDirectory=/vagrant/
    Environment="FLASK_APP=dash"
    Environment="FLASK_ENV=development"
    Environment="APP_SETTINGS=dash.config.DevelopmentConfig"
    ExecStart=/home/vagrant/env/bin/gunicorn --workers 3 -b 0.0.0.0:5000 "dash:create_app()"

    [Install]
    WantedBy=multi-user.target
EOF

    # Install the virtualenv in ~vagrant but the project in /vagrant.
    sudo -u vagrant -H -s <<'EOF' || exit 1
cd /vagrant/
virtualenv -p /usr/bin/python3 /home/vagrant/env
source /home/vagrant/env/bin/activate
yes | pip install -r requirements.txt
export APP_SETTINGS=dash.config.DevelopmentConfig
/home/vagrant/env/bin/python /vagrant/manage.py create_db
/home/vagrant/env/bin/python /vagrant/manage.py create_admin --email=dash@lakesite.net --password=dash
EOF

    service dash start

    touch /home/vagrant/provisioned
fi
