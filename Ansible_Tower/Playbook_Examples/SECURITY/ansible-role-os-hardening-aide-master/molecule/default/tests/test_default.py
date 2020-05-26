import os

import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("name,version", [
    ("aide", "0.15.1"),
])
def test_aide_packages(host, name, version):
    pkg = host.package(name)
    assert pkg.is_installed
    assert pkg.version.startswith(version)


def test_aide_configuration_file(host):
    f = host.file('/etc/aide.conf')

    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'


def test_aide_configuration_dir(host):
    d = host.file('/etc/aide/aide.conf.d')

    assert d.exists
    assert d.is_directory
    assert d.mode == 0o750
    assert d.user == 'root'
    assert d.group == 'root'


def test_aide_exclusions_configuration_file(host):
    f = host.file('/etc/aide/aide.conf.d/ZZ_aide_exclusions')

    assert f.exists
    assert f.is_file
    assert f.mode == 0o640
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.contains('!/opt')
    assert f.contains('!/run')
    assert f.contains('!/var')


def test_aide_database(host):
    f = host.file('/var/lib/aide/aide.db.gz')

    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'


def test_cron_directory(host):
    d = host.file('/etc/cron.d')

    assert d.exists
    assert d.is_directory
    assert d.mode == 0o750
    assert d.user == 'root'
    assert d.group == 'root'


def test_cron_aide(host):
    f = host.file('/etc/cron.d/aide')

    assert f.exists
    assert f.is_file
    assert f.mode == 0o644
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.contains('aide --check | /bin/mail -s "$HOSTNAME - Daily AIDE check run" root')  # noqa: E501
