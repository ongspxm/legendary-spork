import sqlite3

DB = "data.db"

def getConn():
    return sqlite3.connect(DB);

### return [rows]
def select(table, where="", vals=[]):
    conn = getConn()
    db = conn.cursor()

    db.execute("select * from %s %s"%(table, where), vals)
    res = db.fetchall()
    fld = db.description
    conn.close()

    out = []
    for val in res:
        row, cnt = {}, len(val)

        for i in range(cnt):
            row[fld[i][0]] = val[i]
        out.append(row)

    return out

### return True
def insert(table, obj):
    conn = getConn()
    db = conn.cursor()

    fstr,vals=[],[]
    for key in obj.keys():
        fstr.append(key)
        vals.append(obj.get(key, ""))

    qry = "insert into %s(%s) values(%s)"%(
            table,
            ",".join(fstr),
            ",".join(["?"]*len(vals)))

    db.execute(qry, vals)
    conn.commit()
    conn.close()
    return True

### return True
def delete(table, where, vals):
    conn = getConn()
    db = conn.cursor()

    db.execute("delete from %s %s"%(table, where), vals)
    conn.commit()
    conn.close()
    return True

### return True
def update(table, where, wvals, obj):
    conn = getConn()
    db = conn.cursor()

    vals, flds = [], []
    for key in obj.keys():
        flds.append(key+"=?")
        vals.append(obj[key])

    qry = "update %s set %s %s"%(
            table,
            ",".join(flds),
            where)

    db.execute(qry, vals+wvals)
    conn.commit()
    conn.close()
    return True
