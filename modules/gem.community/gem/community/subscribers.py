from gem.community.interfaces import ICommunity
from gem.community.config import WIKI_AREA_ID 
from gem.community.config import FILE_AREA_ID 


def initialize_community(obj, event):
    """ """
    
    if ICommunity.providedBy(obj):
        obj_ids = obj.objectIds()
        if WIKI_AREA_ID not in obj_ids:
            obj.invokeFactory(type_name='WikiArea', id=WIKI_AREA_ID)
            wiki = getattr(obj, WIKI_AREA_ID)
            wiki.setTitle('Wiki')
            wiki.reindexObject()
        if FILE_AREA_ID not in obj_ids:
            obj.invokeFactory(type_name='FileArea', id=FILE_AREA_ID)
            files = getattr(obj, FILE_AREA_ID)
            files.setTitle('Files')
            files.reindexObject()
 
