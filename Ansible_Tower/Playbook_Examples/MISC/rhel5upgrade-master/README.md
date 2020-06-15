Use Case:
  Client wants to remotely image RHEL 5 servers to install RHEL 7
  
Requirements:
 - Can not use PXE Server (no network imaging)
 - No DHCP
 - Can not use any remote repo on the network (HTTP, FTP, NFS, etc...)
 - Can not transfer any large files over the network
 - Every server will have a sdb drive with the RedHat ISO on it.
 - All important data from sda will be backed up to sdb (so no wiping it)
 - Only sda will be used for the install
 - No DHCP, so server will need network setup automatically on RHEL 7
 - Will utilize Ansible / Ansible Tower

To accomplish this, we will create an Ansible playbook that utilizes the PXE 
images installed locally.  We extract the PXE images from the ISO and copy them
to /boot and modify grub to boot to it.  We add a Kickstart script and pass all
network information to grub via kernel parameters.  The Kickstart script does
the rest after the server is rebooted.  Since we tell Kickstart to utilize the
sdb drive for its packages (via the ISO) it will automatically ignore that drive
when clearing partitions.

- [x] Completed task
    - [x] Utilize PXE vmlinuz and initrd.img from ISO file
    - [x] Use Kickstart script on HD
    - [x] Use Redhat ISO on HD for Package Installation
    - [x] Modify grub.conf to boot to local PXE
    - [x] Utilize UUID to reference HD (for Grub and Kickstart)
    - [x] Pass network parameters to Kernel via Grub
    - [x] Kickstart will use kernel parameters to setup networking

