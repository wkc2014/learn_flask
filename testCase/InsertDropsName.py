import sqlite3
import os


file_dir = 'D:\\FlaskForDrops\\drops_server\\app\\static\\drops_html\\'

filename = []

for root,dirs,files in os.walk(file_dir,topdown=False):
	filename = files

def insetr_sql(db_name):
    conn = sqlite3.connect(db_name)
    num = 1

    for name in filename:

        insert_sql = '''insert into drops(id,name,path,read) values (%s,'%s','static/drops_html/%s','')''' % (num, name.decode('GBK'),name.decode('GBK'))
        
        print insert_sql

        conn.execute(insert_sql)
        num = num + 1

    conn.commit()
    conn.close()


if __name__ == '__main__':
    db_name = 'D:\\FlaskForDrops\\drops_server\\data-dev.sqlite'
    insetr_sql(db_name)
