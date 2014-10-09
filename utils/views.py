import datetime
import json
import os

from django import http
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views import generic
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import FormMixin, ProcessFormView
from wkhtmltopdf.views import PDFTemplateResponse


class PdfMixin(TemplateResponseMixin):
    """
    Bypass the default rendering of a template, gets his content and wraps on a
    wkhtmltopdf PDF Response.
    """
    response_class = PDFTemplateResponse
    print_header_title = None

    def render_to_response(self, context, **response_kwargs):
        context['STATIC_ROOT'] = settings.STATIC_ROOT
        if self.print_header_title:
            context['print_header_title'] = self.print_header_title
        response_kwargs['header_template'] = 'print_header.html'
        return super(PdfMixin, self).render_to_response(context, **response_kwargs)


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class JsonView(View):
    """
    A view that can be used to render an python object in a json format.
    """
    def get_json_response(self):
        json_object = self.get_json_object()
        response = http.HttpResponse(mimetype="application/x-javascript")
        json.dump(json_object, response)
        return response

    def get_json_object(self):
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        json_response = self.get_json_response()
        return json_response

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class AjaxMixin(TemplateResponseMixin):
    template_name_ajax_suffix = '_ajax'

    def get_template_names(self):
        """
        For each filename in the template names, suffix it with _ajax. In
        general, the non-ajax template will include the ajax template for
        non-ajax calls.
        """
        original_template_names = super(AjaxMixin, self).get_template_names()
        if not self.request.is_ajax():
            return original_template_names
        else:
            template_names = []
            for filename in original_template_names[::-1]:
                name, ext = os.path.splitext(filename)
                ajax_filename = ''.join([name, self.template_name_ajax_suffix, ext])
                template_names.insert(0, filename)
                template_names.insert(0, ajax_filename)
            return template_names

    def form_invalid(self, form):
        """
        Changes the status code of the response to 422 (UNPROCESSABLE
        ENTITY). This is used to trigger the error method on jquery.
        """
        return self.render_to_response(self.get_context_data(form=form), status=422)


class MonthArchiveWithDefaultView(generic.MonthArchiveView):
    """
    Base month archive that defaults to current month if no month is specified.
    """
    allow_empty = True
    allow_future = True
    date_field = 'date'
    month_format = '%m'

    @cached_property
    def today(self):
        return datetime.datetime.today()

    def get_year(self):
        """ Gets the year from request params or the latest as a fallback. """
        try:
            return super(MonthArchiveWithDefaultView, self).get_year()
        except Http404:
            return self.today.strftime(self.year_format)

    def get_month(self):
        """ Gets the month from request params or the latest as a fallback. """
        try:
            return super(MonthArchiveWithDefaultView, self).get_month()
        except Http404:
            return self.today.strftime(self.month_format)


class MultipleFormsMixin(FormMixin):
    """
    A mixin that provides a way to show and handle several forms in a
    request.
    """
    form_classes = {} # set the form classes as a mapping

    def get_form_classes(self):
        return self.form_classes

    def get_forms_kwargs(self):
        kwargs = self.get_form_kwargs()
        keys = self.get_form_classes().keys()
        return dict([(key, kwargs.copy()) for key in keys])

    def get_forms(self, form_classes):
        kwargs = self.get_forms_kwargs()
        return dict([(key, klass(**kwargs[key])) \
            for key, klass in form_classes.items()])

    def forms_valid(self, forms):
        return super(MultipleFormsMixin, self).form_valid(forms)

    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(forms=forms))


class ProcessMultipleFormsView(ProcessFormView):
    """
    A mixin that processes multiple forms on POST. Every form must be
    valid.
    """
    def get(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        return self.render_to_response(self.get_context_data(forms=forms))

    def validate_forms(self, forms):
        return all([form.is_valid() for form in forms.values()])

    def post(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        if self.validate_forms(forms):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)


class BaseMultipleFormsView(MultipleFormsMixin, ProcessMultipleFormsView):
    """
    A base view for displaying several forms.
    """

class MultipleFormsView(TemplateResponseMixin, BaseMultipleFormsView):
    """
    A view for displaing several forms, and rendering a template response.
    """
