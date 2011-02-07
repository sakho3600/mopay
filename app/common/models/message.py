from app.common.models import db

def msg_out_save(msg):
    result = db.query(("insert into msg_out(body, date, receiver, tid, type,"
                        "cashout_id) values(%s, %s, %s, %s, %s, %s)"),
                        (msg.get('body'), msg.get('date'), msg.get('receiver'),
                         msg.get('tid'), msg.get('type'), msg.get('cashout_id')))
    return result

def msg_in_save(msg):
    result = db.query('insert into msg_in(body, sender, date) values(%s, %s, %s)',
                      (msg.get('body'), msg.get('sender'), msg.get('date')))
    return result