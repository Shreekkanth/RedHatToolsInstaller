#!/usr/bin/bash
tarname="firewalld.tar.gz"
rm -rf ${tarname}
tar zcvf ${tarname} ./firewalld
