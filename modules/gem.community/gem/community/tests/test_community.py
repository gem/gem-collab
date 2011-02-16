from zope.event import notify

from gem.community.tests.base import FunctionalTestCase
from gem.community.config import WIKI_AREA_ID, FILE_AREA_ID

from Products.Archetypes.event import ObjectInitializedEvent



class TestCommunity(FunctionalTestCase):
    """ """

    def afterSetUp(self):
        self.loginAsPortalOwner()

        self.portal.invokeFactory('Community', 'com1')
        self.community1 = self.portal.com1
        notify(ObjectInitializedEvent(self.community1))
        
    def test_areas(self):
        """ Test area creations """
        self.assertTrue(WIKI_AREA_ID in self.community1.objectIds())
        self.assertTrue(FILE_AREA_ID in self.community1.objectIds())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCommunity))
    return suite


