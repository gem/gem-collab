from zope.event import notify
from Products.Archetypes.event import ObjectInitializedEvent

from gem.community.tests.base import FunctionalTestCase
from gem.community.config import GROUP_ADMINISTRATOR_ROLE

from gem.community.config import WIKI_AREA_ID, FILE_AREA_ID


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

        self.portal.portal_membership.addMember('user1',
                                                'secret',
                                                ('Member'), [])

        self.portal.portal_membership.addMember('gadmin1',
                                                'secret',
                                                ('Member', 'GroupAdministrator'), [])

        
    def test_exists(self):
        """Tests workflow existance"""
        self.assertTrue('wiki_workflow' in self.portal.portal_workflow)
        self.assertTrue('file_workflow' in self.portal.portal_workflow)
        self.assertTrue('community_workflow' in self.portal.portal_workflow)

    def test_wf_assigned(self):
        """Tests workflow"""
        for portal_type, chain in self.portal.portal_workflow.listChainOverrides():
            if portal_type == 'File':            
                self.assertTrue(('file_workflow',), chain)
            if portal_type == 'Document':            
                self.assertTrue(('wiki_workflow',), chain)
            if portal_type == 'Community':            
                self.assertTrue(('community_workflow',), chain)


    def test_create_user(self):
        """user can't create anything on the root"""
        from AccessControl import Unauthorized
        self.login('user1')
        self.assertRaises(Unauthorized, self.portal.invokeFactory,'Document', "testdoc1")
        self.assertRaises(Unauthorized, self.portal.invokeFactory,'Community', "community")
        
    def test_group_admin_create_content(self):
        """group administrators can create communities and manage them (create content, add local roles)
        """
        self.login('gadmin1')
        #group administrator can create communities
        self.assertTrue(self.portal.invokeFactory('Community', "community1"))
        notify(ObjectInitializedEvent(self.portal.community1))
        wikiarea = getattr(self.portal.community1, WIKI_AREA_ID)
        filearea = getattr(self.portal.community1, FILE_AREA_ID)
        #group administrator can create docs and files
        self.assertTrue(wikiarea.invokeFactory('Document', "testdoc1"))
        self.assertTrue(filearea.invokeFactory('File', "testfile1"))


    def test_users_create_content(self):
        """a user can create content when a group admin assign local roles to him"""
        self.login('gadmin1')
        #group administrator can create communities
        self.portal.invokeFactory('Community', "community1")
        notify(ObjectInitializedEvent(self.portal.community1))
        wikiarea = getattr(self.portal.community1, WIKI_AREA_ID)
        filearea = getattr(self.portal.community1, FILE_AREA_ID)

        # add local roles to user1
        self.portal.community1.manage_addLocalRoles('user1', ['Reader', 'Contributor'])
        self.portal.community1.reindexObjectSecurity()

        self.login('user1')
        #user1 can create docs and files
        self.assertTrue(wikiarea.invokeFactory('Document', "userdoc1"))
        self.assertTrue(filearea.invokeFactory('File', "userfile1"))


    def test_group_admin(self):
        """group administrator can't create content on the site except communities"""
        self.login('gadmin1')
        from AccessControl import Unauthorized
        # group admin cannot create a document different than a community in the portal
        self.assertRaises(Unauthorized, self.portal.invokeFactory,'Document', "testdoc1")

    def tearDown(self):
        self.logout()

