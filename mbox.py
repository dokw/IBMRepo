import sqlite3
import urllib.request

conn = sqlite3.connect('orgdb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''CREATE TABLE Counts (org TEXT,count INTEGER)''')

fname = input('Enter file name:')
if (len(fname)<1): fname = 'mbox.txt'
#if (len(fname)<1): fname = 'http://www.py4e.com/code3/mbox.txt'
#fh = urllib.request.urlopen(fname)
fh = open(fname)
for line in fh:
    if not line.startswith('From:'): continue
    pieces = line.split()
    email = pieces[1]
    email_domain = email.split('@')
    domain_pieces = email_domain[1]
    cur.execute('SELECT count FROM Counts WHERE org=?',(domain_pieces,))
    row= cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org,count) VALUES (?,1)''',(domain_pieces,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',(domain_pieces,))
    conn.commit()

sqlstr = 'SELECT org,count FROM COUNTS ORDER BY count DESC'

for row in cur.execute(sqlstr):
    print(str(row[0]),row[1])

cur.close()
