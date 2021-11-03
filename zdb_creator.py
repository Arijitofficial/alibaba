import sqlite3

conn = sqlite3.connect('db.sqlite3')

count = 1
gender = ['men ', 'women ','kids ']
searches = ['sandal','sports shoes' ]
for g in gender:
    for search in searches:
        with open("{}{}".format(g,search), 'r') as f:
            lines = f.readlines()
        for line in lines:
            data = line.split("|")
            # id -> name -> gender -> category -> color -> price -> desc -> image
            cur = conn.cursor()
            cur.execute('''INSERT INTO alibaba_product VALUES(?,?,?,?,?,?,?,?)''',(count,data[0], search, data[0]+"|{}|".format(search)+data[2], data[2], g, data[3], data[4]))
            cur.close()
            count += 1
conn.commit()