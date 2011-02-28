from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    location = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=15,unique=True)
    is_agent = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.phone
    
class Card(models.Model):
    pin = models.CharField(max_length=20, unique=True)
    serial = models.CharField(max_length=30, unique=True)
    value = models.IntegerField()
    used = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.serial
    
class Transaction(models.Model):
    id = models.CharField(max_length=30, unique=True, primary_key=True)
    status = models.CharField(max_length=15)
    card = models.ForeignKey(Card)
    sender = models.ForeignKey(User, related_name='transactionSender')
    receiver = models.ForeignKey(User, related_name='transactionReceiver')
    timestamp = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.id
    
class Cashout(models.Model):
    id = models.CharField(max_length=30,unique=True, primary_key=True)
    agent = models.ForeignKey(User, related_name='cashoutAgent')
    receiver = models.ForeignKey(User, related_name='cashoutReceiver')
    transaction = models.ForeignKey(Transaction)
    confirmed = models.BooleanField()
    timestamp = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.id
    
class IncomingMessage(models.Model):
    sender = models.ForeignKey(User)
    body = models.TextField()
    timestamp = models.CharField(max_length=20)

class OutgoingMessage(models.Model):
    body = models.TextField()
    receiver = models.ForeignKey(User)
    timestamp = models.CharField(max_length=20)
    type = models.CharField(max_length=50, null=True)
    transaction = models.ForeignKey(Transaction, null=True)
    cashout = models.ForeignKey(Cashout, null=True)
    