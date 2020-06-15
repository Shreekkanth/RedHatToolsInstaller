# Automazione provisioning di sistemi con Ansible

Una serie di playbook Ansible e procedure documentate per automatizzare completamente o in parte le attività di provisioning di nuovi sistemi virtuali RHEL su piattaforma VMware vSphere presso CDP Cassa Depositi e Prestiti.

Questo repository contiene:

* [ansible](ansible) Playbook, role e variabili default per il provisioning
* [CreazioneTemplateRHEL.md](CreazioneTemplateRHEL.md) Documentazione sulla generazione del Template VMware per una RHEL 7.x minimal
* [CreazioneFloppy.md](CreazioneFloppy.md) Documentazione sulla generazione del floppy con Kickstart
* [ks.cfg](ks.cfg) File di Kickstart utilizzato per la creazione dei Template RHEL
* [ProvisioningVM.md](ProvisioningVM.md) Documentazione sull'uso dei Playbook assieme ai Template VMware per la creazione di nuove VM preconfigurate e pronte all'uso
