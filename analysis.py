import sys,sqlite3,os,pdb,re,string
from wordcloud import WordCloud
from nltk.tokenize import TreebankWordTokenizer
import matplotlib.pyplot as plt
from pre_process import process_text
def word_cloud_generator2(data,description):
	from wordcloud import STOPWORDS

	STOPWORDS|=set(list(string.ascii_lowercase))	
	print "generating tag cloud",description	
	wordcloud = WordCloud(stopwords=STOPWORDS,
	                      background_color='black',
	                      width=2500,
	                      height=2000,
	                     ).generate(data)

	filename=description+'.png'
	plt.imshow(wordcloud)
	plt.axis('off')
	plt.savefig(filename, dpi=300)
	plt.show()
	print "done",description

db_names=['twitter_NarcoticsAnonymous_02-03_03-11-01',
'twitter_AlcoholicsAnonymous_01-18_09-50-21']
table_names=['NarcoticsAnonymous','AlcoholicsAnonymous']
text=[]
#connect to databases and get data
for db_name,table_name in zip(db_names, table_names):
	conn = sqlite3.connect('./data/'+db_name+'.db')
	c=conn.cursor()
	for row in c.execute('SELECT content From '+table_name):
		text.append(row[0])
	break
#generate wordcloud
#tokens=process_text(text)
tokens=process_text(text)
word_cloud_generator2("\n".join(tokens),"checking")

pdb.set_trace()
