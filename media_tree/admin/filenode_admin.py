# TODO: tree_change_list.html is not used
# TODO: _ref_node_id -- use foreignkey widget that only displays folders (also for moves)
# TODO: ghost can't be dropped properly if it contains a tall image
# TODO: search results are falsely indented
# TODO: how to present top-level folders in collapsed form initially?
# TODO: restore breadcrumbs to show path

# TODO: Restore upload functionality
# TODO: ForeignKeyRawIdWidget
# TODO: Admin actions


from ..models import FileNode
from .. import settings as app_settings
from .forms import MoveForm, FileForm, FolderForm, UploadForm
from .utils import get_current_request, set_current_request,  \
    get_request_attr, set_request_attr, is_search_request
from ..media_backends import get_media_backend
from ..widgets import AdminThumbWidget

from treebeard.admin import TreeAdmin

from django.contrib import admin, messages
from django.contrib.admin.options import csrf_protect_m
from django.template.loader import render_to_string
from django.utils.translation import ugettext, ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.db import models
from django.http import HttpResponseBadRequest

import os

STATIC_SUBDIR = app_settings.MEDIA_TREE_STATIC_SUBDIR


class FileNodeAdmin(TreeAdmin):

    list_display = app_settings.MEDIA_TREE_LIST_DISPLAY
    list_filter = app_settings.MEDIA_TREE_LIST_FILTER
    search_fields = app_settings.MEDIA_TREE_SEARCH_FIELDS

    formfield_overrides = {
        models.FileField: {'widget': AdminThumbWidget},
        models.ImageField: {'widget': AdminThumbWidget},
    }

    ADD_FOLDER_VIEW_NAME = 'add_folder'

    class Media:
        js = [
            #os.path.join(STATIC_SUBDIR, 'lib/jquery', 'jquery-1.7.1.min.js').replace("\\","/"),
            #os.path.join(STATIC_SUBDIR, 'lib/jquery', 'jquery.ui.js').replace("\\","/"),
            #os.path.join(STATIC_SUBDIR, 'lib/jquery', 'jquery.cookie.js').replace("\\","/"),
            #os.path.join(STATIC_SUBDIR, 'lib/jquery.fineuploader-4.4.0', 'jquery.fineuploader-4.4.0.js').replace("\\","/"),
            #os.path.join(STATIC_SUBDIR, 'js', 'admin_enhancements.js').replace("\\","/"),
            #os.path.join(STATIC_SUBDIR, 'js', 'django_admin_fileuploader.js').replace("\\","/"),
        ]
        css = {
            'all': (
                os.path.join(STATIC_SUBDIR, 'css', 'filenode_admin.css').replace("\\","/"),
            )
        }

    def node_preview(self, node, icons_only=False):
        request = get_current_request()
        template = 'admin/media_tree/filenode/includes/preview.html'
        thumbnail_backend = get_media_backend(handles_media_types=(node.media_type,), supports_thumbnails=True)
        if not thumbnail_backend:
            icons_only = True
            template = 'media_tree/filenode/includes/icon.html'
            # TODO SPLIT preview.html in two: one that doesn't need media backend!

        context = {
            'node': node,
            'preview_file': node.get_icon_file() if icons_only else node.get_preview_file(),
            'class': 'collapsed-folder' if node.is_folder() else '',
        }

        if not icons_only:
            thumb_size_key = get_request_attr(request, 'thumbnail_size') or 'default'
            context['thumbnail_size'] = app_settings.MEDIA_TREE_ADMIN_THUMBNAIL_SIZES[thumb_size_key]
            thumb = thumbnail_backend.get_thumbnail(context['preview_file'], {'size': context['thumbnail_size']})
            context['thumb'] = thumb

        preview = render_to_string(template, context).strip()

        if node.is_folder():
            preview = "%s%s" % (preview, render_to_string(template, {
                'node': node,
                'preview_file': node.get_preview_file(default_name='_folder_expanded'),
                'class': 'expanded-folder hidden'
            }).strip())
        return preview
    node_preview.short_description = ''
    node_preview.allow_tags = True

    def node_preview_and_name(self, node):
        return '%s<span class="name">%s</span>' % (self.node_preview(node).strip(), node.name)
    node_preview_and_name.short_description = _('media object')
    node_preview_and_name.allow_tags = True

    def size_formatted(self, node, with_descendants=True):
        if node.node_type == FileNode.FOLDER:
            if with_descendants:
                descendants = node.get_descendants()
                if descendants.count() > 0:
                    size = descendants.aggregate(models.Sum('size'))['size__sum']
                else:
                    size = None
            else:
                size = None
        else:
            size = node.size
        if not size:
            return ''
        else:
            return '<span class="filesize">%s</span>' % filesizeformat(size)
    size_formatted.short_description = _('size')
    size_formatted.admin_order_field = 'size'
    size_formatted.allow_tags = True

    def metadata_check(self, node):
        return node.has_metadata_including_descendants()
    metadata_check.short_description = _('Metadata')
    metadata_check.allow_tags = True
    metadata_check.boolean = True

    def _get_form_class(self, request, obj):
        if obj:
            node_type = obj.node_type
        else:
            if request.path_info.strip('/').split('/').pop() == self.ADD_FOLDER_VIEW_NAME:
                node_type = FileNode.FOLDER
            else:
                node_type = FileNode.FILE
        if node_type == FileNode.FILE:
            return FileForm
        if node_type == FileNode.FOLDER:
            return FolderForm

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = self._get_form_class(request, obj)
        return super(FileNodeAdmin, self).get_form(request, obj, **kwargs)

    def try_to_move_node(self, as_child, node, pos, request, target):
        # Make sure to validate using the appropriate form. This will validate
        # allowed media types, whether parent is a folder, etc.
        params = {
            '_ref_node_id': target.pk,
            '_position': pos,
            'node_type': node.node_type
        }
        form = MoveForm(params, instance=node)
        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return HttpResponseBadRequest('Malformed POST params')
        return super(FileNodeAdmin, self).try_to_move_node(as_child, node, pos, request, target)

    def get_fieldsets(self, request, obj=None):
        fieldsets = getattr(self._get_form_class(request, obj).Meta, 'fieldsets', None)
        if fieldsets:
            return fieldsets
        return super(FileNodeAdmin, self).get_fieldsets(request, obj)

    def get_urls(self):
        try:
            from django.conf.urls.defaults import patterns, url
        except ImportError:
            # Django 1.6
            from django.conf.urls import patterns, url
        urls = super(FileNodeAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.module_name
        url_patterns = patterns('',
            url(r'^jsi18n/', self.admin_site.admin_view(self.i18n_javascript), name='media_tree_jsi18n'),
            #url(r'^upload/$',
            #    self.admin_site.admin_view(self.upload_file_view),
            #    name='%s_%s_upload' % info),
            url(r'^%s/$' % self.ADD_FOLDER_VIEW_NAME,
                self.admin_site.admin_view(self.add_folder_view),
                name='%s_%s_add_folder' % info),
            #url(r'^!/(?P<path>.*)/$',
            #    self.admin_site.admin_view(self.open_path_view),
            #    name='%s_%s_open_path' % info),
            #url(r'^!/$',
            #    self.admin_site.admin_view(self.open_path_view),
            #    name='%s_%s_open_root' % info),
            #url(r'^(.+)/expand/$',
            #    self.admin_site.admin_view(self.folder_expand_view),
            #    name='%s_%s_folder_expand' % info),
        )
        url_patterns.extend(urls)
        return url_patterns

    def changelist_view(self, request, extra_context=None):
        set_current_request(request)
        return super(FileNodeAdmin, self).changelist_view(request, extra_context)

    @csrf_protect_m
    def add_folder_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['form'] = 'foo'
        return self.add_view(request, form_url, extra_context)

    def i18n_javascript(self, request):
        """
        Displays the i18n JavaScript that the Django admin requires.

        This takes into account the USE_I18N setting. If it's set to False, the
        generated JavaScript will be leaner and faster.
        """
        if settings.USE_I18N:
            from django.views.i18n import javascript_catalog
        else:
            from django.views.i18n import null_javascript_catalog as javascript_catalog
        return javascript_catalog(request, packages=['media_tree'])

admin.site.register(FileNode, FileNodeAdmin)
