from django.contrib import admin
from .models import Music, IPAddress, MusicViewsHit

admin.site.register(IPAddress)


class MusicManyInline(admin.StackedInline):
    model = MusicViewsHit
    extra = 0
    classes = ('collapse',)


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'music', 'thumbnail_tag', 'singer', 'album', 'status']
    list_filter = ['published_at', 'status']
    search_fields = ('name', 'music')
    actions = ['make_accept', 'make_pending']
    inlines = [MusicManyInline]

    def make_accept(self, request, queryset):
        changed_numbers = queryset.update(status='A')
        if changed_numbers == 1:
            message = "1 music status change to Accept successfully"
        else:
            message = "%s musics status change to Accept successfully" % changed_numbers
        self.message_user(request, message)
    make_accept.short_description = 'change status to Accept'

    def make_pending(self, request, queryset):
        changed_numbers = queryset.update(status='p')
        if changed_numbers == 1:
            message = "1 music status change to Pending successfully"
        else:
            message = "%s music status change to Pending successfully" % changed_numbers
        self.message_user(request, message)
    make_pending.short_description = 'change status to Pending'
