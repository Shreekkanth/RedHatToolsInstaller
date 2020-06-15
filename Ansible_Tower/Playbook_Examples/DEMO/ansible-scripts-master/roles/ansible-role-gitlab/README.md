## Ansible Role: GitLab (ansible-role-gitlab)

There are two software distributions of GitLab: the open source Community Edition (CE), and the open core Enterprise Edition (EE). GitLab is 
available under different subscriptions.

New versions of GitLab are released in stable branches and the master branch is for bleeding edge development.

Both EE and CE require some add-on components called gitlab-shell and Gitaly. These components are available from the gitlab-shell and gitaly 
repositories respectively. New versions are usually tags but staying on the master branch will give you the latest stable version. New releases 
are generally around the same time as GitLab CE releases with exception for informal security updates deemed critical.

Here's the manual install process if you choose to do it:

 1. Install and configure the necessary dependencies

On RHEL 7, the commands below will also open HTTP and SSH access in the system firewall.

sudo yum install -y curl policycoreutils-python openssh-server
sudo systemctl enable sshd
sudo systemctl start sshd
sudo firewall-cmd --permanent --add-service=http
sudo systemctl reload firewalld

Next, install Postfix to send notification emails. If you want to use another solution to send emails please skip this step and configure an external SMTP server after GitLab has been installed.

sudo yum install postfix
sudo systemctl enable postfix
sudo systemctl start postfix

During Postfix installation a configuration screen may appear. Select 'Internet Site' and press enter. Use your server's external DNS for 'mail name' and press enter. If additional screens appear, continue to press enter to accept the defaults.

2. Add the GitLab package repository and install the package

Add the GitLab package repository.

curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.rpm.sh | sudo bash

Next, install the GitLab package. Change `http://gitlab.example.com` to the URL at which you want to access your GitLab instance. Installation will automatically configure and start GitLab at that URL. HTTPS requires additional configuration after installation.

sudo EXTERNAL_URL="http://gitlab.example.com" yum install -y gitlab-ee

3. Browse to the hostname and login

On your first visit, you'll be redirected to a password reset screen. Provide the password for the initial administrator account and you will be redirected back to the login screen. Use the default account's username root to login.

See our documentation for detailed instructions on installing and configuration.
4. Set up your communication preferences

Visit our email subscription preference center to let us know when to communicate with you. We have an explicit email opt-in policy so you have complete control over what and how often we send you emails.

Twice a month, we send out the GitLab news you need to know, including new features, integrations, docs, and behind the scenes stories from our dev teams. For critical security updates related to bugs and system performance, sign up for our dedicated security newsletter.

IMPORTANT NOTE: If you do not opt-in to the security newsletter, you will not receive security alerts.

### Requirements

Need to download the gitlab-ce-10.8.3-ce.0.el7.x86_64.rpm ROM file and add it to the roles 'files' directory under the role.

### Role Variables

None for now

### Dependencies

None

### Example Playbook


---
- hosts: all

  roles:
    - ansible-role-ntp-server


### License


### Author Information

Red Hat Inc.
This role was created in for Army Cyber













Role Name
=========

A brief description of the role goes here.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
