import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.views import generic

from clients.models import Client
from demonstrations import forms, models
from exercises.models import Category, Program
from exercises.views.main import BaseChanceCreateView, BaseChanceDetailView
from utils import EmailFromTemplate


class DemonstrationCreateView(generic.CreateView):
    """
    Uses a PersonCreateForm to make a new person, a new client, attach the
    person to the client and a demonstration for him in the current date.
    """
    form_class = forms.PersonForDemonstrationForm
    template_name = 'demonstrations/demonstration_create.html'

    @method_decorator(transaction.commit_on_success)
    def form_valid(self, form):
        client = Client.objects.create(name=form.cleaned_data['client_name'],
                                       status='prospect')
        client.demonstration_set.create()

        person = form.save(commit=False)
        person.client = client
        person.save()

        # creates a task for the client
        client.followup_set.create(
            content=_('Demonstration requested for a just registered client.'),
            due_date=timezone.now() + datetime.timedelta(days=1),
            responsible=User.objects.all().order_by('id')[0],
        )

        return redirect('demonstrations:demo-create-done')


class DemonstrationSendView(generic.FormView):
    form_class = forms.DemonstrationSendForm
    template_name = 'admin/demonstrations/demonstration_send.html'

    def dispatch(self, request, *args, **kwargs):
        demo = models.Demonstration.objects.get(pk=kwargs['pk'])
        if demo.is_expired():
            messages.error(request, _('Cannot send an expired demonstration!'))
            return redirect('admin:clients_client_change', demo.client.pk)
        if not self.emails:
            messages.error(request, _('There are no possible destinataries '
                                      'to send the demonstration!'))
            return redirect('admin:clients_client_change', demo.client.pk)

        return super(DemonstrationSendView, self).dispatch(request, *args, **kwargs)

    @cached_property
    def demonstration(self):
        return get_object_or_404(models.Demonstration, pk=self.kwargs['pk'])

    @cached_property
    def emails(self):
        """
        Returns persons emails and the institutional email to be used as
        choices for the form.
        """
        client = self.demonstration.client
        emails = [(p.email, p.fancy_name) for p in client.person_set.all()]
        if client.email:
            name = _('{0} <{1}> (Institutional)').format(client.name,
                                                         client.email)
            emails.insert(0, (client.email, name))
        return emails

    def get_form_kwargs(self):
        kwargs = super(DemonstrationSendView, self).get_form_kwargs()
        kwargs['emails'] = self.emails
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DemonstrationSendView, self).get_context_data(**kwargs)
        context['title'] = _('Send demonstration')
        context['demonstration'] = self.demonstration
        return context

    def form_valid(self, form):
        to_emails = form.cleaned_data['emails']
        greeting = form.cleaned_data['greeting']

        email = EmailFromTemplate(
            subject=_('Access your Mainiti\'s demonstration'),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to_emails,
            template_name='demonstrations/demonstration_email',
            context={'demonstration': self.demonstration,
                     'greeting': greeting},
        )
        email.send()

        messages.success(self.request, _('Demonstration sent with success!'))

        client_pk = self.demonstration.client.pk
        return redirect('admin:clients_client_change', client_pk)


class LimitedDemoMixin(object):
    def dispatch(self, *args, **kwargs):
        demo = models.Demonstration.objects.get(pk=kwargs['pk'])
        if demo.is_expired():
            return redirect('demonstrations:demo-expired')
        return super(LimitedDemoMixin, self).dispatch(*args, **kwargs)


