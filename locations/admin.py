from django.contrib import admin

from locations.models import Location, Track


class LocationAdmin(admin.ModelAdmin):
    list_filter = ("track__label",)


class LocationInline(admin.TabularInline):
    model = Location


class TrackAdmin(admin.ModelAdmin):
    fields = ("user", "label", "processed", "ended", )
    inlines = [
        LocationInline,
    ]

admin.site.register(Location, LocationAdmin)
admin.site.register(Track, TrackAdmin)
