# Provisioning di nuove VM da Template

Durante un provisioning basato su Template, VMware copia il template e i dischi contenuti, modifica il virtual hardware in base alle scelte effettuate in fase di creazione, e avvia la VM.

All'atto del primo avvio del sistema, i VMware Tools configurano quanto indicato nei dati di personalizzazione e procede alla scrittura dei file e all'eventuale riavvio del sistema. Dopo questa fase, il sistema è pronto all'uso.

## Provisioning attraverso playbook Ansible

### Requisiti per i moduli `vmware_*` di Ansible

I moduli Ansible relativi a VMware necessitano che la libreria PyVmomi sia installata sulla macchina che effettua le chiamate REST alle API VMware, in questo caso i sistemi Ansible Tower che sono già provvisti di tale libreria.


### Struttura dei playbook


### Uso dei playbook con Ansible Tower

Sull'attuale installazione di Ansible Tower è presente un progetto denominato VM-PROVISIONING. È basato sul contenuto di questo repository Git.

Da questo Progetto sono stati creati i due Job Template:

1. VM Deploy by Survey
2. VM Deploy by YAML

Entrambi i playbook prevedono una fase di creazione VM interagendo direttamente con VMware vSphere, e una successiva fase di configurazione adattabile alle necessità.


### Uso del VM Deploy tramite Survey

Il playbook [ansible/deployvm_survey.yaml](ansible/deployvm_survey.yaml) utilizza una Survey semplificata per l'attivazione di nuove VM.

I campi richiesti sono i seguenti:

* Gli Short hostname delle VM da creare (nome senza suffisso .cdpsede.cassaddpp.it)
* Gli Indirizzi IP delle VM da creare
* Il Port Group VMware delle VM
* La Netmask delle VM
* Il Default Gateway delle VM
* Il numero di CPU delle VM
* La quantità di memoria RAM delle VM espressa in MiB
* La dimensione del disco primario delle VM
* Registrazione a Satellite e Activation Keys
* Aggiornamento sistema post-installazione

Data la semplificazione in Survey, le VM si intendono:

- tutte appartenenti alla medesima VLAN (stesso netmask, stesso gw, stesso VLAN id)
- tutte con la medesima quantità di CPU, Memoria RAM e Disco primario
- tutte generate dal medesimo template di sistema operativo

I valori predefiniti della Survey consentono immediatamente di generare una VM denominata RHEL74ANSIBLE01 con indirizzo IP 192.168.18.24/24 su rete PG_10, 2 CPU e 2GB di RAM, da template RHEL 7.4.


### Uso del VM Deploy tramite YAML

Il playbook [ansible/deployvm.yaml](ansible/deployvm.yaml) utilizza una struttura dati YAML per il provisioning. Questa modalità consente di creare VM completamente eterogenee tra loro, con il massimo grado di personalizzazione.

Il playbook richiede che venga valorizzata, attraverso le `extra_vars`, il dizionario `instances` come l'esempio seguente:

```yaml
instances:
- name: "rhel-74-ansible-1"
  hardware:
    memory_mb: "2048"
    num_cpus: "1"
    scsi: "paravirtual"
  disk:
  - size_gb: 40
    type: thick
    autoselect_datastore: true
  networks:
  - name: "PG_10"
    ip: "192.168.18.24"
    netmask: "255.255.252.0"
    gateway: "192.168.16.1"
    device_type: vmxnet3
    start_connected: true
  template: "RHEL-7.4-Server-Template"
  register_to_satellite: true
  register_to_puppet: false
  set_local_facts: true
  update_packages: true
  activation_keys:
  - "RHEL_7_TEST"
  local_facts:
  - file: test.fact
    content: |
      {
        "test": "1",
        "prova": "2"
      }

- name: "rhel-74-ansible-2"
  hardware:
    memory_mb: "3072"
    num_cpus: "2"
  disk:
  - size_gb: 35
    type: thick
    autoselect_datastore: true
  networks:
  - name: "PG_10"
    ip: "192.168.18.26"
    netmask: "255.255.252.0"
    gateway: "192.168.16.1"
    device_type: vmxnet3
    start_connected: true
  template: "RHEL-7.4-Server-Template"
  register_to_satellite: true
  activation_keys:
  - "RHEL_7_TEST"
  update_packages: false

```

### Credenziali utilizzate

I playbook accedono a VMware vSphere per la creazione di VM ed eventualmente altri sistemi per il completamento della configurazione (es. Satellite 6).

Le variabili utilizzate o predisposte all'utilizzo sono valorizzate nel file [ansible/group_vars/all.yaml](ansible/group_vars/all.yaml). 

*Nota:* Dalla versione 3.2.0 di Ansible Tower è possibile creare oggetti di tipo Credenziali Custom in cui inserire (e proteggere) le credenziali di qualsiasi altro tipo.  È inoltre possibile assegnare ad un Job credenziali multiple ed utilizzarle nel playbook.  È fortemente consigliato l'upgrade all'ultima versione di Tower (v3.3.0)






