from django import forms
from django.utils.functional import cached_property

from utils.models import MultiDict
import models


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()


class ChanceItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChanceItemForm, self).__init__(*args, **kwargs)

        answer = kwargs['initial']['answer']
        attrs = {'tabindex': answer.tabindex}

        if answer.type.startswith('digit'):
            attrs['maxlength'] = 1

        self.fields['answer'].widget = forms.HiddenInput()
        if answer.type == 'boolean':
            self.fields['value'].widget = forms.HiddenInput(attrs=attrs)
        else:
            self.fields['value'].localize = True
            self.fields['value'].widget = forms.TextInput(attrs=attrs)

    def has_changed(self):
        """
        Tells the formsets that this form always changed, otherwise, the
        cleaned_data won't be build and the form would try to save null values.
        """
        return True


class BaseChanceItemFormSet(forms.models.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.exercise = kwargs.pop('exercise')
        super(BaseChanceItemFormSet, self).__init__(*args, **kwargs)

    @cached_property
    def forms(self):
        """
        Instatiates one form for each answer.
        """
        forms = []
        for i, answer in enumerate(self.exercise.answer_set.all()):
            initial = {'answer': answer}
            forms.append(self._construct_form(i, initial=initial))
        return forms

    def initial_form_count(self):
        """
        The formset will always be used to create a chance, never to
        update him, this way, the initial forms are always zero.
        """
        return 0

    def total_form_count(self):
        return len(self.forms)

    def answers(self):
        """ Group the forms by the answer's group. """
        return MultiDict(self.forms, group_callback=lambda f: f.initial['answer'].group)


ChanceItemFormSet = forms.models.modelformset_factory(models.ChanceItem, form=ChanceItemForm, formset=BaseChanceItemFormSet,
    fields=('answer', 'value', 'choices'), extra=0)
