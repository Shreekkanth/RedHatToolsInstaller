zone "example.com" IN {
        type master;
        file "master/example.com";
};

zone "99.16.172.in-addr.arpa" IN {
        type master;
        file "master/99.16.172.in-addr.arpa";
};

