import os

# import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_disabled_modules_config(host):
    f = host.file('/etc/modprobe.d/00-ansible-hardening.conf')

    assert f.exists
    assert f.is_file
    assert f.mode == 0o644
    assert f.user == 'root'
    assert f.group == 'root'


def test_disabled_modules_kernel(host):
    f = host.file('/etc/modprobe.d/00-ansible-hardening.conf')

    assert f.contains('install usb-storage /bin/true')
    assert f.contains('install cramfs /bin/true')
    assert f.contains('install freevfxs /bin/true')
    assert f.contains('install jffs2 /bin/true')
    assert f.contains('install hfs /bin/true')
    assert f.contains('install hfsplus /bin/true')
    assert f.contains('install udf /bin/true')
    assert f.contains('install bluetooth /bin/true')
    assert f.contains('install net-pf-31 /bin/true')
    assert f.contains('install dccp /bin/true')
    assert f.contains('install sctp /bin/true')
    assert f.contains('install rds /bin/true')
    assert f.contains('install tipc /bin/true')


# @pytest.mark.parametrize("name,value", [
#     ("net.ipv4.conf.all.accept_source_route", "0"),
#     ("net.ipv4.conf.default.accept_source_route", "0"),
#     ("net.ipv4.icmp_echo_ignore_broadcasts", "1"),
#     ("net.ipv4.conf.all.send_redirects", "0"),
#     ("net.ipv4.conf.default.send_redirects", "0"),
#     ("net.ipv4.ip_forward", "0"),
#     ("net.ipv6.conf.all.accept_source_route", "0"),
#     ("net.ipv4.conf.default.accept_redirects", "0"),
#     ("net.ipv4.icmp_echo_ignore_all", "1"),
#     ("net.ipv4.tcp_max_syn_backlog", "2048"),
#     ("net.ipv4.tcp_synack_retries", "2"),
#     ("net.ipv4.tcp_syn_retries", "5"),
#     ("net.ipv4.conf.all.log_martians", "1"),
#     ("net.ipv4.conf.default.log_martians", "1"),
#     ("net.ipv4.conf.all.accept_source_route", "0"),
#     ("net.ipv4.conf.default.accept_source_route", "0"),
#     ("net.ipv4.conf.all.accept_redirects", "1"),
#     ("net.ipv4.conf.default.accept_redirects", "0"),
#     ("net.ipv4.conf.all.secure_redirects", "0"),
#     ("net.ipv4.conf.default.secure_redirects", "0"),
#     ("net.ipv4.conf.all.send_redirects", "0"),
#     ("net.ipv4.conf.default.send_redirects", "0"),
#     ("net.ipv4.tcp_timestamps", "1"),
#     ("net.ipv4.ip_local_port_range", "2000 65000"),
#     ("net.ipv4.tcp_rmem", "4096 87380 8388608"),
#     ("net.ipv4.tcp_wmem", "4096 87380 8388608"),
#     ("net.ipv4.tcp_window_scaling", "1"),
#     ("net.core.rmem_max", "8388608"),
#     ("net.core.wmem_max", "8388608"),
#     ("net.core.netdev_max_backlog", "5000"),
#     ("net.ipv4.ip_forward", 0),
#     ("net.ipv4.conf.all.rp_filter", 1),
#     ("net.ipv4.conf.default.rp_filter", 1),
#     ("net.ipv4.icmp_echo_ignore_broadcasts", 1),
#     ("net.ipv4.icmp_ignore_bogus_error_responses", 1),
#     ("net.ipv4.icmp_ratelimit", 100),
#     ("net.ipv4.icmp_ratemask", 88089),
#     ("net.ipv4.tcp_timestamps", 0),
#     ("net.ipv4.conf.all.arp_ignore", 1),
#     ("net.ipv4.conf.all.arp_announce", 2),
#     ("net.ipv4.tcp_rfc1337", 1),
#     ("net.ipv4.tcp_syncookies", 1),
#     ("net.ipv6.conf.all.disable_ipv6", 1),
#     ("net.ipv6.conf.all.forwarding", 0),
#     ("net.ipv6.conf.all.accept_ra", 0),
#     ("net.ipv6.conf.default.accept_ra", 0),
#     ("net.ipv6.conf.all.rp_filter", "1"),
#     ("net.ipv6.conf.all.accept_source_route", "0"),
#     ("net.ipv6.conf.default.accept_source_route", "0"),
#     ("net.ipv6.conf.all.accept_redirects", "0"),
#     ("net.ipv6.conf.default.accept_redirects", "0"),
#     ("net.ipv6.conf.default.router_solicitations", "0"),
#     ("net.ipv6.conf.default.accept_ra_rtr_pref", "0"),
#     ("net.ipv6.conf.default.accept_ra_pinfo", "0"),
#     ("net.ipv6.conf.default.accept_ra_defrtr", "0"),
#     ("net.ipv6.conf.default.autoconf", "0"),
#     ("net.ipv6.conf.default.dad_transmits", "0"),
#     ("net.ipv6.conf.default.max_addresses", "1"),
#     ("kernel.exec-shield", 1),
#     ("kernel.randomize_va_space", "2"),
#     ("kernel.pid_max", "65536")
# ])
# def test_sysctl_settings(host, name, value):
#     s = host.sysctl(name)
#     assert s == value
#
#
# def test_sysctl_configuration_file(host):
#     f = host.file('/etc/sysctl.conf')
#
#     assert f.exists
#     assert f.is_file
#     assert f.mode == 0o644
#     assert f.user == 'root'
#     assert f.group == 'root'
#
#
# def test_kdump_service(host):
#     s = host.service('kdump')
#
#     assert not s.is_enabled


def test_fips_mode(host):
    c = host.run("cat /proc/sys/crypto/fips_enabled")

    assert c.stdout.rstrip('\n') == '1'
