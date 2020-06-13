import os

import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("name,version", [
    ('clamav', '0.99.2'),
    ('clamav-data', '0.99.2'),
    ('clamav-devel', '0.99.2'),
    ('clamav-filesystem', '0.99.2'),
    ('clamav-lib', '0.99.2'),
    ('clamav-scanner', '0.99.2'),
    ('clamav-scanner-systemd', '0.99.2'),
    ('clamav-server', '0.99.2'),
    ('clamav-server-systemd', '0.99.2'),
    ('clamav-update', '0.99.2')
])
def test_clamav_packages(host, name, version):
    pkg = host.package(name)
    assert pkg.is_installed
    assert pkg.version.startswith(version)


def test_clamav_binary(host):
    f = host.file('/usr/bin/clamdscan')

    assert f.exists


@pytest.mark.parametrize("name", [
    ('/etc/clamd.d/scan.conf'),
    ('/etc/freshclam.conf')
])
def test_clamav_configuration_files(host, name):
    f = host.file(name)

    assert f.exists
    assert f.is_file
    assert f.mode == 0o640
    assert f.user == 'root'
    assert f.group == 'root'
    assert not f.contains('Example')


def test_clamav_sysconfig_file(host):
    f = host.file('/etc/sysconfig/freshclam')

    assert f.exists
    assert f.is_file
    assert f.mode == 0o644
    assert f.user == 'root'
    assert f.group == 'root'
    assert not f.contains('^FRESHCLAM_DELAY')


# def test_clamav_service(host):
#     s = host.service('clamd@scan')
#
#     assert s.is_enabled
