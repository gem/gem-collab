from zope.component import getMultiAdapter
from zope.interface import implements
from zope.viewlet.interfaces import IViewlet

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

class FileVersions(BrowserView):
    """ fileversions viewlet
    """
    implements(IViewlet)

    def __init__(self, context, request, view, manager=None):
        super(FileVersions, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager

    @property
    def portal_catalog(self):
        return getMultiAdapter((self.context,self.request),name=u"plone_tools").catalog()

    @property
    def reference_catalog(self):
        return getToolByName(self.context, 'reference_catalog')

    def getOldVersion(self):
        obj = self.context.getField('old_version').get(self.context)
        if obj:
            return dict(title=obj.Title(), url=obj.absolute_url())
        return None

    def getNewVersion(self):
        backreferenced_refs = self.reference_catalog.getBackReferences(self.context, 'oldVersion')
        backreferenced_UID = [ref.sourceUID for ref in backreferenced_refs]

        #uid to brains
        brains = self.portal_catalog.searchResults(UID=backreferenced_UID)
        if brains:
            return dict(title=brains[0].Title, url=brains[0].getURL())
        else:
            return None

