sudo apt update
sudo apt install git -y

git clone https://github.com/AAYUSH-SAHAY-24326711019/ERP_College_Django.git

sudo systemctl stop docker
sudo systemctl stop docker.socket
sudo apt purge -y docker.io docker-buildx docker-compose python3-compose python3-docker python3-dockerpty
sudo apt autoremove -y
sudo apt autoclean

sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
sudo rm -rf /etc/docker
sudo rm -rf ~/.docker

sudo apt install -y docker.io docker-compose-v2
sudo systemctl enable docker
sudo systemctl start docker
docker pull postgres:15

git clone https://github.com/AAYUSH-SAHAY-24326711019/ERP_College_Django.git
cd ERP_College_Django/ExecutableCodes/erpCollege
docker image ls
docker run --name test_erp_db_pgsql -e POSTGRES_PASSWORD=root -p 5432:5432 -d postgres:15
docker exec -it test_erp_db_pgsql psql -U postgres
cp erp_db.sql /home/aayush/Desktop/
docker exec -i test_erp_db_pgsql psql -U postgres -d erp_db < /home/aayush/Desktop/erp_db.sql

cd erpCollege
nano settings.py
# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'erp_db',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'test_erp_db_pgsql',
        'PORT': '5432',
    }
}

# create docker file(refer to the docker file there ExecutableCodes/erpCollege as Dockerfile)

docker build -t erpcollege_app .
stop the postgres container

docker network create erp_network
docker network inspect erp_network
docker network connect erp_network test_erp_db_pgsql

start the postgres container
then inspect the erp_network

docker run --name erpcollege_container --network erp_network -p 8000:8000 -d erpcollege_app
then inspect the erp_network

check the logs
docker logs -f erpcollege_container
check the logs

cleanup ..
docker ps -a
stop the containers by id : docker stop <id>
delete the containers by id : docker rm <id>
docker network ls
delete the network by id : docker network rm <id>
docker image ls
delete the image by id : docker rmi <id>




#run success