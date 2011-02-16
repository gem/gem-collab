"""Definition of the WikiArea content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from gem.community.interfaces import IWikiArea
from gem.community.config import PROJECTNAME

WikiAreaSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

WikiAreaSchema['title'].storage = atapi.AnnotationStorage()
WikiAreaSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    WikiAreaSchema,
    folderish=True,
    moveDiscussion=False
)


class WikiArea(folder.ATFolder):
    """Wiki Area"""
    implements(IWikiArea)

    meta_type = "WikiArea"
    schema = WikiAreaSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(WikiArea, PROJECTNAME)
