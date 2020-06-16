The Ansible configuration is heavily influenced by https://github.com/maxamillion/maxible/

I use [GNU Stow](https://www.gnu.org/software/stow/) to manage my dotfiles.  I am basically using the methodology that [Alex Pearce describes](https://alexpearce.me/2016/02/managing-dotfiles-with-stow/).  A key difference is that my `.dotfiles` directory is actually a set of directories in this repository.  Additionally, some of the dotfiles are stored here in encrypted form.  They are made available to my session by having them mounted in decrypted form at login.  Details below.

# Getting Data from the old laptop

1. Save Firefox and Chrome Bookmarks
   - ideally this is done manually, if not look here:
     * Firefox: .mozilla/firefox/<profile>/places.sqlite
     * Chrome: .config/google-chrome/Default/Bookmarks
1. BACKUP (minimally /home and /etc)
   * save off to wifi passwords from /etc/sysconfig/network-scripts/keys*
1. See private-manual-steps.md for other needs

# Building a new laptop

1. Install Fedora Workstation
   * Encrypt disk
   * 1 data partition + boot + swap
   * After reboot, create bexelbie
1. Check for bios updates with fwupdmgr
   1. fwupdmgr refresh
   2. fwupdmgr get-devices # verify machine is in the list
   3. fwupdmgr get-updates
   4. fwupdmgr update
1. Manually update the system `dnf update -y` and reboot
1. Set up `pass` and reload my password store - see step0.md
1. `sudo dnf install -y ansible python3-dnf git`
1. Clone this repository into ~bexelbie/Repositories/ - see step0.md for a note
1. Verify settings in inventory version numbers
1. Install the remote roles: ansible-galaxy install -r requirements.yml
1. `ansible-playbook workstation.yml -i inventory --ask-become-pass`
1. Run manual steps in manual-steps.md and private-manual-steps.md
1. Manually update the system `dnf update -y` and reboot again

# Notes/FAQs

* What are all these weird unreadable blocks of text in some files?

  Some files are stored here in an encrypted form generated by either `ansible-vault` for `gocryptfs`.  There are two ansible vaults in use in this playbook.  One is used for work related configurations and the other for personal configurations.  If you work with me - you can request the password for the ones relevant to our work by emailing me.

  * To encrypt files with ansible-vault: `ansible-vault encrypt --encrypt-vault-id <bex|RH> <file>`
  * To view files with ansible-vault: `ansible-vault view <file>`

  * To mount with gocryptfs: `gocryptfs secure.encrypted secure` # in the right directory

* How do you use all these encrypted files then at install and run-time?

  Ansible knows how to unlock ansible-vaults when the playbook is run.  Additionally, I have setup the `ansible.cfg` to automatically use the shell scripts in `bin/` to pull my passwords from `pass`.

  At the point of graphical login, my system mounts the gocryptfs volume that contains my encrypted doc.  This is not yet fully documented, but can be teased out by look at `tasks/user.yml`.  The short version is that Gnome autostarts a script that starts a systemd --user target.  That target then pulls in the gocryptfs-mounter.service.

* You keep using pass but I don't see it setup.  What's the deal?  How are you recovering this and your GPG key?

  I use my GPG key to manage both GPG and SSH.  You can see some hints about how to do this in `docs/gpg-notes.md`.  Until someone actually asks for details, I am not going to write up the specific instructions in a clean way.

* Why are you hiding some of your dotfiles?

  My dotfiles are all present in this repo, but some are encrypted.  This is because they contain metadata that I'd prefer not be published.  If you're looking for dotfile examples, see the many fine repos at https://dotfiles.github.io

* I heared that you should never publish files that have sekrits in them, even if they are encrypted.  Why are you doing this?

  While this may be true, I believe that the two different encryption schemes used in this repo (gocryptfs and ansible-vault) are well made.  I have selected what I believe to be good phrases and taken appropriate key security.  Additionally, the encrypted data contains metadata, such as hostnames that exist behind firewalls or non-obvious repository urls, which if exposed do not represent harm in the manner of a traditional sekrit.

# File Inventory

* **README.md**: This File
* **Ansible files**: Used to make Ansible Go
  * ansible.cfg
  * bin
  * requirements.yml
  * handlers
  * inventory
  * tasks
  * varfiles
  * workstation.yml
* **docs**: Additional Notes and setup steps
* **dot-files**: My dotfiles and files used for setup.  The secure.encrypted directory is ... encrypted.  It gets mounted to dot-files/secure