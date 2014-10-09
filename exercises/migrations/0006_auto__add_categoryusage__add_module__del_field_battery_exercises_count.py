# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CategoryUsage'
        db.create_table('exercises_categoryusage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('battery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Battery'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Category'])),
            ('exercises_count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('exercises', ['CategoryUsage'])

        # Adding model 'Module'
        db.create_table('exercises_module', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('program', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Program'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('batteries_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('exercises', ['Module'])

        # Deleting field 'Battery.exercises_count'
        db.delete_column('exercises_battery', 'exercises_count')

        # Deleting field 'Battery.program'
        db.delete_column('exercises_battery', 'program_id')

        # Adding field 'Battery.module'
        db.add_column('exercises_battery', 'module',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['exercises.Module']),
                      keep_default=False)

        # Removing M2M table for field manual_exercises on 'Battery'
        db.delete_table(db.shorten_name('exercises_battery_manual_exercises'))

        # Removing M2M table for field categories on 'Battery'
        db.delete_table(db.shorten_name('exercises_battery_categories'))


    def backwards(self, orm):
        # Deleting model 'CategoryUsage'
        db.delete_table('exercises_categoryusage')

        # Deleting model 'Module'
        db.delete_table('exercises_module')


        # User chose to not deal with backwards NULL issues for 'Battery.exercises_count'
        raise RuntimeError("Cannot reverse this migration. 'Battery.exercises_count' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Battery.program'
        raise RuntimeError("Cannot reverse this migration. 'Battery.program' and its values cannot be restored.")
        # Deleting field 'Battery.module'
        db.delete_column('exercises_battery', 'module_id')

        # Adding M2M table for field manual_exercises on 'Battery'
        m2m_table_name = db.shorten_name('exercises_battery_manual_exercises')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('battery', models.ForeignKey(orm['exercises.battery'], null=False)),
            ('exercise', models.ForeignKey(orm['exercises.exercise'], null=False))
        ))
        db.create_unique(m2m_table_name, ['battery_id', 'exercise_id'])

        # Adding M2M table for field categories on 'Battery'
        m2m_table_name = db.shorten_name('exercises_battery_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('battery', models.ForeignKey(orm['exercises.battery'], null=False)),
            ('category', models.ForeignKey(orm['exercises.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['battery_id', 'category_id'])


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
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'managed_clients'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'teachers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'involved_to_clients'", 'blank': 'True', 'through': "orm['clients.Teacher']", 'to': "orm['auth.User']"})
        },
        'clients.contract': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Contract'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Client']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klasses_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'})
        },
        'clients.klass': {
            'Meta': {'object_name': 'Klass'},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Contract']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_students': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password_list_printed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'students_klass_set'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'students_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'teachers_klass_set'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'clients.teacher': {
            'Meta': {'unique_together': "(('client', 'teacher'),)", 'object_name': 'Teacher'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Client']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['exercises.Category']", 'null': 'True', 'through': "orm['exercises.CategoryUsage']", 'blank': 'True'}),
            'categories_names': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matters_names': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Module']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
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
        'exercises.categoryusage': {
            'Meta': {'object_name': 'CategoryUsage'},
            'battery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Battery']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Category']"}),
            'exercises_count': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        'exercises.module': {
            'Meta': {'ordering': "('position',)", 'object_name': 'Module'},
            'batteries_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Program']"})
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
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'program_usage'", 'unique': 'True', 'to': "orm['clients.Klass']"}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Program']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 6, 10, 0, 0)'})
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
            'Meta': {'ordering': "('position',)", 'object_name': 'UserBatteryExercise'},
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