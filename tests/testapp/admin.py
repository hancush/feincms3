from django.contrib import admin
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from content_editor.admin import ContentEditor
from feincms3.plugins import external, html, image, richtext, snippet
from feincms3.admin import AncestorFilter, TreeAdmin

from . import models


@admin.register(models.Page)
class PageAdmin(ContentEditor, TreeAdmin):
    list_display = [
        "indented_title",
        "move_column",
        "is_active",
        "menu",
        "language_code",
        "template_key",
        "application",
    ]
    list_filter = ["is_active", "menu", AncestorFilter]
    list_editable = ["is_active"]
    prepopulated_fields = {"slug": ("title",)}
    radio_fields = {
        "menu": admin.HORIZONTAL,
        "language_code": admin.HORIZONTAL,
        "template_key": admin.HORIZONTAL,
        "application": admin.HORIZONTAL,
    }
    raw_id_fields = ["parent"]

    fieldsets = [
        (None, {"fields": ("is_active", "title", "parent")}),
        (
            capfirst(_("path")),
            {"fields": ("slug", "static_path", "path"), "classes": ("tabbed",)},
        ),
        (
            capfirst(_("settings")),
            {
                "fields": (
                    "menu",
                    "language_code",
                    "template_key",
                    "application",
                    "optional",
                ),
                "classes": ("tabbed",),
            },
        ),
    ]

    inlines = [
        richtext.RichTextInline.create(model=models.RichText),
        image.ImageInline.create(model=models.Image),
        snippet.SnippetInline.create(model=models.Snippet),
        external.ExternalInline.create(model=models.External),
        html.HTMLInline.create(model=models.HTML),
    ]

    class Media:
        css = {
            "all": (
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css",  # noqa
            )
        }
        js = ("app/plugin_buttons.js",)
