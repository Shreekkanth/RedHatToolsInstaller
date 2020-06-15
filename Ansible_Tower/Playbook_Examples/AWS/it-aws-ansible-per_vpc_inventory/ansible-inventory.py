#! /usr/bin/env python
"""
Script for automatically generating inventory for Ansible

@author: Jeff Hubbard <jhubbard@redhat.com>
"""

import os
import shutil
import commands

try:
    import boto
    import boto.ec2
    import boto.vpc
except:
    print("Error, could not import Boto libary, please install a recent "
        " version of Boto.  ")
    print("The latest version from Pip is recommended, older versions have "
        "bugs that may affect the operation of this script.")
    exit(999)

def reverse_dns(a_ip_address):
    result = commands.getoutput("dig +short -x {0}".format(a_ip_address))
    result = result.strip()
    result = result.strip(".")
    if result:
        return result
    else:
        return a_ip_address

INVENTORY_DIR = "inventory"

TAGS = (
    "ServicePhase", "ServiceName", "ServiceComponent",
    "Name") #"ServiceOwner",

class FileManager:
    def __init__(self):
        self._dict = {}

    def add_item(self, a_key, a_value):
        if a_key not in self._dict:
            self._dict[a_key] = []
        self._dict[a_key].append(a_value)

    def serialize(self):
        if os.path.isdir(INVENTORY_DIR):
            shutil.rmtree(INVENTORY_DIR)
        for k in sorted(self._dict):
            print("Processing {0}".format(k))
            v = self._dict[k]
            dir_name = os.path.dirname(k)
            if not os.path.isdir(dir_name):
                os.makedirs(dir_name)
            # Python2.6 compatible syntax instead of dict comprehension
            value_dict = dict([(x[0], []) for x in v])
            for x in v:
                if len(x) < 3:
                    print("Error: malformed tags {0}".format(x))
                else:
                    value_dict[x[0]].append(x[2])
            with open(k, "w") as file_handle:
                for x, y in value_dict.items():
                    if not x.strip():
                        print("Error:  Empty tag value in {0}, "
                            "not adding hosts\n{1}".format(k, y))
                        print("Fix this by setting the ServiceComponent tag")
                    else:
                        file_handle.write("\n\n[{0}]\n\n".format(x))
                        file_handle.write("\n".join(sorted(y)))


FILE_MANAGER = FileManager()

def is_tagged(a_dict):
    for x in TAGS:
        if x not in a_dict or not a_dict[x].strip():
            return None
    path = INVENTORY_DIR + "/"
    path += "/".join(a_dict[x.strip()] for x in TAGS[:2])
    value = [a_dict[x.strip()] for x in TAGS[2:]]
    return path, value

def create_inventory():
    try:
        conn = boto.ec2.EC2Connection()
    except boto.exception.NoAuthHandlerFound:
        return False
    if not conn:
        return False
    region_list = [x.name for x in conn.get_all_regions()]
    conn.close()
    for region in region_list:
        conn = boto.ec2.connect_to_region(region)
        if not conn:
            print("Could not connect to {0}".format(region))
            continue
        for instance in (
        x for x in conn.get_only_instances() if x.vpc_id == VPC_ID):
            tagged = is_tagged(instance.tags)
            if not tagged:
                print("Instance is not tagged properly: "
                    "{0}".format(instance.id))
                continue
            path, value = tagged
            if instance.private_ip_address:
                value.append(reverse_dns(instance.private_ip_address))
            elif instance.ip_address:
                value.append(reverse_dns(instance.ip_address))
            else:
                for nic in instance.interfaces:
                    for x in nic.private_ip_addresses:
                        nic_dns = reverse_dns(x)
                        if nic_dns != x:
                            value.append(nic_dns)
                            continue
                if instance.private_dns_name:
                    value.append(instance.private_dns_name)
                    continue
                print("No IP address or DNS for {0}".format(instance.id))
            FILE_MANAGER.add_item(*tagged)
    FILE_MANAGER.serialize()
    return True


def get_current_vpc():
    identity_obj = boto.utils.get_instance_identity()
    current_instance_id = identity_obj["document"]["instanceId"]
    region = identity_obj["document"]["availabilityZone"][:-1]
    conn = boto.ec2.connect_to_region(region)

    if not conn:
        print("Could not connect to EC2/{0}".format(region))
        exit(1)

    if not conn:
        print("Could not connect to VPC/{0}".format(region))
        exit(1)

    print("Operating in region {0}".format(region))
    current_instance = conn.get_only_instances([current_instance_id])[0]
    vpc_id = current_instance.vpc_id
    print("Operating in VPC {0}".format(vpc_id))
    return vpc_id

VPC_ID = get_current_vpc()

if __name__ == "__main__":
    if not create_inventory():
        if not "AWS_ACCESS_KEY_ID" in os.environ or \
        not "AWS_SECRET_ACCESS_KEY" in os.environ:
            print("Error connecting to AWS:  If no instance role "
                "is available (or you're running the script locally)"
                "You must export your AWS access key "
                "credentials to the AWS_ACCESS_KEY_ID and "
                "AWS_SECRET_ACCESS_KEY environment "
                "variables before running this script")
            exit(1)
        else:
            print("Unknown error connecting to AWS, "
                "check your network connectivity and/or credentials")
