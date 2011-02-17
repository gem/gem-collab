
from gem.community.tests.base import FunctionalTestCase




class TestPortal(FunctionalTestCase):
    """ """

    def test_user_actions(self):
        """ Test user actions """
        self.assertTrue('manage_users' in self.portal.portal_actions.user.objectIds())
        self.assertTrue('manage_groups' in self.portal.portal_actions.user.objectIds())



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortal))
    return suite


