# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Config'
        db.create_table('app_config', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('app', ['Config'])

        # Adding model 'User'
        db.create_table('app_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True, null=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('phone', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('pin', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pin_salt', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('balance', self.gf('django.db.models.fields.FloatField')(default=5000)),
        ))
        db.send_create_signal('app', ['User'])

        # Adding model 'Agent'
        db.create_table('app_agent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('password_salt', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('id_filename', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('sig_filename', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
        ))
        db.send_create_signal('app', ['Agent'])

        # Adding model 'Admin'
        db.create_table('app_admin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('password_salt', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('app', ['Admin'])

        # Adding model 'Card'
        db.create_table('app_card', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pin', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('serial', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('used', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('app', ['Card'])

        # Adding model 'Transaction'
        db.create_table('app_transaction', (
            ('id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='start', max_length=15)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('receiver', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('app', ['Transaction'])

        # Adding model 'CashoutTicket'
        db.create_table('app_cashoutticket', (
            ('id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50, primary_key=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('receiver', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('transaction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Transaction'])),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('app', ['CashoutTicket'])

        # Adding model 'RequestCashoutTicket'
        db.create_table('app_requestcashoutticket', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Agent'])),
            ('cashout_ticket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.CashoutTicket'])),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('app', ['RequestCashoutTicket'])

        # Adding model 'IncomingMessage'
        db.create_table('app_incomingmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('app', ['IncomingMessage'])

        # Adding model 'OutgoingMessage'
        db.create_table('app_outgoingmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('receiver', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('meta', self.gf('app.db.fields.BlobField')(null=True)),
        ))
        db.send_create_signal('app', ['OutgoingMessage'])


    def backwards(self, orm):
        
        # Deleting model 'Config'
        db.delete_table('app_config')

        # Deleting model 'User'
        db.delete_table('app_user')

        # Deleting model 'Agent'
        db.delete_table('app_agent')

        # Deleting model 'Admin'
        db.delete_table('app_admin')

        # Deleting model 'Card'
        db.delete_table('app_card')

        # Deleting model 'Transaction'
        db.delete_table('app_transaction')

        # Deleting model 'CashoutTicket'
        db.delete_table('app_cashoutticket')

        # Deleting model 'RequestCashoutTicket'
        db.delete_table('app_requestcashoutticket')

        # Deleting model 'IncomingMessage'
        db.delete_table('app_incomingmessage')

        # Deleting model 'OutgoingMessage'
        db.delete_table('app_outgoingmessage')


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
            'type': ('django.db.models.fields.CharField', [], {'max_length': '15'})
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
