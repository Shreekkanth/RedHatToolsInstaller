Ansible-tasks-flowchart-role
=========

Given a task list in an Ansible role on a Bitbucket Git repo, this role
will take that main.yml and convert the list of tasks into a flowchart. The generated files are stored in the
playbook repo under the ``./svg`` folder for SVGs and ``./pngs`` for PNGs.

This role only works if all the Ansible role tasks are listed in a single ``./tasks/`` file. For example ``./tasks/main.yml``.   This role does not take into account ``when:`` statements (conditionals). It just prints out all the task list in a flowchart diagram. Example

![Sample FLowchart output](https://docs.google.com/uc?id=0BxEoKNT8HmJ6WUphOEdVckVobHM)


Requirements
------------

Requires NodeJS 6+ running on the localhost and the following NPM apps

* [diagrams](https://www.npmjs.com/package/diagrams)
* [svgexport](https://www.npmjs.com/package/svgexport)

Role Variables
--------------

* ``list_of_roles``:  Assumes that one manages their roles in separate Git repos.
Provide a list of Ansible role repos that this role will iterate through and
print out the flow chart


* ``git_repo_base_url``: Base url for the Git repo. Example:  ``https://github.com``

* ``git_repo_prefix``: The URL prefix before one mentions the role name.  Example: ``{{ git_repo_base_url}}/network-automation``


* ``branch_name``: define from which branch to pull the main.yml from. Default is ``master``.

* ``task_file_name``: The name of the task file to parse. By default it is ``main.yml``

* ``npm_config_prefix``:  Location of NPM files. ``diagrams`` and ``svgexport`` NodeJS apps are stored in the bin directory of this folder.

Dependencies
------------

This module depends of two modules available from Ansible Galaxy. These modules
are [geerlingguy.repo-epel](https://github.com/geerlingguy/ansible-role-repo-epel) and [geerlinguy.nodejs](https://github.com/geerlingguy/ansible-role-nodejs). Both of these are defined in
the ``meta/main.yml`` of this repo.

It is not a requirement to use these Ansible roles. You just need to find a way to get Node.js
 [diagrams](https://www.npmjs.com/package/diagrams) and [svgexport](https://www.npmjs.com/package/svgexport) onto the localhost where this playbook is run.

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
           git_repo_base_url: "http://stash.cdk.com/"
           git_repo_prefix: "{{ git_repo_base_url}}/projects/PSSAP/repos/"
           npm_config_prefix: "/usr/local/lib/npm"

```

License
-------

MIT

Author Information
------------------

Stanley Karunditu ( Red Hat Contractor )
