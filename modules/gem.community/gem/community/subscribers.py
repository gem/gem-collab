from Products.CMFCore.utils import getToolByName

from gem.community.interfaces import ICommunity
from gem.community.config import WIKI_AREA_ID 
from gem.community.config import FILE_AREA_ID 


def initialize_community(obj, event):
    """ """
    
    portal_types = getToolByName(obj, 'portal_types')
    obj_ids = obj.objectIds()
    if WIKI_AREA_ID not in obj_ids:
        portal_types.constructContent('WikiArea', obj, WIKI_AREA_ID)
        wiki = getattr(obj, WIKI_AREA_ID)
        wiki.setTitle('Wiki')
        wiki.reindexObject()
    if FILE_AREA_ID not in obj_ids:
        portal_types.constructContent('FileArea', obj, FILE_AREA_ID)
        files = getattr(obj, FILE_AREA_ID)
        files.setTitle('Files')
        files.reindexObject()

    mtool = getToolByName(obj, 'portal_membership')
    member = mtool.getAuthenticatedMember()
    if member:
        obj.manage_addLocalRoles(member.getId(), [ 'Contributor', 'Editor']) 
        obj.reindexObjectSecurity()
 
