# -*- encoding: utf-8 -*-
from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create combination of straight lines exercises."
    matter = 'matematica'
    subject = 'geometria'
    category = 'retas-paralelas-perpendiculares-secantes'
    description = u'{0}, {1} (comb. retas)'
    bulk_create_answers = False

    TYPES = {
        'parallel': u'Paralelas',
        'perpendicular': u'Secantes/concorrentes e perpendiculares',
        'secant': u'Secantes/concorrentes e não perpendiculares',
    }

    COMBINATIONS = {
        ('a', 'b'): 'parallel',
        ('a', 'b'): 'parallel',
        ('a', 'c'): 'secant',
        ('a', 'd'): 'perpendicular',
        ('a', 'f'): 'perpendicular',
        ('b', 'c'): 'secant',
        ('b', 'd'): 'perpendicular',
        ('b', 'f'): 'perpendicular',
        ('c', 'd'): 'secant',
        ('c', 'f'): 'secant',
        ('d', 'f'): 'parallel',
    }

    def split_terms(self, terms):
        """
        Expects a pair of strings representing segment names. E.g: "a,b".
        """
        term1, term2 = terms.split(',')
        type = self.COMBINATIONS[(term1, term2)]
        return term1, term2, type

    def generate_operations(self):
        """
        Max limit is number of the combinations.
        """
        combinations = self.COMBINATIONS.items()[:self.limit]
        for (term1, term2), type in combinations:
            yield (term1, term2, type)

    def create_exercise(self, term1, term2, correct_type):
        desc = self.description.format(term1, term2)
        exercise, created = self.category.exercise_set.get_or_create(
            description=desc)

        if not created:
            return  # avoid duplicate exercise

        self.questions.append(models.Question(
            exercise=exercise, type='char', position=0,
            group='term1', char_value=term1
        ))

        self.questions.append(models.Question(
            exercise=exercise, type='char', position=1,
            group='term2', char_value=term2
        ))

        choices = [u'+{0}'.format(self.TYPES[correct_type])]
        for type, description in self.TYPES.items():
            if type != correct_type:
                choices.append(u'-{0}'.format(description))

        # Offer only 3 choices, one of them right
        self.answers.append(models.Answer(
            exercise=exercise, type='radio', position=0, tabindex=1,
            group='result', choices_sample=3, choices_map='\n'.join(choices),
        ))

        return exercise
