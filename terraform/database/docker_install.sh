#!/bin/bash -e
echo "============================================================================================="
echo "Installing Docker"
echo "============================================================================================="
sudo apt-get update
sudo apt-get install -qy apt-transport-https ca-certificates curl gnupg lsb-release
sudo rm -f /usr/share/keyrings/docker-archive-keyring.gpg
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
sudo bash -c "echo \"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null"
sudo apt-get update
sudo apt-get install -qy docker-ce docker-ce-cli containerd.io
sudo docker swarm init --default-addr-pool 12.20.0.0/16 --default-addr-pool-mask-length 26
sudo usermod -aG docker admin
mkdir -p /opt/orp/infrastructure
sudo sysctl -w net.ipv4.ip_forward=1
sudo systemctl restart docker
sudo apt-get install unzip