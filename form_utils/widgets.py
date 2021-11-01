# -*- coding: utf-8 -*-
"""
widgets for django-form-utils

parts of this code taken from http://www.djangosnippets.org/snippets/934/
 - thanks baumer1122

"""
from __future__ import unicode_literals

import posixpath

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from .settings import JQUERY_URL

try:
    from sorl.thumbnail import get_thumbnail

    def thumbnail(image_path, width, height):
        geometry_string = "x".join([str(width), str(height)])
        t = get_thumbnail(image_path, geometry_string)
        return '<img src="%s" alt="%s" />' % (t.url, image_path)


except ImportError:
    try:
        from easy_thumbnails.files import get_thumbnailer

        def thumbnail(image_path, width, height):
            thumbnail_options = dict(size=(width, height), crop=True)
            thumbnail = get_thumbnailer(image_path).get_thumbnail(thumbnail_options)
            return '<img src="%s" alt="%s" />' % (thumbnail.url, image_path)

    except ImportError:

        def thumbnail(image_path, width, height):
            absolute_url = posixpath.join(settings.MEDIA_URL, image_path)
            return '<img src="%s" alt="%s" />' % (absolute_url, image_path)


class ImageWidget(forms.FileInput):
    image_template_name = "widgets/imagewidget.html"
    # Not the best kind of checking, but it will do.
    file_extensions = (".png", ".jpg", ".gif", ".jpeg")

    def __init__(self, attrs=None, template_name=None, width=200, height=200):
        if template_name is not None:
            self.image_template_name = template_name
        self.width = width
        self.height = height
        super().__init__(attrs)

    def get_context(self, name, value, attrs=None):
        context = super().get_context(name, value, attrs)
        if (
            value
            and value.name
            and any(value.name.endswith(ext) for ext in self.file_extensions)
        ):
            context["widget"]["image"] = thumbnail(value.name, self.width, self.height)
            context["widget"]["template_name"] = self.image_template_name
            self.template_name = self.image_template_name
        return context


class ClearableFileInput(forms.MultiWidget):
    default_file_widget_class = forms.FileInput
    template_name = "widgets/clearablefileinput.html"

    def __init__(self, file_widget=None, attrs=None, template_name=None):
        if template_name is not None:
            self.template_name = template_name

        file_widget = file_widget or self.default_file_widget_class()
        super().__init__(widgets=[file_widget, forms.CheckboxInput()], attrs=attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if isinstance(value, list):
            self.value = value[0]
        else:
            self.value = value

        return super().render(name, value, attrs, renderer)

    def decompress(self, value):
        # the clear checkbox is never initially checked
        return [value, None]

    def format_output(self, rendered_widgets):
        if self.value:
            return self.template % {
                "input": rendered_widgets[0],
                "checkbox": rendered_widgets[1],
            }
        return rendered_widgets[0]


root = lambda path: posixpath.join(settings.STATIC_URL, path)


class AutoResizeTextarea(forms.Textarea):
    """
    A Textarea widget that automatically resizes to accomodate its contents.
    """

    class Media:
        js = (
            JQUERY_URL,
            root("form_utils/js/jquery.autogrow.js"),
            root("form_utils/js/autoresize.js"),
        )

    def __init__(self, *args, **kwargs):
        attrs = kwargs.setdefault("attrs", {})
        try:
            attrs["class"] = "%s autoresize" % (attrs["class"],)
        except KeyError:
            attrs["class"] = "autoresize"
        attrs.setdefault("cols", 80)
        attrs.setdefault("rows", 5)
        super(AutoResizeTextarea, self).__init__(*args, **kwargs)


class InlineAutoResizeTextarea(AutoResizeTextarea):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.setdefault("attrs", {})
        try:
            attrs["class"] = "%s inline" % (attrs["class"],)
        except KeyError:
            attrs["class"] = "inline"
        attrs.setdefault("cols", 40)
        attrs.setdefault("rows", 2)
        super(InlineAutoResizeTextarea, self).__init__(*args, **kwargs)
