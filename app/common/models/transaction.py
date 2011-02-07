from app.common.models import db

def get(tid):
    """Gets transaction details"""
    result = db.query('select * from transaction where id=%s', (tid))
    return result

def get_active_transaction(tid):
    """Gets an active transaction"""
    result = db.query('select * from transaction where id=%s and status=%s',
                      (tid, 'active'))
    return result

def get_by_pin(pin):
    """Gets a pin in active transaction"""
    result = db.query('select * from transaction where pin=%s and status=%s',
                      (pin, 'active'))
    return result

def save(transaction):
    """Save transaction"""
    result = db.query('insert into transaction(id, status, sender, pin, \
                      receiver, date) values (%s, %s, %s, %s, %s, %s)',
                      (transaction['id'], transaction['status'], 
                       transaction['sender'], transaction['pin'], 
                       transaction['receiver'], transaction['date']))
    return result

def update(transaction):
    """Update transaction"""
    result = db.query('update transaction set status=%s, sender=%s, pin=%s, \
                      receiver=%s, date=%s where id=%s', 
                      (transaction['status'], transaction['sender'], 
                       transaction['pin'], transaction['receiver'], 
                       transaction['date'], transaction['id']))
    return result