#!/bin/sh

#sudo mkdir -p /var/log/microdom
#sudo chmod 0777 /var/log/microdom
#sudo cp -uva etc/microdom.conf /etc

echo "Building microdom-cloud-home docker image..."
docker build -t microdom-cloud-home .
echo "Stop microdom-cloud-home..."
docker stop microdom-cloud-home
sleep 1
echo "Remove microdom-cloud-home..."
docker rm microdom-cloud-home
sleep 1
docker run -it \
  -d --restart unless-stopped \
  -e DBUSER=dompi_cloud \
  -e DBPASSWORD=dompi_cloud \
  -e DBHOST=192.168.10.32 \
  -e DBNAME=DB_DOMPICLOUD \
  --name microdom-cloud-home \
  -v /var/log/microdom:/app/logs \
  -p 8080:8080 microdom-cloud-home
