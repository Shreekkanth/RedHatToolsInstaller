# A collection of playbooks I use. #

**These are completely unsupported!**

## Red Hat ##

If you want to run Red Hat containers on your Fedora machine, you will need to
register it with Red Hat. The playbook `setup_fedora_laptop.yml` supports this,
provided you run the following commands:

```
$ export SUB_USERNAME='username'
$ ansible-playbook -i 'localhost,' -c local setup_fedora_laptop.yml \
  -e rhsm_user="${SUB_USERNAME}"
```

\* Replace `SUB_USERNAME` with your Red Hat username.

[Reference][1] for subscribing Fedora to Red Hat.


[1]: https://mojo.redhat.com/docs/DOC-1143808
