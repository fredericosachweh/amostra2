# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table('clients_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('clients', ['Client'])

        # Adding M2M table for field managers on 'Client'
        m2m_table_name = db.shorten_name('clients_client_managers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('client', models.ForeignKey(orm['clients.client'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['client_id', 'user_id'])

        # Adding model 'Contract'
        db.create_table('clients_contract', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Client'])),
            ('number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('document', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('klasses_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('clients', ['Contract'])

        # Adding model 'Teacher'
        db.create_table('clients_teacher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Client'])),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('is_confirmed', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('clients', ['Teacher'])

        # Adding unique constraint on 'Teacher', fields ['client', 'teacher']
        db.create_unique('clients_teacher', ['client_id', 'teacher_id'])

        # Adding model 'Klass'
        db.create_table('clients_klass', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Contract'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('max_students', self.gf('django.db.models.fields.IntegerField')(default=50)),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='teachers_klass_set', null=True, to=orm['auth.User'])),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('students_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('password_list_printed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('clients', ['Klass'])

        # Adding M2M table for field students on 'Klass'
        m2m_table_name = db.shorten_name('clients_klass_students')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('klass', models.ForeignKey(orm['clients.klass'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['klass_id', 'user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Teacher', fields ['client', 'teacher']
        db.delete_unique('clients_teacher', ['client_id', 'teacher_id'])

        # Deleting model 'Client'
        db.delete_table('clients_client')

        # Removing M2M table for field managers on 'Client'
        db.delete_table(db.shorten_name('clients_client_managers'))

        # Deleting model 'Contract'
        db.delete_table('clients_contract')

        # Deleting model 'Teacher'
        db.delete_table('clients_teacher')

        # Deleting model 'Klass'
        db.delete_table('clients_klass')

        # Removing M2M table for field students on 'Klass'
        db.delete_table(db.shorten_name('clients_klass_students'))


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
            'document': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klasses_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'})
        },
        'clients.klass': {
            'Meta': {'object_name': 'Klass'},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Contract']"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
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
        }
    }

    complete_apps = ['clients']