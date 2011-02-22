from zope.component import adapts
from zope.interface import implements

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField
from archetypes.referencebrowserwidget import ReferenceBrowserWidget

from Products.Archetypes.public import ReferenceField
from Products.ATContentTypes.interface import IATFile
from Products.CMFCore.utils import getToolByName

from gem.community import communityMessageFactory as _
from gem.community.config import PROJECTNAME

class MyReferenceField(ExtensionField, ReferenceField):
     """ Another reference field """


class FileExtender(object):
    adapts(IATFile)
    implements(ISchemaExtender)


    fields = [
        MyReferenceField(u'old_version',
              relationship='oldVersion',
              allowed_types=['File',],
              multiValued=False,
              widget = ReferenceBrowserWidget(
                  label=_(u'old_version_label', default=u'Old version'),
                  description=_(u'old_version_label', default=u'This file is the archived version'),
                  ),
              ),
             ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        # TODO: use archetypes schema tuning
        portal_quickinstaller = getToolByName(self.context, 'portal_quickinstaller')
        if portal_quickinstaller.isProductInstalled(PROJECTNAME):
            return self.fields
        return []


