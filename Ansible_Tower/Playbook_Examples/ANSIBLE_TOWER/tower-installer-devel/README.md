# tower-installer

This project provides an Ansible playbook that can be used to installed various
artifacts into Ansible Tower based on the concept of an input "catalog".  The 
playbook works by reading the catalog path and performing various installation
activites on a Tower system.  

To configure the catalog path, set the `ansible_tower_catalog_path` value in 
the inventory file to point at the desired directory that contains the 
variables.  Be sure to update the Tower host values as necessary for your given 
environment.
