# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Matter'
        db.create_table('exercises_matter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('exercises', ['Matter'])

        # Adding model 'Subject'
        db.create_table('exercises_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('matter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Matter'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('exercises', ['Subject'])

        # Adding model 'Category'
        db.create_table('exercises_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Subject'])),
            ('matter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Matter'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('exercises', ['Category'])

        # Adding M2M table for field sites on 'Category'
        db.create_table('exercises_category_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm['exercises.category'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('exercises_category_sites', ['category_id', 'site_id'])

        # Adding model 'QuestionType'
        db.create_table('exercises_questiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Category'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('group', self.gf('django.db.models.fields.SlugField')(max_length=10)),
            ('repeat', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('exercises', ['QuestionType'])

        # Adding model 'AnswerType'
        db.create_table('exercises_answertype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Category'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('group', self.gf('django.db.models.fields.SlugField')(max_length=10)),
            ('repeat', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('exercises', ['AnswerType'])

        # Adding model 'Exercise'
        db.create_table('exercises_exercise', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Category'])),
            ('matter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Matter'], null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Subject'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('times_used', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('exercises', ['Exercise'])

        # Adding model 'Question'
        db.create_table('exercises_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exercise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Exercise'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('group', self.gf('django.db.models.fields.SlugField')(max_length=10)),
            ('char_value', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('boolean_value', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('text_value', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image_value', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('exercises', ['Question'])

        # Adding model 'Answer'
        db.create_table('exercises_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exercise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Exercise'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('group', self.gf('django.db.models.fields.SlugField')(max_length=10)),
            ('value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=9, blank=True)),
            ('error_limit', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=9, blank=True)),
            ('choices_map', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('exercises', ['Answer'])

        # Adding model 'Choice'
        db.create_table('exercises_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Answer'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('is_correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('exercises', ['Choice'])

        # Adding model 'Program'
        db.create_table('exercises_program', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('batteries_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('exercises', ['Program'])

        # Adding model 'Battery'
        db.create_table('exercises_battery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('program', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Program'])),
            ('exercises_count', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('matters_names', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('subjects_names', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('exercises', ['Battery'])

        # Adding M2M table for field categories on 'Battery'
        db.create_table('exercises_battery_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('battery', models.ForeignKey(orm['exercises.battery'], null=False)),
            ('category', models.ForeignKey(orm['exercises.category'], null=False))
        ))
        db.create_unique('exercises_battery_categories', ['battery_id', 'category_id'])

        # Adding M2M table for field manual_exercises on 'Battery'
        db.create_table('exercises_battery_manual_exercises', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('battery', models.ForeignKey(orm['exercises.battery'], null=False)),
            ('exercise', models.ForeignKey(orm['exercises.exercise'], null=False))
        ))
        db.create_unique('exercises_battery_manual_exercises', ['battery_id', 'exercise_id'])

        # Adding model 'ProgramUsage'
        db.create_table('exercises_programusage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Client'])),
            ('program', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Program'])),
            ('start_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 25, 0, 0))),
        ))
        db.send_create_signal('exercises', ['ProgramUsage'])

        # Adding model 'BatterySchedule'
        db.create_table('exercises_batteryschedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('program_usage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.ProgramUsage'])),
            ('battery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Battery'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('attempts', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('exercises', ['BatterySchedule'])

        # Adding model 'UserBattery'
        db.create_table('exercises_userbattery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('battery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Battery'])),
        ))
        db.send_create_signal('exercises', ['UserBattery'])

        # Adding model 'UserBatteryExercise'
        db.create_table('exercises_userbatteryexercise', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_battery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.UserBattery'])),
            ('exercise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Exercise'])),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('exercises', ['UserBatteryExercise'])

        # Adding model 'Chance'
        db.create_table('exercises_chance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_battery_exercise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.UserBatteryExercise'])),
            ('number', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('exercise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Exercise'])),
            ('user_battery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.UserBattery'])),
        ))
        db.send_create_signal('exercises', ['Chance'])

        # Adding model 'ChanceItem'
        db.create_table('exercises_chanceitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Chance'])),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Answer'])),
            ('value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=9, blank=True)),
        ))
        db.send_create_signal('exercises', ['ChanceItem'])

        # Adding M2M table for field choices on 'ChanceItem'
        db.create_table('exercises_chanceitem_choices', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('chanceitem', models.ForeignKey(orm['exercises.chanceitem'], null=False)),
            ('choice', models.ForeignKey(orm['exercises.choice'], null=False))
        ))
        db.create_unique('exercises_chanceitem_choices', ['chanceitem_id', 'choice_id'])


    def backwards(self, orm):
        # Deleting model 'Matter'
        db.delete_table('exercises_matter')

        # Deleting model 'Subject'
        db.delete_table('exercises_subject')

        # Deleting model 'Category'
        db.delete_table('exercises_category')

        # Removing M2M table for field sites on 'Category'
        db.delete_table('exercises_category_sites')

        # Deleting model 'QuestionType'
        db.delete_table('exercises_questiontype')

        # Deleting model 'AnswerType'
        db.delete_table('exercises_answertype')

        # Deleting model 'Exercise'
        db.delete_table('exercises_exercise')

        # Deleting model 'Question'
        db.delete_table('exercises_question')

        # Deleting model 'Answer'
        db.delete_table('exercises_answer')

        # Deleting model 'Choice'
        db.delete_table('exercises_choice')

        # Deleting model 'Program'
        db.delete_table('exercises_program')

        # Deleting model 'Battery'
        db.delete_table('exercises_battery')

        # Removing M2M table for field categories on 'Battery'
        db.delete_table('exercises_battery_categories')

        # Removing M2M table for field manual_exercises on 'Battery'
        db.delete_table('exercises_battery_manual_exercises')

        # Deleting model 'ProgramUsage'
        db.delete_table('exercises_programusage')

        # Deleting model 'BatterySchedule'
        db.delete_table('exercises_batteryschedule')

        # Deleting model 'UserBattery'
        db.delete_table('exercises_userbattery')

        # Deleting model 'UserBatteryExercise'
        db.delete_table('exercises_userbatteryexercise')

        # Deleting model 'Chance'
        db.delete_table('exercises_chance')

        # Deleting model 'ChanceItem'
        db.delete_table('exercises_chanceitem')

        # Removing M2M table for field choices on 'ChanceItem'
        db.delete_table('exercises_chanceitem_choices')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'})
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
            'user_battery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.UserBattery']"}),
            'user_battery_exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.UserBatteryExercise']"})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Program']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 25, 0, 0)'})
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