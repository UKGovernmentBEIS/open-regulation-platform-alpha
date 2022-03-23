<!---
2021 Alastair McKinley (a.mckinley@analyticsengines.com)
-->

# Development System Deployment

Begin by cloning the ORP Alpha Git Repository

```bash
git clone git@github.com:analyticsengines/orp_alpha.git
cd orp_alpha
```

The development system is designed to be deployed using Docker Swarm.

This works on many flavours of Linux and instructions are document for Debian 10.

On a fresh Debian 10 VM, run the following commands to install docker

```bash
sudo apt-get update
sudo apt-get install -qy apt-transport-https ca-certificates curl gnupg lsb-release
sudo rm -f /usr/share/keyrings/docker-archive-keyring.gpg
curl -fsSL https://download.docker.com/linux/debian/gpg | \
    sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
sudo bash -c "\
    echo \"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
    https://download.docker.com/linux/debian $(lsb_release -cs) stable\" \
    | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null\
"
sudo apt-get update
sudo apt-get install -qy docker-ce docker-ce-cli containerd.io
sudo docker swarm init --default-addr-pool 12.20.0.0/16 --default-addr-pool-mask-length 26
sudo usermod -aG docker admin
mkdir -p /opt/orp/infrastructure
sudo sysctl -w net.ipv4.ip_forward=1
sudo systemctl restart docker
sudo apt-get install unzip
```

Other package prerequisites for deploying and running the tests are ```tput```, ```httpie``` and ```virtualenv```.

Having installed the prerequisites and docker, simply run the deployment of the dev stack with the test data set by running ```./redeploy.sh```.

For local docker deployments, in ```build.sh``` change ```--build-arg API_BASE_URL=/``` to ```--build-arg API_BASE_URL=http://localhost:3001/```.

For AWS deployments, change the credentials (in particular, the JWT token) in each of the container services ```*.env``` files to new values before deployment with ```./redeploy.sh```.

To execute the tests run ```./redeploy_and_test.sh```.

# Streamlit Demo App Deployment

To run the Streamlit demo app, execute ```cd api_demo && ./run_demo.sh``` from the top level of the project.  Navigate in your web browser to http://127.0.0.1:8501 to view the contents page.

