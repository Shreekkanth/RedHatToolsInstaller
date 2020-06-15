# Installing Red Hat Satellite 6 with Vagrant and Ansible

**vagabond**
vag·a·bond | \ ˈva-gə-ˌbänd \

## _adjective_

- moving from place to place without a fixed home

## _noun_

- a person who wanders from place to place without a fixed home

---

The goal of this project is for anyone, with minimal setup and effort, to be
able to install and configure Satellite 6 current GA on a RHEL 7 virtual
machine.  In testing, it takes about 30 minutes from the time you hit enter
until the time you can log in to your newly installed Satellite server. That
time will slightly vary depending on system resources available to your virtual
environment.

## Environment Notes

The following details are essential before deploying.  As I can't anticipate
every possible environment configuration, I'll explain the current setup.
You will need to make changes to the settings if you make any modifications
to fit in your unique environment.

### Storage pool

I have configured the virtual storage pool as *default* if you are using a
different storage pool location, you will need to update the *Vagrantfile* to
reflect that change.

```ruby
    libvirt.storage_pool_name = "default"
```

>NOTE: The libvirt provider in Vagrant cannot manage LVM backed storage only
file-backed storage.

The base OS image size is 20 GB, and during installation, an additional 40 GB
image is created for the Satellite server.  Verify that you have ample space in
your storage pool.

If you would like to create a new storage pool follow the steps in
[Creating a Storage Pool](Creating_a_Storage_Pool.md).

### Memory and CPUs

The Satellite Server image is configured to be deployed with 8 GB RAM and
2 CPUs.  Those settings are already below the recommendations for a
Satellite 6 server, and I wouldn't recommend setting it any lower.
However, if you would like to make changes to the resources edit the following
lines in the _Vagrantfile_.

```ruby
      domain.memory = 8192
      domain.cpus = 2
```

## Installing Ansible On Your Hypervisor

You will need to have Ansible installed on the system that will host the virtual
Satellite Server.

### Fedora

Installing on Fedora is pretty straightforward.

```terminal
sudo dnf install ansible
```

### Red Hat Enterprise Linux 7

To install ansible on RHEL 7, you will need to enable the Ansible repo.

```terminal
sudo subscription-manager repos --enable=rhel-7-server-ansible-2.8-rpms
sudo yum install ansible
```

## Installing Vagrant

Information on installing and configuring Vagrant can be found in the
[Vagrant.md](Vagrant.md) instructions.

## Final Customizations

You will need to provide your manifest file to use during installation of the
Satellite server.  Place it in the following location.

```terminal
roles/postinstall/files/manifest.zip
```

Edit _group_vars/all/vars_ to update the name of your Organization and Location
that you'd like to use during the install.  You can also edit the username and
password of the admin user to modify to your liking.

>**NOTE:** Organization and Location names cannot contain spaces

You will also need to create an ansible vault and secret file.

```terminal
$ ansible-vault create group_vars/all/vault
New Vault password:
```

The contents of the vault file should look like:

```yml
---
rhn_user: RHN_USERNAME
rhn_pass: RHN_PASSWORD
# Employee Satellite
pool_id: 8a85f9863f14fed3013f81ba2b6120b2
```

Of course replacing the *RHN_USERNAME* and *RHN_PASSWORD* with your credentials.
Then create *secret.txt* that contains your password to decrypt the vault.

## Installing a Vagrant Box

You can create a Vagrant box if you wish, I have a
[How To](https://github.com/unxfrek/vagrant/blob/master/HOWTO-Create_Vagrant_Box.md)
for the process.  I have also created a RHEL 7.7 based box that you can
[download](http://file.rdu.redhat.com/~jhunt/vagrant/).  Once you've downloaded
the box, you will need to add it to vagrant.

>**Note:** vagrant boxes are stored at _~/.vagrant.d/boxes_ make sure you have
enough space for the box(es).

```terminal
vagrant box add --name rhel7 RHEL7.7.box
```

Once the box is in place, you should be able to view it.

```terminal
$ vagrant box list
rhel7 (libvirt, 0)
```

## Installing the Satellite Server

OK, so how does all this work?  If you have completed all the setup steps, you
are ready to install your satellite 6 server.  your directory should look like
the following.

```terminal
$ ls
ansible.cfg  Creating_a_Storage_Pool.md  group_vars  images  library  README.md
requirements.txt  roles  secret.txt  site.yml  Vagrantfile  Vagrant.md
```

You are ready to go, kick it off with the following command.

```terminal
vagrant up
```

This will install a basic Satellite 6 server, it will have the manifest imported
but no further configurations. If you would like something more fully configured
run the following command.

```terminal
ANSIBLE_TAGS=full,all vagrant up
```

In addition to installing Satellite this will enable repositories, create
lifecycle environments, content views, activation keys...etc.

So what exactly is going on?  Well, vagrant creates the system as defined in the
_Vagrantfile_.

We then move onto the provisioning process using `ansible`.

```ruby
  config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.tags = ENV['ANSIBLE_TAGS'] ||= "all"
    ansible.playbook = "site.yml"
    ansible.compatibility_mode = "2.0"
  end
```

The ansible playbook _site.yml_ is used, which works through three roles.

- preinstall - Pre-installation checks and a few other steps.
  - Package repo setup
  - Firewall configuration
  - Additional package install
  - Enable any needed services
  - Partition and create file systems from */dev/vdb*
- install - Install the satellite packages and run the satellite installer
- postinstall - Configure the installed Satellite server
  - Create Org and Location
  - Upload the manifest
  - Full Install (optional)
    - Create lifecycle environments
    - Create a few RHEL repos
    - Create a content view and add repos to the content view
    - Create activation keys
    - Create subnet
    - Create hostgroup

The whole process takes about 30 minutes, once done you can log into the
satellite server and get the IP address, the */etc/motd* is configured to
provide that information.

```terminal
$ vagrant ssh
Last login: Thu Sep 19 12:27:08 2019 from 192.168.121.1


----------------------------------------
Welcome to host sat6
RedHat 7.7 x86_64
----------------------------------------

FQDN: sat6.local
IP:  192.168.121.41

Memory:  15885 MB
----------------------------------------

You can access the Satellite 6.5 WebUI through the following links

https://192.168.121.41

or

https://sat6.local

```

You can then use that URL to access the WebUI to you new satellite server!

When you are done with the satellite server and don't need it anymore, run the
following command while the server is up.

```terminal
vagrant destroy
```

The reason you run that command with the server up, it will un-register itself
from RHSM.  If you destroy it while not online, you will have to clean up your
registrations manually.

I hope this process is useful, if you find any mistakes or typos in the
instructions, please let me know I would like to ensure everything is correct as
possible.
