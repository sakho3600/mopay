import time

from app.common.models import db

def get(id):
    result = db.query("select * from cashout where id=%s", (id))
    return result

def save(cashout):
    result = db.query(("insert into cashout (id, agent, tid, receiver, date)"
                       " values (%s, %s, %s, %s, %s)"), (cashout.get('id'), 
                       cashout.get('agent'), cashout.get('tid'), 
                       cashout.get('receiver'), time.time()))
    return result

def confirm(cashout):
    result = db.query(("update cashout set confirmed=%s where id=%s"),
                      ("1", cashout.get('id')))
    return result