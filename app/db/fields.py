import pickle
from cStringIO import StringIO
from django.db import models

class BlobField(models.Field):
    """A field for persisting binary data in mysql database that we support."""
    __metaclass__ = models.SubfieldBase

    def __unicode__(self):
        return u'blobdata'
    
    def db_type(self):
        return 'LONGBLOB'
        
    def get_db_prep_value(self, value):
        src = StringIO()
        pickler = pickle.Pickler(src)
        pickler.dump(value)
        return src.getvalue()

    def to_python(self, value):
        if value:
            try:
                data = StringIO(value)
                return pickle.Unpickler(data).load()
            except Exception:
                return value
        else:
            return None
        