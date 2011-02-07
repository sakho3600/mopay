import MySQLdb as db

def query(sql, args=()):
    con = db.connect(host='localhost', user='dammy',passwd='dammy', db='mopay')
    cursor = con.cursor(db.cursors.DictCursor)
    cursor.execute(sql, args)
    result = cursor.fetchall()
    if len(result) == 0:
        result = None
    elif len(result) == 1:
        result = result[0]
    con.commit()
    con.close()
    return result  