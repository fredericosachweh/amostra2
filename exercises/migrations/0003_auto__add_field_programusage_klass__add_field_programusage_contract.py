# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ProgramUsage.klass'
        db.add_column('exercises_programusage', 'klass',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['clients.Klass']),
                      keep_default=False)

        # Adding field 'ProgramUsage.contract'
        db.add_column('exercises_programusage', 'contract',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['clients.Contract']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ProgramUsage.klass'
        db.delete_column('exercises_programusage', 'klass_id')

        # Deleting field 'ProgramUsage.contract'
        db.delete_column('exercises_programusage', 'contract_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'clients.client': {
            'Meta': {'object_name': 'Client'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'clients.contract': {
            'Meta': {'object_name': 'Contract'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Client']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'})
        },
        'clients.klass': {
            'Meta': {'object_name': 'Klass'},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Contract']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_students': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'students_klass_set'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'students_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'teachers_klass_set'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'exercises.answer': {
            'Meta': {'ordering': "('group', 'position')", 'object_name': 'Answer'},
            'choices_map': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'error_limit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '9', 'blank': 'True'}),
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Exercise']"}),
            'group': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '9', 'blank': 'True'})
        },
        'exercises.answertype': {
            'Meta': {'ordering': "('group',)", 'object_name': 'AnswerType'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Category']"}),
            'group': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repeat': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'exercises.battery': {
            'Meta': {'ordering': "('position',)", 'object_name': 'Battery'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['exercises.Category']", 'null': 'True', 'blank': 'True'}),
            'exercises_count': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manual_exercises': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['exercises.Exercise']", 'null': 'True', 'blank': 'True'}),
            'matters_names': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Program']"}),
            'subjects_names': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'exercises.batteryschedule': {
            'Meta': {'ordering': "('date',)", 'object_name': 'BatterySchedule'},
            'attempts': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'battery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Battery']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'program_usage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.ProgramUsage']"})
        },
        'exercises.category': {
            'Meta': {'ordering': "('subject', 'name')", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Matter']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Subject']"})
        },
        'exercises.chance': {
            'Meta': {'object_name': 'Chance'},
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Exercise']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user_battery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.UserBattery']", 'null': 'True', 'blank': 'True'}),
            'user_battery_exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.UserBatteryExercise']", 'null': 'True', 'blank': 'True'})
        },
        'exercises.chanceitem': {
            'Meta': {'object_name': 'ChanceItem'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Answer']"}),
            'chance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Chance']"}),
            'choices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['exercises.Choice']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '9', 'blank': 'True'})
        },
        'exercises.choice': {
            'Meta': {'ordering': "('id',)", 'object_name': 'Choice'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Answer']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'exercises.exercise': {
            'Meta': {'object_name': 'Exercise'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'matter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Matter']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Subject']", 'null': 'True', 'blank': 'True'}),
            'times_used': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'exercises.matter': {
            'Meta': {'object_name': 'Matter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'exercises.program': {
            'Meta': {'object_name': 'Program'},
            'batteries_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'exercises.programusage': {
            'Meta': {'object_name': 'ProgramUsage'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Client']"}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Contract']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Klass']"}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Program']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 31, 0, 0)'})
        },
        'exercises.question': {
            'Meta': {'ordering': "('group', 'position')", 'object_name': 'Question'},
            'boolean_value': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'char_value': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Exercise']"}),
            'group': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_value': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'text_value': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'exercises.questiontype': {
            'Meta': {'ordering': "('group',)", 'object_name': 'QuestionType'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Category']"}),
            'group': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repeat': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'exercises.subject': {
            'Meta': {'object_name': 'Subject'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Matter']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'exercises.userbattery': {
            'Meta': {'ordering': "('battery__position',)", 'object_name': 'UserBattery'},
            'battery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Battery']"}),
            'exercises': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['exercises.Exercise']", 'symmetrical': 'False', 'through': "orm['exercises.UserBatteryExercise']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'exercises.userbatteryexercise': {
            'Meta': {'object_name': 'UserBatteryExercise'},
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Exercise']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user_battery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.UserBattery']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['exercises']
