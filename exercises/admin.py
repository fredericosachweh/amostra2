from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import PositiveIntegerField, Count, Max
from django.template.defaultfilters import floatformat
from django.utils.translation import ugettext_lazy as _

import models


class MatterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'matter', 'slug')
    list_filter = ('matter',)
    prepopulated_fields = {'slug': ('name',)}


class QuestionTypeInline(admin.TabularInline):
    model = models.QuestionType
    extra = 0


class AnswerTypeInline(admin.TabularInline):
    model = models.AnswerType
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (QuestionTypeInline, AnswerTypeInline)
    list_display = (
        'matter', 'subject', 'name', 'slug', 'get_exercises_count',
        'get_upper_limit1', 'get_upper_limit2', 'get_sites',
        'eligible_for_demos'
    )
    list_display_links = ('matter', 'subject', 'name')
    list_filter = ('sites', 'matter', 'subject', 'eligible_for_demos')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def queryset(self, request):
        qs = super(CategoryAdmin, self).queryset(request)
        qs = qs.select_related('subject', 'matter') \
               .prefetch_related('sites') \
               .annotate(exercises=Count('exercise'),
                         upper_limit1=Max('exercise__filter1'),
                         upper_limit2=Max('exercise__filter2'))
        return qs

    def get_sites(self, instance):
        return '<br/>'.join([s.name for s in instance.sites.all()])
    get_sites.allow_tags = True
    get_sites.short_description = _('sites')

    def get_exercises_count(self, instance):
        return '<a href="{url}?category__id__exact={cat}">{count}</a>'.format(
            cat=instance.pk,
            url=reverse('admin:exercises_exercise_changelist'),
            count=instance.exercises
        )
    get_exercises_count.allow_tags = True
    get_exercises_count.short_description = _('exercises')

    def get_formatted_limit(self, limit):
        return limit and floatformat(limit, -3) or '--'

    def get_upper_limit1(self, instance):
        return self.get_formatted_limit(instance.upper_limit1)
    get_upper_limit1.short_description = _('upper limit 1')

    def get_upper_limit2(self, instance):
        return self.get_formatted_limit(instance.upper_limit2)
    get_upper_limit2.short_description = _('upper limit 2')


class AnswerInline(admin.TabularInline):
    model = models.Answer
    extra = 0
    # make the position control the inline sorting and make it hidden
    sortable_field_name = 'position'
    formfield_overrides = {
        PositiveIntegerField: {'widget': forms.widgets.HiddenInput},
    }

    def _media(self):
        media = super(AnswerInline, self).media
        return media + forms.Media(
            js=('javascripts/answer_form_by_type.js',),
            css={'all': ('stylesheets/form_by_type.css',)},
        )
    media = property(_media)


class QuestionInline(admin.TabularInline):
    model = models.Question
    extra = 0
    # make the position control the inline sorting and make it hidden
    sortable_field_name = 'position'
    formfield_overrides = {
        PositiveIntegerField: {'widget': forms.widgets.HiddenInput},
    }

    def _media(self):
        media = super(QuestionInline, self).media
        return media + forms.Media(
            js=('javascripts/question_form_by_type.js',),
            css={'all': ('stylesheets/form_by_type.css',)},
        )
    media = property(_media)


class ExerciseAdmin(admin.ModelAdmin):
    inlines = (QuestionInline, AnswerInline)
    list_display = (
        'description', 'category', 'tags', 'subject', 'matter',
        'created_at', 'times_used', 'is_public', 'get_view_link'
    )
    list_filter = ('is_public', 'category', 'subject', 'matter')
    search_fields = ('description', 'tags')
    raw_id_fields = ('category',)

    def queryset(self, request):
        qs = super(ExerciseAdmin, self).queryset(request)
        qs = qs.select_related('matter', 'subject', 'category')
        return qs

    def get_view_link(self, instance):
        return _('<a href="%s">View on site</a>') % instance.get_absolute_url()
    get_view_link.allow_tags = True
    get_view_link.short_description = _('view')

    def get_search_results(self, request, queryset, search_term):
        """
        Filters the queryset by clauses ignored by default django behavior.

        Django ignores repeated keywords from GET. This method uses the ignored
        tags repeat occurrences and adds them with a AND operator.
        """
        qs, use_distinct = super(ExerciseAdmin, self).get_search_results(
                request, queryset, search_term)
        tags = request.GET.getlist('tags__icontains')
        if tags:
            tags.remove(request.GET['tags__icontains'])  # already applied
            for tag in tags:
                qs = qs.filter(tags__icontains=tag)
        return qs, use_distinct


class ChoiceInline(admin.TabularInline):
    model = models.Choice
    extra = 0


class ChanceItemInline(admin.TabularInline):
    model = models.ChanceItem


class ChanceAdmin(admin.ModelAdmin):
    inlines = (ChanceItemInline,)
    list_display = ('exercise',)


class ModuleInline(admin.TabularInline):
    model = models.Module
    sortable_field_name = 'position'
    readonly_fields = ('batteries_count',)
    extra = 0


class ProgramAdmin(admin.ModelAdmin):
    inlines = (ModuleInline,)
    list_display = ('name', 'batteries_count')
    readonly_fields = ('batteries_count',)


class BatteryScheduleInline(admin.TabularInline):
    model = models.BatterySchedule
    extra = 0


class ProgramUsageAdmin(admin.ModelAdmin):
    inlines = (BatteryScheduleInline,)
    list_display = ('program', 'client', 'klass')

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Restrict choices of klasses to the related to current user.

        Get the user from request and filters klasses from clients where the
        user is manager. This way, it is not possible to start a program for a
        client through admin, it is only possible to start a program to himself
        for test purpouses.
        """
        field = super(ProgramUsageAdmin, self).formfield_for_dbfield(
            db_field, **kwargs)
        if db_field.name == 'klass' and 'request' in kwargs:
            user = kwargs['request'].user
            field.queryset = models.Klass.objects.filter(
                contract__client__managers=user)
        return field

    def save_model(self, request, obj, form, change):
        """
        Saves the object, distrib. the batteries and force himself as student.

        Uses default program's modules order for batteries distribution and
        makes the current user student of program usage's klass for test
        purpouses.
        """
        super(ProgramUsageAdmin, self).save_model(request, obj, form, change)
        modules = list(obj.program.module_set.values_list('pk', flat=True))
        if not change:
            obj.distribute_batteries(modules)
            obj.klass.students.add(request.user)


class CategoryUsageInline(admin.TabularInline):
    model = models.CategoryUsage
    extra = 0


class BatteryAdmin(admin.ModelAdmin):
    inlines = (CategoryUsageInline,)


admin.site.register(models.Matter, MatterAdmin)
admin.site.register(models.Subject, SubjectAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Exercise, ExerciseAdmin)
admin.site.register(models.Chance, ChanceAdmin)
admin.site.register(models.Program, ProgramAdmin)
admin.site.register(models.ProgramUsage, ProgramUsageAdmin)
admin.site.register(models.Battery, BatteryAdmin)
