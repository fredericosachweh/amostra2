# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Category.elegible_for_demos'
        db.add_column(u'exercises_category', 'elegible_for_demos',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Category.elegible_for_demos'
        db.delete_column(u'exercises_category', 'elegible_for_demos')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'clients.client': {
            'Meta': {'object_name': 'Client'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'cnpj': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '19', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'complement': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'managed_clients'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_clients'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'phones': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'quarter': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'suspect'", 'max_length': '20'}),
            'teachers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'involved_to_clients'", 'blank': 'True', 'through': u"orm['clients.Teacher']", 'to': u"orm['auth.User']"})
        },
        u'clients.contract': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Contract'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Client']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'document': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klasses_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'})
        },
        u'clients.klass': {
            'Meta': {'object_name': 'Klass'},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Contract']"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'db_index': 'True'}),
            'max_students': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password_list_printed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'took_klasses'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'students_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'taught_klasses'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'clients.teacher': {
            'Meta': {'unique_together': "(('client', 'teacher'),)", 'object_name': 'Teacher'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'exercises.answer': {
            'Meta': {'ordering': "('group', '-position')", 'object_name': 'Answer'},
            'choices_map': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'choices_sample': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'error_limit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '9', 'blank': 'True'}),
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Exercise']"}),
            'group': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'tabindex': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '9', 'blank': 'True'})
        },
        u'exercises.answertype': {
            'Meta': {'ordering': "('group',)", 'object_name': 'AnswerType'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Category']"}),
            'group': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            'group_short': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_group': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'exercises.battery': {
            'Meta': {'ordering': "('module', 'position')", 'object_name': 'Battery'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['exercises.Category']", 'null': 'True', 'through': u"orm['exercises.CategoryUsage']", 'blank': 'True'}),
            'categories_names': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matters_names': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Module']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'subjects_names': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'exercises.batteryschedule': {
            'Meta': {'ordering': "('date',)", 'object_name': 'BatterySchedule'},
            'attempts': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'battery': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Battery']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'program_usage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.ProgramUsage']"})
        },
        u'exercises.category': {
            'Meta': {'ordering': "('subject', 'name')", 'object_name': 'Category'},
            'elegible_for_demos': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Matter']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Subject']"})
        },
        u'exercises.categoryusage': {
            'Meta': {'ordering': "('battery', 'id')", 'object_name': 'CategoryUsage'},
            'battery': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Battery']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Category']"}),
            'exercises_count': ('django.db.models.fields.IntegerField', [], {}),
            'filter1_lower': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '17', 'decimal_places': '9', 'blank': 'True'}),
            'filter1_upper': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '17', 'decimal_places': '9', 'blank': 'True'}),
            'filter2_lower': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '17', 'decimal_places': '9', 'blank': 'True'}),
            'filter2_upper': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '17', 'decimal_places': '9', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'random_sorting': ('django.db.models.fields.BooleanField', [], {}),
            'tags': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'})
        },
        u'exercises.chance': {
            'Meta': {'unique_together': "(('user_battery_exercise', 'number'),)", 'object_name': 'Chance'},
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Exercise']"}),
            'finished_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user_battery': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.UserBattery']", 'null': 'True', 'blank': 'True'}),
            'user_battery_exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.UserBatteryExercise']", 'null': 'True', 'blank': 'True'})
        },
        u'exercises.chanceitem': {
            'Meta': {'object_name': 'ChanceItem'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Answer']"}),
            'chance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Chance']"}),
            'choices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['exercises.Choice']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '9', 'blank': 'True'})
        },
        u'exercises.choice': {
            'Meta': {'ordering': "('id',)", 'object_name': 'Choice'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Answer']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_correct': ('django.db.models.fields.BooleanField', [], {})
        },
        u'exercises.exercise': {
            'Meta': {'object_name': 'Exercise'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'filter1': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '17', 'decimal_places': '9', 'blank': 'True'}),
            'filter2': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '17', 'decimal_places': '9', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'matter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Matter']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Subject']", 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'times_used': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'exercises.matter': {
            'Meta': {'object_name': 'Matter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'exercises.module': {
            'Meta': {'ordering': "('position',)", 'object_name': 'Module'},
            'batteries_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Program']"})
        },
        u'exercises.program': {
            'Meta': {'object_name': 'Program'},
            'batteries_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Matter']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'exercises.programusage': {
            'Meta': {'object_name': 'ProgramUsage'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Client']"}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Contract']"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'program_usage'", 'unique': 'True', 'to': u"orm['clients.Klass']"}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Program']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 2, 13, 0, 0)'})
        },
        u'exercises.question': {
            'Meta': {'ordering': "('group', '-position')", 'object_name': 'Question'},
            'boolean_value': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'char_value': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Exercise']"}),
            'group': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_value': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'text_value': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'exercises.questiontype': {
            'Meta': {'ordering': "('group',)", 'object_name': 'QuestionType'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Category']"}),
            'group': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            'group_short': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'exercises.subject': {
            'Meta': {'object_name': 'Subject'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Matter']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'exercises.userbattery': {
            'Meta': {'ordering': "('battery__position',)", 'object_name': 'UserBattery'},
            'attempts_spent': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '5'}),
            'battery': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Battery']"}),
            'battery_schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.BatterySchedule']", 'null': 'True', 'blank': 'True'}),
            'correct_answers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'exercises': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['exercises.Exercise']", 'symmetrical': 'False', 'through': u"orm['exercises.UserBatteryExercise']", 'blank': 'True'}),
            'exercises_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time_spent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'exercises.userbatteryexercise': {
            'Meta': {'ordering': "('position',)", 'unique_together': "(('user_battery', 'position'),)", 'object_name': 'UserBatteryExercise'},
            'attempts_spent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Exercise']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_correct': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'time_spent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_battery': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.UserBattery']"})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['exercises']