class DemonstrationStartView(LimitedDemoMixin, generic.UpdateView):
    """
    Offers the time for user read the terms of usage.
    """
    queryset = models.Demonstration.objects.active()
    form_class = forms.DemonstrationStartForm
    template_name = 'demonstrations/demonstration_start.html'

    def get_new_usages(self):
        """
        Chooses 10 random categories to be used for demonstration.
        """
        categories = Category.objects.eligible_for_demos()
        categories = categories.order_by('?')[:10]
        for n, cat in enumerate(categories):
            yield models.CategoryUsage(demonstration=self.object,
                                       category=cat,
                                       position=n)

    def get_success_url(self):
        """
        Clears any previous attempt and start/restart the
        demonstration for the user.
        """
        usages = self.object.categoryusage_set.all()
        pending = usages.exclude(chance__finished_at__isnull=False)

        try:
            first_cat = pending[0]  # continue where stopped
        except IndexError:
            usages.delete()

            # create a new demonstration
            new_usages = self.get_new_usages()
            models.CategoryUsage.objects.bulk_create(new_usages)
            first_cat = self.object.categoryusage_set.all()[0]
        return reverse('demonstrations:chance-create',
                       kwargs={'pk': self.object.pk, 'cat': first_cat.pk})


class CategoryUsageMixin(object):
    @cached_property
    def category_usage(self):
        return get_object_or_404(models.CategoryUsage,
                                 demonstration__pk=self.kwargs['pk'],
                                 pk=self.kwargs['cat'])

    def get_next_usage(self):
        usages = self.category_usage.demonstration.categoryusage_set.all()
        pending = usages.exclude(chance__finished_at__isnull=False)
        forward = pending.filter(position__gt=self.category_usage.position)

        try:
            return forward[0]
        except IndexError:
            try:
                return pending[0]
            except IndexError:
                return None

    def get_next_url(self):
        usage = self.get_next_usage()
        if not usage:
            return None
        else:
            return reverse('demonstrations:chance-create',
                           kwargs={'pk': usage.demonstration.pk,
                                   'cat': usage.pk})

    def get_pager(self):
        usage = self.category_usage
        return {'current': usage.position + 1,
                'count': usage.demonstration.categoryusage_set.count()}


class ChanceCreateView(LimitedDemoMixin, CategoryUsageMixin, BaseChanceCreateView):
    """
    Show a chance form for the demonstration's category usage.
    """
    def create_chance(self, exercise):
        """
        Creates a chance for the specified exercise and category usage.
        """
        chance = exercise.chance_set.create()
        self.category_usage.chance = chance
        self.category_usage.save()
        return chance

    def get_object(self):
        """
        Sort a new exercise of category or reuse the pending one.

        There is no need to bother with finished attempts as they get filtered
        in the Base class dispatch method.
        """
        if self.category_usage.chance:
            chance = self.category_usage.chance
        else:
            exercise = self.category_usage.category.exercise_set.get_random()
            chance = self.create_chance(exercise)
        return chance

    def warn_done(self):
        """
        Creates a follow up task for the client when all the category usages
        from a demonstration are done.
        """
        demo = self.category_usage.demonstration
        pending = demo.categoryusage_set.exclude(
            chance__finished_at__isnull=False)
        if not pending.exists():
            demo.client.followup_set.create(
                content=_('The client just done his demonstration, contact '
                          'him to keep the negotiation.'),
                due_date=timezone.now() + datetime.timedelta(days=1),
                responsible=demo.client.owner,
            )

    def get_success_url(self):
        self.warn_done()
        return reverse('demonstrations:chance-detail',
                       kwargs={'pk': self.category_usage.demonstration.pk,
                               'cat': self.category_usage.pk})


class ChanceDetailView(LimitedDemoMixin, CategoryUsageMixin, BaseChanceDetailView):
    def get_object(self):
        return self.category_usage.chance

    def get_done_url(self):
        return reverse('demonstrations:demo-done',
                       kwargs={'pk': self.category_usage.demonstration.pk})


class DemonstrationDoneView(LimitedDemoMixin, generic.DetailView):
    template_name = 'demonstrations/demonstration_done.html'
    queryset = models.Demonstration.objects.active()


class ProgramListView(generic.ListView):
    template_name = 'demonstrations/program_list.html'
    model = Program

    def get_context_data(self, **kwargs):
        context = super(ProgramListView, self).get_context_data(**kwargs)
        context['demonstration'] = get_object_or_404(models.Demonstration,
                                                     pk=self.kwargs['pk'])
        return context
