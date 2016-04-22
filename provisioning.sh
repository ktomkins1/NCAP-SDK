#!/usr/bin/env bash
#
# Vagrant provisioning script
#
# Copyright 2016, James Ethridge <jeethridge@gmail.com>
# License: MIT
#
echo "Running Provisiong Script"
#Update
echo "Updating..."
sudo apt-get update

echo "Setting up Python..."
# Set up python
sudo apt-get install python-dev python-pip -q -y
#cd /vagrant
pip install tox
python setup.py install

echo "Setting up Prosody..."
# Install Prosody XMPP server
sudo apt-get install prosody -y
# Place config
sudo cp prosody.cfg.lua /etc/prosody/prosody.cfg.lua

sudo /etc/init.d/prosody restart

sudo prosodyctl register developer ncaplite.loc mypassword
sudo prosodyctl register ncap      ncaplite.loc mypassword
sudo prosodyctl register unittest  ncaplite.loc mypassword
