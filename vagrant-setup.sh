#update package listings
sudo apt-get update

#install useful linux packages
sudo apt-get install -y git python python-dev python-pip python-virtualenv postgresql libpq-dev postgis postgresql-9.1-postgis poppler-utils gdal-bin vim

# upgrade to most recent pip
sudo pip install -U pip

# install useful python packages
sudo pip install psycopg2

# set up requirements
 cd /vagrant
sudo pip install -r requirements.txt


#set up postgres for vagrant
# sudo -u postgres createuser root -s
# sudo -u postgres createuser vagrant -s
# createdb vagrant
