# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'User'
        db.create_table('app_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('is_agent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('app', ['User'])

        # Adding model 'Card'
        db.create_table('app_card', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pin', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('serial', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('used', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('app', ['Card'])

        # Adding model 'Transaction'
        db.create_table('app_transaction', (
            ('id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Card'])),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactionSender', to=orm['app.User'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactionReceiver', to=orm['app.User'])),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('app', ['Transaction'])

        # Adding model 'Cashout'
        db.create_table('app_cashout', (
            ('id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, primary_key=True)),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cashoutAgent', to=orm['app.User'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cashoutReceiver', to=orm['app.User'])),
            ('transaction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Transaction'])),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('app', ['Cashout'])

        # Adding model 'IncomingMessage'
        db.create_table('app_incomingmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.User'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('app', ['IncomingMessage'])

        # Adding model 'OutgoingMessage'
        db.create_table('app_outgoingmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.User'])),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('transaction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Transaction'], null=True)),
            ('cashout', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Cashout'], null=True)),
        ))
        db.send_create_signal('app', ['OutgoingMessage'])


    def backwards(self, orm):
        
        # Deleting model 'User'
        db.delete_table('app_user')

        # Deleting model 'Card'
        db.delete_table('app_card')

        # Deleting model 'Transaction'
        db.delete_table('app_transaction')

        # Deleting model 'Cashout'
        db.delete_table('app_cashout')

        # Deleting model 'IncomingMessage'
        db.delete_table('app_incomingmessage')

        # Deleting model 'OutgoingMessage'
        db.delete_table('app_outgoingmessage')


    models = {
        'app.card': {
            'Meta': {'object_name': 'Card'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'serial': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
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
