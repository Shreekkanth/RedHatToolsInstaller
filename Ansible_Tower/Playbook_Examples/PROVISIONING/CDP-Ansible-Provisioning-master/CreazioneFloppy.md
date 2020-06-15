# Creazione immagine floppy con Kickstart

L'immagine floppy virtuale contiene il file di Kickstart ks.cfg e può essere montato nell'unità virtuale Floppy di ogni virtual machine VMware.

La seguente procedura richiede privilegi di root su un sistema Linux che abbia installata l'utility mkfs.vfat (package: dosfstools)

Creazione di un file immagine vuoto, dimensione 1,44MB:

```sh
# dd if=/dev/zero of=RHEL-Kickstart-floppy.img bs=1440 count=1
```

Creazione del filesystem FAT32 all'interno del file:

```sh
# mkfs.vfat -L OEMDRV RHEL-Kickstart-floppy.img
```

Mount dell'immagine nel sistema:

```sh
# mkdir /mnt/floppy
# mount -o loop RHEL-Kickstart-floppy.img /mnt/floppy
```

Copia del file ks.cfg nella root del floppy:

```sh
# cp ks.cfg /mnt/floppy
```

Unmount dell'immagine:

```sh
# umount /mnt/floppy
```

Il file RHEL-Kickstart-floppy.img è ora pronto per essere assegnato all'unità floppy virtuale della VM.
Risulta pratico caricare questo file in uno dei Datastore, assieme alle immagini ISO di RHEL.

