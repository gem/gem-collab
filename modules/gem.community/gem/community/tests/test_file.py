from gem.community.tests.base import FunctionalTestCase


class TestFile(FunctionalTestCase):
    """ """
    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory(type_name='File', id='file1')
        self.file1 = self.portal.file1
        self.portal.invokeFactory(type_name='File', id='file2')
        self.file2 = self.portal.file2
        
    def test_schema_extender(self):
        """ Tests schema extender """
        from gem.community.config import PROJECTNAME
        self.assertTrue(self.file2.getField('old_version'))
        self.portal.portal_quickinstaller.uninstallProducts([PROJECTNAME])
        self.assertFalse(self.file2.getField('old_version'))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFile))
    return suite


