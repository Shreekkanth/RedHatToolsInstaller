import os
import pytest

class TestClass(object):
    pytestmark = [
        pytest.mark.ipamasters
        ]
    #Test Directory Services
    def test_DirectoryServices(self):
        ds = os.popen('ipactl status | grep Directory').read().strip()
        assert ds == "Directory Service: RUNNING", "Directory Service not running"

     # Test KRB5 Service
    def test_krb5Services(self):
        krb5 = os.popen('ipactl status | grep krb5kdc').read().strip()
        assert krb5 == "krb5kdc Service: RUNNING", "krb5kdc Service not running"

     # Test kadmin service
    def test_kadmin(self):
        kadmin = os.popen('ipactl status | grep kadmin').read().strip()
        assert kadmin == "kadmin Service: RUNNING", "kadmin Service not running"

    # Test named DNS service
    def test_named(self):
        named = os.popen('ipactl status | grep named').read().strip()
        assert named == "named Service: RUNNING", "named Service not running"

     # Test the ipa_memcached service
    def ipa_memcached(self):
        memcache = os.popen('ipactl status | grep ipa_memcached').read().strip()
        assert memcache == "ipa_memcached Service: RUNNING", "ipa_memcached not running"

    # Test web service for configuration UI
    def test_webservice(self):
        webservice = os.popen('ipactl status | grep httpd ').read().strip()
        assert webservice == "httpd Service: RUNNING", "Apache Service not running"

    # Test pki-tomcatd service
    def test_pkitomcatd(self):
        tomcat = os.popen('ipactl status | grep  pki-tomcatd').read().strip()
        assert tomcat == "pki-tomcatd Service: RUNNING", "pki-tomcatd Service not running"

    # Test named ipa-otpd service
    def test_ipaotpd(self):
        otpd = os.popen('ipactl status | grep ipa-otpd').read().strip()
        assert otpd == "ipa-otpd Service: RUNNING", "ipa-otpd Service not running"
