# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"


  #If the hostmanager plugin is available, use it.
  if Vagrant.has_plugin?("vagrant-hostmanager")

    config.hostmanager.enabled = true
    config.hostmanager.manage_host = true
    config.hostmanager.manage_guest = true
    config.hostmanager.ignore_private_ip = false
    config.hostmanager.include_offline = true

    config.vm.define 'ncaplite' do |node|
      node.vm.hostname = 'ncaplite'
      node.vm.network :private_network, ip: '10.10.100.4'
      node.hostmanager.aliases = %w(ncaplite.loc ncaplite)
    end

  else
    #otherwise we just do a plain setup
    #specify network address for the vm
    config.vm.network :private_network, ip: '10.10.100.4'
  end

  config.vm.provision :shell do |s|
    s.inline = "cd /vagrant && bash provisioning.sh"
  end

  config.vm.provider "virtualbox" do |vb|
    vb.name = "ncaplite"
    # Customize the amount of memory on the VM:
    vb.memory = "512"
    # Use 2 CPUs
    vb.cpus = 1
  end
end
