import sqlite3
def query (sql):
    with sqlite3.connect('users.db') as conn:
        cur=conn.cursor()
        rows = cur.execute(sql)
        return list(rows)

def data():
    rows = (query(f"SELECT * FROM users "))
    table =[]
    for row in rows:
        table.append({'name':row[0],'username':row[1],'password':row[2],'email':row[3],'team':row[4]})
    return table
# print(query(f"SELECT username FROM users WHERE username LIKE '{'dan1'}'"))