class TestWorkflowPermissions(FunctionalTestCase):
    """community1 is a community of groupadministrator
       """
    def afterSetUp(self):
        FunctionalTestCase.afterSetUp(self)
        #create two users
        self.portal.portal_membership.addMember('groupmember',
                                                'secret',
                                                ('Member'), [])

        self.portal.portal_membership.addMember('otheruser',
                                                'secret',
                                                ('Member'), [])
        
        self.portal.portal_membership.addMember('othergroupmember',
                                                'secret',
                                                ('Member'), [])

        #create two group admin
        self.portal.portal_membership.addMember('groupadministrator',
                                                'secret',
                                                ('Member', 'GroupAdministrator'), [])

        self.portal.portal_membership.addMember('othergroupadministrator',
                                                'secret',
                                                ('Member', 'GroupAdministrator'), [])

        #
        # create content
        #
        self.login('groupadministrator')
        #group administrator can create communities
        self.portal.invokeFactory('Community', "community")
        notify(ObjectInitializedEvent(self.portal.community))
        self.wikiarea = getattr(self.portal.community, WIKI_AREA_ID)
        self.filearea = getattr(self.portal.community, FILE_AREA_ID)
        #group administrator can create docs and files
        self.wikiarea.invokeFactory('Document', "gadminwikiprivate")
        self.wikiarea.invokeFactory('Document', "gadminwikipublished")

        self.filearea.invokeFactory('File', "gadminfileprivate")
        self.filearea.invokeFactory('File', "gadminfilesubmitted")
        self.filearea.invokeFactory('File', "gadminfilepublished")

        # add local roles to groupmember
        self.portal.community.manage_addLocalRoles('groupadministrator', [ 'Contributor', 'Editor']) 
        self.portal.community.manage_addLocalRoles('groupmember', [ 'Contributor']) 
        self.portal.community.manage_addLocalRoles('othergroupmember', [ 'Contributor']) 
        self.portal.community.reindexObjectSecurity()

        self.login('groupmember')
        #groupmember can create docs and files
        self.wikiarea.invokeFactory('Document', "gmemberwikiprivate")
        self.wikiarea.invokeFactory('Document', "gmemberwikipublished")

        self.filearea.invokeFactory('File', "gmemberfileprivate")
        self.filearea.invokeFactory('File', "gmemberfilesubmitted")
        self.filearea.invokeFactory('File', "gmemberfilepublished")


        #
        # set workflow state
        #
        self.login('groupadministrator')
        wf = self.portal.portal_workflow
        wf.doActionFor(self.wikiarea.gadminwikipublished, action="publish")
        wf.doActionFor(self.filearea.gadminfilesubmitted, action="submit")
        wf.doActionFor(self.filearea.gadminfilepublished, action="publish")
        wf.doActionFor(self.wikiarea.gmemberwikipublished, action="publish")
        wf.doActionFor(self.filearea.gmemberfilesubmitted, action="submit")
        wf.doActionFor(self.filearea.gmemberfilepublished, action="publish")


    #
    # testing community
    #

    def test_gadmin_community(self):
        """group admin / community permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('groupadministrator')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.portal.community))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.portal.community))

    def test_other_gadmin_community(self):
        """other group admin / community permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('othergroupadministrator')
        sm = getSecurityManager()

        self.assertFalse(sm.checkPermission(View, self.portal.community))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.portal.community))

    def test_gmember_community(self):
        """group member / community permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('groupmember')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.portal.community))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.portal.community))

    def test_otheruser_community(self):
        """other users / community permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('otheruser')
        sm = getSecurityManager()

        self.assertFalse(sm.checkPermission(View, self.portal.community))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.portal.community))

    #
    # testing wiki private 
    #

    def test_gadmin_wiki_private(self):
        """group administrator/ private wiki permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('groupadministrator')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.wikiarea.gadminwikiprivate))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.wikiarea.gadminwikiprivate))
        self.assertTrue(sm.checkPermission(ReviewPortalContent, self.wikiarea.gadminwikiprivate))

        self.assertTrue(sm.checkPermission(View, self.wikiarea.gmemberwikiprivate))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.wikiarea.gmemberwikiprivate))
        self.assertTrue(sm.checkPermission(ReviewPortalContent, self.wikiarea.gmemberwikiprivate))


    def test_othergadmin_wiki_private(self):
        """other group administrator/ private wiki permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('othergroupadministrator')
        sm = getSecurityManager()

        self.assertFalse(sm.checkPermission(View, self.wikiarea.gadminwikiprivate))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.wikiarea.gadminwikiprivate))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.wikiarea.gadminwikiprivate))

        self.assertFalse(sm.checkPermission(View, self.wikiarea.gmemberwikiprivate))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.wikiarea.gmemberwikiprivate))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.wikiarea.gmemberwikiprivate))

    def test_gmember_wiki_private(self):
        """group member / private wiki permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('groupmember')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.wikiarea.gadminwikiprivate))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.wikiarea.gadminwikiprivate))
        self.assertTrue(sm.checkPermission(ReviewPortalContent, self.wikiarea.gadminwikiprivate))

        self.assertTrue(sm.checkPermission(View, self.wikiarea.gmemberwikiprivate))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.wikiarea.gmemberwikiprivate))
        self.assertTrue(sm.checkPermission(ReviewPortalContent, self.wikiarea.gmemberwikiprivate))

    def test_otheruser_wiki_private(self):
        """otheruser / private wiki permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('otheruser')
        sm = getSecurityManager()

        self.assertFalse(sm.checkPermission(View, self.wikiarea.gadminwikiprivate))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.wikiarea.gadminwikiprivate))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.wikiarea.gadminwikiprivate))

        self.assertFalse(sm.checkPermission(View, self.wikiarea.gmemberwikiprivate))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.wikiarea.gmemberwikiprivate))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.wikiarea.gmemberwikiprivate))

    #
    # testing wiki published 
    #

    def test_gadmin_wiki_published(self):
        """group administrator/ published wiki permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('groupadministrator')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.wikiarea.gadminwikipublished))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.wikiarea.gadminwikipublished))
        self.assertTrue(sm.checkPermission(ReviewPortalContent, self.wikiarea.gadminwikipublished))

        self.assertTrue(sm.checkPermission(View, self.wikiarea.gmemberwikipublished))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.wikiarea.gmemberwikipublished))
        self.assertTrue(sm.checkPermission(ReviewPortalContent, self.wikiarea.gmemberwikipublished))

    def test_othergadmin_wiki_published(self):
        """other group administrator/ published wiki permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('othergroupadministrator')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.wikiarea.gadminwikipublished))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.wikiarea.gadminwikipublished))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.wikiarea.gadminwikipublished))

        self.assertTrue(sm.checkPermission(View, self.wikiarea.gmemberwikipublished))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.wikiarea.gmemberwikipublished))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.wikiarea.gmemberwikipublished))

    def test_gmember_wiki_published(self):
        """group member / published wiki permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('groupmember')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.wikiarea.gadminwikipublished))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.wikiarea.gadminwikipublished))
        self.assertTrue(sm.checkPermission(ReviewPortalContent, self.wikiarea.gadminwikipublished))

        self.assertTrue(sm.checkPermission(View, self.wikiarea.gmemberwikipublished))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.wikiarea.gmemberwikipublished))
        self.assertTrue(sm.checkPermission(ReviewPortalContent, self.wikiarea.gmemberwikipublished))

    def test_otheruser_wiki_published(self):
        """otheruser / published wiki permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('otheruser')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.wikiarea.gadminwikipublished))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.wikiarea.gadminwikipublished))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.wikiarea.gadminwikipublished))

        self.assertTrue(sm.checkPermission(View, self.wikiarea.gmemberwikipublished))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.wikiarea.gmemberwikipublished))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.wikiarea.gmemberwikipublished))

    #
    # testing file private 
    #

    def test_gadmin_file_private(self):
        """group administrator/ private file permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('groupadministrator')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.filearea.gadminfileprivate))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.filearea.gadminfileprivate))
        self.assertTrue(sm.checkPermission(ReviewPortalContent, self.filearea.gadminfileprivate))

        self.assertTrue(sm.checkPermission(View, self.filearea.gmemberfileprivate))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.filearea.gmemberfileprivate))
        self.assertTrue(sm.checkPermission(ReviewPortalContent, self.filearea.gmemberfileprivate))


    def test_othergadmin_file_private(self):
        """other group administrator/ private file permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('othergroupadministrator')
        sm = getSecurityManager()

        self.assertFalse(sm.checkPermission(View, self.filearea.gadminfileprivate))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gadminfileprivate))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gadminfileprivate))

