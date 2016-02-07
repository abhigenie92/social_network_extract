#Things to fix still
#1.Scroll down to get unlimited tweets-DONE
#2.Fix other language profile names-DONE
#3.Fix remove of photos thumbnails as tweets-DONE
#4.Better way to print the progress-?
from pprint import pprint
from extract_tweets import extract_tweets
from bs4 import BeautifulSoup

#from twitter_datetimegraph import plot_date_time_graph 
import sys,requests,retweetsAndFavExtract,sqlite3,os,pdb,datetime
reload(sys)
sys.setdefaultencoding("utf-8")
driver='firefox_no'
if driver =='firefox':
	from firefox_driver_code import return_html_code
else:
	from check import return_html_code


def search_twitter(query):
	#initialization parameters and store_lists 
	start_date=datetime.datetime.strptime('2006-03-21','%Y-%m-%d').date()
	text_tweet_list=[];text_date_list=[];text_time_list=[];text_username_list=[];
	text_profilename_list=[];text_retweet_list=[];text_fav_list=[]
	
	flag=True
	while flag:
		flag,start_date,query,text_tweet,text_date,text_time,text_username\
										,text_profilename,text_retweet,text_fav=get_twitter_data(query,start_date,True)
		#add whatever we have
		text_tweet_list.extend(text_tweet)
		text_date_list.extend(text_date)
		text_time_list.extend(text_time)
		text_username_list.extend(text_username)
		text_profilename_list.extend(text_profilename)
		text_fav_list.extend(text_fav)
	db_name=write_data_to_db(query,text_tweet_list,text_date_list,text_time_list,text_username_list,text_profilename_list,\
		text_retweet_list,text_fav_list)

	print 'Data stored at - .'+os.path.sep+'data'+os.path.sep+ db_name
	#plot_date_time_graph(db_name,search.title().replace(" ",""))

def get_twitter_data(query,start_date,debug_out=None):
	search = query.replace(" ","%20")	
	flag=True
	#list of values to be returned
	text_tweet=[];text_date=[];text_time=[];text_username=[];text_profilename=[];text_retweet=[];text_fav=[]
	
	#dates intialization
	final_date=datetime.date.today()
	
	while flag:
		#dates setting in time interval
		end_date=(start_date+datetime.timedelta(2*365/12)) #time-gap of 2 months
		if end_date > final_date:
			end_date=(final_date+datetime.timedelta(1))
			flag=False
		#url generation according to dates
		url='https://twitter.com/search?q='+search+'%20since%3A'+start_date.isoformat()+'%20until%3A'+end_date.isoformat()+'&src=typd&lang=en'
		
		if debug_out:
			print start_date, end_date
			print url	
		try:
			html_full=return_html_code(url,False)
		except Exception as error:
			print error
			break #1. Return data we have and start_date, we will start again
		if html_full:
			soup = BeautifulSoup(html_full, "html.parser")
			alltweets = soup.find_all(attrs={'data-item-type' : 'tweet','class':"js-stream-item stream-item stream-item expanding-stream-item "})
			if len(alltweets)> 1:
				text_tweet,text_date,text_time,text_username,text_profilename,text_retweet,text_fav\
			 = (x+y for x,y in zip((text_tweet,text_date,text_time,text_username,text_profilename,text_retweet,text_fav)\
			 	, extract_tweets(alltweets)))
		start_date=end_date-datetime.timedelta(1)

	return flag,start_date,query,text_tweet,text_date,text_time,text_username,text_profilename,text_retweet,text_fav



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
if __name__ == '__main__':
	directory='data' # stores the output
	if not os.path.exists(directory): os.makedirs(directory)
	search_twitter('Alcoholics Anonymous Drunk')
	#search_twitter('Error Check')
