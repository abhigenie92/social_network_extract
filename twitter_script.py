#Things to fix still
#1.Scroll down to get unlimited tweets-DONE
#2.Fix other language profile names-DONE
#3.Fix remove of photos thumbnails as tweets-DONE
#4.Better way to print the progress-?
from scrollDownHtmlCode import return_html_code
from pprint import pprint
from extract_tweets import extract_tweets
#from twitter_datetimegraph import plot_date_time_graph 
import sys,requests,retweetsAndFavExtract,sqlite3,os,pdb,datetime
reload(sys)
sys.setdefaultencoding("utf-8")

def get_twitter_data(query):
	text_tweet=[];text_date=[];text_time=[];text_username=[];text_profilename=[];text_retweet=[];text_fav=[];
	final_date=datetime.date.today()
	start_date=dateobj = datetime.datetime.strptime('2006-03-21','%Y-%m-%d').date()
	search = query.replace(" ","%20")	
	flag=True
	while flag:
		end_date=(start_date+datetime.timedelta(1*365/12))
		print start_date, end_date

		if end_date > final_date:
			end_date=(final_date+datetime.timedelta(1))
			flag=False
		url='https://twitter.com/search?q='+search+'%20since%3A'+start_date.isoformat()+'%20until%3A'+end_date.isoformat()+'&src=typd&lang=en'
		html_full=return_html_code(url)
		if html_full:
			text_tweet,text_date,text_time,text_username,text_profilename,text_retweet,text_fav\
		 = (x+y for x,y in zip((text_tweet,text_date,text_time,text_username,text_profilename,text_retweet,text_fav)\
		 	, extract_tweets(html_full)))

		start_date=end_date-datetime.timedelta(1)
	return query,text_tweet,text_date,text_time,text_username,text_profilename,text_retweet,text_fav

def write_data_to_db(search,text_tweet,text_date,text_time,text_username,text_profilename,text_retweet,text_fav):
	db_name=('twitter '+search.title().replace(" ","")+'_'+str(datetime.datetime.now())[5:19]+'.db').replace(" ","_").replace(":","-")
	path='data'+os.path.sep+db_name
	conn = sqlite3.connect(path)
	table_name=search.title().replace(" ","")
	conn.execute('CREATE TABLE '+table_name+' (content text,date_posted text,time_posted text,username \
		text,profilename text,retweets numeric,favs numeric)')
	values=zip(text_tweet,text_date,text_time,text_username,text_profilename,text_retweet\
				,text_fav)
	conn.executemany("INSERT INTO "+table_name+ "(content,date_posted,time_posted,username,profilename,\
				retweets,favs)VALUES (?,?,?,?,?,?,?)",values)
	conn.commit()
	conn.close()
	return db_name
def search_twitter(query):
	db_name=write_data_to_db(*get_twitter_data(query))
	print 'Data stored at - .'+os.path.sep+'data'+os.path.sep+ db_name
	#plot_date_time_graph(db_name,search.title().replace(" ",""))
if __name__ == '__main__':
	directory='data' # stores the output
	if not os.path.exists(directory): os.makedirs(directory)
	search_twitter('Alcoholics Anonymous Drunk')
	#search_twitter('Error Check')
