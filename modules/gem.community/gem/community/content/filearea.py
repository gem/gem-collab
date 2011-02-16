"""Definition of the FileArea content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from gem.community.interfaces import IFileArea
from gem.community.config import PROJECTNAME

FileAreaSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

FileAreaSchema['title'].storage = atapi.AnnotationStorage()
FileAreaSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    FileAreaSchema,
    folderish=True,
    moveDiscussion=False
)


class FileArea(folder.ATFolder):
    """File Area"""
    implements(IFileArea)

    meta_type = "FileArea"
    schema = FileAreaSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(FileArea, PROJECTNAME)
