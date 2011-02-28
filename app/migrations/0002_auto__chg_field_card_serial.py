# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Card.serial'
        db.alter_column('app_card', 'serial', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50))


    def backwards(self, orm):
        
        # Changing field 'Card.serial'
        db.alter_column('app_card', 'serial', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True))


    models = {
        'app.card': {
            'Meta': {'object_name': 'Card'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'serial': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'app.cashout': {
            'Meta': {'object_name': 'Cashout'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cashoutAgent'", 'to': "orm['app.User']"}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cashoutReceiver'", 'to': "orm['app.User']"}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Transaction']"})
        },
        'app.incomingmessage': {
            'Meta': {'object_name': 'IncomingMessage'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.User']"}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'app.outgoingmessage': {
            'Meta': {'object_name': 'OutgoingMessage'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'cashout': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Cashout']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.User']"}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Transaction']", 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        'app.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Card']"}),
            'id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactionReceiver'", 'to': "orm['app.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactionSender'", 'to': "orm['app.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'app.user': {
            'Meta': {'object_name': 'User'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_agent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'})
        }
    }

    complete_apps = ['app']
