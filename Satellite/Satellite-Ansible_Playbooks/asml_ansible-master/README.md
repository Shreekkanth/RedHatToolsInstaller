# asml_ansible

## Playbooks
### cook-cow

Makes customized and sealed qcow2 (and tar) image via Satellite
* Lifecycle environment, CV, provisioning template, ks etc. are preinstalled in Satellite
* A disposable VM is created off a Host Group that supplies all the settings
* VM gets registered to Satellite and gets access to all necessary customer systems (artifactory, git, etc.)
* VM gets customized to te required state
* VM is unregistered from Satellite and sealed
* VM is shutdown
* qcow (or whatever disk format) is uploaded to desination (likely artifactory)
* tar is made off qcow and uploaded to the destination
* VM is removed 


##### Roles
