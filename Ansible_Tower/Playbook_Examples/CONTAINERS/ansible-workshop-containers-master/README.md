Ansible Workshop - Containers
====================

Repository to support an introduction to containers to support the Ansible Workshop

## Running the Example

This example demonstrates how to build a container image and run an image of [Flask](http://flask.pocoo.org/) based Python application that exposes a RESTful API using the following Ansible modules:

* [docker_image](https://docs.ansible.com/ansible/latest/modules/docker_image_module.html)
* [docker_container](https://docs.ansible.com/ansible/latest/modules/docker_container_module.html)

### Prerequisites

Please refer to the module references above for all prerequisites that are needed

### Building and Running the Example

To perform the execution against a local machine, execute the following command to run the playbook:

```
ansible-playbook -i inventory.local ansible-docker.yml
```

Once complete, API will be available at [http://localhost:5000/api/items](http://localhost:5000/items)

### Deprovision

Execute the following command to deprovision the container

```
ansible-playbook -i inventory.local ansible-docker.yml
```