
Ansible-tasks-flowchart-playbook
=========

Playbook that leverages the [ansible-tasks-flowchart-role](https://gitlab.consulting.redhat.com/skarundi/ansible-task-flowchart-role).


Requirements
------------

Requires NodeJS 6+ running on the localhost and the following NPM apps

* [diagrams](https://www.npmjs.com/package/diagrams)
* [svgexport](https://www.npmjs.com/package/svgexport)


Example Playbook
----------------
```
    - hosts: localhost
      connection: local
      become: true
      roles:
         - role: ansible-task-flowchart-role
           list_of_roles:
               - linux-ansible-deploy-artifact
               - linux-java-webapp-deploy-role
           git_repo_prefix: "http://stash.cdk.com/projects/PSSAP/repos/"
           npm_config_prefix: "/usr/local/lib/npm"

```

License
-------

MIT

Author Information
------------------

Stanley Karunditu (skarundi at redhat.com)
