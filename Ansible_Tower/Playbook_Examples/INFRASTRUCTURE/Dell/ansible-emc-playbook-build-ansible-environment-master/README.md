# Build Ansible Environment
An Ansible Playbook to configure EMC's Ansible environment, and ensure it is configured as defined.  It could also be run on a `cron` schedule (once deployed) to ensure the environment is in a desired state.

## How to use this playbook
  a. Install Ansible and git on the RHEL server:  
  `yum install -y ansible git`

  b. Clone this repository on to the RHEL server from Gitlab (`prometheus2.isus.emc.com`):  
  `git clone git@prometheus2.isus.emc.com:ansible/build-ansible-environment.git`

  c. Change in to the cloned repository:  
  `cd ./build-ansible-environment`

  d. Run the playbook to configure the Ansible environment as a user that has sudo rights (or root privileges):  
  `ansible-playbook build-ansible-environment.yml`

  e. That's it!  
  * Cloned Playbooks will be found under: `/apps/data/ansible/playbooks`
  * Cloned Roles will be found under: `/apps/data/ansible/roles`
  * Cloned Kickstart files will be found under: `/apps/data/kickstart`

To run the playbook without the prompt:  
`ansible-playbook build-ansible-environment.yml -e ans_data_home=/apps/data`  
Replace `/apps/data` with the directory you want the base of the Ansible environment to install to.

## Variables
| Variable Name | Description | Variable File | Type |
| --- | --- | --- | :---: |
| ans_data_home | Root of filesystem to build the Ansible environment in. You will be prompted for this when the playbook runs.  It is defaulted to /apps/data | [vars/build_ansible_env_vars.yml](vars/build_ansible_env_vars.yml) | string |
| ans_env_dirs | List of directories to create relative to the `ans_data_home` variable value (`/apps/data`). | [vars/build_ansible_env_vars.yml](vars/build_ansible_env_vars.yml) | list |
| ans_env_role_repos | List of roles to git clone.  Source of the git repo - `src` key.  Where to git clone the role to - `dest` key (will be relative to the value of the `ans_data_home` variable). Version/tag/branch/commit of the repository to clone - `ver` key (defaults to "HEAD") when not specified. | [vars/build_ansible_env_vars.yml](vars/build_ansible_env_vars.yml) | list of dictionaries |
| ans_env_playbook_repos | List of playbooks to git clone.  Source of the git repo - `src` key.  Where to git clone the role to - `dest` key (will be relative to the value of the `ans_data_home` variable). Version/tag/branch/commit of the repository to clone - `ver` key (defaults to "HEAD") when not specified. | [vars/build_ansible_env_vars.yml](vars/build_ansible_env_vars.yml) | list of dictionaries |
| ans_env_python_libraries | List of Python libraries/modules to install that Ansible modules in your playbooks/roles depend on. | [vars/build_ansible_env_vars.yml](vars/build_ansible_env_vars.yml) | list |
| ks_image_ssh_priv_key | Private key used to connect to EMC Template during build process. This is stored encrypted in an Ansible Vault file. | [vars/encrypted-ssh-priv-keys.yml](vars/encrypted-ssh-priv-keys.yml) | string |
| ks_image_ssh_pub_key | Public key used to work with EMC Template during build process.  This is injected into the template via the templates kickstart `rhel7-ks.cfg`.  See the [kickstart](https://prometheus2.isus.emc.com/ansible/emc-vm-template-kickstart) repository. | [vars/encrypted-ssh-priv-keys.yml](vars/encrypted-ssh-priv-keys.yml) | string |
| gitlab_ssh_priv_key | Private key used to clone all Ansible repositories from Gitlab (prometheus2.isus.emc.com).  This is stored encrypted in an Ansible Vault file | [vars/encrypted-ssh-priv-keys.yml](vars/encrypted-ssh-priv-keys.yml) | string |
| gitlab_ssh_pub_key | Public key that is set on all Ansible repositories in Gitlab.  This allows us to git clone via this playbook without user/pass or other keys. | [vars/encrypted-ssh-priv-keys.yml](vars/encrypted-ssh-priv-keys.yml) | string |

## Maintenance
Since this playbook is idempotent, it can be run as often as desired.  It is recommended as you add more Ansible Roles and Playbooks to your environment to maintain the variable lists `ans_env_role_repos` and `ans_env_playbook_repos` found in [vars/build_ansible_env_vars.yml](vars/build_ansible_env_vars.yml).  The playbook can then be re-run with the updated variables, and will ensure all required playbook and roles have been installed into the Ansible environment.

As you progress with Ansible, you may want to use specific Playbook and Role repository versions.  Please see the [Variables](#Variables) section above to add the `ver` key to your repo lists.  This means you can specify a specific tag/branch/commit to lock your code to.  This is extremely important in production environments, where running with the latest code is not necessarily the best decision if frequent changes happen on the Roles/Playbooks that could break mission critical processes.

## Author
[Andrew J. Huffman](mailto:ahuffman@redhat.com)
