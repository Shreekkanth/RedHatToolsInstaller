/usr/bin/echo "password" | /usr/bin/kinit "admin"
ipa dnsrecord-add lmlab.local ocpmaster1 --a-ip-address 10.2.0.22 --a-create-reverse
ipa dnsrecord-add lmlab.local ocpmaster2 --a-ip-address 10.2.0.23 --a-create-reverse
ipa dnsrecord-add lmlab.local ocpmaster3 --a-ip-address 10.2.0.24 --a-create-reverse
ipa dnsrecord-add lmlab.local ocpinfra1 --a-ip-address 10.2.0.25 --a-create-reverse
ipa dnsrecord-add lmlab.local ocpinfra2 --a-ip-address 10.2.0.26 --a-create-reverse
ipa dnsrecord-add lmlab.local ocpinfra3 --a-ip-address 10.2.0.27 --a-create-reverse
ipa dnsrecord-add lmlab.local lmlabdns01 --a-ip-address 10.2.0.21 --a-create-reverse
ipa dnsrecord-add lmlab.local cfmeui --a-ip-address 10.2.0.28 --a-create-reverse
