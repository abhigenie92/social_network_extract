import sys,sqlite3,os,pdb

db_name='twitter_AlcoholicsAnonymous_01-18_09-50-21'
table_name='AlcoholicsAnonymous'
conn = sqlite3.connect('./data/'+db_name+'.db')
c=conn.cursor()
text=[]
for row in c.execute('SELECT content From '+table_name):
	text.append(row)
pdb.set_trace()