###
June 07, 2019
Mike McDonough
mike.mcdonough@redhat.com

System prep steps -
1) Requirements:

Python 2.7.5
Ansible 2.7.9
Tower CLI 3.3.4
Version of tower_credential.py from Devel branch

2) These roles and playbooks require the tower-cli command. Install pip and then use pip to install the ansible-tower-cli module.

curl -o epel-release-latest-7.noarch.rpm https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
rpm -ivh epel-release-latest-7.noarch.rpm
yum clean all
yum install python-pip
pip install --upgrade pip
pip install ansible-tower-cli

3) tower_credential.py module

The GA module version does not support custom type Tower credentials. A newer version of tower_credential.py (downloaed from GitHub) is provided in the tower_creds role as tower_credential_beta.py. This version of the Python module supports custom credential types and addresses a file not found error when attempting to add a ssh key.

See:
https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/web_infrastructure/ansible_tower/tower_credential.py
https://github.com/ansible/ansible/blob/29dcdeaba1f80e9ede9b52a443f89b1a632c1496/lib/ansible/modules/web_infrastructure/ansible_tower/tower_credential.py
https://github.com/ansible/ansible/issues/47832

4) The tower_send module from Ansible 2.8 is required for these playbooks. A copy of this modules is included with the tower_send_assets role.

NOTE: The tower_receive module (new with Ansible 2.8) is available on GitHub but isn't currenlty used by any playbooks in this repo. If needed for a future playbook, it can be downloaded from GitHub.

5) Ansible Tower supports vault encrypted variables but not encrypted files, at least directly. Use "ansible-vault encrypt_string" to encrypt a variable value for inclusiong in a vars file or playbook. Example:

ansible-vault encrypt_string --stdin-name 'password'
Reading plaintext input from stdin. (ctrl-d to end input)
password123
password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          30353236363731663836666631633839353138343634383661666134636663393330356665373066
          3032663262306239366363306665306231306332303134650a626432313739346332363532313137
          62316637643531613731383431353338393539656466666437623866306333353632373535343565
          6364646663373032380a363438656265666563653165653739353839343132636337373430653366
          3433
Encryption successful

To enable a Tower job to decrypt vault encrypted variables, use one of the following options: 

   1) create a Vault type credential, then add it to the Template along with other required credentials (ex: machine credentials)
   ---OR---
   2) add "ANSIBLE_VAULT_PASSWORD: <vault paassword>" as an Extra Variable to the Template

Note: Various workarounds are possible that enable a Tower Job to utilize Vault encrypted files. However, SCM sync jobs can be problematic if a Vault encrypted file is included under groups_vars/.

###
