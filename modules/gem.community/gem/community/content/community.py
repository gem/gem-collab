"""Definition of the Community content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from gem.community.interfaces import ICommunity
from gem.community.config import PROJECTNAME

CommunitySchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

CommunitySchema['title'].storage = atapi.AnnotationStorage()
CommunitySchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    CommunitySchema,
    folderish=True,
    moveDiscussion=False
)


class Community(folder.ATFolder):
    """Community area"""
    implements(ICommunity)

    meta_type = "Community"
    schema = CommunitySchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Community, PROJECTNAME)
