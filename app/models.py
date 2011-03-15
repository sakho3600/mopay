from django.db import models
from db.fields import BlobField

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^app\.db\.fields\.BlobField"])

class Config(models.Model):
    key = models.CharField(max_length=30, unique=True)
    value = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.key + ": " + self.value
    
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, null=True, unique=True)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    pin = models.CharField(max_length=50)
    pin_salt = models.CharField(max_length=70)
    balance = models.FloatField(default=5000)
    
    def __unicode__(self):
        return self.phone
    
class Agent(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    password_salt = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    id_filename = models.CharField(max_length=80, null=True)
    sig_filename = models.CharField(max_length=80, null=True)

class Admin(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    password_salt = models.CharField(max_length=50)
    
class Card(models.Model):
    pin = models.CharField(max_length=20, unique=True)
    serial = models.CharField(max_length=50, unique=True)
    value = models.IntegerField()
    used = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.serial
    
class Transaction(models.Model):
    id = models.CharField(max_length=30, unique=True, primary_key=True)
    status = models.CharField(max_length=15, default='start')
    sender = models.ForeignKey(User, related_name='transactionSender')
    receiver = models.ForeignKey(User, related_name='transactionReceiver')
    timestamp = models.CharField(max_length=30)
    amount = models.FloatField()
    type = models.CharField(max_length=15)
    
    def __unicode__(self):
        return self.id

class CashoutTicket(models.Model):
    id = models.CharField(max_length=50, unique=True, primary_key=True)
    sender = models.ForeignKey(User, related_name='cashoutTicketSender')
    receiver = models.ForeignKey(User, related_name='cashoutTicketReceiver')
    transaction = models.ForeignKey(Transaction)
    timestamp = models.CharField(max_length=30)

class RequestCashoutTicket(models.Model):
    agent = models.ForeignKey(Agent)
    cashout_ticket = models.ForeignKey(CashoutTicket)
    confirmed = models.BooleanField()
    
class IncomingMessage(models.Model):
    sender = models.ForeignKey(User)
    body = models.TextField()
    timestamp = models.CharField(max_length=30)

class OutgoingMessage(models.Model):
    body = models.TextField()
    receiver = models.ForeignKey(User)
    timestamp = models.CharField(max_length=30)
    type = models.CharField(max_length=50, null=True)
    meta = BlobField(null=True)
    