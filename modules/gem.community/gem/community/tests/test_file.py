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

class TestFileViewlet(FunctionalTestCase):
    """ """
    def afterSetUp(self):
    
        self.loginAsPortalOwner()
        self.portal.invokeFactory(type_name='File', id='file1')
        self.file1 = self.portal.file1
        self.portal.invokeFactory(type_name='File', id='file2')
        self.file2 = self.portal.file2
        self.file2.getField('old_version').set(self.file2, self.file1)

    def test_newer_versions(self):
        from gem.community.browser.viewlets import FileVersions
        fv = FileVersions(self.file1, self.app.REQUEST, None, None)
        new = fv.getNewVersion()
        self.assertEquals(new['url'], self.file2.absolute_url())
        self.assertEquals(new['title'], self.file2.Title())
        
    def test_older_versions(self):
        from gem.community.browser.viewlets import FileVersions
        fv = FileVersions(self.file2, self.app.REQUEST, None, None)
        old = fv.getOldVersion()
        self.assertEquals(old['url'], self.file1.absolute_url())
        self.assertEquals(old['title'], self.file1.Title())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFile))
    suite.addTest(makeSuite(TestFileViewlet))
    return suite


