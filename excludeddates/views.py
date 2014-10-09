import datetime
import calendar

from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.utils.functional import cached_property
from django.views import generic

import models
from clients.models import Client, Teacher
from utils.views import JsonView, MonthArchiveWithDefaultView


class BaseArchiveView(MonthArchiveWithDefaultView):
    def get_excluded_dates(self):
        """
        Returns a list of lists of dates. This group would be flatten and the
        dates being excluded, re-included or re-excluded depends on how many
        times a date is present in the flatten group:

        - if it appears once, it is excluded
        - if it appears twice, it is re-included
        - if it appears three times, it is re-excluded
        """
        raise NotImplementedError

    def get_dated_queryset(self, **lookup):
        """
        Instead on one queryset, returns as many query as defined in the
        get_excluded_dates method.
        """
        queries = self.get_excluded_dates()
        return [qs.filter(**lookup) for qs in queries]

    def get_date_list(self, queryset, date_type):
        """
        Merge the querysets gotten from get_dated_queryset method into a flat
        list and make it a calendar.
        """
        date_field = self.get_date_field()
        dates_group = [list(qs.dates(date_field, date_type)) for qs in queryset]
        dates = [d.day for d in reduce(lambda a, b: a + b, dates_group, [])]

        calendar.setfirstweekday(6)  # starts at sunday
        month = self.get_month()
        year = self.get_year()
        cal = calendar.monthcalendar(int(year), int(month))

        for i, week in enumerate(cal):
            for j, day in enumerate(week):
                state = models.DATE_STATES[dates.count(day)]
                cal[i][j] = {'day': day, 'state': state}
        return cal


class BaseToggleView(JsonView):
    def get(self, request, *args, **kwargs):
        """
        Toggle the date and returns his state as json or redirects to the
        corresponding list view if it is not an ajax request.
        """
        self.date_state = self.toggle_date()
        if request.is_ajax():
            return super(BaseToggleView, self).get(request, *args, **kwargs)
        else:
            return redirect(request.META['HTTP_REFERER'])

    def get_json_object(self):
        return {'state': self.date_state}

    def get_excluded_dates(self):
        """
        With the same idea of the date month archive view, returns a lists of
        dates where the current date could be present. The count of how many
        times the date appears would tell his state.
        """
        raise NotImplementedError

    def create_instance(self, date):
        """
        Given a date, creates a new instance of his date for the context
        (system, client or teacher).
        """
        raise NotImplementedError

    def toggle_date(self):
        """
        Returns the number of times a date is present in different lists of
        dates after this date be toggled.
        """
        dt = datetime.date(
            int(self.request.GET['year']),
            int(self.request.GET['month']),
            int(self.request.GET['day'])
        )

        instances = []
        for qs in self.get_excluded_dates():
            try:
                instance = qs.get(date=dt)
            except qs.model.DoesNotExist:
                instance = None

            if instance is not None:
                instances.append(instance)

        # Toggle the date instance from the last loop (from last query of
        # get_excluded_dates)
        if instance is not None:
            instance.delete()
            instances.pop()
        else:
            instance = self.create_instance(date=dt)
            instances.append(instance)

        # Returns the final state for this date
        return models.DATE_STATES[len(instances)]


class DisambiguationView(generic.ListView):
    """
    Base for disambiguation lists (for clients of the logged in manager or from
    teacher instances of the logged in user).

    Redirects to the archive view if there is only one choice.
    """
    redirect_url = None

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        if qs.count() == 1:
            return redirect(self.redirect_url, pk=qs[0].pk)
        else:
            return super(DisambiguationView, self).get(request, *args, **kwargs)

#
# System Dates, defined by the admin staff
#

class SystemDateMixin(object):
    def get_excluded_dates(self):
        return [
            models.SystemDate.objects.all()
        ]


class SystemArchiveView(SystemDateMixin, BaseArchiveView):
    template_name = 'excludeddates/system_archive.html'

    def get_context_data(self, **kwargs):
        context = super(SystemArchiveView, self).get_context_data(**kwargs)
        context.update({
            'archive_url': reverse('excludeddates:system-archive'),
            'toggle_url': reverse('excludeddates:system-toggle')
        })
        return context


class SystemToggleView(SystemDateMixin, BaseToggleView):
    def create_instance(self, date):
        return models.SystemDate.objects.create(date=date)

#
# Client Dates, defined by a client's manager
#

class ClientDateMixin(SystemDateMixin):
    @cached_property
    def client(self):
        return get_object_or_404(Client, pk=self.kwargs['pk'],
                                         managers=self.request.user)

    def get_excluded_dates(self):
        return super(ClientDateMixin, self).get_excluded_dates() + [
            self.client.clientdate_set.all()
        ]


class ClientArchiveView(ClientDateMixin, BaseArchiveView):
    template_name = 'excludeddates/client_archive.html'

    def get_context_data(self, **kwargs):
        context = super(ClientArchiveView, self).get_context_data(**kwargs)
        context.update({
            'client': self.client,
            'archive_url': reverse('excludeddates:client-archive', kwargs={'pk': self.client.pk}),
            'toggle_url': reverse('excludeddates:client-toggle', kwargs={'pk': self.client.pk})
        })
        return context


class ClientToggleView(ClientDateMixin, BaseToggleView):
    def create_instance(self, date):
        return self.client.clientdate_set.create(date=date)


class ClientDisambiguationView(DisambiguationView):
    template_name = 'excludeddates/client_disambiguation.html'
    redirect_url = 'excludeddates:client-archive'

    def get_queryset(self):
        return Client.objects.filter(managers=self.request.user)

#
# Teacher dates, defined by a user
#

class TeacherDateMixin(ClientDateMixin):
    @cached_property
    def teacher(self):
        return get_object_or_404(Teacher, pk=self.kwargs['pk'],
                                          teacher=self.request.user)

    @cached_property
    def client(self):
        return self.teacher.client
    
    def get_excluded_dates(self):
        return super(TeacherDateMixin, self).get_excluded_dates() + [
            self.teacher.teacherdate_set.all()
        ]


class TeacherArchiveView(TeacherDateMixin, BaseArchiveView):
    template_name = 'excludeddates/teacher_archive.html'

    def get_context_data(self, **kwargs):
        context = super(TeacherArchiveView, self).get_context_data(**kwargs)
        context.update({
            'client': self.client,
            'archive_url': reverse('excludeddates:teacher-archive', kwargs={'pk': self.teacher.pk}),
            'toggle_url': reverse('excludeddates:teacher-toggle', kwargs={'pk': self.teacher.pk})
        })
        return context


class TeacherToggleView(TeacherDateMixin, BaseToggleView):
    def create_instance(self, date):
        return self.teacher.teacherdate_set.create(date=date)


class TeacherDisambiguationView(DisambiguationView):
    template_name = 'excludeddates/teacher_disambiguation.html'
    redirect_url = 'excludeddates:teacher-archive'

    def get_queryset(self):
        return Teacher.objects.filter(teacher=self.request.user)
