# Install Fedora like CSB in an automated manner #

## Provision your laptop ##

1. Use fedora-csb-ks.cfg
1. Search for `ADAPT` and adapt the file to your needs
1. Place it on a webserver of your choice (and trust)
1. Boot your laptop from any Fedora-Boot-ISO
1. Press tab when arrived on the Grub prompt
1. vmlinuz initrd=initrd.img ks=http://yourwebserver:yourport/fedora-csb-ks.cfg

## Configure your laptop ##

1. Adapt the file `local_vars.yml` to your needs / preferences
1. Create a file `credentials.yml` with following content (replace `wheel` with another group if you don't want your user to have sudo rights):
```
---
kerberos_user: <yourloginid>
local_group: wheel
```
1. run `./setup-machine.sh`


The following error might be due to Ansible being updated during Playbook execution, just retry:

```
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: ImportError: cannot import name AnsibleVaultEncryptedUnicode
fatal: [localhost]: FAILED! => {"failed": true, "msg": "Unexpected failure during module execution.", "stdout": ""}
```

## Configure your user ##

Once you've configured your laptop, you can login as your definitive (Kerberos)
user and execute `ansible-playbook fedora-user.yml`.
