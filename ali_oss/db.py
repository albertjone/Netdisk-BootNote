import sqlite3
import datetime

test_list= [('ae93836a.png','C:\Users\Mr.Guan\Boostnote\attachments\6f10a622-8367-4884-b363-46c9741f9f9a\ae93836a.png','file','12c593c5bd2f0972188eb30e32bee7ad4060be582c2c6826caff89372ca84707'),
('boostnote.json','C:\Users\Mr.Guan\Boostnote\boostnote.json','file','d45328dc310c0a00a67232d0cc5b07e17e5844aad817842af012a49dbea32c25'),
('6f10a622-8367-4884-b363-46c9741f9f9a.cson','C:\Users\Mr.Guan\Boostnote\notes\6f10a622-8367-4884-b363-46c9741f9f9a.cson','file','dd00532786bdbdf5a49895c62764d35ed175a714221db1969b1d6ae5193c4e67'),
('82db4928-d99b-4ad0-b336-86750a9b38b4.cson','C:\Users\Mr.Guan\Boostnote\notes\82db4928-d99b-4ad0-b336-86750a9b38b4.cson','file','48bcfcbdfb02907a7a6a6d7c4a9ca0dd226dc1217dee9b24ae5f46196f035f5d'),
('8976e923-598c-4cdb-8c80-21cbcb74985d.cson','C:\Users\Mr.Guan\Boostnote\notes\8976e923-598c-4cdb-8c80-21cbcb74985d.cson','file','948eccf9e783e453c023e3c06f0aafc18cb2cadfc1d132b6f42272cf1271b785'),
('a5a4236c-ff1f-4282-bbd5-b39ca6ad7a92.cson','C:\Users\Mr.Guan\Boostnote\notes\a5a4236c-ff1f-4282-bbd5-b39ca6ad7a92.cson','file','588f48b51593dda0a5cff9cb27a4b0de5b7d7245a93f28b0f7d8b54451da1322')]
def initial_db(db_url):
    records_sql = 'CREATE TABLE records(name text, url text PRIMARY KEY, typ text, hash text)'
    date_sql = 'CREATE TABLE date(date date, ts timestamp)'
    insert_date = 'INSERT INTO date(date, ts) values (?, ?)'
    today = datetime.date.today()
    now = datetime.datetime.now()
    conn = sqlite3.connect(db_url)
    c = conn.cursor()
    c.execute(records_sql)
    c.execute(date_sql)
    c.execute(insert_date, (today, now))
    conn.commit()
    conn.close()


def get_timestamp(db_url):
    conn = sqlite3.connect(db_url)
    c = conn.cursor()
    sql = 'SELECT * FROM date'
    c.execute(sql)
    return c.fetchone()[1]


def get_all_from_db(db_url):
    sql = 'SELECT * FROM records '
    item_dict_list = []
    conn = sqlite3.connect(db_url)
    c = conn.cursor()
    for row in c.execute(sql):
        item_dict = {}
        item_dict['name'] = row[0]
        item_dict['url'] = row[1]
        item_dict['type'] = row[2]
        item_dict['hash'] = row[3]
        item_dict_list.append(item_dict)
    return item_dict_list


def save_to_db(db_url, write_list):
    sql = "INSERT INTO records VALUES(?,?,?,?)"
    conn = sqlite3.connect(db_url)
    c = conn.cursor()
    try:
        c.executemany(sql, write_list)
    except Exception("records already exits"):
        print("value already exits")
    conn.commit()
    conn.close()

# initial_db('test-g-2.db')
# write_to_db('test-g-2.db', test_list)
# get_all_from_db('test-g-2.db')