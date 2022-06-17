#!/bin/bash

# basic requirements
sudo apt update
sudo apt-get install build-essential -y
sudo apt install git -y curl wget


# install brew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/home/ubuntu/.linuxbrew/bin/brew shellenv)"' >> /home/ubuntu/.profile
eval "$(/home/ubuntu/.linuxbrew/bin/brew shellenv)"
brew install gcc

#test -d ~/.linuxbrew && eval "$(~/.linuxbrew/bin/brew shellenv)"
#test -d /home/linuxbrew/.linuxbrew && eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
#test -r ~/.bash_profile && echo "eval \"\$($(brew --prefix)/bin/brew shellenv)\"" >> ~/.bash_profile
#echo "eval \"\$($(brew --prefix)/bin/brew shellenv)\"" >> ~/.profile

# install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

## configure aws account
aws configure


# Docker
sudo apt-get install docker.io -y

## add current user to docker user group
## to run docker commands without sudo
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo usermod -aG docker $USER
## you should restart instance if still need sudo

## install codedeploy agent with ruby 3
sudo apt-get install ruby-full ruby-webrick wget -y
cd /tmp
wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/releases/codedeploy-agent_1.3.2-1902_all.deb
mkdir codedeploy-agent_1.3.2-1902_ubuntu22
dpkg-deb -R codedeploy-agent_1.3.2-1902_all.deb codedeploy-agent_1.3.2-1902_ubuntu22
sed 's/Depends:.*/Depends:ruby3.0/' -i ./codedeploy-agent_1.3.2-1902_ubuntu22/DEBIAN/control
dpkg-deb -b codedeploy-agent_1.3.2-1902_ubuntu22/
sudo dpkg -i codedeploy-agent_1.3.2-1902_ubuntu22.deb
systemctl list-units --type=service | grep codedeploy
sudo service codedeploy-agent start
cd ~

# Optional: Virtual env
brew install pyenv pyenv-virtualenv
pyenv install 3.10.4
pyenv virtualenv 3.10.4 py310
pyenv global py310

# reboot instance to change docker permissions