# Kernel hardening

This roles manages different aspects of kernel hardening using primarily
`sysctl` settings releated to the network stack, but also covering other aspects
such as:

  - Protection against BPF JIT spraying. A technique used to compromise a kernel
    using a Just In Time compiler available in modern kernels.
    Read a [discussion](http://www.openwall.com/lists/kernel-hardening/2016/05/23/2) about the background of this feature.
    An [article](https://mainisusuallyafunction.blogspot.co.uk/2012/11/attacking-hardened-linux-systems-with.html) describing
    the technique and a [PoC](https://github.com/01org/jit-spray-poc-for-ksp).
    The original [paper](http://www.semantiscope.com/research/BHDC2010/BHDC-2010-Paper.pdf) where JIT
    spray attacks are described.
    Lastly, why this is important in the scope of defeating a hardware protection
    such as [SMEP](http://vulnfactory.org/blog/2011/06/05/smep-what-is-it-and-how-to-beat-it-on-linux/)

Different tunables available to reduce information leakage:

  - [`kptr_restrict`](https://marc.info/?l=linux-kernel&m=129306980917336&w=2)

  - [`dmesg_restrict`](https://marc.info/?l=linux-kernel&m=128943183202231&w=2)

## Requirements

None. The required packages are managed by the role.

## Role Variables

- From `defaults/main.yml`

```yml
# Disable USB storage support.
security_rhel7_disable_usb_storage: 'yes'                      # V-71983
# Disable uncommon file systems
security_rhel7_disable_cramfs: 'yes'                           # V-71983
security_rhel7_disable_freevfxs: 'yes'                         # V-71983
security_rhel7_disable_jffs2: 'yes'                            # V-71983
security_rhel7_disable_hfs: 'yes'                              # V-71983
security_rhel7_disable_hfsplus: 'yes'                          # V-71983
security_rhel7_disable_udf: 'yes'                              # V-71983
# Disable BlueTooth
security_rhel7_disable_bluetooth: 'yes'                        # V-71983
# Disable uncommon network protocols
security_rhel7_disable_net_pf_31: 'yes'                        # V-71983
security_rhel7_disable_dccp: 'yes'                             # V-71983
security_rhel7_disable_sctp: 'yes'                             # V-71983
security_rhel7_disable_rds: 'yes'                              # V-71983
security_rhel7_disable_tipc: 'yes'                             # V-71983

# Disable kdump.
security_disable_kdump: 'yes'                                  # V-72057

# Disallow forwarding IPv4/IPv6 source routed packets on all interfaces
# immediately and by default on new interfaces.
# yamllint disable-line
security_disallow_source_routed_packet_forward_ipv4: 'yes'     # V-72283 / V-72285
security_disallow_source_routed_packet_forward_ipv6: 'yes'     # V-72319
# Disallow responses to IPv4 ICMP echoes sent to broadcast address.
security_disallow_echoes_broadcast_address: 'yes'              # V-72287
# Disallow IPV4 ICMP redirects on all interfaces immediately and by default on
# new interfaces.
# yamllint disable-line
security_disallow_icmp_redirects: 'yes'                        # V-73175 / V-72289 / V-72291 / V-72293
# Disallow IP forwarding.
security_disallow_ip_forwarding: 'yes'                         # V-72309

security_icmp_echo_ignore_all: 'yes'
security_tcp_max_syn_backlog: 'yes'
security_tcp_synack_retries: 'yes'
security_tcp_syn_retries: 'yes'
security_log_martians: 'yes'
security_accept_redirects: 'yes'
security_secure_redirects: 'yes'
security_send_redirects: 'yes'
security_ip_local_port_range: 'yes'
security_tcp_rmem: 'yes'
security_tcp_wmem: 'yes'
security_tcp_window_scaling: 'yes'
security_rmem_max: 'yes'
security_wmem_max: 'yes'
security_netdev_max_backlog: 'yes'
# Disable IPv4 traffic forwarding.
security_ip_forward: 'yes'
# Enable RFC-recommended source validation feature.
security_rp_filter: 'yes'
# Reduce the surface on SMURF attacks.
# yamllint disable-line
# Make sure to ignore ECHO broadcasts, which are only required in broad network analysis.
security_icmp_echo_ignore_broadcasts: 'yes'
# yamllint disable-line
# There is no reason to accept bogus error responses from ICMP, so ignore them instead.
security_icmp_ignore_bogus_error_responses: 'yes'
# Limit the amount of traffic the system uses for ICMP.
security_icmp_ratelimit: 'yes'
# Adjust the ICMP ratelimit to include ping, dst unreachable,
# source quench, ime exceed, param problem, timestamp reply, information reply
security_icmp_ratemask: 'yes'
# Protect against wrapping sequence numbers at gigabit speeds
security_tcp_timestamps: 'yes'
# Define restriction level for announcing the local source IP
security_arp_ignore: 'yes'
# Define mode for sending replies in response to
# received ARP requests that resolve local target IP addresses
security_arp_announce: 'yes'
# RFC 1337 fix F1
security_tcp_rfc1337: 'yes'
# Syncookies is used to prevent SYN-flooding attacks.
security_tcp_syncookies: 'yes'
# Disable IPv6 traffic forwarding.
security_ipv6_all_forwarding: 'yes'
# Ignore RAs on Ipv6.
security_accept_ra: 'yes'
# Disable IPv6
security_disable_ipv6: 'yes'
security_accept_source_route: 'yes'
security_router_solicitations: 'yes'
security_accept_ra_rtr_pref: 'yes'
security_accept_ra_pinfo: 'yes'
security_accept_ra_defrtr: 'yes'
security_autoconf: 'yes'
security_dad_transmits: 'yes'
security_max_addresses: 'yes'
# ExecShield protection against buffer overflows
security_exec_shield: 'yes'
# Enable Address Space Layout Randomization (ASLR).
security_randomize_va_space: 'yes'
security_pid_max: 'yes'
security_dmesg_restrict: 'yes'
security_kptr_restrict: 'yes'
security_kexec_load_disabled: 'yes'
security_sysrq: 'yes'
security_yama_ptrace_scope: 'yes'
# fs.suid_dumpable = 0
security_bpf_jit: 'yes'
```

- From `vars/main.yml`

```yml
## module blacklisting settings
#
# Each dictionary has this structure:
#
#   name: the module name
#   enabled: whether the variable should be set or not
#
modprobe_settings_rhel7:
  - name: usb-storage
    enabled: "{{ security_rhel7_disable_usb_storage }}"
  - name: cramfs
    enabled: "{{ security_rhel7_disable_cramfs }}"
  - name: freevfxs
    enabled: "{{ security_rhel7_disable_freevfxs }}"
  - name: jffs2
    enabled: "{{ security_rhel7_disable_jffs2 }}"
  - name: hfs
    enabled: "{{ security_rhel7_disable_hfs }}"
  - name: hfsplus
    enabled: "{{ security_rhel7_disable_hfsplus }}"
  - name: udf
    enabled: "{{ security_rhel7_disable_udf }}"
  - name: bluetooth
    enabled: "{{ security_rhel7_disable_bluetooth }}"
  - name: net-pf-31
    enabled: "{{ security_rhel7_disable_net_pf_31 }}"
  - name: dccp
    enabled: "{{ security_rhel7_disable_dccp }}"
  - name: sctp
    enabled: "{{ security_rhel7_disable_sctp }}"
  - name: rds
    enabled: "{{ security_rhel7_disable_rds }}"
  - name: tipc
    enabled: "{{ security_rhel7_disable_tipc }}"

## sysctl settings
# This variable is used in main.yml to set sysctl
# configurations on hosts.
#
# Each dictionary has this structure:
#
#   name: the sysctl configuration name
#   value: the value to set for the sysctl configuration
#   enabled: whether the variable should be set or not
#
sysctl_settings_rhel7_ipv4:
  - name: net.ipv4.conf.all.accept_source_route
    value: 0
    enabled: "{{ security_disallow_source_routed_packet_forward_ipv4 | bool }}"
  - name: net.ipv4.conf.default.accept_source_route
    value: 0
    enabled: "{{ security_disallow_source_routed_packet_forward_ipv4 | bool}}"
  - name: net.ipv4.icmp_echo_ignore_broadcasts
    value: 1
    enabled: "{{ security_disallow_echoes_broadcast_address | bool }}"
  - name: net.ipv4.conf.all.send_redirects
    value: 0
    enabled: "{{ security_disallow_icmp_redirects | bool }}"
  - name: net.ipv4.conf.default.send_redirects
    value: 0
    enabled: "{{ security_disallow_icmp_redirects | bool }}"
  - name: net.ipv4.ip_forward
    value: 0
    enabled: "{{ security_disallow_ip_forwarding | bool }}"
  - name: net.ipv4.conf.default.accept_redirects
    value: 0
    enabled: "{{ security_disallow_icmp_redirects | bool }}"
  - name: net.ipv4.icmp_echo_ignore_all
    value: '1'
    enabled: "{{ security_icmp_echo_ignore_all | bool }}"
  - name: net.ipv4.tcp_max_syn_backlog
    value: '2048'
    enabled: "{{ security_tcp_max_syn_backlog | bool }}"
  - name: net.ipv4.tcp_synack_retries
    value: '2'
    enabled: "{{ security_tcp_synack_retries | bool }}"
  - name: net.ipv4.tcp_syn_retries
    value: '5'
    enabled: "{{ security_tcp_syn_retries | bool }}"
  - name: net.ipv4.conf.all.log_martians
    value: '1'
    enabled: "{{ security_log_martians | bool }}"
  - name: net.ipv4.conf.default.log_martians
    value: '1'
    enabled: "{{ security_log_martians | bool }}"
  - name: net.ipv4.conf.all.accept_source_route
    value: '0'
    enabled: "{{ security_accept_source_route | bool }}"
  - name: net.ipv4.conf.default.accept_source_route
    value: '0'
    enabled: "{{ security_accept_source_route | bool }}"
  - name: net.ipv4.conf.all.accept_redirects
    value: '1'
    enabled: "{{ security_accept_redirects | bool }}"
  - name: net.ipv4.conf.default.accept_redirects
    value: '0'
    enabled: "{{ security_accept_redirects | bool }}"
  - name: net.ipv4.conf.all.secure_redirects
    value: '0'
    enabled: "{{ security_secure_redirects | bool }}"
  - name: net.ipv4.conf.default.secure_redirects
    value: '0'
    enabled: "{{ security_secure_redirects | bool }}"
  - name: net.ipv4.conf.all.send_redirects
    value: '0'
    enabled: "{{ security_send_redirects | bool }}"
  - name: net.ipv4.conf.default.send_redirects
    value: '0'
    enabled: "{{ security_send_redirects | bool }}"
  - name: net.ipv4.ip_local_port_range
    value: '2000 65000'
    enabled: "{{ security_ip_local_port_range | bool }}"
  - name: net.ipv4.tcp_rmem
    value: '4096 87380 8388608'
    enabled: "{{ security_tcp_rmem | bool }}"
  - name: net.ipv4.tcp_wmem
    value: '4096 87380 8388608'
    enabled: "{{ security_tcp_wmem | bool }}"
  - name: net.ipv4.tcp_window_scaling
    value: '1'
    enabled: "{{ security_tcp_window_scaling | bool }}"
  - name: net.ipv4.ip_forward
    value: 0
    enabled: "{{ security_ip_forward | bool }}"
  - name: net.ipv4.conf.all.rp_filter
    value: 1
    enabled: "{{ security_rp_filter | bool }}"
  - name: net.ipv4.conf.default.rp_filter
    value: 1
    enabled: "{{ security_rp_filter | bool }}"
  - name: net.ipv4.icmp_echo_ignore_broadcasts
    value: 1
    enabled: "{{ security_icmp_echo_ignore_broadcasts | bool }}"
  - name: net.ipv4.icmp_ignore_bogus_error_responses
    value: 1
    enabled: "{{ security_icmp_ignore_bogus_error_responses | bool }}"
  - name: net.ipv4.icmp_ratelimit
    value: 100
    enabled: "{{ security_icmp_ratelimit | bool }}"
  - name: net.ipv4.icmp_ratemask
    value: 88089
    enabled: "{{ security_icmp_ratemask | bool }}"
  - name: net.ipv4.tcp_timestamps
    value: 0
    enabled: "{{ security_tcp_timestamps | bool }}"
  - name: net.ipv4.conf.all.arp_ignore
    value: 1
    enabled: "{{ security_arp_ignore | bool }}"
  - name: net.ipv4.conf.all.arp_announce
    value: 2
    enabled: "{{ security_arp_announce | bool }}"
  - name: net.ipv4.tcp_rfc1337
    value: 1
    enabled: "{{ security_tcp_rfc1337 | bool }}"
  - name: net.ipv4.tcp_syncookies
    value: 1
    enabled: "{{ security_tcp_syncookies | bool }}"

sysctl_settings_rhel7_kernel:
  - name: kernel.dmesg_restrict
    value: '1'
    enabled: "{{ security_dmesg_restrict | bool }}"
  - name: kernel.kptr_restrict
    value: '2'
    enabled: "{{ security_kptr_restrict | bool }}"
  - name: kernel.kexec_load_disabled
    value: '1'
    enabled: "{{ security_kexec_load_disabled | bool }}"
  - name: kernel.pid_max
    value: '65536'
    enabled: "{{ security_pid_max | bool }}"
  - name: kernel.randomize_va_space
    value: '2'
    enabled: "{{ security_randomize_va_space | bool }}"
  - name: kernel.sysrq
    value: '0'
    enabled: "{{ security_sysrq | bool }}"
  - name: kernel.yama.ptrace_scope
    value: '1'
    enabled: "{{ security_yama_ptrace_scope | bool }}"

sysctl_settings_rhel7_net:
  - name: net.core.bpf_jit_enable
    value: '0'
    enabled: "{{ security_bpf_jit | bool }}"
  - name: net.core.rmem_max
    value: '8388608'
    enabled: "{{ security_rmem_max | bool }}"
  - name: net.core.wmem_max
    value: '8388608'
    enabled: "{{ security_wmem_max | bool }}"
  - name: net.core.netdev_max_backlog
    value: '5000'
    enabled: "{{ security_netdev_max_backlog | bool }}"

sysctl_settings_rhel7_ipv6:
  - name: net.ipv6.conf.all.accept_source_route
    value: 0
    enabled: "{{ security_disallow_source_routed_packet_forward_ipv6 | bool }}"
  - name: net.ipv6.conf.all.disable_ipv6
    value: 1
    enabled: "{{ security_disable_ipv6 | bool }}"
  - name: net.ipv6.conf.all.forwarding
    value: 0
    enabled: "{{ security_ipv6_all_forwarding | bool }}"
  - name: net.ipv6.conf.all.accept_ra
    value: 0
    enabled: "{{ security_accept_ra | bool }}"
  - name: net.ipv6.conf.default.accept_ra
    value: 0
    enabled: "{{ security_accept_ra | bool }}"
  - name: net.ipv6.conf.all.rp_filter
    value: '1'
    enabled: "{{ security_rp_filter | bool }}"
  - name: net.ipv6.conf.all.accept_source_route
    value: '0'
    enabled: "{{ security_accept_source_route | bool }}"
  - name: net.ipv6.conf.default.accept_source_route
    value: '0'
    enabled: "{{ security_accept_source_route | bool }}"
  - name: net.ipv6.conf.all.accept_redirects
    value: '0'
    enabled: "{{ security_accept_redirects | bool }}"
  - name: net.ipv6.conf.default.accept_redirects
    value: '0'
    enabled: "{{ security_accept_redirects | bool }}"
  - name: net.ipv6.conf.default.router_solicitations
    value: '0'
    enabled: "{{ security_router_solicitations | bool }}"
  - name: net.ipv6.conf.default.accept_ra_rtr_pref
    value: '0'
    enabled: "{{ security_accept_ra_rtr_pref | bool }}"
  - name: net.ipv6.conf.default.accept_ra_pinfo
    value: '0'
    enabled: "{{ security_accept_ra_pinfo | bool }}"
  - name: net.ipv6.conf.default.accept_ra_defrtr
    value: '0'
    enabled: "{{ security_accept_ra_defrtr | bool }}"
  - name: net.ipv6.conf.default.autoconf
    value: '0'
    enabled: "{{ security_autoconf | bool }}"
  - name: net.ipv6.conf.default.dad_transmits
    value: '0'
    enabled: "{{ security_dad_transmits | bool }}"
  - name: net.ipv6.conf.default.max_addresses
    value: '1'
    enabled: "{{ security_max_addresses | bool }}"
```

## Dependencies

None.

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yml
    - hosts: servers
      roles:
         - { role: ansible-os-hardening-kernel }
```

## License

Apache 2.0, as this work is derived from [OpenStack's ansible-hardening role](https://github.com/openstack/ansible-hardening).

## Author Information

[David Sastre](david.sastre@redhat.com)
