import datetime
import calendar

from django.views import generic
from django.utils.decorators import method_decorator

from base import KlassDetailMixin
from utils.views import AjaxMixin, LoginRequiredMixin, MonthArchiveWithDefaultView
from utils.payments import check_payments


class KlassScheduleView(AjaxMixin, KlassDetailMixin, LoginRequiredMixin, MonthArchiveWithDefaultView):
    template_name = 'teachers/clients/klass_schedule.html'

    @method_decorator(check_payments)
    def dispatch(self, request, *args, **kwargs):
        return super(KlassScheduleView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.klass.program_usage.batteryschedule_set.all()

    def get_date_list(self, queryset, **kwargs):
        date_list = super(KlassScheduleView, self).get_date_list(queryset, **kwargs)

        calendar.setfirstweekday(6)  # starts at sunday
        month = int(self.get_month())
        year = int(self.get_year())
        cal = calendar.monthcalendar(year, month)

        for i, week in enumerate(cal):
            for j, day in enumerate(week):
                d = {'day': day, 'is_included': False, 'is_past': False}
                if day:
                    date = datetime.date(year, month, day)
                    if date in date_list:
                        d['is_included'] = True
                        if date < self.today.date():
                            d['is_past'] = True
                cal[i][j] = d
        return cal

    def get_context_data(self, *args, **kwargs):
        context = super(KlassScheduleView, self).get_context_data(*args, **kwargs)
        context['klass'] = self.klass
        return context


class KlassScheduleDetailView(AjaxMixin, KlassDetailMixin, LoginRequiredMixin, generic.DetailView):
    template_name = 'teachers/clients/klass_schedule_detail.html'

    def get_object(self):
        d = datetime.date(year=int(self.kwargs['year']),
                          month=int(self.kwargs['month']),
                          day=int(self.kwargs['day']))
        return self.klass.program_usage.batteryschedule_set.get(date=d)

    def get_context_data(self, **kwargs):
        context = super(KlassScheduleDetailView, self).get_context_data(**kwargs)
        context['klass'] = self.klass
        return context
