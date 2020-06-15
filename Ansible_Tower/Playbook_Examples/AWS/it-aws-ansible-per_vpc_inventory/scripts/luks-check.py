#!/usr/bin/python2
"""
Script for discovering non-root volumes that do not
have Luks encryption

@author: Jeff Hubbard <jhubbard@redhat.com>
"""

import commands

MOUNTS = commands.getoutput("mount")
RESULT = 0

def print_invalid_device(a_name, a_mount):
    global RESULT
    RESULT = 1
    print("{0} mounted on {1} is NOT a valid LUKS device".format(
        a_name, a_mount))

for mount in MOUNTS.split("\n"):
    mount_arr = mount.split()
    if mount_arr[0].startswith("/dev") and mount_arr[2] != "/":
        cmd = "cryptsetup status '{0}'".format(mount_arr[0])
        result = commands.getoutput(cmd).strip()
        if result:
            fs_type = [x for x in result.split("\n") if "type:" in x]
            if not fs_type:
                print_invalid_device(mount_arr[0], mount_arr[2])
            elif "LUKS" in fs_type[0].upper():
                print("Device {0} mounted on {1} is a valid LUKS "
                    "device".format(mount_arr[0], mount_arr[2]))
            else:
                print_invalid_device(mount_arr[0], mount_arr[2])
        else:
            print_invalid_device(mount_arr[0], mount_arr[2])

exit(RESULT)
