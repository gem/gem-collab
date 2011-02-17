
from gem.community.tests.base import FunctionalTestCase




class TestFile(FunctionalTestCase):
    """ """

    def afterSetUp(self):
        self.loginAsPortalOwner()

        self.portal.invokeFactory('File', 'file1')
        self.file1 = self.portal.file1
        self.portal.invokeFactory('File', 'file2')
        self.file2 = self.portal.file2
        self.file2.getField('old_version').set(self.file2, self.file1)
        
    def test_fields(self):
        """ Test schema extender field """
        field = self.file1.getField('old_version')
        # ok, the new field exists
        self.assertEquals('old_version', field.getName())
        # the field should be single valued
        self.assertFalse(field.multiValued)

    def test_reference(self):
        """ Test reference field """
        # file1 is the previous version of file2
        self.assertEquals(self.file2.getField('old_version').get(self.file2), self.file1)



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFile))
    return suite


