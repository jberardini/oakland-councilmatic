# -*- mode: ruby -*-
# vi: set ft=ruby :

# Please don't change it unless you know what you're doing.

Vagrant.configure(2) do |config|

  # Box
  config.vm.box = "precise32"

  # Box url
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`.
  config.vm.box_check_update = false

  # Checksum on the box checked on download, box url must be specified
  # config.vm.box_download_checksum = true

  # Checksum type
  # config.vm.box_download_checksum_type = "sha256"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network "forwarded_port", guest: 8000, host: 8000
 

  # Enable provisioning with a shell script.
  config.vm.provision :shell, path: "vagrant-setup.sh"

  # Set the amount of RAM the virtual machine has access to
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end

  ########### CONTENT BELOW FROM DEFAULT VAGRANTFILE ##########

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

end
