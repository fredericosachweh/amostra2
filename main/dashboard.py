"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'source.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.ModelList(
            _('Users'),
            collapsible=True,
            column=1,
            models=[
                'clients.models.*',
                'django.contrib.auth.models.User',
            ]
        ))

        self.children.append(modules.ModelList(
            _('Exercises'),
            collapsible=True,
            column=1,
            models=[
                'exercises.models.Matter',
                'exercises.models.Subject',
                'exercises.models.Category',
                'exercises.models.Exercise',
            ]
        ))

        self.children.append(modules.ModelList(
            _('Exercise Programs'),
            collapsible=True,
            column=1,
            models=[
                'exercises.models.Program',
                'exercises.models.ProgramUsage',
            ]
        ))

        self.children.append(modules.ModelList(
            _('Excluded dates'),
            collapsible=True,
            column=1,
            models=[
                'excludeddates.models.SystemDate',
            ]
        ))

        self.children.append(modules.AppList(
            _('Advanced'),
            collapsible=True,
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=['django.contrib.*', '*'],
        ))

        self.children.append(modules.LinkList(
            _('Payment'),
            column=2,
            children=[
                {'title': _('Payments'), 'url': reverse('admin:payments_payment_changelist')},
            ]
        ))

        self.children.append(modules.LinkList(
            _('Follow Up'),
            column=2,
            children=[
                {'title': _('Tasks'), 'url': reverse('admin:followup_task_changelist')},
            ]
        ))

        self.children.append(modules.LinkList(
            _('Complementar actions'),
            column=3,
            children=[
                {'title': _('Usage documentation'), 'url': '/docs/'},
                {'title': _('Demonstrations'), 'url': reverse('demonstrations:demo-create')},
                {'title': _('Flatpages'), 'url': reverse('admin:flatpages_flatpage_changelist')},
            ]
        ))
