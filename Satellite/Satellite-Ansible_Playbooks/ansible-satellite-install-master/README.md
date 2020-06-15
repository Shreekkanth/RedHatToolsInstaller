# ansible-satellite-install

This playbook can be run on a freshly installed (unentitled) RHEL7 server and will result in a functioning WEBUI of Satellite Server.

Set your facts in **satellite_facts.yaml** for non-interactive install... 

The IP and hostname entered in the satellite_facts.yaml will be set statically.  The "target machine" ip can be the original DHCP assigned at new build.  My process:


1. new RHEL builds from latest RHEL7 ISO, basic packages (recommendations might not match official recommendations.  I'll fix eventually)
  *satellite and capsule both recommend identical hardware configuration:
  *200GB storage for repos
  *16GB RAM
  *2 CPU

2. power down the machine, snapshot the VMs so you can lather, rinse, repeat if necessary

3. boot both, receiving DHCP and generic hostname.  It's assumed that neither server is registered with subscription-manager at this point.

4. run this *satellite_install.yaml* playbook to the DHCP address of the satellite server

5. when playbook completes, manually reboot.

6. configure content manually (this feature is coming soon once I master hammer commands to do so)

7. once content is completely synched, run *capsule_install.yaml* against the capsule server.

These playbooks will set the IPs and hostnames as defined in the /etc/ansible/satellite_facts.yaml file.  Please make sure to move it to the correct path after cloning this repo.

