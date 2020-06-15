# Creazione Template RHEL 7.x

Per un processo di provisioning molto rapido, è generalmente consigliato fare uso di Template di macchine virtuali. VMware vSphere consente la creazione di nuove virtual machine basate su Template dove la personalizzazione avviene attraverso i VMware Tools (package open-vm-tools, fornito con RHEL) in fase di first-boot. 

## Il Template RHEL-Server-7.5

Questo template è basato sulla release 7.5 di RHEL, installata su una vm con il seguente virtual hardware:

* 1 cpu
* 2GB Ram
* 1 vDisk, 30GB
* no sch. rete

Il file di Kickstart [ks.cfg](ks.cfg) è stato preparato per installare RHEL 7.x con le seguenti caratteristiche:

* Installazione cdrom-based (package su file ISO montato su device DVD virtuale VMware)
* Lingua base: Inglese
* Selinux: Enforcing
* Firewall: Disabilitato
* Password di root preimpostata e predeterminata
* Utente `ansible` con chiave RSA autorizzata al login automatico
* Timezone Europe/Rome
* Layout di partizionamento minimale che consenta espansione dei filesystem e/o aggiunta di nuovi filesystem
* Lista di package ridotto al minimo
* Poweroff al termine dell'installazione per una pulizia maggiore del sistema
* Nessuna configurazione di rete preinstallata
* open-vm-tools preinstallati per una personalizzazione al primo boot


In modo analogo, possono essere creati dei Template basati su una release differente di RHEL 7.


## Generazione del Template partendo da DVD + Kickstart

Il file di Kickstart può essere utilizzato caricandolo su un'immagine floppy virtuale. Vedi [CreazioneFloppy.md](CreazioneFloppy.md).

Assieme al DVD ISO di installazione di RHEL 7.x, scaricabile da https://access.redhat.com/downloads, è possibile creare una VM Template seguendo questi step:

1. Accesso all'interfaccia di management di VMware vSphere
2. Creazione di una nuova VM con le caratteristiche virtual HW sopra citate. Il nome della VM potrà essere ad esempio *RHEL-Server-7.5*
3. Aggancio della ISO *rhel-server-7.5-x86_64-dvd.iso* al device DVDROM virtuale della Virtual Machine con connessione al boot
4. Aggancio del file .img *floppyks.img* al device Floppy virtuale della Virtual Machine senza connessione al boot
5. Avvio della VM e apertura della console remota
6. Con il tasto freccia sù, selezionare la voce di menù *Install Red Hat Enterprise Linux 7.5* e premere `tab` per editare la *command line* di boot
7. Aggiungere alla command line la stringa `ks=hd:fd0` che indica la posizione del file ks.cfg sul device fd0 (floppy) senza premere Invio.
8. Dall'interfaccia VMware, connettere anche il floppy
9. Tornando alla console della VM, premere invio. Il sistema si avvia e viene installato. Al termine, il sistema si arresta.
10. Dall'interfaccia VMware vSphere, sganciare l'immagine ISO dal device DVDROM Virtuale e l'immagine floppy dal device Floppy virtuale.
11. Avviare una volta la VM ed attendere il prompt su console `localhost login:`. Servirà ad aggiornare lo stato dei VMware Tools in vSphere.
12. Spegnere la VM tramite il pulsante shutdown.
11. Convertire la VM in Template (menu contestuale -> Template -> Convert VM to Template)

Il Template è ora pronto per essere usato nella creazione di nuove VM. Ogni nuova VM avrà virtual hardware specifico secondo le esigenze.


## Generazione di un DVD di installazione Template con Kickstart incluso

È inoltre possibile includere il file ks.cfg all'interno del DVD di installazione per generare un'immagine autoinstallante di RHEL 7.x che non abbia bisogno del floppy e della command line customizzata.

**TODO**
- clone repo
- estrazione ISO
- copia ks.cfg
- customizzazione isolinux.cfg
- lancio script [mkiso.sh](mkiso.sh)




