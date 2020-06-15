$TTL 60

@                       IN              SOA     example.com. root.example.com. (
                                        17062201        ; Serial
                                        3600            ; Refresh
                                        900             ; Retry
                                        3600000         ; Expire
                                        3600            ; Minimum
                                )
                        IN      NS      ns.example.com.

ns			IN	A	172.16.99.11

ocp36-lb1			IN	A	172.16.99.18
ocp36-lb2			IN	A	172.16.99.19
ocp36-lb			IN	A	172.16.99.20
ocp36-master1			IN	A	172.16.99.21
ocp36-master2			IN	A	172.16.99.22
ocp36-master3			IN	A	172.16.99.23
ocp36-infra1			IN	A	172.16.99.31
ocp36-infra2			IN	A	172.16.99.32
ocp36-node1			IN	A	172.16.99.41
ocp36-node2			IN	A	172.16.99.42

*.app			IN	A	172.16.99.30
