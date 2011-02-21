from zope.interface import implements
from zope.component import adapts

from Products.Archetypes.interfaces import IObjectPostValidation
from Products.CMFCore.utils import getToolByName

from Products.ATContentTypes.interface import IATFile
from gem.community import communityMessageFactory as _
from gem.community.config import PROJECTNAME


class FilePostValidation(object):
    """ """
    implements(IObjectPostValidation)
    adapts(IATFile)

    def __init__(self, context):
        self.context = context

    def __call__(self, request):
        """Validate the context object. Return a dict with keys of fieldnames
        and values of error strings.
        """
        portal_quickinstaller = getToolByName(self.context, 'portal_quickinstaller')
        results = dict()
        if not portal_quickinstaller.isProductInstalled(PROJECTNAME):
            return results 

        old_version = request.get('old_version')
        import pdb; pdb.set_trace()
        #results['certificate'] = _(u'certificate_err', default='You must provide a certificate number')

        return results


