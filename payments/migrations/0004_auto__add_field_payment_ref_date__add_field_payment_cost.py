# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Payment.ref_date'
        db.add_column(u'payments_payment', 'ref_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 3, 27, 0, 0)),
                      keep_default=False)

        # Adding field 'Payment.cost'
        db.add_column(u'payments_payment', 'cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Payment.ref_date'
        db.delete_column(u'payments_payment', 'ref_date')

        # Deleting field 'Payment.cost'
        db.delete_column(u'payments_payment', 'cost')


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
            'has_agreed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'payment_day': ('django.db.models.fields.IntegerField', [], {'default': '15'}),
            'pending_payment': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'clients.klass': {
            'Meta': {'object_name': 'Klass'},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Contract']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'default': "'70'", 'max_digits': '10', 'decimal_places': '2'}),
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
        u'payments.klasspayment': {
            'Meta': {'object_name': 'KlassPayment'},
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'current_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Klass']"}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payments.Payment']"}),
            'update_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'})
        },
        u'payments.open': {
            'Meta': {'object_name': 'Open'},
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payments.Payment']"})
        },
        u'payments.payment': {
            'Meta': {'object_name': 'Payment'},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Contract']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klasses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['clients.Klass']", 'through': u"orm['payments.KlassPayment']", 'symmetrical': 'False'}),
            'payment_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'ref_date': ('django.db.models.fields.DateField', [], {}),
            'was_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'payments.visit': {
            'Meta': {'object_name': 'Visit'},
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payments.Payment']"})
        }
    }

    complete_apps = ['payments']