from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from media_tree import media_types
from media_tree.contrib.media_tree_cms_plugins.helpers import PluginLink

MEDIA_TREE_LIST_DISPLAY = ('browse_controls', 'size_formatted', 'extension', 'resolution_formatted', 'get_descendant_count_display', 'modified', 'modified_by', 'has_metadata_including_descendants', 'caption', 'position')

MEDIA_TREE_LIST_FILTER = ('media_type', 'extension', 'has_metadata')

#MEDIA_TREE_LIST_DISPLAY_LINKS = ('name',)

MEDIA_TREE_SEARCH_FIELDS = ('name', 'title', 'description', 'author', 'copyright', 'override_caption', 'override_alt')

MEDIA_TREE_ORDERING_DEFAULT = ['name']    

MEDIA_TREE_UPLOAD_SUBDIR = 'upload'

MEDIA_TREE_PREVIEW_SUBDIR = 'upload/_preview'

MEDIA_TREE_MEDIA_SUBDIR = 'media_tree'

MEDIA_TREE_ICONS_DIR = 'media_tree/img/icons'

MEDIA_TREE_ADMIN_ACTIONS = None

MEDIA_TREE_THUMBNAIL_SIZES = {
    'default': (100, 100),
    'medium': (250, 250),
    'large': (400, 400),
    'full': None, # None means: use original size
}

MEDIA_TREE_ALLOWED_FILE_TYPES = (
    'aac', 'ace', 'ai', 'aiff', 'avi', 'bmp', 'dir', 'doc', 'docx', 'dmg', 'eps', 'fla', 'flv', 'gif', 'gz', 'hqx', 'htm', 'html', 'ico', 'indd', 'inx', 'jpg', 'jar', 'jpeg', 'md', 'mov', 'mp3', 'mp4', 'mpc', 'mkv', 'mpg', 'mpeg', 'ogg', 'odg', 'odf', 'odp', 'ods', 'odt', 'otf', 'pdf', 'png', 'pps', 'ppsx', 'ps', 'psd', 'rar', 'rm', 'rtf', 'sit', 'swf', 'tar', 'tga', 'tif', 'tiff', 'ttf', 'txt', 'wav', 'wma', 'wmv', 'xls', 'xlsx', 'xml', 'zip'
)

MEDIA_TREE_THUMBNAIL_EXTENSIONS = ('jpg', 'png')

MEDIA_TREE_MEDIA_EXTENDERS = (
    'media_tree.media_extensions.core.images.focal_point.FocalPointExtender',
#    'media_tree.media_extensions.core.images.metadata.ExifIptcExtender',
)

MEDIA_TREE_THUMBNAIL_SIZE_TINY = '50x50'

MEDIA_TREE_FILE_SIZE_LIMIT = 1000000000 # 1 GB

MEDIA_TREE_SWFUPLOAD = True

"""
List of mimetypes not convered by the `mimetypes` Python module (for instance, .flv is not guessed
by `guess_mimetype`.)
"""
MEDIA_TREE_EXT_MIMETYPE_MAP = {
    'flv': 'video/x-flv',
}

MEDIA_TREE_MIMETYPE_CONTENT_TYPE_MAP = {
    'application/octet-stream': media_types.FILE,
    'application/zip': media_types.ARCHIVE,
    'application/x-rar-compressed': media_types.ARCHIVE,
    'application/x-tar': media_types.ARCHIVE,
    'application/x-ace-compressed': media_types.ARCHIVE,
    'application': media_types.DOCUMENT,
    'audio': media_types.AUDIO,
    'image': media_types.IMAGE,
    'text': media_types.TEXT,
    'video': media_types.VIDEO,
}

MEDIA_TREE_CONTENT_TYPE_CHOICES = (
    (media_types.FOLDER, _('folder')),
    (media_types.ARCHIVE, _('archive')),
    (media_types.AUDIO, _('audio')),
    (media_types.DOCUMENT, _('document')),
    (media_types.IMAGE, _('image')),
    (media_types.SUPPORTED_IMAGE, _('web image')),
    (media_types.TEXT, _('text')),
    (media_types.VIDEO, _('video')),
    (media_types.FILE, _('other')),
)

