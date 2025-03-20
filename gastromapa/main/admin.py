from django.contrib import admin
from .models import Category, Business, Product, Review, Media
from django.utils.html import format_html


class BusinessInline(admin.TabularInline):
    model = Business
    extra = 0
    fields = ['name', 'address', 'description', 'owner']
    readonly_fields = ['name', 'address', 'description', 'owner']


class MediaInline(admin.TabularInline):
    model = Media
    extra = 1
    fields = ['media_type', 'file', 'description']
    readonly_fields = ['media_type', 'file']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [BusinessInline]


class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'category', 'owner', 'image_thumb', 'video']
    search_fields = ['name', 'address', 'category__name']
    list_filter = ['category']
    readonly_fields = ['image_thumb', ]
    exclude = ['products']
    inlines = [MediaInline]

    def image_thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "-"

    image_thumb.short_description = 'Thumbnail'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Media)
