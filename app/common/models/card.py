from app.common.models import db

def get(pin):
    result = db.query('select * from card where pin=%s', (pin))
    return result

def save(card):
    result = db.query('insert into card(pin, serial, value) values(%s, %s, %s)', 
                      (card.get('pin'),card.get('serial'), card.get('value')))
    return result

def mark_used(card):
    result = db.query(('update card set used=%s where pin=%s'), 
                      ("1", card.get('pin')))
    return result