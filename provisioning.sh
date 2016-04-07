#!/usr/bin/env bash
#
# Vagrant provisioning script
#
# Copyright 2016, James Ethridge <jeethridge@gmail.com>
# License: MIT
#

#
# Install Prosody XMPP server
sudo apt-get install prosody -y
# Place config
sudo cp /vagrant/prosody.cfg.lua /etc/prosody/prosody.cfg.lua

sudo /etc/init.d/prosody restart

sudo prosodyctl register developer ncaplite.loc mypassword
sudo prosodyctl register ncap      ncaplite.loc mypassword
sudo prosodyctl register unittest  ncaplite.loc mypassword

# Set up python
#TBD

#
# Un-comment to install nginx for static file serving
#
# apt-get install -y nginx
# cp /vagrant/nginx-default.conf /etc/nginx/sites-available/default
# /etc/init.d/nginx restart
