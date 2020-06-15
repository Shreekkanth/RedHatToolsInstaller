# About

WARNING: This project is not fully functional yet.

## Background

Why?

Packstack is simple enough, why wrap it with Ansible?

There have been several projects I've helped with that do not require the overhead of a Director install, simple all-on-one or just a few nodes will suffice. The intent is really to focus on other products that integrate with OpenStack such as CloudForms or RHV. These projects have needed OpenStack up quick and simple and in a repeatable way. PackStack is the natural choice for this. However, in many of these projects, the users are not proficient in OpenStack. So, I decided to automate the pieces that PackStack does not - prep of the host(s), generation of the answer file based on commonly changes settings for the environment, and creation of user, project, images, network, instances, etc. I've also included configuring a NFS backend for Cinder.

The bash script has proven very successful for this purpose, but it is time to convert it into Ansible. The work here is NOT COMPLETE and I'm hosting it here in case others want to contribute.


## Bash Script

* The original bash script is here: https://gitlab.cee.redhat.com/vvaldez/packstack-plus
* Detailed explanation here: https://youtu.be/kJIWQHDm-FE

# Usage

Edit the group_vars/all and inventory/hosts files to match your environment then run **deploy.yml**
