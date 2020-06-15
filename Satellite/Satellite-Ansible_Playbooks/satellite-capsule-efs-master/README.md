
Install
-------
run `ansible-galaxy install -r requirements.txt`

`ansible-playbook -i <inventory> playbook/provision.yaml`



Plugins
-------

Plugins are loaded from the library installed path and the configured plugins directory (check your ansible.cfg). The location can vary depending on how you installed Ansible (pip, rpm, deb, etc) or by the OS/Distribution/Packager. Plugins are automatically loaded when you have one of the following subfolders adjacent to your playbook or inside a role:

 * action_plugins
 * lookup_plugins
 * callback_plugins
 * connection_plugins
 * inventory_plugins
 * filter_plugins
 * strategy_plugins
 * cache_plugins
 * test_plugins
 * shell_plugins
 * vars_plugins

When shipped as part of a role, the plugin will be available as soon as the role is called in the play. 

