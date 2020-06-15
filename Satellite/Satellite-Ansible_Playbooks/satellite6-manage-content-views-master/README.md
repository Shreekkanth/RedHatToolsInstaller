# sat6-manage-content-views

Playbooks to manage automated publishing and promotion of Satellite6 content views.

# Variables
Content view variables are stored in the [vars](vars) directory of this repository.

Satellite6 username and password are prompted on execution, but the playbooks can be run silently if desired by passing `sat6_user` and `sat6_pass` as extra variables (`--extra_vars`).

Satellite6 fully-qualified domain name (`sat6_fqdn`) and organization (`sat6_organization`) are set in each playbook.

For variable information related to the content views, please refer to the documenation found in the [role-satellite6_manage_content_views](https://prometheus2.isus.emc.com/ansible/role-satellite6_manage_content_views) repository for full usage details.

## Playbook Execution
All playbooks can be run with the following command:
`ansible-playbook <playbook name>`

You will be prompted for a Satellite6 username and password that has access to manipulate content views (i.e. publish, promote, remove versions).

Please note, these playbooks were intended to be run in the order listed (i.e. 1, 2, 3.)


| Playbook name | Description |
| --- | --- |
| [1-publish-and-promote-non-prod.yml](1-publish-and-promote-non-prod.yml) | Publishes a new content view version of each content view, and then promotes them to non-prod lifecycle environment |
| [2-promote-prod.yml](2-promote-prod.yml) | Promotes the content view version created with 1-publish-and-promote-non-prod.yml to the `prod` lifecycle environment. |
| [3-promote-prev-quarter-1.yml](3-promote-prev-quarter-1.yml) | Promotes the content view version created with 1-publish-and-promote-non-prod.yml to the `prev-quarter-1` lifecycle environment. Once the version has been promoted, it removes the previous content view version from the Satellite6 environment.|

## Author Information
[Andrew J. Huffman](mailto:ahuffman@redhat.com)
