import os

import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_restricted_shell_security_profile_configuration_file(host):
    f = host.file('/etc/profile.d/security.sh')

    assert f.exists
    assert f.is_file
    assert f.mode == 0o644
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.contains('  HISTCONTROL=$HISTCONTROL${HISTCONTROL+,}ignoredups')
    assert f.contains('  PROMPT_COMMAND="history -a"')
    assert f.contains('  TMOUT=300')
    assert f.contains('  LESSSECURE=1')
    assert f.contains('  PATH="$HOME/bin"')
    assert f.contains('  readonly HISTCONTROL HISTFILE HISTIGNORE HISTSIZE HISTTIMEFORMAT IFS LESSSECURE PATH PROMPT_COMMAND PS1 TMOUT SHELL')  # noqa: ignore=E501
    assert f.contains('  export HISTCONTROL HISTFILE HISTIGNORE HISTSIZE HISTTIMEFORMAT IFS LESSSECURE PATH PROMPT_COMMAND PS1 TMOUT SHELL')  # noqa: ignore=E501
    assert f.contains('  umask 077')


def test_restricted_shell_rbash_activation_link(host):
    f = host.file('/usr/bin/rbash')

    assert f.exists
    assert f.is_symlink
    assert f.linked_to == '/usr/bin/bash'
    assert f.user == 'root'
    assert f.group == 'root'


@pytest.mark.parametrize("name", [
    ('bash_aliases'),
    ('config/bash_completion'),
    ('bash_logout'),
    ('bash_profile'),
    ('bashrc'),
    ('exrc'),
])
def test_restricted_shell_skel_files(host, name):
    f = host.file('/etc/skel/.' + name)

    assert f.exists
    assert f.is_file
    assert f.mode == 0o755
    assert f.user == 'root'
    assert f.group == 'root'


@pytest.mark.parametrize("name,target", [
    ('clear', 'clear'),
    ('sudo', 'sudo'),
    ('sudoedit', 'sudo'),
    ('rvim', 'vim'),
    ('rview', 'vi'),
    ('less', 'less'),
    ('passwd', 'passwd'),
    ('top', 'top'),
    ('grep', 'grep'),
    ('fgrep', 'fgrep'),
    ('egrep', 'egrep'),
    ('arch', 'arch'),
    ('base64', 'base64'),
    ('basename', 'basename'),
    ('cat', 'cat'),
    ('chcon', 'chcon'),
    ('chgrp', 'chgrp'),
    ('chmod', 'chmod'),
    ('chown', 'chown'),
])
def test_restricted_shell_skel_allowed_binaries(host, name, target):
    f = host.file('/etc/skel/.local/bin/' + name)

    assert f.exists
    assert f.is_symlink
    assert f.linked_to == '/usr/bin/' + target
    assert f.user == 'root'
    assert f.group == 'root'


@pytest.mark.parametrize("name", [
    ('awk'),
    ('elinks'),
    ('scp'),
    ('ftp'),
    ('python'),
    ('perl'),
])
def test_restricted_shell_skel_disallowed_binaries(host, name):
    f = host.file('/etc/skel/.local/bin/' + name)

    assert not f.exists
