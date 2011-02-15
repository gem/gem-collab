from gem.community.tests.base import FunctionalTestCase
from gem.community.config import GROUP_ADMINISTRATOR_ROLE


class TestRoles(FunctionalTestCase):
    """ """

    def test_roles(self):
        """ Test roles availability """
        self.assertTrue(GROUP_ADMINISTRATOR_ROLE in list(getattr(self.portal, '__ac_roles__')))

    def test_roles_permissions(self):
        """ Assigned by default the right permissions to the new GroupAdministrator role? """
        # we should grant the add portal member
        self.assertTrue(GROUP_ADMINISTRATOR_ROLE in [item['name'] for item in self.portal.rolesOfPermission('Add portal member') if item['selected']])
        # we don't have to purge other permission settings
        self.assertTrue('Manager' in [item['name'] for item in self.portal.rolesOfPermission('Add portal member') if item['selected']])
        self.assertTrue('Owner' in [item['name'] for item in self.portal.rolesOfPermission('Add portal member') if item['selected']])

        # and the manage users permission
        self.assertTrue(GROUP_ADMINISTRATOR_ROLE in [item['name'] for item in self.portal.rolesOfPermission('Manage users') if item['selected']])



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRoles))
    return suite


