# ##### BEGIN CC0 LICENSE BLOCK #####
#
# CC0 is a public domain dedication from Creative Commons. A work released under CC0 is 
# dedicated to the public domain to the fullest extent permitted by law. If that is not 
# possible for any reason, CC0 also provides a simple permissive license as a fallback. 
# Both public domain works and the simple license provided by CC0 are compatible with the GNU GPL.
#
#  You should have received a copy of the Creative Commons Zero Licence
#
# ##### END CC0 LICENSE BLOCK #####

# by Anime Nyan

from . import Flexify

bl_info = {
    "name": "Flexify - Transfer Shape Keys",
    "author": "Anime Nyan",
    "version": (1, 0, 1),
    "blender": (3, 3, 0),
    "location": "3D View > Properties > Shapekeys",
    "description": "Addon for transfering shape keys",
    "warning": "",
    "wiki_url": "https://github.com/AnimNyan/Flexify/",
    "category": "Rigging",
    "tracker_url": "https://github.com/AnimNyan/Flexify/issues"
}

def register():
    Flexify.register()

def unregister():
    Flexify.unregister()
