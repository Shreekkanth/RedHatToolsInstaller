# Ansible Roles and Playbooks                                                               
These are the scripts that will be part of deploying the Enterprise Services for the LMCO ALIS group. Each service will be deployed using Ansible Roles. As we mature the Enterprise Services we will continue to add more Ansible Roles to support the full deployment of the LMCO ALIS Enterprise Services.

[Ansible rsyslog Role](https://gitlab.consulting.redhat.com/ARCYBER/ansible-scripts/blob/master/README.md#ansible-role-rsyslog-ansible-role-rsyslog)

[Ansible NFS Role](https://gitlab.consulting.redhat.com/ARCYBER/ansible-scripts/blob/master/README.md#ansible-role-nfs)

[Ansible NTP Role](https://gitlab.consulting.redhat.com/ARCYBER/ansible-scripts/blob/master/README.md#ansible-role-ntp)

[Ansible GitLab Role](https://gitlab.consulting.redhat.com/ARCYBER/ansible-scripts/blob/master/README.md#ansible-role-gitlab-ansible-role-gitlab)

[Ansible Confluence Role](https://gitlab.consulting.redhat.com/ARCYBER/ansible-scripts/blob/master/README.md#ansible-role-confluence-ansible-role-confluence)

## Ansible Role: rsyslog (ansible-role-rsyslog)

 - Assumes rsyslog is installed and configured to include /etc/rsyslog.d/\*.conf
 - Installs a config file into /etc/rsyslog.d
 - Restarts rsyslog if that file changed.

 - If listener is set true then setup UDP and TCP listeners on port 514
 - Create a directory to store logs
 - Configure logrotate to rotate the logs

### Requirements

The listener conditional syntax is rsyslog7 specific. It uses "stop" instead of &~

### Role Variables

For shipping over UDP:

central_log_host: "@Address.To.Loghost"

For shipping over TCP:

central_log_host: "@@Address.To.Loghost"

For listening:

 - central_log_listener: False
 - central_logs_directory: "/var/log/remote/servers"
 - central_logs_retention_days: 30
 - central_log_by_function: False

Setting log_by_function to True will store logs not in %hostname% but per function instead.

For extra settings:
<pre>
central_log_extra_settings:
 - "$MainMsgQueueType LinkedList"
 - "$MainMsgQueueHighWatermark 400000"
 - "$MainMsgQueueHighWatermark 100000"
 - "$MainMsgQueueDequeueBatchSize 10000"
 - "$MainMsgQueueSaveOnShutdown on"
 - "$MainMsgQueueWorkerThreads 8"
 - "$ActionQueueWorkerThreads 8"
 - "$ActionQueueSize 1000000"
 - "$ActionQueueDequeueBatchSize 500000"
 - "$ActionQueueType LinkedList"
</pre>

### Dependencies

### Example Playbook

### License

### Author Information

Red Hat Inc.
This role was created in for LMCO ALIS


## Ansible Role: NFS

Installs NFS utilities on RedHat 7

### Requirements

None.

### Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    nfs_exports: []

A list of exports which will be placed in the `/etc/exports` file. 

Example: `nfs_exports: [ "/home/public    *(rw,sync,no_root_squash)" ]`

### Dependencies

None.

### Example Playbook

    - hosts: nfs-servers
      roles:
        - ansible-role-nfs

### Author Information

Red Hat Inc.
This role was created in for LMCO ALIS


## Ansible Role: NTP

Installs NTP on Linux.

### Requirements

None.

### Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    ntp_enabled: true

Whether to start the ntpd service and enable it at system boot. On many virtual machines that run inside a container (like OpenVZ or VirtualBox), it's recommended you don't run the NTP daemon, since the host itself should be set to synchronize time for all it's child VMs.

    ntp_timezone: Etc/UTC

Set the timezone for your server.

    ntp_manage_config: false

Set to true to allow this role to manage the NTP configuration file (`/etc/ntp.conf`).

    ntp_area: ''

Set the [NTP Pool Area](http://support.ntp.org/bin/view/Servers/NTPPoolServers) to use. Defaults to none, which uses the worldwide pool.

    ntp_servers:
      - "0{{ ntp_area }}.pool.ntp.org iburst"
      - "1{{ ntp_area }}.pool.ntp.org iburst"
      - "2{{ ntp_area }}.pool.ntp.org iburst"
      - "3{{ ntp_area }}.pool.ntp.org iburst"

Specify the NTP servers you'd like to use. Only takes effect if you allow this role to manage NTP's configuration, by setting `ntp_manage_config` to `true`.

    ntp_restrict:
      - "127.0.0.1"
      - "::1"

Restrict NTP access to these hosts; loopback only, by default.

### Dependencies

None.

### Example Playbook

    - hosts: all
      roles:
        - ansible-roles-ntp

*Inside `vars/main.yml`*:

    ntp_timezone: America/Chicago

### License


### Author Information

Red Hat Inc. This role was for LMCO ALIS



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

````
---
- hosts: all

  roles:
    - ansible-role-ntp-server

````

### License


### Author Information

Red Hat Inc.
This role was created in for LMCO ALIS


## Ansible Role: Confluence (ansible-role-confluence)

Ansible role which installs and configures an Atlassian Confluence instance.

### Dependencies

#### Oracle Java JDK

This role requires the Java JDK to be installed. The exact path can be
configured, see below for variables.
 
Please download the JDK using the links in the files/please-download-files.txt 

#### Oracle Java default keystore

When using self signed certificates, it may be required to add those as trusted
certificates in the default keystore.

Please download dependency links in the files/please-download-files.txt 
You can use `ansible-java-keystore` for this.

#### RDBMS

A relational database is required for Confluence, e.g. MySQL, Postgres or
Oracle.

Please configure postgres DB and add it to the tasks in this role.

#### JDBC driver

Confluence needs a JDBC driver to connect to the database, which may not be
provided by the Confluence distribution. The exact path must be configured.


#### Packetfilter

It may be need to configure packetilter rules for incoming or outgoing network
connections.  

### Role Variables

Available variables are listed below, along with default values (see
`defaults/main.yml`).  

All variables have set sensible defaults and usually should not need any
configuration, The only variable required to be set is the path to the installed
JDK.  

### General settings

    confluence_user_name: confluence

User name under which the application will be installed. The account will be
created if it does not exist.  

    confluence_group_name: confluence

Group name under which the application will be installed. The group will be
created if it does not exist.

    confluence_service_name: confluence

Service name of the application.

    confluence_provide_root_environment: false

Provide preconfigured aliases to the root shell for easier navigation to
Confluence-specific directories.

    confluence_start_on_boot :false

Start Confluence automatically at boot.

Set this to true in production environments. Even better, use a process
supervisor e.g. systemd or monit.

### Installation variables

    confluence_perform_installation: false

Install or upgrade Atlassian Confluence automatically.

Upgrade is the same as installation, but the previously installed version
will not be removed. If the configured Confluence version does not match the
current Confluence version on the host, the configured Confluence version
will be installed.

This flag can be used as an additional safety mechanism so the Confluence
installation is not accidentally changed. It could e.g. be enabled only in
a special, separate playbook for installations.

    confluence_start_after_installation: false

Start Confluence instance after the role has finished an installation or an
upgrade.

This is handy if you want to restore a backup before the instance is started.

    confluence_installation_archive_url: https://www.atlassian.com/software/confluence/downloads/binary/atlassian-confluence-6.9.1.tar.gz

HTTP URL where to get the tar.gz archive for the Confluence application.

Depending on the environment, a HTTP proxy configuration may be needed in
ansible.

    confluence_installation_archive_name: atlassian-confluence-6.9.1

Folder name of the extracted Confluence instance.

    Use sha1sum to generate the correct checksum for the tar ball

    confluence_installation_archive_checksum: sha1:4c8e877122686d138bf5588ae3ca8d53ead70030

Checksum of the tar.gz archive for the given version.

    confluence_installation_software_directory: /opt/atlassian/confluence

Path to a directory where the Confluence instance should be installed.

    confluence_installation_jdbc_driver_jar_source_path: (empty)

Optional path to a JDBC driver jar file on the control machine that will be
copied into the Confluence instance lib directory on the remote machine.

### Configuration variables

    confluence_config_jre_directory: ''

Required path to the directory that contains the Oracle JDK 1.8.

    confluence_config_home_directory: /var/atlassian/application-data/confluence

Path to the Confluence home directory.

    confluence_config_jvm_heap_size: 1024m

How much memory the JVM should use.

This is passed to the `-xXs` and `-Xmx` JVM options.

    confluence_config_jvm_opts: ''

Additional JVM configuration options.

    confluence_config_tomcat_context_path: ''

The tomcat context path for the Confluence instance. By default,  Confluence is
reachable at /.

    confluence_config_tomcat_connectors:
      standalone:
        enabled: true
        type: standalone
        listening_port: 8090
      reverse_proxy:
        enabled: false
        type: proxy
        listening_port: 8091
        proxied_hostname: jira.example.org
        proxied_port: 443

Dictionary with tomcat connector configurations. The dictionary can contain an
arbitrary number of connectors with arbitrary names.

### Example Playbook

    - hosts: confluence-servers
      roles:
         - role: ansible-role-confluence
           confluence_config_jre_directory: '/usr/java/jdk1.8.0_72'

### License

