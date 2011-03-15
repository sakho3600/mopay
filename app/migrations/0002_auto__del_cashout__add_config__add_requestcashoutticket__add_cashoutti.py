# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Cashout'
        db.delete_table('app_cashout')

        # Adding model 'Config'
        db.create_table('app_config', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('app', ['Config'])

        # Adding model 'RequestCashoutTicket'
        db.create_table('app_requestcashoutticket', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Agent'])),
            ('cashout_ticket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.CashoutTicket'])),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('app', ['RequestCashoutTicket'])

        # Adding model 'CashoutTicket'
        db.create_table('app_cashoutticket', (
            ('id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50, primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cashoutTicketSender', to=orm['app.User'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cashoutTicketReceiver', to=orm['app.User'])),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Agent'])),
            ('transaction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Transaction'])),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('app', ['CashoutTicket'])

        # Adding model 'Agent'
        db.create_table('app_agent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('id_filename', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('sig_filename', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('app', ['Agent'])

        # Changing field 'IncomingMessage.timestamp'
        db.alter_column('app_incomingmessage', 'timestamp', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Deleting field 'OutgoingMessage.cashout'
        db.delete_column('app_outgoingmessage', 'cashout_id')

        # Adding field 'OutgoingMessage.request_cashout'
        db.add_column('app_outgoingmessage', 'request_cashout', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.RequestCashoutTicket'], null=True), keep_default=False)

        # Changing field 'OutgoingMessage.timestamp'
        db.alter_column('app_outgoingmessage', 'timestamp', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Deleting field 'Transaction.card'
        db.delete_column('app_transaction', 'card_id')

        # Adding field 'Transaction.amount'
        db.add_column('app_transaction', 'amount', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)

        # Adding field 'Transaction.type'
        db.add_column('app_transaction', 'type', self.gf('django.db.models.fields.CharField')(default='', max_length=15), keep_default=False)

        # Changing field 'Transaction.timestamp'
        db.alter_column('app_transaction', 'timestamp', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Deleting field 'User.is_agent'
        db.delete_column('app_user', 'is_agent')

        # Adding field 'User.username'
        db.add_column('app_user', 'username', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True, null=True), keep_default=False)

        # Adding field 'User.pin'
        db.add_column('app_user', 'pin', self.gf('django.db.models.fields.CharField')(default='', max_length=50), keep_default=False)

        # Adding field 'User.pin_salt'
        db.add_column('app_user', 'pin_salt', self.gf('django.db.models.fields.CharField')(default='', max_length=10), keep_default=False)

        # Adding field 'User.balance'
        db.add_column('app_user', 'balance', self.gf('django.db.models.fields.FloatField')(default=5000), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'Cashout'
        db.create_table('app_cashout', (
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('transaction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Transaction'])),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cashoutAgent', to=orm['app.User'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cashoutReceiver', to=orm['app.User'])),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, primary_key=True)),
        ))
        db.send_create_signal('app', ['Cashout'])

        # Deleting model 'Config'
        db.delete_table('app_config')

        # Deleting model 'RequestCashoutTicket'
        db.delete_table('app_requestcashoutticket')

        # Deleting model 'CashoutTicket'
        db.delete_table('app_cashoutticket')

        # Deleting model 'Agent'
        db.delete_table('app_agent')

        # Changing field 'IncomingMessage.timestamp'
        db.alter_column('app_incomingmessage', 'timestamp', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Adding field 'OutgoingMessage.cashout'
        db.add_column('app_outgoingmessage', 'cashout', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Cashout'], null=True), keep_default=False)

        # Deleting field 'OutgoingMessage.request_cashout'
        db.delete_column('app_outgoingmessage', 'request_cashout_id')

        # Changing field 'OutgoingMessage.timestamp'
        db.alter_column('app_outgoingmessage', 'timestamp', self.gf('django.db.models.fields.CharField')(max_length=20))

        # User chose to not deal with backwards NULL issues for 'Transaction.card'
        raise RuntimeError("Cannot reverse this migration. 'Transaction.card' and its values cannot be restored.")

        # Deleting field 'Transaction.amount'
        db.delete_column('app_transaction', 'amount')

        # Deleting field 'Transaction.type'
        db.delete_column('app_transaction', 'type')

        # Changing field 'Transaction.timestamp'
        db.alter_column('app_transaction', 'timestamp', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Adding field 'User.is_agent'
        db.add_column('app_user', 'is_agent', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'User.username'
        db.delete_column('app_user', 'username')

        # Deleting field 'User.pin'
        db.delete_column('app_user', 'pin')

        # Deleting field 'User.pin_salt'
        db.delete_column('app_user', 'pin_salt')

        # Deleting field 'User.balance'
        db.delete_column('app_user', 'balance')


    models = {
        'app.agent': {
            'Meta': {'object_name': 'Agent'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_filename': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'sig_filename': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
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
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Agent']"}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'request_cashout': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.RequestCashoutTicket']", 'null': 'True'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Transaction']", 'null': 'True'}),
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
