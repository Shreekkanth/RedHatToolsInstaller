import os

import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("name", [
    ("login"),
    ("remote"),
    ("sshd"),
])
def test_polyinstantiation_pam_configuration(host, name):
    f = host.file('/etc/pam.d/' + name)

    assert f.exists
    assert f.is_file
    assert f.mode == 0o644
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.contains('pam_namespace.so unmnt_remnt gen_hash require_selinux')


def test_polyinstantiation_namespace_configuration_file(host):
    f = host.file('/etc/security/namespace.conf')

    assert f.exists
    assert f.is_file
    assert f.mode == 0o644
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.contains('/tmp   /tmp/.inst/tmp-$USER   context:create:iscript=tmp    root')  # noqa: ignore=E501
    assert f.contains('/var/tmp   /tmp/.inst/var-tmp-$USER   context:create:iscript=var-tmp    root')  # noqa: ignore=E501
    assert f.contains('$HOME   /home/.inst/home-$USER   context:create:iscript=home    root')  # noqa: ignore=E501


@pytest.mark.parametrize("name", [
    ("tmp"),
    ("var-tmp"),
    ("home"),
])
def test_polyinstantiation_namespace_bootstrap_script_files(host, name):
    f = host.file('/etc/security/namespace.d/' + name)

    assert f.exists
    assert f.is_file
    assert f.mode == 0o755
    assert f.user == 'root'
    assert f.group == 'root'
