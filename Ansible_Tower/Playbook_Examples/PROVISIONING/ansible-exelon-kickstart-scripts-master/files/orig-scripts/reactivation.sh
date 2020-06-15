#!/usr/bin/python
try:
    import xmlrpclib
    import shutil
    import sys
    import os.path
    old_system_id = "/etc/sysconfig/rhn/systemid"
    if os.path.exists(old_system_id):
        client =  xmlrpclib.Server("http://satadmin.exelonds.com/rpc/api")
        key = client.system.obtain_reactivation_key(open(old_system_id).read())
        print key
except:
    # xml rpc due to  a old/bad system id
    # we don't care about those
    # we'll register those as new.
    pass
    