#        community workflow : owner add review portal content
#        file workflow, wiki workflow: acquire review portal content permission

        self.assertFalse(sm.checkPermission(View, self.filearea.gmemberfileprivate))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gmemberfileprivate))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gmemberfileprivate))

    def test_gmember_file_private(self):
        """group member / private file permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('groupmember')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.filearea.gadminfileprivate))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gadminfileprivate))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gadminfileprivate))

        self.assertTrue(sm.checkPermission(View, self.filearea.gmemberfileprivate))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.filearea.gmemberfileprivate))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gmemberfileprivate))
        self.assertTrue(sm.checkPermission(RequestReview, self.filearea.gmemberfileprivate))

    def test_otheruser_file_private(self):
        """otheruser / private file permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('otheruser')
        sm = getSecurityManager()

        self.assertFalse(sm.checkPermission(View, self.filearea.gadminfileprivate))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gadminfileprivate))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gadminfileprivate))

        self.assertFalse(sm.checkPermission(View, self.filearea.gmemberfileprivate))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gmemberfileprivate))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gmemberfileprivate))

    #
    # testing file submitted 
    #

    def test_gadmin_file_submitted(self):
        """group administrator/ submitted file permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('groupadministrator')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.filearea.gadminfilesubmitted))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.filearea.gadminfilesubmitted))
        self.assertTrue(sm.checkPermission(ReviewPortalContent, self.filearea.gadminfilesubmitted))

        self.assertTrue(sm.checkPermission(View, self.filearea.gmemberfilesubmitted))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.filearea.gmemberfilesubmitted))
        self.assertTrue(sm.checkPermission(ReviewPortalContent, self.filearea.gmemberfilesubmitted))


    def test_othergadmin_file_submitted(self):
        """other group administrator/ submitted file permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('othergroupadministrator')
        sm = getSecurityManager()

        self.assertFalse(sm.checkPermission(View, self.filearea.gadminfilesubmitted))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gadminfilesubmitted))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gadminfilesubmitted))

        self.assertFalse(sm.checkPermission(View, self.filearea.gmemberfilesubmitted))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gmemberfilesubmitted))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gmemberfilesubmitted))

    def test_gmember_file_submitted(self):
        """group member / submitted file permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('groupmember')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.filearea.gadminfilesubmitted))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gadminfilesubmitted))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gadminfilesubmitted))

        self.assertTrue(sm.checkPermission(View, self.filearea.gmemberfilesubmitted))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gmemberfilesubmitted))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gmemberfilesubmitted))

    def test_otheruser_file_submitted(self):
        """otheruser / submitted file permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('otheruser')
        sm = getSecurityManager()

        self.assertFalse(sm.checkPermission(View, self.filearea.gadminfilesubmitted))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gadminfilesubmitted))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gadminfilesubmitted))

        self.assertFalse(sm.checkPermission(View, self.filearea.gmemberfilesubmitted))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gmemberfilesubmitted))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gmemberfilesubmitted))

    #
    # testing file published 
    #

    def test_gadmin_file_published(self):
        """group administrator/ published file permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('groupadministrator')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.filearea.gadminfilepublished))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.filearea.gadminfilepublished))
        self.assertTrue(sm.checkPermission(ReviewPortalContent, self.filearea.gadminfilepublished))

        self.assertTrue(sm.checkPermission(View, self.filearea.gmemberfilepublished))
        self.assertTrue(sm.checkPermission(ModifyPortalContent, self.filearea.gmemberfilepublished))
        self.assertTrue(sm.checkPermission(ReviewPortalContent, self.filearea.gmemberfilepublished))


    def test_othergadmin_file_published(self):
        """other group administrator/ published file permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('othergroupadministrator')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.filearea.gadminfilepublished))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gadminfilepublished))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gadminfilepublished))

        self.assertTrue(sm.checkPermission(View, self.filearea.gmemberfilepublished))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gmemberfilepublished))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gmemberfilepublished))

    def test_gmember_file_published(self):
        """group member / published file permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('groupmember')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.filearea.gadminfilepublished))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gadminfilepublished))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gadminfilepublished))

        self.assertTrue(sm.checkPermission(View, self.filearea.gmemberfilepublished))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gmemberfilepublished))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gmemberfilepublished))

    def test_otheruser_file_published(self):
        """otheruser / published file permissions"""
        from AccessControl import Unauthorized, getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent, View, ReviewPortalContent, RequestReview
        self.login('otheruser')
        sm = getSecurityManager()

        self.assertTrue(sm.checkPermission(View, self.filearea.gadminfilepublished))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gadminfilepublished))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gadminfilepublished))

        self.assertTrue(sm.checkPermission(View, self.filearea.gmemberfilepublished))
        self.assertFalse(sm.checkPermission(ModifyPortalContent, self.filearea.gmemberfilepublished))
        self.assertFalse(sm.checkPermission(ReviewPortalContent, self.filearea.gmemberfilepublished))

    def tearDown(self):
        self.logout()
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRoles))
    suite.addTest(makeSuite(TestWorkflows))
    suite.addTest(makeSuite(TestWorkflowPermissions))
    return suite

