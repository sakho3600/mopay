# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Transaction.type'
        db.alter_column('app_transaction', 'type', self.gf('django.db.models.fields.CharField')(max_length=50))


    def backwards(self, orm):
        
        # Changing field 'Transaction.type'
        db.alter_column('app_transaction', 'type', self.gf('django.db.models.fields.CharField')(max_length=15))


    models = {
        'app.admin': {
            'Meta': {'object_name': 'Admin'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password_salt': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'app.agent': {
            'Meta': {'object_name': 'Agent'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_filename': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password_salt': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'sig_filename': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'app.card': {
            'Meta': {'object_name': 'Card'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'serial': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'app.cashoutticket': {
            'Meta': {'object_name': 'CashoutTicket'},
            'id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Transaction']"})
        },
        'app.config': {
            'Meta': {'object_name': 'Config'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'app.incomingmessage': {
            'Meta': {'object_name': 'IncomingMessage'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'app.outgoingmessage': {
            'Meta': {'object_name': 'OutgoingMessage'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('app.db.fields.BlobField', [], {'null': 'True'}),
            'receiver': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        'app.requestcashoutticket': {
            'Meta': {'object_name': 'RequestCashoutTicket'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Agent']"}),
            'cashout_ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.CashoutTicket']"}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'app.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'start'", 'max_length': '15'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'app.user': {
            'Meta': {'object_name': 'User'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'balance': ('django.db.models.fields.FloatField', [], {'default': '5000'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'phone': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pin_salt': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['app']
