# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
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

        # Deleting field 'OutgoingMessage.request_cashout'
        db.delete_column('app_outgoingmessage', 'request_cashout_id')

        # Deleting field 'OutgoingMessage.transaction'
        db.delete_column('app_outgoingmessage', 'transaction_id')

        # Adding field 'Agent.password'
        db.add_column('app_agent', 'password', self.gf('django.db.models.fields.CharField')(default='', max_length=50), keep_default=False)

        # Adding field 'Agent.password_salt'
        db.add_column('app_agent', 'password_salt', self.gf('django.db.models.fields.CharField')(default='', max_length=50), keep_default=False)

        # Changing field 'Agent.id_filename'
        db.alter_column('app_agent', 'id_filename', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

        # Changing field 'Agent.sig_filename'
        db.alter_column('app_agent', 'sig_filename', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

        # Deleting field 'CashoutTicket.confirmed'
        db.delete_column('app_cashoutticket', 'confirmed')

        # Deleting field 'CashoutTicket.agent'
        db.delete_column('app_cashoutticket', 'agent_id')


    def backwards(self, orm):
        
        # Deleting model 'Admin'
        db.delete_table('app_admin')

        # Adding field 'OutgoingMessage.request_cashout'
        db.add_column('app_outgoingmessage', 'request_cashout', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.RequestCashoutTicket'], null=True), keep_default=False)

        # Adding field 'OutgoingMessage.transaction'
        db.add_column('app_outgoingmessage', 'transaction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Transaction'], null=True), keep_default=False)

        # Deleting field 'Agent.password'
        db.delete_column('app_agent', 'password')

        # Deleting field 'Agent.password_salt'
        db.delete_column('app_agent', 'password_salt')

        # Changing field 'Agent.id_filename'
        db.alter_column('app_agent', 'id_filename', self.gf('django.db.models.fields.CharField')(default='', max_length=15))

        # User chose to not deal with backwards NULL issues for 'Agent.sig_filename'
        raise RuntimeError("Cannot reverse this migration. 'Agent.sig_filename' and its values cannot be restored.")

        # Adding field 'CashoutTicket.confirmed'
        db.add_column('app_cashoutticket', 'confirmed', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'CashoutTicket.agent'
        raise RuntimeError("Cannot reverse this migration. 'CashoutTicket.agent' and its values cannot be restored.")


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
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_filename': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password_salt': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'sig_filename': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
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
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cashoutTicketReceiver'", 'to': "orm['app.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cashoutTicketSender'", 'to': "orm['app.User']"}),
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
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.User']"}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'app.outgoingmessage': {
            'Meta': {'object_name': 'OutgoingMessage'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.User']"}),
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
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactionReceiver'", 'to': "orm['app.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactionSender'", 'to': "orm['app.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'start'", 'max_length': '15'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'app.user': {
            'Meta': {'object_name': 'User'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'balance': ('django.db.models.fields.FloatField', [], {'default': '5000'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pin_salt': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['app']
