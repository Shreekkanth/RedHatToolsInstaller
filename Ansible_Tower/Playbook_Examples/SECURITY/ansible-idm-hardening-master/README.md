# README (WIP)

Check the inventory file to match your environment:

* **hosts.arteixo** for arteixo deployment.

Add a non root user with sudo privileges to the inventory file. This user will be used to run the playbook:

```
ansible_user=your_user_with_sudo_privileges
```

Run the playbook:

```
$ ansible-playbook -i hosts.arteixo patch-all-idempotent-tasks.yml
```

The playbook **patch-all-non-idempotent-tasks.yml** run tasks which are not idempotent so this playbook must be executed only once:

```
$ ansible-playbook -i hosts.arteixo patch-all-non-idempotent-tasks.yml
```

After that all servers in the inventory have to be rebooted:

* To be certain that servers are in condition to boot after the changes.
* To be certain all changes are loaded.
