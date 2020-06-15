# How To Install and Configure Vagrant

Vagrant is a handy tool to quickly create virtual systems for all sort of uses
we will be using them for our Anisble labs.

## Installing Vagrant

By default, Vagrant uses VirtualBox as it's virtualization platform.  The
following instructions configure Vagrant to use libvirt as the default provider.

>**NOTE:** You can leave it to use VirtualBox, but I haven't done any testing of
this setup with VirtualBox.  At a minimum, you will have to modify the
_Vagrantfile_ as it is configured to use libvirt.

### Install on Fedora

Installing Vagrant on Fedora is pretty straightforward, as the package is
available in the Fedora repositories.

```terminal
sudo dnf -y install vagrant vagrant-libvirt vagrant-registration
```

### Install on Red Hat Enterprise Linux

Installing Vagrant on RHEL is more of a manual process, the package isn't
available in the RHEL repositories.  First, we must download the package from
the [Vagrant website](https://www.vagrantup.com/downloads.html).  Then install
the package.

```terminal
sudo yum localinstall vagrant_2.2.5_x86_64.rpm
```

Next, we'll install a few dependencies for the libvirt and registration plugins.

```terminal
sudo yum install -y gcc libvirt-devel
```

Then install the plugins.

```terminal
vagrant plugin install vagrant-libvirt
vagrant plugin install vagrant-registration
```

## Notes about the plugins

The `vagrant-registration` plugin will unregister your system from RHSM when you
you issue a `vagrant destroy`. It is important to remember to `destroy` your
systems when you are done with them. Otherwise your have multiple systems
consuming entitlements

## Common Configuration

Now we'll configure the vagrant group to access libvirt without authentication
for each command.

```terminal
$ sudo su -
# groupadd vagrant
# cat > /etc/polkit-1/rules.d/10-vagrant-libvirt.rules << "EOF"
polkit.addRule(function(action, subject) {
  if ((action.id == "org.libvirt.unix.manage"
    || action.id == "org.libvirt.unix.monitor")
    && subject.isInGroup("vagrant")) {
    return polkit.Result.YES;
  }
});
EOF
# usermod -a -G vagrant $USER
```

Also add your user to the libvirt group.

```terminal
sudo usermod -a -G libvirt $USER
```

>**Note:** You'll need to log out and back in for the new group memberships to
take effect.

As mentioned earlier the default virtualization provider for Vagrant is
VirtualBox; we will need to modify the settings to use libvirt instead so you
don't have to type `--provider=libvirt` every time you create a system.  To do
this edit your _~/.bashrc_ and add the following.

```bash
export VAGRANT_DEFAULT_PROVIDER=libvirt
```

Make sure you are using the updated variables from your _~/.bashrc_.

```terminal
source ~/.bashrc
```

## Installing a Vagrant Box

These playbook is configured to use the box
[rhel7](http://file.rdu.redhat.com/jhunt/vagrant/rhel7/RHEL7.7.box) from the
Vagrant boxes repository.

>**Note:** vagrant boxes are stored at _~/.vagrant.d/boxes_ make sure you have
enough space for the box(es).

## Common Vagrant Commands

Create or boot a Vagrant guest

```terminal
vagrant up
```

If you want to do the full Satellite install.

```terminal
ANSIBLE_TAGS=full,all vagrant up
```

Once a guest starts the playbook automatically runs, if you need to run the
playbook again

```terminal
vagrant provision
```

Or if you are doing the full Satellite install.

```terminal
ANSIBLE_TAGS=full,all vagrant provision
```

To log into the Vagrant guest

```terminal
vagrant ssh
```

To shutdown the Vagrant guest

```terminal
vagrant halt
```

When you are done with the system and don't need it anymore

```terminal
vagrant destroy
```
