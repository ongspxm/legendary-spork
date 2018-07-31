"""wrapper for sqlite library"""
import sqlite3

DB = "data.db"

def get_conn():
    """get a connection to sqlite"""
    return sqlite3.connect(DB)

### return [rows]
def select(table, where="", vals=None):
    """select from sqlite db"""
    conn = get_conn()
    cur = conn.cursor()

    if not where:
        where = ""

    if not vals:
        vals = []

    cur.execute("select * from %s %s"%(table, where), vals)
    res = cur.fetchall()
    fld = cur.description
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
    """insert into sqlite db"""
    conn = get_conn()
    cur = conn.cursor()

    fstr, vals = [], []
    for key in obj.keys():
        fstr.append(key)
        vals.append(obj.get(key, ""))

    qry = "insert into %s(%s) values(%s)"%(
        table,
        ",".join(fstr),
        ",".join(["?"]*len(vals)))

    cur.execute(qry, vals)
    conn.commit()
    conn.close()
    return True

### return True
def delete(table, where, vals):
    """delete from sqlite db"""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("delete from %s %s"%(table, where), vals)
    conn.commit()
    conn.close()
    return True

### return True
def update(table, where, wvals, obj):
    """update vals in sqlite db"""
    conn = get_conn()
    cur = conn.cursor()

    vals, flds = [], []
    for key in obj.keys():
        flds.append(key+"=?")
        vals.append(obj[key])

    qry = "update %s set %s %s"%(
        table,
        ",".join(flds),
        where)

    cur.execute(qry, vals+wvals)
    conn.commit()
    conn.close()
    return True
