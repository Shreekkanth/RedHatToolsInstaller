import pytest


class TestClass(object):
    pytestmark = [
        pytest.mark.ipaserver
    ]

    @pytest.fixture
    def provider(self):
        """ Construct an AD endpoint """
        from parcels.provider import Provider
        return Provider.Define("ad",
                               "https://ad-s-001.corp.def.ic.com.au:5986",
                               auth=("cloud-user", "1800RedHat"),
                               server_cert_validation='ignore')

    @pytest.fixture
    def user(self, provider):
        """ Produce a User object """
        return provider.user_show("dkelly")

    @pytest.fixture
    def group(self, provider):
        """ Produce a Group object """
        return provider.group_show("Domain Users")

    def test_user_uid(self, user):
        """ Assert the user has the correct uid produced by AD """
        assert user.uid == 1450186

    def test_group_gid(self, group):
        """ Assert the group has the correct gid produced from AD """
        assert group.gid == 1010101

    def test_user_no_private_group(self, user, group):
        """ Assert the user has the same gid as group """
        assert user.gid == group.gid
