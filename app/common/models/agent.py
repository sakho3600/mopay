from app.common.models import db

def get(id):
    result = db.query('select * from agent where id=%s', (id))
    return result

def get_by_phone(phone):
    """Get an agent by phone number"""
    result = db.query('select * from agent where phone=%s', (phone))
    return result