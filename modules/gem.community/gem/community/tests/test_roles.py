from gem.community.tests.base import FunctionalTestCase


class TestRoles(FunctionalTestCase):
    """ """

    def test_roles(self):
        """ Test roles availability """
        self.assertTrue(self.portal.portal_quickinstaller.isProductInstalled('ceflasuite.corporate'))
        self.assertTrue('GroupAdministrator' in list(getattr(self.portal, '__ac_roles__')))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRoles))
    return suite


