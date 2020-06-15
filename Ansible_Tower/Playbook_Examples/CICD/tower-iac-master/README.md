# Tower Infrastructure as Code

## Goal
Setup a CI/CD pipeline to migrate assets from one Tower instance to another. Tower assets are anything that can be created within tower: organizations, credentials, job templates, etc.

## The Process
The process flow will be as follows:

![alt text](Tower%20CI%20CD.png "Workflow")
1. A Tower developer builds or modifies an asset in the dev version of Tower.
2. A Tower administrator runs a job telling dev Tower to export its assets.
3. The job commits the files into an SCM
4. The SCM notifies a CI tool (or the CI tool polls the SCM)
5. The CI tool calls to the import job on the Dev Tower instance
6. The job on the Dev Tower instance calls to the Prod Tower instance to update its assets.

## Demonstration Video
[![Example Video](https://drive.google.com/open?id=1o3bXgwqPW2cN4YyHpVGRZeFcmIQohAfl)](https://drive.google.com/open?id=1o3bXgwqPW2cN4YyHpVGRZeFcmIQohAfl "Example Video")

## Environment
For this example we are going to have two instances of Tower:
10.0.1.161 will be our “development” Tower instance.
10.0.1.193 will be our “production” Tower instance.

The Tower version needs to be at least 3.2.2 so that we have the “Ansible Tower” credential type. In addition we need Ansible version 2.5 or later so that we have the proper base fo the TowerCLI modules. For this particular environment I am going to use Tower 3.2.3 (the latest as of this writing) with Ansible 2.5.0.

Since the code for TowerCLI and Ansible is not yet released we need to custom build TowerCLI and manually install the required Ansible Modules.

In addition, we will have a second GitLab instance. In our example, we will use https://gitlab.consulting.redhat.com/jowestco/tower-iac-target

Finally, we will have a Jenkins instance running on localhost:8080 with the Ansible Tower plugin.

## Setting Up The Ansible Environment
This step should be done on both the dev and prod Tower servers.
Starting with a base version of RHEL 7, install Ansible and Tower:
```bash
yum update -y
yum install -y yum-utils
yum-config-manager --enable rhel-7-server-ansible-2-rpms
yum install -y ansible
curl https://releases.ansible.com/ansible-tower/setup/ansible-tower-setup-3.2.3.tar.gz > ansible-tower-setup-3.2.3.tar.gz
tar -xzvf ansible-tower-setup-3.2.3.tar.gz
cd ansible-tower-setup-3.2.3
ansible localhost -m blockinfile -a "path=./inventory block=admin_password='password'\npg_password='password'\nrabbitmq_password='password'"
ansible-playbook -i inventory install.yml
```

Install TowerCLI:
```bash
cd ~
git clone https://github.com/ansible/tower-cli.git
cd tower-cli
make install
```
Validate you have a correct version:
```bash
tower-cli --help | grep send
```
This should return:
>    send     Import assets into Tower.

Install the Ansible tower_send and tower_receive modules:
```bash
cd /usr/lib/python2.7/site-packages/ansible/modules/web_infrastructure/ansible_tower/
curl https://raw.githubusercontent.com/john-westcott-iv/ansible/TowerCLI/lib/ansible/modules/web_infrastructure/ansible_tower/tower_send.py > tower_send.py
curl https://raw.githubusercontent.com/john-westcott-iv/ansible/TowerCLI/lib/ansible/modules/web_infrastructure/ansible_tower/tower_receive.py > tower_receive.py
```

## Setup the CI/CD Environment
This step can be done just on the dev server.
Clone the data from gitlab:
```bash
cd ~
git clone https://gitlab.consulting.redhat.com/jowestco/tower-iac.git
cd tower-iac
tower-cli send --tower-host 10.0.1.161 --tower-username admin --tower-password password tower_assets/server_assets.json
```

In the dev server Tower UI, you now need to update the following passwords:
* SR Dev Tower Credential – This is a url and password to get into the dev Tower server
* SR Prod Tower Credential – This is a url and password to get into the prod Tower server
* SR SCM Credential – This is a credential to connect to the main gitlap repo (tower-iac)
* SR Machine Credential – This is a user/password to get into localhost
* SR GitLab Credential – This is the password to your protected repository to store Tower assets

Complete the asset imports
```bash
tower-cli send --tower-host 10.0.1.161 --tower-username admin --tower-password password tower_assets/server_project.json
```

Finally, fix the job templates to point to your repository by changing the extra vars in the following job templates:
* SR Export Assets
* SR Import Assets


## Testing the Export job
The export process can now be tested by running the job template SR Export Assets on the dev server. Once this job completes you should now see content in your target repository representing the content of this server.


## Setting up Jenkins for CI/CD of Tower
Log into your Jenkins instance as Admin.
Navigate to: Manage Jenkins => Manage Plugins => Installed (tab). In the filter enter “Ansible Tower Plugin” and make sure that the Tower plugin is listed in the install list.
If the plugin is not installed click on the Available tab and use the filter to search for “Ansible Tower Plugin” and select the checkbox next to the plugin and click the “Install without restart” button to perform the installation.
Repeat this process for a plugin called AnsiColor.

In the left hand menu select “Back to Dashboard”.
In the left hand menu select “Credentials”
In the left hand menu select “System”
In the main body select “Global credentials (unrestricted)”
In here we are going to create two credentials:
* Ansible Tower credentials to connect to your dev server
* GitLab credentials to connect to your repository

In the left had menu select “Add Credentials” and enter the following information:
* Kind: Username with passwords
* Scope: Global (Jenkins, nodes, items, all child items, etc)
* Username: <Your Tower username>
* Password: <Your Tower password>
* ID: DevTowerCredentials
* Description: A username password credential used to connect to Tower.
Click on the “OK” button
Click “Add Credentials” in the left hand menu and enter the following information:
* Kind: SSH Username with private key
* Scope: Global (Jenkins, nodes, items, all child items, etc)
* Username: <Your SCM username>
* Private Key: <Either enter it directory or load it from a file>
* Passphrase: <Enter if needed>
* ID: SCMCredentialsForTowerRepo
* Description: These credentials connect you to the repository of Tower assets.
Click on the “OK” button

Navigate back to the main screen and select “Manage Jenkins” and then select “Configure System”.
In this list, search for the section called “Ansible Tower”.
Click the “Add” button.
Enter the following information:
* Name: My Dev Server
  * If you change this name you need to update the groovy code below.
* URL: <the IP of your dev server>
* Credentials: <Select the credential with the description: “A username password credential used to connect to Tower.”>
* Force Trust Cert: <checked if needed>
Click on the “Test Connection” button to validate that Jenkins is able to reach the server.
Once you have successfully connected click on the “Save” button at the bottom of the screen.

Navigate to the main screen and select “New Item”. Enter a name like “Sync Tower Servers”, select “Freestyle Project” and click the “OK” button.

Enter the following information:
* Source Code Management:
  * Git: Checked
    * Repository URL: <The URL to your repo>
    * Credentials: <The credential you built (description:  These credentials connect you to the repository of Tower assets)>
  * Build Triggers:
    * Pool SCM: Checked
      * Note: If you are able to you can use a WebHook to notify Jenkins instead of an SCM Poll
    * Schedule: * * * * *
      * Again, note, this will run every minute. This is ok for doing some testing. A better way to do this is to use a webhook to have GitLab notify Jenkins when its time to build.
  * Build Environment:
    * Color ANSI Console Output: Checked
  * Build:
    * Add a build Step for “Ansible Tower”
      * Tower Server: My Dev Server
      * Template Type: job
      * Template Id: SR Import Assets
      * Import Tower Output: checked

Save the job.
In the left had menu click “Build Now” to test the job.
## Author
[John Westcott](mailto:jowestco@redhat.com)