MEDIA_TREE_CONTENT_TYPES = dict(MEDIA_TREE_CONTENT_TYPE_CHOICES)

"""
MEDIA_TREE_FILE_ICONS = {
    'pdf': 'mimetypes/pdf.png',
    media_types.FOLDER: 'folder/folder.png',
    media_types.FILE: 'mimetypes/binary.png',
    media_types.ARCHIVE: 'mimetypes/tar.png',
    media_types.AUDIO: 'mimetypes/sound.png',
    media_types.DOCUMENT: 'mimetypes/document.png',
    media_types.IMAGE: 'mimetypes/image.png',
    media_types.SUPPORTED_IMAGE: 'mimetypes/image.png',
    media_types.TEXT: 'mimetypes/text.png',
    media_types.VIDEO: 'mimetypes/video.png',
}
"""

MEDIA_TREE_FILE_ICONS = {
    'pdf': 'nuvola/22x22/mimetypes/pdf.png',
    'html': 'nuvola/22x22/mimetypes/html.png',
    'swf': 'nuvola/22x22/mimetypes/html.png',
    media_types.FOLDER: 'folder/folder.png',
    media_types.FILE: 'nuvola/22x22/mimetypes/binary.png',
    media_types.ARCHIVE: 'nuvola/22x22/mimetypes/tar.png',
    media_types.AUDIO: 'nuvola/22x22/mimetypes/sound.png',
    media_types.DOCUMENT: 'nuvola/22x22/mimetypes/document.png',
    media_types.IMAGE: 'nuvola/22x22/mimetypes/image.png',
    media_types.SUPPORTED_IMAGE: 'nuvola/22x22/mimetypes/image.png',
    media_types.TEXT: 'nuvola/22x22/mimetypes/txt.png',
    media_types.VIDEO: 'nuvola/22x22/mimetypes/video.png',
}

MEDIA_TREE_LEVEL_INDICATOR = unichr(0x00A0) * 3;

MEDIA_TREE_NAME_UNIQUE_NUMBERED_FORMAT = '%(name)s_%(number)i%(ext)s'

MEDIA_TREE_CMS_PLUGIN_LINK_TYPE_CHOICES = (
    (PluginLink.LINK_PAGE, _('Link to page')), 
    (PluginLink.LINK_URL, _('Link to web address')), 
    (PluginLink.LINK_IMAGE_DETAIL, _('Link to full size image')),
    (PluginLink.LINK_URL_REVERSE, _('Link to URL pattern')),
)

MEDIA_TREE_GLOBAL_THUMBNAIL_OPTIONS = {
    'sharpen': None, # None means enabled 
}

MEDIA_TREE_CMS_PLUGIN_LINK_TYPE_DEFAULT = PluginLink.LINK_IMAGE_DETAIL if getattr(settings, 'CMS_APPLICATIONS_URLS', {}).has_key('media_tree.urls') else None

MEDIA_TREE_SLIDESHOW_TRANSITION_FX_CHOICES = (
    ('blindX','blindX',),
    ('blindY','blindY',),
    ('blindZ','blindZ',),
    ('cover','cover',),
    ('curtainX','curtainX',),
    ('curtainY','curtainY',),
    ('fade','fade',),
    ('fadeZoom','fadeZoom',),
    ('growX','growX',),
    ('growY','growY',),
    ('none','none',),
    ('scrollUp','scrollUp',),
    ('scrollDown','scrollDown',),
    ('scrollLeft','scrollLeft',),
    ('scrollRight','scrollRight',),
    ('scrollHorz','scrollHorz',),
    ('scrollVert','scrollVert',),
    ('shuffle','shuffle',),
    ('slideX','slideX',),
    ('slideY','slideY',),
    ('toss','toss',),
    ('turnUp','turnUp',),
    ('turnDown','turnDown',),
    ('turnLeft','turnLeft',),
    ('turnRight','turnRight',),
    ('uncover','uncover',),
    ('wipe','wipe',),
    ('zoom','zoom',),
)