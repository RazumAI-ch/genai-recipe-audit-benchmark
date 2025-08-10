#!/usr/bin/env bash
set -e

if command -v docker >/dev/null 2>&1; then
    echo "Docker already installed. Skipping installation."
    exit 0
fi

echo "Installing Docker & Docker Compose..."
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
docker --version
docker compose version

sudo usermod -aG docker "$USER"
echo "Docker installation complete. Switching to newgrp docker..."
newgrp docker <<EONG
echo "Docker group applied. You can now run Docker without sudo."