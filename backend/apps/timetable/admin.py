from django.contrib import admin
from .models import Subject, Room, Period, TimetableEntry, SubstitutionEntry

admin.site.register(Subject)
admin.site.register(Room)
admin.site.register(Period)


@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("subject", "school_class", "teacher", "day", "period", "room")
    list_filter = ("day", "school_class", "subject")


@admin.register(SubstitutionEntry)
class SubstitutionEntryAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("date", "original_entry", "substitute_teacher", "is_cancelled")
    list_filter = ("date", "is_cancelled")
