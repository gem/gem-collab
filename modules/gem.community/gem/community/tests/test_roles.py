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

class TestWorkflows(FunctionalTestCase):
    """ """
    def afterSetUp(self):
        FunctionalTestCase.afterSetUp(self)
#        roles = ('Member', 'Contributor')
#        self.portal.portal_membership.addMember('contributor',
#                                                'secret',
#                                                roles, [])

        self.loginAsPortalOwner()
        self.portal.invokeFactory('Document', id="testdoc")
        self.portal.invokeFactory('File', id="testfile")
        
    def test_exists(self):
        """Tests workflow existance"""
        self.assertTrue('wiki_workflow' in self.portal.portal_workflow)
        self.assertTrue('file_workflow' in self.portal.portal_workflow)

    def test_wf_assigned(self):
        """Tests workflow"""
        for portal_type, chain in self.portal.portal_workflow.listChainOverrides():
            if portal_type == 'File':            
                self.assertTrue(('file_workflow',), chain)
            if portal_type == 'Document':            
                self.assertTrue(('wiki_workflow',), chain)

#    def test_wiki_wf(self):
#        """Tests workflow"""
#        wf = self.portal.portal_workflow
#        wf.doActionFor(self.portal.testdoc, action="")


    def tearDown(self):
        self.logout()
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRoles))
    suite.addTest(makeSuite(TestWorkflows))
    return suite


