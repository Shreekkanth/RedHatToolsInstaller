# Red Hat Laptop Setup
This is a first attempt to write an ansible playbook that assists user getting all the basics in place that they want on a Red Hat Laptop.

The ansible playbook is using tags for each section. The following tags are implemented so far:
```
$ ansible-playbook --list-tags setup.yml 
 [WARNING]: provided hosts list is empty, only localhost is available


playbook: setup.yml

  play #1 (localhost): localhost	TAGS: []
      TASK TAGS: [always, certificates, kerberos, openvpn, packages]
```

This means that you can choose to implement everything at once, or just one specific tag at a time, you can also skip one or several tags if you want almost everything.

## Installation Examples

### Prerequisites

Sadly, since ansible requires python and split into several modules its not in there by default on many system. Which means before you can configure the system with ansible you need to add additional packages to the default installation. The following is needed:

```
$ sudo yum install -y ansible git curl libselinux-python python2-dnf
$ git clone https://gitlab.consulting.redhat.com/arydekul/rh-laptop-setup.git
$ cd rh-laptop-setup
```


### Install everything

```
$ ansible-playbook --ask-sudo-pass setup.yml -e rh_username=arydekul
```

As you can tell by the above command, we require four things.
  1. Ansible with the required modules and packages
  2. A clone of this repository with all files
  3. Sudo permissions, either to run it without a password or by supplying a password on runtime
  4. Learning what your Red Hat Username is. Not assuming you are using the same at your laptop

### Install Certificates only

```
$ ansible-playbook --ask-sudo-pass setup.yml -e rh_username=arydekul -t certificates
```

### Install everything but kerberos

```
$ ansible-playbook --ask-sudo-pass setup.yml -e rh_username=arydekul --skip-tags kerberos
