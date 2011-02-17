from zope.component import adapts
from zope.interface import implements

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField

from Products.Archetypes.public import ReferenceField
from Products.Archetypes.public import ReferenceWidget
from Products.ATContentTypes.interface import IATFile

from gem.community import communityMessageFactory as _

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
              widget = ReferenceWidget(
                  label=_(u'old_version_label', default=u'Old version'),
                  description=_(u'old_version_label', default=u'This file is the archived version'),
                  ),
              ),
             ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


