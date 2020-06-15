# Importing a private key from the ASC backup

1. Get the software: dnf install -y pinentry gnupg2

2. Load the key files serially: gpg2 --import <keyfile>

3. Verify all keys are loaded: gpg2 -K --with-keygrip

   See the Note in pass as needed (KeyNotes)

# Importing a new ssh key

Reference: https://unix.stackexchange.com/questions/372879/import-my-ssh-key-as-gpg-sub-key-to-use-for-ssh-authentication

1. Export the private key to be added too to a file: gpg2 -a --export-secret-key <key>

2. Put the exported gpg key and the ssh keys in a temporary directory

3. In a clean user, typically a temporary container do this:

4. Install the needed software: dnf install -y gnupg2 pinentry monkeysphere

5. Load the key file: gpg2 --import <keyfile>

6. Import the ssh key: pem2openpgp <TEMP_USERID> < .ssh/id_rsa | gpg2 --import

7. List keys with keygrip: gpg2 -K --with-keygrip

8. Edit the key I want to keep (imported in step 5) and use addkey and existing key.  Don't forget to set Authentication only.

9. Export the final key and save it.  Then import it into your real keychain

# Setting up SSH keys to be served from GPG

Reference: https://ryanlue.com/posts/2017-06-29-gpg-for-ssh-auth

1. Put "enable-ssh-support" in ~/.gnupg/gpg-agent.conf

2. Add keygrips to ~/.gnupg/sshcontrol from `gpg2 -k --with-keygrip`

3. Enable the SSH Socket by adding these lines to ~/.bash_profile

    export SSH_AUTH_SOCK=$(gpgconf --list-dirs agent-ssh-socket)
    gpgconf --launch gpg-agent

4. Kill any running GPG agents

5. Source ~/.bash_profile

6. Test - a good one is `ssh -T git@github.com`
