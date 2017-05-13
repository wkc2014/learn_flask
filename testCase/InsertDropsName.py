import sqlite3
import os


f = file('D:\\drops_file_name.txt','w')
file_dir = 'D:\\testhtml\\'

filename = []

for root,dirs,files in os.walk(file_dir):
	filename = files

def insetr_sql(db_name):
    conn = sqlite3.connect(db_name)
    num = 1

    for name in filename:
        # print name[0:10]
        insert_sql = '''insert into drops(id,name,path,read) values (%s,'%s','file:///D:/drops_html/%s','')''' % (num, name.decode('GBK'),name.decode('GBK'))
        
        print insert_sql

        conn.execute(insert_sql)
        num = num + 1

    conn.commit()
    conn.close()


if __name__ == '__main__':
    db_name = 'E:\\0x01 PythonCode\\FlaskProject\\learn_flask\\data-dev.sqlite'
    insetr_sql(db_name)
